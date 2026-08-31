"""
W4 연속 H 시뮬레이션 + (n,τ) 위상도 (nonidentification_note TODO 4 사양).

DGP (주): H ~ Uniform(-1,1), Δ(H)=H, p_τ(H)=logit⁻¹(H/τ), A~Bern(p_τ),
          Y = H + β(H)·A + N(0,1)  (baseline이 H와 교란되도록 μ0(H)=H)
     (robustness): H ~ N(0,1) — --dgp normal
β(H) 3종: const=1 · smooth=1+exp(−H²) · kink=1+|H|

추정량 배터리 (각자의 target 명시 — 반례 "고정 τ에서 target 불변" 규율):
  ht, hajek, trunc(p∈[.01,.99] clip), aipw_oracle(참 μ_a), or_oracle(참 μ_a plug-in)
    → target = ATE = E[β(H)]
  overlap(OW: treated 1−p / control p 가중)
    → target = β^ov_τ = E[ω_τ β]/E[ω_τ]  (별도 estimand — ATE 대비 편향으로 읽지 말 것)
  or_oracle은 (A3)의 예시다: 참 outcome model을 "믿으면" 붕괴를 피한다
  — 식별을 가정으로 사는 것 (framework §3).

지표: bias·sd·rmse·coverage(conditional/unconditional, 각자 target 기준)
  + 실현 arm-specific Kish ESS + zero-arm rate + population 객체
  (E[1/p_τ]: Uniform 닫힌형 1+τ·sinh(1/τ) — --selftest로 MC 대조,
   E[ω_τ]=overlap mass).

위상도 (β=kink, hajek 기준): 셀 국면 분류
  estimable       : |상대편향| ≤ .10 이고 uncond coverage ≥ .85
  variance-expl   : 나머지 (분산 지배)
  biased-stable   : |상대편향| ≥ .20 이고 sd < |bias| (편향된 채 안정)
  경계선 2개: 점선 log n = δ/τ (δ=1, 고정-gap heuristic)
             실선 log n = log E[1/p_τ] = log(1+τ·sinh(1/τ)) (정확, Uniform)
  ※ 국면 임계값은 presentation 선택이며 민감도는 RMSE·coverage 판을 병기해 방어.

Usage: python continuous_h.py [--nsims 400] [--dgp uniform|normal] [--selftest]
Outputs: ../results/continuous_h_results.csv, continuous_h_battery.png,
         phase_diagram.png (uniform일 때)
"""

import argparse
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd

TAUS = [1.0, 0.6, 0.4, 0.3, 0.22, 0.15, 0.11, 0.08, 0.06, 0.045]
NS = [125, 250, 500, 1000, 2000, 4000, 8000, 16000, 32000]
BETAS = {
    "const": lambda h: np.ones_like(h),
    "smooth": lambda h: 1.0 + np.exp(-h ** 2),
    "kink": lambda h: 1.0 + np.abs(h),
}
Z = 1.959963984540054


def draw_h(dgp, n, rng):
    return rng.uniform(-1, 1, n) if dgp == "uniform" else rng.normal(0, 1, n)


def p_tau(h, tau):
    return 1.0 / (1.0 + np.exp(-h / tau))


def population_objects(dgp, beta_fn, tau, m=2_000_000, seed=0):
    """ATE, β^ov_τ, E[1/p], E[1/(1-p)], E[ω_τ] — MC (Uniform은 닫힌형과 대조 가능)."""
    rng = np.random.default_rng(seed)
    h = draw_h(dgp, m, rng)
    p = p_tau(h, tau)
    b = beta_fn(h)
    w = p * (1 - p)
    return {"ate": b.mean(), "beta_ov": (w * b).sum() / w.sum(),
            "e_inv_p": (1 / p).mean(), "e_inv_q": (1 / (1 - p)).mean(),
            "overlap_mass": w.mean()}


def kish(w):
    s = w.sum()
    return (s * s / (w * w).sum()) if len(w) and s > 0 else 0.0


