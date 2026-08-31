"""
문맥별 유효 점수격차 Δ̂/τ 추정 → 위상도 x축 위 실배치 문맥의 위치 (이론 TODO 4).

식별 주의 (논문에 그대로): softmax 선택확률에서 τ와 Δ는 **따로 식별되지 않는다** —
식별되는 것은 합성량 Δ/τ (temperature 단위의 점수격차)이며, 이것이 정확히
위상도 x축(1/τ에 δ를 곱한 것)에 대응하는 문맥 수준 파라미터다.

방법: 문맥 h의 재생성 k개 라벨에서 2-행동 환원 (modal vs runner-up):
  Δ̂/τ (h) = log[ (c₁+α) / (c₂+α) ],  α = 0.5 (Jeffreys)
c₂ = 0인 문맥(κ=20 해상도 한계)에서는 **하한** log[(c₁+α)/α]만 식별 —
right-censored로 표기하고 별도 카운트한다.

산출: 모델별 Δ̂/τ 분포(중앙값·IQR·censored 비율), 대응 n 규모
  (해당 층의 E[1/p_runnerup] ≈ 1 + exp(Δ̂/τ) → Result A 대입 필요 n),
  전 문맥의 위상도 배치 요약.

Usage: python 12_effective_temperature.py
Output: results/effective_temperature.csv (+콘솔 표)
"""

import json
import os
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

ALPHA = 0.5
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
SPECS = [
    ("qwen7b", "strategy_labels_judge32b.jsonl"),
    ("mistral7b", "strategy_labels_mistral_judge32b.jsonl"),
    ("phi35mini", "strategy_labels_phi_judge32b.jsonl"),
]


def per_context_gap(path):
    by_ctx = defaultdict(list)
    with open(path) as f:
        for r in map(json.loads, f):
            by_ctx[r["context_id"]].append(r["label"])
    rows = []
    for cid, ls in by_ctx.items():
        c = Counter(ls).most_common()
        c1 = c[0][1]
        c2 = c[1][1] if len(c) > 1 else 0
        gap = float(np.log((c1 + ALPHA) / (c2 + ALPHA)))
        rows.append({"context_id": cid, "k": len(ls), "gap": gap,
                     "censored": c2 == 0})
    return pd.DataFrame(rows)


def main():
    out = []
    for name, fn in SPECS:
        df = per_context_gap(os.path.join(DATA, fn))
        g = df.gap
        med = float(g.median())
        row = {
            "model": name, "contexts": len(df),
            "gap_median": round(med, 2),
            "gap_q25": round(float(g.quantile(.25)), 2),
            "gap_q75": round(float(g.quantile(.75)), 2),
            "censored_frac": round(float(df.censored.mean()), 3),
            # Result A 대입: runner-up 행동의 E[1/p] ≈ 1+exp(gap) (2-행동 환원)
            "implied_E_inv_p_median": round(1 + float(np.exp(med)), 1),
            "implied_log_n_boundary": round(float(np.log(1 + np.exp(med))), 2),
        }
        out.append(row)
        df.to_csv(os.path.join(os.path.dirname(__file__), "..", "results",
                               f"effective_temperature_{name}.csv"), index=False)
    res = pd.DataFrame(out)
    print(res.to_string(index=False))
    print()
    print("읽는 법: gap = 식별되는 합성량 Δ̂/τ (τ 단독 아님). censored 문맥의 gap은")
    print("k=20 해상도의 **하한**. implied_log_n_boundary = 위상도에서 해당 문맥이")
    print("추정가능 국면에 들기 위한 log n 하한 (해당 층 한정, Result A 대입).")
    res.to_csv(os.path.join(os.path.dirname(__file__), "..", "results",
                            "effective_temperature.csv"), index=False)
    print("saved results/effective_temperature*.csv")


if __name__ == "__main__":
    main()
