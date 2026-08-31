"""
멀티모델 정책 엔트로피 비교 — "structurally frequent" (Prop 1A v0.4 문구)의 실증.

같은 200 문맥 × k 재생성을 모델별로 반복한 뒤(07), 단일 judge로 분류한
라벨(08 --labels)을 모아 모델 간 결정성 지표를 비교한다. 한 모델의 버릇이
아니라 RLHF 배치 모델들에서 저엔트로피가 반복됨을 보이는 것이 목적.

주의: judge는 반드시 동일 모델로 통일 (judge 간 소수 라벨 κ≈0 —
results/judge_sensitivity.csv). 소수 전략의 정체는 인간 코딩 전 신뢰 불가;
비교 대상은 엔트로피·top_share·최빈 전략 점유율 같은 집계 지표다.

Usage:
  python 11_model_comparison.py --spec qwen7b=../data/strategy_labels_judge32b.jsonl \
      mistral7b=../data/strategy_labels_mistral_judge32b.jsonl [...]
"""

import argparse
import json
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

STRATEGIES = ["FACT", "SOCR", "COMG", "SRCT", "EMPA", "REBT", "CLAIM", "META", "OTHER"]


def summarize(path, name):
    by_ctx = defaultdict(list)
    with open(path) as f:
        for r in map(json.loads, f):
            by_ctx[r["context_id"]].append(r["label"])
    ents, tops = [], []
    pooled = Counter()
    for ls in by_ctx.values():
        k = len(ls)
        c = Counter(ls)
        pooled.update(c)
        p = np.array([v / k for v in c.values()])
        ents.append(float(-(p * np.log2(p)).sum()))
        tops.append(max(c.values()) / k)
    n = sum(pooled.values())
    modal, modal_n = pooled.most_common(1)[0]
    return {
        "model": name, "contexts": len(by_ctx), "draws": n,
        "entropy_median": round(float(np.median(ents)), 3),
        "entropy_mean": round(float(np.mean(ents)), 3),
        "top_share_median": round(float(np.median(tops)), 3),
        "zero_entropy_frac": round(float(np.mean(np.array(ents) == 0)), 3),
        "modal_strategy": modal, "modal_share": round(modal_n / n, 3),
        "n_strategies_seen": len(pooled),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", nargs="+", required=True, help="name=labels.jsonl ...")
    args = ap.parse_args()
    rows = [summarize(path, name) for name, path in
            (s.split("=", 1) for s in args.spec)]
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    import os
    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(os.path.join(outdir, "model_comparison.csv"), index=False)
    print("saved results/model_comparison.csv")


if __name__ == "__main__":
    main()
