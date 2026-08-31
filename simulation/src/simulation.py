"""
Response-adaptive confounding in generative dialogue experiments.

Demonstrates why naive transcript analysis of turn-level strategy effects is
biased when the deployed policy adapts to user reactions, and why known
turn-level randomization (G-MRT) restores identification.

DGP (T = 3 turns, K = 2 strategies):
  U_i          latent resistance (unobserved)
  X_i          observed prior covariate
  D_{t-1}      defensiveness state before turn t (depends on U, X, past strategies)
  S_t in {0,1} strategy: 1 = direct factual evidence, 0 = Socratic question
  Q_t          generator realization quality ~ N(1, sigma_g)  [stochastic generation]
  Y            final belief-accuracy change

Adaptive (observational) logging policy: defensive users are much more likely
to receive the evidence strategy -> evidence-receivers are systematically the
hard-to-persuade -> naive comparison is biased downward (can flip sign).

Estimand: turn-t excursion effect beta_t = E[Y | do(S_t=1)] - E[Y | do(S_t=0)],
with all other turns following the same behavior policy.

Estimators compared, per regime (adaptive logging vs G-MRT uniform):
  naive : difference in means of Y by S_t
  ipw   : Hajek IPW with true propensities (known by design in G-MRT;
          in the observational regime this stands in for a correctly
          specified history model -- the best case for post-hoc analysis)
  dr    : AIPW with linear outcome model on (S_t, D_{t-1}, X)

Usage:  python simulation.py [--nsims 500] [--n 2000] [--seed 7]
Outputs: ../results/results.csv, ../results/bias_plot.png
"""

import argparse
import os

import numpy as np
import pandas as pd

T = 3
TAU_EVIDENCE = 0.30   # per-turn effect of evidence strategy (scaled by Q_t)
TAU_QUESTION = 0.15   # per-turn effect of question strategy
GAMMA_U = -0.80       # resistance lowers final belief change
GAMMA_X = 0.20
SIGMA_G = 0.30        # generator realization noise
SIGMA_Y = 1.00


def defensiveness(u, x, prev_s, prev_d, rng):
    """P(defensive at next turn). Evidence pushed at an already-defensive
    user entrenches; questions de-escalate."""
    logit = 0.9 * u + 0.3 * x - 0.6 + 0.8 * prev_d * prev_s - 0.5 * (1 - prev_s) * prev_d
    p = 1.0 / (1.0 + np.exp(-logit))
    return (rng.uniform(size=u.shape) < p).astype(float)


def propensity(d_prev, regime):
    """P(S_t = evidence | history)."""
    if regime == "adaptive":
        return np.where(d_prev == 1, 0.85, 0.30)
    if regime == "gmrt":
        return np.full_like(d_prev, 0.5, dtype=float)
    raise ValueError(regime)


def simulate(n, rng, regime, do_turn=None, do_value=None):
    """Run the dialogue DGP. Optionally intervene on S at turn `do_turn`."""
    u = rng.normal(size=n)
    x = rng.normal(size=n)
    d = (rng.uniform(size=n) < 1 / (1 + np.exp(-(0.9 * u + 0.3 * x)))).astype(float)

    S, D_hist, P_hist = [], [], []
    contrib = np.zeros(n)
    for t in range(T):
        p = propensity(d, regime)
        s = (rng.uniform(size=n) < p).astype(float)
        if do_turn is not None and t == do_turn:
            s = np.full(n, float(do_value))
        q = rng.normal(1.0, SIGMA_G, size=n)          # generator realization
        tau = np.where(s == 1, TAU_EVIDENCE, TAU_QUESTION) * q
        # entrenchment: evidence on a defensive user loses half its effect
        tau = tau * np.where((s == 1) & (d == 1), 0.5, 1.0)
        contrib += tau
        S.append(s); D_hist.append(d.copy()); P_hist.append(p)
        d = defensiveness(u, x, s, d, rng)

    y = GAMMA_U * u + GAMMA_X * x + contrib + rng.normal(0, SIGMA_Y, size=n)
    return {"y": y, "S": np.array(S).T, "D": np.array(D_hist).T,
            "P": np.array(P_hist).T, "x": x}