def one_sim(dgp, beta_fn, tau, n, rng):
    h = draw_h(dgp, n, rng)
    p = p_tau(h, tau)
    a = (rng.uniform(size=n) < p).astype(float)
    b = beta_fn(h)
    y = h + b * a + rng.normal(0, 1, n)
    mu0, mu1 = h, h + b  # oracle outcome models
    out = {}
    n1, n0 = a.sum(), n - a.sum()
    out["zero_arm"] = float(n1 == 0 or n0 == 0)
    out["kish1"] = kish((a / p)[a == 1]) / n
    out["kish0"] = kish(((1 - a) / (1 - p))[a == 0]) / n

    def rec(name, est, se):
        out[name] = est
        out[name + "_se"] = se

    # HT + Hájek + truncated (influence-curve SE)
    inf = a * y / p - (1 - a) * y / (1 - p)
    rec("ht", inf.mean(), inf.std(ddof=1) / np.sqrt(n))
    for name, pc in (("hajek", p), ("trunc", np.clip(p, 0.01, 0.99))):
        w1, w0 = a / pc, (1 - a) / (1 - pc)
        if w1.sum() == 0 or w0.sum() == 0:
            rec(name, np.nan, np.nan)
            continue
        m1, m0 = (w1 * y).sum() / w1.sum(), (w0 * y).sum() / w0.sum()
        infh = w1 * (y - m1) / w1.mean() - w0 * (y - m0) / w0.mean()
        rec(name, m1 - m0, infh.std(ddof=1) / np.sqrt(n))
    # AIPW (oracle μ) + oracle OR plug-in
    infa = mu1 - mu0 + a * (y - mu1) / p - (1 - a) * (y - mu0) / (1 - p)
    rec("aipw_oracle", infa.mean(), infa.std(ddof=1) / np.sqrt(n))
    rec("or_oracle", (mu1 - mu0).mean(), (mu1 - mu0).std(ddof=1) / np.sqrt(n))
    # Overlap weighting → target β^ov
    w1, w0 = a * (1 - p), (1 - a) * p
    if w1.sum() > 0 and w0.sum() > 0:
        m1, m0 = (w1 * y).sum() / w1.sum(), (w0 * y).sum() / w0.sum()
        info = w1 * (y - m1) / w1.mean() - w0 * (y - m0) / w0.mean()
        rec("overlap", m1 - m0, info.std(ddof=1) / np.sqrt(n))
    else:
        rec("overlap", np.nan, np.nan)
    return out


ESTIMATORS = ["ht", "hajek", "trunc", "aipw_oracle", "or_oracle", "overlap"]


def run_cell(job):
    dgp, bname, tau, n, nsims, seed = job
    beta_fn = BETAS[bname]
    pop = population_objects(dgp, beta_fn, tau, seed=hash((bname, tau)) % 2 ** 31)
    ss = np.random.SeedSequence([seed, NS.index(n), TAUS.index(tau)])
    rngs = [np.random.default_rng(s) for s in ss.spawn(nsims)]
    sims = [one_sim(dgp, beta_fn, tau, n, r) for r in rngs]
    df = pd.DataFrame(sims)
    row = {"dgp": dgp, "beta": bname, "tau": tau, "n": n,
           "ate": pop["ate"], "beta_ov": pop["beta_ov"],
           "e_inv_p": pop["e_inv_p"], "e_inv_q": pop["e_inv_q"],
           "overlap_mass": pop["overlap_mass"],
           "pop_kish_frac": 1.0 / max(pop["e_inv_p"], pop["e_inv_q"]),
           "zero_arm_rate": df["zero_arm"].mean(),
           "kish1_realized": df["kish1"].mean(), "kish0_realized": df["kish0"].mean()}
    for e in ESTIMATORS:
        tgt = pop["beta_ov"] if e == "overlap" else pop["ate"]
        est, se = df[e], df[e + "_se"]
        ok = est.notna() & se.notna()
        cover = ((est - Z * se <= tgt) & (tgt <= est + Z * se))[ok]
        row[f"{e}_bias"] = (est[ok] - tgt).mean() if ok.any() else np.nan
        row[f"{e}_sd"] = est[ok].std(ddof=1) if ok.sum() > 1 else np.nan
        row[f"{e}_rmse"] = np.sqrt(((est[ok] - tgt) ** 2).mean()) if ok.any() else np.nan
        row[f"{e}_estimable_rate"] = ok.mean()
        row[f"{e}_cover_cond"] = cover.mean() if ok.any() else np.nan
        row[f"{e}_cover_uncond"] = (cover.sum() / len(est))
    return row


def selftest():
    for tau in (0.3, 0.15, 0.6):
        mc = population_objects("uniform", BETAS["const"], tau)["e_inv_p"]
        closed = 1 + tau * np.sinh(1 / tau)
        print(f"tau={tau}: MC E[1/p]={mc:.4f}  closed 1+τ·sinh(1/τ)={closed:.4f}")
        assert abs(mc - closed) / closed < 0.01, "closed form mismatch"
    print("[selftest] E[1/p_τ] 닫힌형 일치")


def classify(row):
    ref = abs(row["ate"])
    rb, sd = row["hajek_bias"] / ref, row["hajek_sd"]
    if abs(rb) >= 0.20 and sd < abs(row["hajek_bias"]):
        return "biased-stable"
    if abs(rb) <= 0.10 and row["hajek_cover_uncond"] >= 0.85:
        return "estimable"
    return "variance-explosion"


