"""
Study 0-b 2단계: 동일 문맥 반복 재생성 (정책 엔트로피 측정의 원자료 수집).

각 문맥에 대해 원 실험과 같은 설정(rebuttal 생성)을 k회 반복 호출.
OpenAI-호환 API면 모두 사용 가능 (OPENAI_BASE_URL로 vLLM/기타 지정).

키: 환경변수 OPENAI_API_KEY (secrets 파일 커밋 금지)
캐시: 응답을 jsonl append — 중단 후 재실행하면 이어서 진행 (resume 안전)
비용 추정: --dry-run 은 호출 없이 예상 토큰·비용만 출력

원 논문 rebuttal 프롬프트 구조(epfl-dlab/debategpt 참조)를 따르되,
프롬프트 전문은 prompts/rebuttal_prompt.txt 에서 로드 — 모델·프롬프트
버전은 manifest에 자동 기록된다 (재현성 요건).

Usage:
  python 07_requery.py --contexts ../data/contexts.jsonl --model gpt-4o-mini \
      --k 20 --temperature 1.0 [--dry-run]
"""

import argparse
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "rebuttal_prompt.txt")
PRICE_PER_M = {  # USD (input, output) — 2026-07 기준, 실행 전 갱신할 것
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "gpt-4-0613": (30.00, 60.00),  # 원 논문 모델 (deprecated 가능성 확인)
}


def load_contexts(path):
    with open(path) as f:
        return [json.loads(l) for l in f]


def done_keys(outpath):
    if not os.path.exists(outpath):
        return set()
    with open(outpath) as f:
        return {(r["context_id"], r["draw"]) for r in map(json.loads, f)}


def build_prompt(ctx, template):
    side_ai = "PRO" if str(ctx["human_side"]).upper() in ("CON", "AGAINST", "0") else "CON"
    return (template
            .replace("{{PROPOSITION}}", ctx["proposition"])
            .replace("{{AI_SIDE}}", side_ai)
            .replace("{{OPPONENT_ARGUMENT}}", ctx["human_opening_argument"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contexts", required=True)
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--k", type=int, default=20)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=400)
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=1,
                    help="동시 요청 수 (vLLM 등 로컬 서버는 배칭되므로 16–32 권장)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ctxs = load_contexts(args.contexts)
    template = open(PROMPT_PATH).read()
    outdir = os.path.join(os.path.dirname(__file__), "..", "data")
    outpath = args.out or os.path.join(outdir, f"requery_{args.model.replace('/', '_')}.jsonl")

    n_calls = len(ctxs) * args.k
    avg_in = sum(len(build_prompt(c, template)) for c in ctxs) / len(ctxs) / 4  # ~4 chars/token
    if args.dry_run or args.model in PRICE_PER_M:
        pin, pout = PRICE_PER_M.get(args.model, (0, 0))
        cost = n_calls * (avg_in * pin + args.max_tokens * pout) / 1e6
        print(f"calls={n_calls}  ~input {avg_in:.0f} tok/call  est cost ${cost:,.2f} ({args.model})")
    if args.dry_run:
        return

    from openai import OpenAI
    client = OpenAI()  # OPENAI_API_KEY / OPENAI_BASE_URL 환경변수 사용
    done = done_keys(outpath)
    manifest = {"model": args.model, "temperature": args.temperature,
                "max_tokens": args.max_tokens, "k": args.k,
                "prompt_sha": __import__("hashlib").sha256(template.encode()).hexdigest()[:12],
                "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with open(outpath.replace(".jsonl", "_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    todo = [(ctx, draw) for ctx in ctxs for draw in range(args.k)
            if (ctx["context_id"], draw) not in done]
    lock = threading.Lock()
    n_done = 0

    def one(job):
        nonlocal n_done
        ctx, draw = job
        for attempt in range(5):
            try:
                resp = client.chat.completions.create(
                    model=args.model, temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    messages=[{"role": "user", "content": build_prompt(ctx, template)}])
                rec = {"context_id": ctx["context_id"], "draw": draw,
                       "text": resp.choices[0].message.content,
                       "finish": resp.choices[0].finish_reason}
                with lock:
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    out.flush()
                    n_done += 1
                    if n_done % 100 == 0:
                        print(f"{n_done}/{len(todo)}", flush=True)
                return
            except Exception as e:
                print("retry", attempt, e, flush=True)
                time.sleep(2 ** attempt)

    with open(outpath, "a") as out:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(one, todo))
    print("done ->", outpath)


if __name__ == "__main__":
    main()
