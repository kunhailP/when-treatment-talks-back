"""
Study 0-b (실증 브리지 1단계): 재질의(re-query) 실험용 문맥 추출.

DebateGPT의 rebuttal 단계가 유일한 반응-적응 단계다:
  문맥 = (proposition, side, [개인화 프로필], 상대의 opening argument)
  행동 = AI의 rebuttal
이 문맥들을 층화 추출해 contexts.jsonl로 저장하면, 07_requery.py가
같은 문맥에 대해 응답을 k회 재생성해 정책 엔트로피를 측정한다.

층화: treatmentType(AI 조건들) x 사전 동의 강도(strength) — 반발 강한
상대와 약한 상대 문맥이 고루 들어가야 Result 4(경계 국소화)를 볼 수 있다.

Input : debates.csv (argumentOpponent = 상대 opening, AI행의 rebuttal 등 포함)
Output: ../data/contexts.jsonl (기본 N=200)

Usage: python 06_extract_contexts.py --data ../data/raw/debates.csv [--n 200]
"""

import argparse
import hashlib
import json
import os

import numpy as np  # noqa: F401
import pandas as pd

AI_TREATMENTS = ["Human-AI", "Human-AI, personalized"]


def main(path, n, seed):
    df = pd.read_csv(path)
    # AI가 토론자인 행: side가 AI인 행이 따로 있거나, 참가자 행에 상대(AI) 텍스트가
    # 붙어있는 스키마 둘 다 대응 — argumentOpponent(상대 opening)가 핵심.
    cand_cols = [c for c in ["argument", "argumentOpponent", "rebuttalOpponent", "rebuttal"] if c in df.columns]
    if "argumentOpponent" not in df.columns:
        raise SystemExit(f"argumentOpponent 없음. 사용 가능 텍스트 컬럼: {cand_cols}\n전체: {list(df.columns)}")

    ai = df[df.treatmentType.isin(AI_TREATMENTS)].copy()
    ai = ai.dropna(subset=["argumentOpponent"])
    # 인간 참가자 행 기준: participant의 argument가 'AI가 본 상대 주장'.
    # AI의 rebuttal 문맥 = (proposition/topic, AI side = 참가자 반대편, 참가자 argument)
    ai["strength_pre"] = (ai.sideAgreementPreTreatment - ai.sideAgreementPreTreatment.mean()).abs() \
        if "sideAgreementPreTreatment" in ai.columns else 0.0
    ai["stratum"] = ai.treatmentType + " | " + pd.qcut(ai.strength_pre.rank(method="first"), 4, labels=False).astype(str)

    per = max(1, n // ai.stratum.nunique())
    picks = ai.sample(frac=1, random_state=seed).groupby("stratum").head(per).head(n)

    outdir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, "contexts.jsonl")
    topic_col = next((c for c in ["topic", "proposition", "topicText"] if c in picks.columns), None)
    with open(outpath, "w") as f:
        for _, r in picks.iterrows():
            ctx = {
                "context_id": hashlib.md5(f"{r.get('debateID','')}-{r.get('side','')}".encode()).hexdigest()[:10],
                "debateID": str(r.get("debateID", "")),
                "treatmentType": r.treatmentType,
                "proposition": str(r.get(topic_col, "")) if topic_col else "",
                "human_side": str(r.get("side", "")),
                "human_opening_argument": str(r.argument) if "argument" in picks.columns else "",
                "strength_pre": float(r.strength_pre),
                "stratum": r.stratum,
            }
            f.write(json.dumps(ctx, ensure_ascii=False) + "\n")
    print(f"wrote {len(picks)} contexts -> {outpath}")
    print(picks.stratum.value_counts().to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    main(a.data, a.n, a.seed)
