"""
Temperature-indexed identification collapse (theory/temperature_collapse.md).

The deployed policy is softmax in a history-dependent score gap with effective
temperature tau. At tau = 1 it reproduces simulation.py's adaptive policy
(P(evidence|defensive) = 0.85, P(evidence|receptive) = 0.30). As tau -> 0 the
policy becomes deterministic-in-history.

Validates three predictions:
  P1  SE of IPW grows exponentially in 1/tau, tracking the scaled
      inverse-propensity diagnostic curve (not a formal efficiency bound)
  P2  effective sample collapses exponentially. Reported separately
      (2026-07-30, 4th-critique fix): global arm-specific Kish ESS
      (theory object, n_eff(a)/n -> 1/E[1/p_a]), min stratum-arm cell
      occupancy (NOT Kish -- rare-crossover diagnostic), overlap-weight
      mass E[p(1-p)] (Result B object), and overlap coefficient
      E[2min(p,1-p)] (diagnostic).
  P3  naive analysis gets MORE confident (smaller SE) while staying wrong
      (bias flat, coverage ~ 0) as tau falls. Coverage reported both
      conditional on estimability and unconditional (success-and-cover),
      plus zero-cell / estimability rates so NaN-dropping hides nothing.

Usage: python temperature_collapse.py [--nsims 300] [--n 2000]
Outputs: ../results/collapse_results.csv, ../results/collapse_curve.png
"""

import argparse
import os

import numpy as np
import pandas as pd

T = 3
TAU_EVIDENCE, TAU_QUESTION = 0.30, 0.15
GAMMA_U, GAMMA_X = -0.80, 0.20
SIGMA_G, SIGMA_Y = 0.30, 1.00
# score gaps chosen so tau=1 reproduces the 0.85 / 0.30 adaptive policy
GAP_DEF = np.log(0.85 / 0.15)     # +1.7346 when defensive
GAP_REC = np.log(0.30 / 0.70)     # -0.8473 when receptive
FOCAL_TURN = 1                    # turn index (0-based) reported in the figure


def propensity(d_prev, tau):
    gap = np.where(d_prev == 1, GAP_DEF, GAP_REC)
    return 1.0 / (1.0 + np.exp(-gap / tau))


def defensiveness(u, x, prev_s, prev_d, rng):
    logit = 0.9 * u + 0.3 * x - 0.6 + 0.8 * prev_d * prev_s - 0.5 * (1 - prev_s) * prev_d
    p = 1.0 / (1.0 + np.exp(-logit))
    return (rng.uniform(size=u.shape) < p).astype(float)


def simulate(n, rng, tau, do_turn=None, do_value=None):
    u = rng.normal(size=n)
    x = rng.normal(size=n)
    d = (rng.uniform(size=n) < 1 / (1 + np.exp(-(0.9 * u + 0.3 * x)))).astype(float)
    S, D, P = [], [], []
    contrib = np.zeros(n)
    for t in range(T):
        p = propensity(d, tau)
        s = (rng.uniform(size=n) < p).astype(float)
        if do_turn is not None and t == do_turn:
            s = np.full(n, float(do_value))
        q = rng.normal(1.0, SIGMA_G, size=n)
        eff = np.where(s == 1, TAU_EVIDENCE, TAU_QUESTION) * q
        eff *= np.where((s == 1) & (d == 1), 0.5, 1.0)
        contrib += eff
        S.append(s); D.append(d.copy()); P.append(p)
        d = defensiveness(u, x, s, d, rng)
    y = GAMMA_U * u + GAMMA_X * x + contrib + rng.normal(0, SIGMA_Y, size=n)
    return {"y": y, "S": np.array(S).T, "D": np.array(D).T, "P": np.array(P).T, "x": x}


def est_naive(data, t):
    y, s = data["y"], data["S"][:, t]
    m1, m0 = y[s == 1], y[s == 0]
    if len(m1) < 2 or len(m0) < 2:
        return np.nan, np.nan
    return (m1.mean() - m0.mean(),
            np.sqrt(m1.var(ddof=1) / len(m1) + m0.var(ddof=1) / len(m0)))


def est_ipw(data, t):
    y, s, p = data["y"], data["S"][:, t], data["P"][:, t]
    w1, w0 = s / p, (1 - s) / (1 - p)
    if w1.sum() == 0 or w0.sum() == 0:
        return np.nan, np.nan
    mu1, mu0 = np.sum(w1 * y) / np.sum(w1), np.sum(w0 * y) / np.sum(w0)
    inf = w1 * (y - mu1) / w1.mean() - w0 * (y - mu0) / w0.mean()
    return mu1 - mu0, inf.std(ddof=1) / np.sqrt(len(y))


