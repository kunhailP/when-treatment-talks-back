"""Draw the manuscript figures from simulation/results/separation/{phase,curve}.csv.

  python plot_figures.py            # writes paper/tex/figs/fig1_separation_map.pdf, fig2_temperature_curve.pdf

No computation happens here beyond evaluating the saved exact moments on an (n, 1/tau) grid.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, "..", "..", "results", "separation"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "paper", "tex", "figs"))
DELTA = 0.1
LOSS_LEVELS = [1, 10, 100, 1000]

plt.rcParams.update({"font.size": 9, "axes.titlesize": 9.5, "axes.labelsize": 9,
                     "legend.fontsize": 7.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
                     "pdf.fonttype": 42})
C_POP, C_AIPW, C_BND, C_LOSS = "#b2182b", "#ef8a62", "#2166ac", "#4d4d4d"


def figure1():
    ph = pd.read_csv(os.path.join(RES, "phase.csv")).sort_values("inv_tau")
    inv_tau = ph.inv_tau.to_numpy()
    log_n = np.linspace(2, 9, 281)
    N = 10 ** log_n[:, None]
    rmse_pop = np.sqrt(ph.v_ht.to_numpy()[None, :] / N)
    rmse_bnd = np.sqrt(ph.bias_b.to_numpy()[None, :] ** 2 + ph.v_b.to_numpy()[None, :] / N)
    loss = N * ph.loss_1.to_numpy()[None, :]

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.3), sharey=True, constrained_layout=True)
    panels = [(axes[0], rmse_pop, r"(a) population effect $\theta$ (HT)"),
              (axes[1], rmse_bnd, r"(b) boundary effect $\beta_0$ (Theorem 1)")]
    for ax, rmse, title in panels:
        z = np.clip(np.log10(rmse), -2.5, 1.0)                 # dark = large error
        pc = ax.pcolormesh(inv_tau, log_n, z, cmap="viridis_r", shading="auto", vmin=-2.5, vmax=1.0,
                           rasterized=True)
        ax.contourf(inv_tau, log_n, (rmse <= DELTA).astype(float), levels=[0.5, 1.5],
                    hatches=["////"], colors="none")
        ax.contour(inv_tau, log_n, rmse, levels=[DELTA], colors="white", linewidths=2.0)
        ax.contour(inv_tau, log_n, loss, levels=LOSS_LEVELS, colors="#f0f0f0", linewidths=0.9,
                   linestyles="--")
        for lev in LOSS_LEVELS:                      # label each loss contour at the right edge
            y = np.log10(lev / ph.loss_1.to_numpy()[-1])
            if log_n[0] < y < log_n[-1]:
                ax.text(inv_tau[-1] * 0.93, y + 0.12, rf"$R_n={lev:g}$", ha="right", va="bottom",
                        fontsize=6.5, color="black",
                        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
        feas = rmse <= DELTA
        if feas.any():                               # smallest exploration loss meeting the precision
            i, j = np.unravel_index(np.argmin(np.where(feas, loss, np.inf)), loss.shape)
            ax.plot(inv_tau[j], log_n[i], marker="*", ms=11, color="#ffd92f", mec="black", mew=0.7,
                    zorder=5)
            right = j > len(inv_tau) // 2
            ax.annotate(rf"min $R_n\approx{loss[i, j]:.3g}$", (inv_tau[j], log_n[i]),
                        xytext=(-8 if right else 6, -14), textcoords="offset points", fontsize=7,
                        ha="right" if right else "left",
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
        ax.set_xscale("log")
        ax.set_xlabel(r"sharpness $1/\tau$ (one common temperature)")
        ax.set_title(title)
    axes[0].set_ylabel(r"$\log_{10} n$")
    cb = fig.colorbar(pc, ax=axes, shrink=0.9, pad=0.01)
    cb.set_label(r"$\log_{10}$ RMSE (exact)")
    os.makedirs(FIGS, exist_ok=True)
    fig.savefig(os.path.join(FIGS, "fig1_separation_map.pdf"), dpi=300)
    plt.close(fig)

    # numbers quoted with the figure
    feas_pop, feas_bnd = rmse_pop <= DELTA, rmse_bnd <= DELTA
    def argmin_point(feas):
        i, j = np.unravel_index(np.argmin(np.where(feas, loss, np.inf)), loss.shape)
        return dict(min_loss=float(loss[i, j]), log10_n=float(log_n[i]), inv_tau=float(inv_tau[j]))
    out = dict(delta=DELTA, grid_log10_n=[float(log_n[0]), float(log_n[-1])],
               grid_inv_tau=[float(inv_tau[0]), float(inv_tau[-1])],
               population=argmin_point(feas_pop), boundary=argmin_point(feas_bnd))
    with open(os.path.join(RES, "fig1_numbers.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    return out


def figure2():
    cu = pd.read_csv(os.path.join(RES, "curve.csv")).sort_values("inv_tau")
    x = cu.inv_tau.to_numpy()
    n = int(cu.n.iloc[0])
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7), constrained_layout=True)

    ax = axes[0]
    ax.plot(x, cu.ht_sd_exact, color=C_POP, lw=1.3, label=r"HT, exact SD")
    ax.plot(x, cu.aipw_sd_exact, color=C_AIPW, lw=1.3, ls="-.", label=r"AIPW, exact SD")
    ax.plot(x, cu.bnd_rmse_exact, color=C_BND, lw=1.3, label=r"boundary, exact RMSE")
    ax.plot(x, cu.ht_rmse_mc, "o", color=C_POP, ms=3.5, mfc="none")
    ax.plot(x, cu.aipw_rmse_mc, "s", color=C_AIPW, ms=3.2, mfc="none")
    ax.plot(x, cu.bnd_rmse_mc, "^", color=C_BND, ms=3.5, mfc="none")
    ax.set_yscale("log")
    ax.set_ylim(5e-3, 1e4)
    ax.set_ylabel("RMSE / SD")
    ax.set_title("(a) error (lines exact, markers MC)")
    ax.legend(loc="upper left", frameon=False)

    ax = axes[1]
    for key, col, mk, lab in (("ht", C_POP, "o", r"HT for $\theta$"), ("aipw", C_AIPW, "s", r"AIPW for $\theta$"),
                              ("bnd", C_BND, "^", r"boundary for $\beta_0$")):
        ax.errorbar(x, cu[f"{key}_coverage"], yerr=1.96 * cu[f"{key}_coverage_mcse"], fmt=mk, color=col,
                    ms=3.5, mfc="none", lw=0.8, capsize=1.5, label=lab)
    ax.axhline(0.95, color="grey", lw=0.8, ls=":")
    ax.set_ylim(0, 1.02)
    ax.set_ylabel("Wald coverage (MC)")
    ax.set_title("(b) coverage")
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.42), frameon=False)

    ax = axes[2]
    ax.plot(x, cu.loss_exact, color=C_LOSS, lw=1.3, label=r"loss $R_n$, exact")
    ax.plot(x, cu.loss_mc, "D", color=C_LOSS, ms=3, mfc="none")
    ax.plot(x, cu.offgreedy_exact, color="#7b3294", lw=1.3, ls="--", label="off-greedy actions, exact")
    ax.plot(x, cu.offgreedy_mc, "v", color="#7b3294", ms=3, mfc="none")
    ax.set_yscale("log")
    ax.set_title("(c) exploration")
    ax.legend(loc="lower left", frameon=False)

    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlabel(r"$1/\tau$")
    fig.suptitle(rf"Common temperature, $n={n:,}$, {int(cu.reps.iloc[0]):,} replications per $\tau$",
                 fontsize=9)
    fig.savefig(os.path.join(FIGS, "fig2_temperature_curve.pdf"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    print(figure1())
    if os.path.exists(os.path.join(RES, "curve.csv")):
        figure2()
    print("figures written to", FIGS)
