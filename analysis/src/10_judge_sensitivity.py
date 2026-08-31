"""
Judge 민감도 분석: 두 LLM judge의 전략 라벨 일치도와 n_eff 민감도.

theory/temperature_collapse.md의 요구("핵심 수치에는 judge noise 민감도 병기")
실행. 인간 이중코딩(κ≥0.6, 200턴)의 대체가 아니라 선행 단계다 — 인간 코딩
완료 전까지 모델-간 κ를 보고한다.

산출:
  - Cohen's κ (전체 + REBT 제외 — 지배 라벨이 κ를 부풀리는지 확인)
  - 혼동행렬
  - 전략별 E[1/p̂_s]·n_req를 judge별로 병렬 표기한 민감도 표

Usage:
  python 10_judge_sensitivity.py --labels-a ../data/strategy_labels.jsonl \
      --labels-b ../data/strategy_labels_judge32b.jsonl \
      --name-a qwen7b --name-b qwen32b
"""

import argparse
import json
import os
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

STRATEGIES = ["FACT", "SOCR", "COMG", "SRCT", "EMPA", "REBT", "CLAIM", "META", "OTHER"]


def load(path):
    with open(path) as f:
        return {(r["context_id"], r["draw"]): r["label"] for r in map(json.loads, f)}


def cohens_kappa(a, b):
    labels = sorted(set(a) | set(b))
    idx = {l: i for i, l in enumerate(labels)}
    m = np.zeros((len(labels), len(labels)))
    for x, y in zip(a, b):
        m[idx[x], idx[y]] += 1
    n = m.sum()
    po = np.trace(m) / n
    pe = (m.sum(1) * m.sum(0)).sum() / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, m, labels


def neff_table(keys, lab, alpha=0.5, target_se=0.02, sigma2=1.0):
    by_ctx = defaultdict(list)
    for k in keys:
        by_ctx[k[0]].append(lab[k])
    K = len(STRATEGIES) - 1  # OTHER 제외한 taxonomy 크기
    rows = []
    for s in STRATEGIES[:-1]:
        ps = []
        for cid, ls in by_ctx.items():
            k = len(ls)
            ps.append((Counter(ls).get(s, 0) + alpha) / (k + alpha * K))
        ps = np.array(ps)
        e_inv = float((1 / ps).mean())
        rows.append({"strategy": s, "mean_p": round(float(ps.mean()), 4),
                     "E_inv_p": round(e_inv, 2),
                     "n_req": round(sigma2 * e_inv / target_se ** 2)})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels-a", required=True)
    ap.add_argument("--labels-b", required=True)
    ap.add_argument("--name-a", default="judge_a")
    ap.add_argument("--name-b", default="judge_b")
    args = ap.parse_args()

    la, lb = load(args.labels_a), load(args.labels_b)
    keys = sorted(set(la) & set(lb))
    a = [la[k] for k in keys]
    b = [lb[k] for k in keys]
    kap, m, labels = cohens_kappa(a, b)
    agree = np.mean([x == y for x, y in zip(a, b)])
    print(f"n={len(keys)}  raw agreement={agree:.3f}  Cohen's κ={kap:.3f}")

    # REBT 지배가 κ를 왜곡하는지: 두 judge 모두 REBT가 아닌 표본으로 재계산
    nz = [(x, y) for x, y in zip(a, b) if not (x == "REBT" and y == "REBT")]
    if len(nz) > 10:
        ka2, _, _ = cohens_kappa([x for x, _ in nz], [y for _, y in nz])
        print(f"both-REBT 제외 (n={len(nz)}): agreement="
              f"{np.mean([x == y for x, y in nz]):.3f}  κ={ka2:.3f}")

    cm = pd.DataFrame(m.astype(int), index=labels, columns=labels)
    cm = cm.loc[cm.sum(1) > 0, cm.sum(0) > 0]
    print(f"\n혼동행렬 (행={args.name_a}, 열={args.name_b}):")
    print(cm.to_string())

    ta = neff_table(keys, la).rename(columns=lambda c: c if c == "strategy" else f"{c}_{args.name_a}")
    tb = neff_table(keys, lb).rename(columns=lambda c: c if c == "strategy" else f"{c}_{args.name_b}")
    t = ta.merge(tb, on="strategy")
    t["n_req_ratio"] = (t[f"n_req_{args.name_b}"] / t[f"n_req_{args.name_a}"]).round(2)
    print("\n[judge 민감도 — 전략별 n_eff]")
    print(t.to_string(index=False))

    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    t.to_csv(os.path.join(outdir, "judge_sensitivity.csv"), index=False)
    cm.to_csv(os.path.join(outdir, "judge_confusion.csv"))
    print("saved results/judge_sensitivity.csv, judge_confusion.csv")


if __name__ == "__main__":
    main()
