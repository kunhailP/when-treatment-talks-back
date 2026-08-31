"""
전략 라벨 측정오차 하의 π̂·n_eff 왜곡 (JCI 부록, simulation TODO 2 — Study 0 방어).

질문: judge 오분류율 q가 08의 전략별 E[1/p̂_s]·n_req를 어느 방향으로 얼마나
왜곡하는가?

설계: "참" 문맥별 전략분포는 Study 0-b 실측(judge32b 라벨, Dirichlet 스무딩된
p̂(s|h), 200 문맥)을 그대로 사용 — 합성 가정이 아니라 데이터 접지.
각 문맥에서 k=20 라벨을 참 분포로부터 추출한 뒤 두 노이즈 모델을 통과시킨다:
  symmetric : 확률 q로 라벨을 나머지 7개 중 균등 치환 (전통적 오분류)
  absorbing : 확률 q로 라벨을 REBT로 치환 (지배 라벨 흡수 —
              judge_confusion.csv에서 관측된 7B→32B 패턴의 양식화)
그 후 08과 동일한 Dirichlet(α=0.5) 스무딩 파이프라인으로 E[1/p̂_s]·n_req 재계산.

예상 방향(해석 지침): symmetric 노이즈는 희귀 전략에 q/(K−1) 바닥을 깔아
희귀성을 **과소평가**(n_req 하향 편향 — "주의 2"의 하한 서술과 정합),
absorbing 노이즈는 희귀 전략을 더 희귀해 보이게 해 **과대평가**.
따라서 실측 n_req는 "노이즈 모델에 따라 양방향 편향 가능"으로 보고하고
민감도 범위를 병기한다.

Usage: python label_error.py [--k 20] [--nsim 200]
Output: ../results/label_error.csv, label_error.png
"""

import argparse
import json
import os
from collections import Counter

import numpy as np
import pandas as pd

STRATEGIES = ["FACT", "SOCR", "COMG", "SRCT", "EMPA", "REBT", "CLAIM", "META"]
K = len(STRATEGIES)
REBT_IDX = STRATEGIES.index("REBT")
LABELS_PATH = os.path.join(os.path.dirname(__file__), "..", "..",
                           "analysis", "data", "strategy_labels_judge32b.jsonl")
ALPHA, TARGET_SE, SIGMA2 = 0.5, 0.02, 1.0


def true_dists(path):
    by_ctx = {}
    with open(path) as f:
        for r in map(json.loads, f):
            by_ctx.setdefault(r["context_id"], []).append(r["label"])
    ps = []
    for ls in by_ctx.values():
        k = len(ls)
        c = Counter(l if l in STRATEGIES else "REBT" for l in ls)
        ps.append([(c.get(s, 0) + ALPHA) / (k + ALPHA * K) for s in STRATEGIES])
    return np.array(ps)  # (n_ctx, K)


def corrupt(labels, q, mode, rng):
    n = len(labels)
    flip = rng.uniform(size=n) < q
    if mode == "symmetric":
        out = labels.copy()
        for i in np.where(flip)[0]:
            others = [j for j in range(K) if j != labels[i]]
            out[i] = rng.choice(others)
        return out
    out = labels.copy()
    out[flip] = REBT_IDX
    return out


def pipeline_neff(label_mat):
    """label_mat: (n_ctx, k) int — 08과 동일한 스무딩 파이프라인."""
    n_ctx, k = label_mat.shape
    rows = {}
    for si, s in enumerate(STRATEGIES):
        cnt = (label_mat == si).sum(axis=1)
        ps = (cnt + ALPHA) / (k + ALPHA * K)
        e_inv = float((1.0 / ps).mean())
        rows[s] = {"E_inv_p": e_inv, "n_req": SIGMA2 * e_inv / TARGET_SE ** 2}
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=20)
    ap.add_argument("--nsim", type=int, default=200)
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()

    P = true_dists(LABELS_PATH)
    n_ctx = len(P)
    print(f"true dists from {n_ctx} contexts (judge32b), modal REBT share "
          f"{P[:, REBT_IDX].mean():.3f}")
    rng = np.random.default_rng(args.seed)

    recs = []
    for q in (0.0, 0.05, 0.1, 0.2):
        for mode in ("symmetric", "absorbing"):
            if q == 0.0 and mode == "absorbing":
                continue
            acc = {s: [] for s in STRATEGIES}
            for _ in range(args.nsim):
                lab = np.array([rng.choice(K, size=args.k, p=P[i])
                                for i in range(n_ctx)])
                lab = np.array([corrupt(lab[i], q, mode, rng) for i in range(n_ctx)])
                res = pipeline_neff(lab)
                for s in STRATEGIES:
                    acc[s].append(res[s]["n_req"])
            for s in STRATEGIES:
                a = np.array(acc[s])
                recs.append({"q": q, "mode": mode if q > 0 else "none",
                             "strategy": s,
                             "n_req_mean": round(float(a.mean())),
                             "n_req_lo95": round(float(np.quantile(a, 0.025))),
                             "n_req_hi95": round(float(np.quantile(a, 0.975)))})
    df = pd.DataFrame(recs)
    base = df[df["mode"] == "none"].set_index("strategy")["n_req_mean"]
    df["rel_to_q0"] = df.apply(lambda r: round(r["n_req_mean"] / base[r["strategy"]], 3), axis=1)

    show = df[df.strategy.isin(["FACT", "REBT", "SOCR"])]
    print(show.to_string(index=False))
    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(os.path.join(outdir, "label_error.csv"), index=False)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 3.6))
    for s, marker in (("FACT", "o"), ("SOCR", "s")):
        for mode, ls in (("symmetric", "--"), ("absorbing", "-")):
            sub = df[(df.strategy == s) & (df["mode"].isin(["none", mode]))].sort_values("q")
            ax.plot(sub.q, sub.rel_to_q0, marker=marker, ls=ls, ms=4,
                    label=f"{s} ({mode})")
    ax.axhline(1.0, color="gray", lw=0.7)
    ax.set_xlabel("label error rate q")
    ax.set_ylabel("n_req relative to q=0")
    ax.set_title("label misclassification bias on rare-strategy n_req")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "label_error.png"), dpi=200)
    print("saved results/label_error.csv, label_error.png")


if __name__ == "__main__":
    main()