def min_cell_occupancy(data, t):
    """RENAMED 2026-07-30 (4차 비판): 구명 kish_ess_minority.
    이 DGP에서는 층 내 propensity가 상수라 셀 내부 가중치가 동일하고,
    따라서 이 지표는 Kish ESS가 아니라 'minimum realized stratum-arm cell
    fraction'이다. 희귀 crossover가 표본에서 사라지는 현상의 직접 증거로
    유지하되, 이론의 arm-specific Kish ESS(아래 global_arm_kish)와 혼동 금지."""
    s, p, d = data["S"][:, t], data["P"][:, t], data["D"][:, t]
    n = len(s)
    fracs = []
    for stratum in (0.0, 1.0):
        m = d == stratum
        if m.sum() == 0:
            continue
        for arm in (0.0, 1.0):
            sel = m & (s == arm)
            if sel.sum() == 0:
                fracs.append(0.0); continue
            w = 1.0 / np.where(arm == 1, p[sel], 1 - p[sel])
            fracs.append((w.sum() ** 2 / (w ** 2).sum()) / n)
    return min(fracs) if fracs else 0.0


def global_arm_kish(data, t):
    """NEW 2026-07-30: 이론(Result A)의 arm-specific Kish ESS와 같은 객체.
    n_eff(a)/n -> 1/E[1/p_a(H)]. treated/control 각각의 전역 Kish ESS 비율."""
    s, p = data["S"][:, t], data["P"][:, t]
    n = len(s)
    out = []
    for arm, pa in ((1.0, p), (0.0, 1 - p)):
        sel = s == arm
        if sel.sum() == 0:
            out.append(0.0); continue
        w = 1.0 / pa[sel]
        out.append((w.sum() ** 2 / (w ** 2).sum()) / n)
    return out[0], out[1]  # (treated, control)


def overlap_weight_mass(data, t):
    """Result B의 정리 객체: M^OW = E[p(1-p)] (overlap-weight 질량)."""
    p = data["P"][:, t]
    return float(np.mean(p * (1 - p)))


def overlap_coefficient(data, t):
    """진단용 별도 객체: O = E[2 min(p, 1-p)] (policy overlap coefficient).
    Result B를 직접 검증하는 것은 overlap_weight_mass 쪽이다."""
    p = data["P"][:, t]
    return float(np.mean(2 * np.minimum(p, 1 - p)))


def estimability(data, t):
    """NEW 2026-07-30: 극단 tau에서 NaN 제거가 실패를 숨기지 않도록
    replication 단위 진단 — 빈 arm/셀 여부와 최대 IPW 가중치."""
    s, p, d = data["S"][:, t], data["P"][:, t], data["D"][:, t]
    zero_treated = float((s == 1).sum() == 0)
    zero_control = float((s == 0).sum() == 0)
    zero_cell = 0.0
    for stratum in (0.0, 1.0):
        m = d == stratum
        if m.sum() == 0:
            continue
        for arm in (0.0, 1.0):
            if (m & (s == arm)).sum() == 0:
                zero_cell = 1.0
    w = np.where(s == 1, 1 / p, 1 / (1 - p))
    return zero_treated, zero_control, zero_cell, float(w.max())