def phase_figure(res, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    sub = res[(res.dgp == "uniform") & (res.beta == "kink")].copy()
    sub["regime"] = sub.apply(classify, axis=1)
    order = ["estimable", "variance-explosion", "biased-stable"]
    piv = {}
    for col, f in (("regime", lambda s: order.index(s.iloc[0])),
                   ("hajek_rmse", lambda s: s.iloc[0]),
                   ("hajek_cover_uncond", lambda s: s.iloc[0])):
        piv[col] = sub.pivot_table(index="n", columns="tau", values=col,
                                   aggfunc="first" if col == "regime" else "mean")
        if col == "regime":
            piv[col] = sub.assign(code=sub.regime.map(order.index)).pivot(
                index="n", columns="tau", values="code")

    inv_tau = sorted(1 / np.array(TAUS))
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    x = 1 / piv["regime"].columns.to_numpy()[::-1]
    yv = piv["regime"].index.to_numpy()
    grids = [(piv["regime"].to_numpy()[:, ::-1], "phase (hajek)",
              ListedColormap(["#4daf4a", "#ff7f00", "#e41a1c"]), None),
             (np.log10(piv["hajek_rmse"].to_numpy()[:, ::-1]), "log10 RMSE", "viridis", None),
             (piv["hajek_cover_uncond"].to_numpy()[:, ::-1], "coverage (uncond)", "viridis", (0, 1))]
    tt = np.linspace(min(x), max(x), 200)
    for ax, (g, title, cmap, clim) in zip(axes, grids):
        pc = ax.pcolormesh(x, np.log(yv), g, cmap=cmap, shading="nearest",
                           vmin=None if clim is None else clim[0],
                           vmax=None if clim is None else clim[1])
        ax.plot(tt, tt, "k--", lw=1.2, label=r"log n = $\delta/\tau$ ($\delta$=1)")
        ax.plot(tt, np.log(1 + (1 / tt) * np.sinh(tt)), "k-", lw=1.6,
                label=r"log n = log E[$1/p_\tau$]")
        ax.set_xlabel(r"$1/\tau$")
        ax.set_ylabel("log n")
        ax.set_ylim(np.log(yv.min()), np.log(yv.max()))
        ax.set_title(title)
        if title.startswith("phase"):
            ax.legend(fontsize=7, loc="upper left")
        else:
            fig.colorbar(pc, ax=ax)
    fig.suptitle("(n, τ) phase diagram — DGP H~U(−1,1), β(H)=1+|H|, Hájek", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "phase_diagram.png"), dpi=200, bbox_inches="tight")
    print("saved results/phase_diagram.png")


def battery_figure(res, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sub = res[(res.dgp == "uniform") & (res.beta == "kink") & (res.n == 4000)]
    sub = sub.sort_values("tau")
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.8))
    for e in ESTIMATORS:
        axes[0].plot(1 / sub.tau, sub[f"{e}_bias"].abs(), marker="o", ms=3, label=e)
        axes[1].plot(1 / sub.tau, sub[f"{e}_rmse"], marker="o", ms=3, label=e)
        axes[2].plot(1 / sub.tau, sub[f"{e}_cover_uncond"], marker="o", ms=3, label=e)
    for ax, t in zip(axes, ["|bias| (vs own target)", "RMSE", "coverage (uncond)"]):
        ax.set_xlabel(r"$1/\tau$")
        ax.set_title(t)
        ax.set_xscale("log")
    axes[1].set_yscale("log")
    axes[2].axhline(0.95, color="gray", lw=0.7, ls=":")
    axes[0].legend(fontsize=7)
    fig.suptitle("estimator battery — U(-1,1), beta=1+|H|, n=4000 (overlap targets beta^ov)", y=1.03)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "continuous_h_battery.png"), dpi=200, bbox_inches="tight")
    print("saved results/continuous_h_battery.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nsims", type=int, default=400)
    ap.add_argument("--dgp", default="uniform", choices=["uniform", "normal"])
    ap.add_argument("--betas", default="const,smooth,kink")
    ap.add_argument("--procs", type=int, default=min(64, os.cpu_count() or 8))
    ap.add_argument("--seed", type=int, default=20260730)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return

    jobs = [(args.dgp, b, tau, n, args.nsims, args.seed)
            for b in args.betas.split(",") for tau in TAUS for n in NS]
    print(f"cells={len(jobs)}  nsims={args.nsims}  procs={args.procs}")
    with Pool(args.procs) as pool:
        rows = pool.map(run_cell, jobs)
    res = pd.DataFrame(rows)

    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"continuous_h_results_{args.dgp}.csv")
    res.to_csv(path, index=False)
    print("saved", path)
    if args.dgp == "uniform":
        battery_figure(res, outdir)
        phase_figure(res, outdir)


if __name__ == "__main__":
    main()
