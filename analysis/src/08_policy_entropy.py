"""
Study 0-b 3단계: 전략 분류 -> 문맥별 정책 엔트로피 -> 식별 붕괴 공식 대입.

입력: 07_requery.py 출력 (문맥당 k개의 재생성 rebuttal)
1) 각 rebuttal을 전략 분류 (prompts/strategy_classifier.txt, LLM judge)
2) 문맥별 전략분포 p̂(s|h) -> 엔트로피 H(h), 최빈 전략 점유율
3) theory/temperature_collapse.md Result 2 대입 — **전략별로** (FIX 2026-07-30, 4차 비판):
     구 방식(문맥별 minority_p 혼합)은 문맥마다 minority 전략의 정체가 달라
     E[1/minority_p]가 어떤 고정 행동 a의 E[1/π(a|H)]에도 대응하지 않았음.
     새 방식: 고정 전략 s마다  n_eff(s) = n / E[1/p̂_s(H)],
       p̂_s는 Dirichlet(α) smoothing (zero-probability 처리) + percentile 불확실성 구간.
     causal estimand와 연결되는 필요 표본은 전략별 표로 보고한다.
출력: results/policy_entropy.csv, results/policy_entropy_by_strategy.csv, results/policy_entropy.png

전략 분류 검증: 200턴 인간 이중코딩 -> Cohen's kappa 보고 (README 절차)

Usage:
  python 08_policy_entropy.py --requery ../data/requery_gpt-4o-mini.jsonl \
      --judge-model gpt-4o-mini [--classify]   # --classify 없으면 분류 캐시 사용
"""

import argparse
import json
import os
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

STRATEGIES = ["FACT", "SOCR", "COMG", "SRCT", "EMPA", "REBT", "CLAIM", "META"]
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "strategy_classifier.txt")