def theory_se(tau, n, rng, m=200_000):
    """Scaled inverse-propensity diagnostic (NOT a formal efficiency bound):
    sqrt( E[1/p] + E[1/(1-p)] ) / sqrt(n), scaled by a constant calibrated
    at the largest tau. Tracks the exponential growth rate of Result 2."""
    data = simulate(m, rng, tau)
    p = data["P"][:, FOCAL_TURN]
    return np.sqrt((np.mean(1 / p) + np.mean(1 / (1 - p))) / n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nsims", type=int, default=300)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    taus = [4.0, 2.0, 1.0, 0.6, 0.4, 0.3, 0.22, 0.15]
    rows = []
    for tau in taus:
        y1 = simulate(150_000, rng, tau, do_turn=FOCAL_TURN, do_value=1)["y"].mean()
        y0 = simulate(150_000, rng, tau, do_turn=FOCAL_TURN, do_value=0)["y"].mean()
        truth = y1 - y0
        res = {"naive": [], "ipw": []}
        occ, k1, k0, owm, ovc = [], [], [], [], []
        zt, zc, zcell, maxw = [], [], [], []
        for _ in range(args.nsims):
            data = simulate(args.n, rng, tau)
            res["naive"].append(est_naive(data, FOCAL_TURN))
            res["ipw"].append(est_ipw(data, FOCAL_TURN))
            occ.append(min_cell_occupancy(data, FOCAL_TURN))
            e1, e0 = global_arm_kish(data, FOCAL_TURN)
            k1.append(e1); k0.append(e0)
            owm.append(overlap_weight_mass(data, FOCAL_TURN))
            ovc.append(overlap_coefficient(data, FOCAL_TURN))
            a, b, c, w = estimability(data, FOCAL_TURN)
            zt.append(a); zc.append(b); zcell.append(c); maxw.append(w)
        row = {"tau": tau, "truth": truth,
               "min_cell_occupancy": float(np.mean(occ)),        # 구명 ess_frac (Kish 아님)
               "kish_ess1_frac": float(np.mean(k1)),             # 이론 대응: 1/E[1/p]
               "kish_ess0_frac": float(np.mean(k0)),             # 이론 대응: 1/E[1/(1-p)]
               "overlap_weight_mass": float(np.mean(owm)),       # Result B 객체 E[p(1-p)]
               "overlap_coefficient": float(np.mean(ovc)),       # 진단 E[2min(p,1-p)]
               "zero_treated_rate": float(np.mean(zt)),
               "zero_control_rate": float(np.mean(zc)),
               "zero_stratum_arm_rate": float(np.mean(zcell)),
               "median_max_weight": float(np.median(maxw)),
               "p95_max_weight": float(np.quantile(maxw, 0.95)),
               "theory_se_raw": theory_se(tau, args.n, rng)}
        for name in ["naive", "ipw"]:
            arr = np.array(res[name], dtype=float)
            est, se = arr[:, 0], arr[:, 1]
            ok = ~np.isnan(est)
            hit = (est[ok] - 1.96 * se[ok] <= truth) & (truth <= est[ok] + 1.96 * se[ok])
            row.update({f"{name}_bias": np.nanmean(est) - truth,
                        f"{name}_rmse": float(np.sqrt(np.nanmean((est - truth) ** 2))),
                        f"{name}_sd": np.nanstd(est, ddof=1),
                        f"{name}_estimable_rate": float(ok.mean()),
                        # conditional: 추정 가능한 replication 중 커버율
                        f"{name}_cover_cond": float(np.mean(hit)) if ok.sum() else np.nan,
                        # unconditional: 추정 실패를 커버 실패로 집계 (success-and-cover)
                        f"{name}_cover_uncond": float(hit.sum() / len(est))})
        rows.append(row)
        print(f"tau={tau:5.2f}  truth={truth:+.4f}  "
              f"naive bias={row['naive_bias']:+.3f} (cover_c {row['naive_cover_cond']:.2f})  "
              f"ipw sd={row['ipw_sd']:.3f} est_rate={row['ipw_estimable_rate']:.2f}  "
              f"occ={row['min_cell_occupancy']:.4f} kish1={row['kish_ess1_frac']:.4f}")

    df = pd.DataFrame(rows)
    # calibrate theory curve to simulated IPW SD at the largest tau
    c = df["ipw_sd"].iloc[0] / df["theory_se_raw"].iloc[0]
    df["theory_se"] = c * df["theory_se_raw"]

    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(os.path.join(outdir, "collapse_results.csv"), index=False)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    inv = 1 / df["tau"]
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.6))

    ax = axes[0]
    ax.plot(inv, df["ipw_sd"], "o", label="IPW SE (simulated)")
    ax.plot(inv, df["theory_se"], "-",
            label="scaled inverse-propensity diagnostic\n$\\propto\\sqrt{E[1/p]+E[1/(1-p)]}$")
    ax.set_yscale("log"); ax.set_xlabel("policy determinism  $1/\\tau$")
    ax.set_ylabel("SE of excursion-effect estimate")
    ax.set_title("P1: SE explodes; at extreme 1/τ empirical SD\nunderstates (rare crossovers unobserved → bias)", fontsize=9)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    ax.plot(inv, np.minimum(df["kish_ess1_frac"], df["kish_ess0_frac"]), "o-",
            label="min arm Kish ESS/n (theory object)")
    ax.plot(inv, df["min_cell_occupancy"], "^:",
            label="min stratum-arm cell fraction\n(NOT Kish; rare-crossover diagnostic)")
    ax.plot(inv, df["overlap_weight_mass"], "s--",
            label="$E[p(1-p)]$ (Result B object)")
    ax.plot(inv, df["overlap_coefficient"], "d-.",
            label="$E[2\\min(p,1-p)]$ (overlap coef.)")
    ax.legend(frameon=False, fontsize=7)
    ax.set_yscale("log"); ax.set_xlabel("policy determinism  $1/\\tau$")
    ax.set_ylabel("fraction of n")
    ax.set_title("P2: effective sample & overlap collapse")

    ax = axes[2]
    ax.plot(inv, df["naive_bias"], "o-", color="crimson", label="naive bias")
    ax.plot(inv, df["naive_sd"], "s--", color="gray", label="naive SE")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("policy determinism  $1/\\tau$")
    ax.set_title("P3: naive gets confidently wrong\n(cond. coverage = "
                 f"{df['naive_cover_cond'].min():.0%}–{df['naive_cover_cond'].max():.0%})")
    ax.legend(frameon=False, fontsize=8)

    fig.suptitle("Identification collapse under an adaptive deployed policy "
                 "(softmax temperature $\\tau$)", y=1.02, fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "collapse_curve.png"), dpi=200, bbox_inches="tight")
    print("saved results/collapse_curve.png")


if __name__ == "__main__":
    main()