def true_excursion(regime, turn, rng, n=400_000):
    y1 = simulate(n, rng, regime, do_turn=turn, do_value=1)["y"].mean()
    y0 = simulate(n, rng, regime, do_turn=turn, do_value=0)["y"].mean()
    return y1 - y0


def est_naive(data, t):
    y, s = data["y"], data["S"][:, t]
    m1, m0 = y[s == 1], y[s == 0]
    est = m1.mean() - m0.mean()
    se = np.sqrt(m1.var(ddof=1) / len(m1) + m0.var(ddof=1) / len(m0))
    return est, se


def est_ipw(data, t):
    y, s, p = data["y"], data["S"][:, t], data["P"][:, t]
    w1, w0 = s / p, (1 - s) / (1 - p)
    mu1, mu0 = np.sum(w1 * y) / np.sum(w1), np.sum(w0 * y) / np.sum(w0)
    est = mu1 - mu0
    n = len(y)
    inf = w1 * (y - mu1) / w1.mean() - w0 * (y - mu0) / w0.mean()
    se = inf.std(ddof=1) / np.sqrt(n)
    return est, se


def est_dr(data, t):
    y, s, p = data["y"], data["S"][:, t], data["P"][:, t]
    d_prev, x = data["D"][:, t], data["x"]
    Z = np.column_stack([np.ones_like(y), s, d_prev, x, s * d_prev])
    beta, *_ = np.linalg.lstsq(Z, y, rcond=None)
    Z1 = Z.copy(); Z1[:, 1] = 1; Z1[:, 4] = d_prev
    Z0 = Z.copy(); Z0[:, 1] = 0; Z0[:, 4] = 0
    m1, m0 = Z1 @ beta, Z0 @ beta
    if1 = m1 + s / p * (y - m1)
    if0 = m0 + (1 - s) / (1 - p) * (y - m0)
    inf = if1 - if0
    return inf.mean(), inf.std(ddof=1) / np.sqrt(len(y))


ESTIMATORS = {"naive": est_naive, "ipw": est_ipw, "dr": est_dr}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nsims", type=int, default=500)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    rows = []
    for regime in ["adaptive", "gmrt"]:
        truths = {t: true_excursion(regime, t, rng) for t in range(T)}
        results = {(t, e): [] for t in range(T) for e in ESTIMATORS}
        for _ in range(args.nsims):
            data = simulate(args.n, rng, regime)
            for t in range(T):
                for name, fn in ESTIMATORS.items():
                    results[(t, name)].append(fn(data, t))
        for t in range(T):
            for name in ESTIMATORS:
                arr = np.array(results[(t, name)])
                est, se = arr[:, 0], arr[:, 1]
                truth = truths[t]
                cover = np.mean((est - 1.96 * se <= truth) & (truth <= est + 1.96 * se))
                rows.append({
                    "regime": regime, "turn": t + 1, "estimator": name,
                    "truth": round(truth, 4), "mean_est": round(est.mean(), 4),
                    "bias": round(est.mean() - truth, 4),
                    "rmse": round(np.sqrt(((est - truth) ** 2).mean()), 4),
                    "coverage95": round(cover, 3),
                })

    df = pd.DataFrame(rows)
    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(os.path.join(outdir, "results.csv"), index=False)
    print(df.to_string(index=False))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
        for ax, regime, title in zip(
            axes, ["adaptive", "gmrt"],
            ["Adaptive deployed policy\n(observational transcripts)",
             "G-MRT\n(known turn-level randomization)"]):
            sub = df[df.regime == regime]
            for i, name in enumerate(ESTIMATORS):
                s = sub[sub.estimator == name]
                ax.bar(np.arange(T) + (i - 1) * 0.25, s["bias"], width=0.24, label=name)
            ax.axhline(0, color="k", lw=0.8)
            ax.set_xticks(range(T), [f"turn {t+1}" for t in range(T)])
            ax.set_title(title, fontsize=10)
        axes[0].set_ylabel("bias of estimated excursion effect")
        axes[1].legend(frameon=False)
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, "bias_plot.png"), dpi=200)
        print("\nSaved figure to results/bias_plot.png")
    except ImportError:
        print("matplotlib not available; skipped figure")


if __name__ == "__main__":
    main()