def classify_all(records, model, workers=1, cache_path=None):
    from openai import OpenAI
    client = OpenAI()
    template = open(PROMPT_PATH).read()
    if cache_path is None:
        cache_path = os.path.join(os.path.dirname(__file__), "..", "data", "strategy_labels.jsonl")
    done = set()
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            done = {(r["context_id"], r["draw"]) for r in map(json.loads, f)}
    todo = [r for r in records if (r["context_id"], r["draw"]) not in done]
    lock = threading.Lock()

    def one(r):
        resp = client.chat.completions.create(
            model=model, temperature=0, max_tokens=10,
            messages=[{"role": "user", "content": template.replace("{{TEXT}}", r["text"])}])
        label = resp.choices[0].message.content.strip().upper()[:5].rstrip(".,")
        label = label if label in STRATEGIES else "OTHER"
        with lock:
            out.write(json.dumps({**{k: r[k] for k in ("context_id", "draw")}, "label": label}) + "\n")
            out.flush()

    with open(cache_path, "a") as out:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(one, todo))
    return cache_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--requery", required=True)
    ap.add_argument("--judge-model", default="gpt-4o-mini")
    ap.add_argument("--classify", action="store_true")
    ap.add_argument("--workers", type=int, default=1,
                    help="judge 동시 요청 수 (로컬 vLLM은 16–32 권장)")
    ap.add_argument("--labels", default=None,
                    help="라벨 캐시 경로 (judge별 분리용; 기본 data/strategy_labels.jsonl)")
    ap.add_argument("--out-suffix", default="",
                    help="results 파일명 접미사 (예: _judge32b)")
    ap.add_argument("--target-se", type=float, default=0.02, help="목표 SE (효과크기 ~0.05 가정)")
    ap.add_argument("--sigma2", type=float, default=1.0, help="결과 분산 (pilot에서 캘리브레이션)")
    ap.add_argument("--alpha", type=float, default=0.5, help="Dirichlet smoothing (Jeffreys 0.5)")
    ap.add_argument("--nboot", type=int, default=2000, help="문맥 bootstrap 반복 (불확실성 구간)")
    args = ap.parse_args()

    with open(args.requery) as f:
        records = [json.loads(l) for l in f]
    labels_path = args.labels or os.path.join(
        os.path.dirname(__file__), "..", "data", "strategy_labels.jsonl")
    if args.classify:
        labels_path = classify_all(records, args.judge_model, workers=args.workers,
                                   cache_path=labels_path)
    with open(labels_path) as f:
        labels = [json.loads(l) for l in f]

    by_ctx = defaultdict(list)
    for r in labels:
        by_ctx[r["context_id"]].append(r["label"])

    a = args.alpha
    K = len(STRATEGIES)
    rows = []
    for cid, ls in by_ctx.items():
        k = len(ls)
        counts = Counter(ls)
        raw = np.array([counts.get(s, 0) / k for s in STRATEGIES])
        # Dirichlet(alpha) posterior mean — zero-probability를 0이 아닌 값으로 처리
        smooth = np.array([(counts.get(s, 0) + a) / (k + a * K) for s in STRATEGIES])
        nz = raw[raw > 0]
        rows.append({
            "context_id": cid, "k": k,
            "entropy_bits": float(-(nz * np.log2(nz)).sum()),
            "top_share": float(raw.max()),
            **{f"p_{s}": float(p) for s, p in zip(STRATEGIES, raw)},
            **{f"ps_{s}": float(p) for s, p in zip(STRATEGIES, smooth)},
        })
    df = pd.DataFrame(rows)

    # ---- Result 2 대입: 전략별 (FIX 2026-07-30) ----
    # 고정 전략 s의 E[1/p̂_s(H)] (smoothed) -> implied ESS fraction, 필요 대화 수.
    # 문맥 단위 bootstrap으로 percentile 구간.
    rng = np.random.default_rng(7)
    strat_rows = []
    for s in STRATEGIES:
        ps = df[f"ps_{s}"].to_numpy()
        raw_mean = float(df[f"p_{s}"].mean())
        inv = 1.0 / ps
        e_inv = float(inv.mean())
        boots = np.array([
            (1.0 / ps[rng.integers(0, len(ps), len(ps))]).mean()
            for _ in range(args.nboot)]) if len(ps) > 1 else np.array([e_inv])
        n_req_s = args.sigma2 * e_inv / (args.target_se ** 2)
        strat_rows.append({
            "strategy": s, "mean_p_raw": round(raw_mean, 4),
            "mean_p_smoothed": round(float(ps.mean()), 4),
            "E_inv_p": round(e_inv, 2),
            "E_inv_p_lo95": round(float(np.quantile(boots, 0.025)), 2),
            "E_inv_p_hi95": round(float(np.quantile(boots, 0.975)), 2),
            "implied_ess_frac": round(1.0 / e_inv, 5),
            "n_req": round(n_req_s),
        })
    sdf = pd.DataFrame(strat_rows).sort_values("E_inv_p")
    print(df[["entropy_bits", "top_share"]].describe().round(3).to_string())
    print("\n[전략별 Result 2 대입]  n_eff(s) = n / E[1/p̂_s(H)]  (Dirichlet α=%.2f smoothing)" % a)
    print(sdf.to_string(index=False))
    print("[주의 1] p̂_s는 고정 재질의 프로토콜 하의 정책 불확실성이며 실제 배치 propensity가 아님 — judge noise 민감도와 함께 보고할 것")
    print("[주의 2] smoothing된 p̂_s의 E[1/p]는 k=%.0f 해상도 한계에서의 **하한**임 (미관측 전략의 실제 p는 더 작을 수 있음)" % df.k.mean())
    print("[주의 3] 특정 대비(예: FACT vs SOCR)의 필요 표본은 두 전략의 E[1/p] 합 규모")

    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(os.path.join(outdir, f"policy_entropy{args.out_suffix}.csv"), index=False)
    sdf.to_csv(os.path.join(outdir, f"policy_entropy_by_strategy{args.out_suffix}.csv"), index=False)
    n_req = float(sdf["n_req"].max())  # 그림 캡션용: 가장 희귀한 전략 기준

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    axes[0].hist(df.entropy_bits, bins=20)
    axes[0].set_xlabel("per-context strategy entropy (bits)")
    axes[0].set_ylabel("contexts")
    axes[0].set_title("How deterministic is the deployed policy?")
    axes[1].hist(df.top_share, bins=20)
    axes[1].set_xlabel("modal-strategy share")
    axes[1].set_title(f"rarest-strategy n_req (lower bound): {n_req:,.0f}")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, f"policy_entropy{args.out_suffix}.png"), dpi=200)
    print(f"saved results/policy_entropy{args.out_suffix}.png")


if __name__ == "__main__":
    main()
