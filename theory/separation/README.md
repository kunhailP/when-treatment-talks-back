# Separation results (branch `jci-separation`)

This directory contains the proposed core of the JCI revision:

> For effects at the policy's decision boundary, valid inference is possible while cumulative exploration
> loss vanishes. For the population average effect, in a model without extrapolation structure, precision
> can be bought only with exploration loss, and deployment scale n does not substitute for it. A single
> common temperature makes that loss diverge; uniform mixing or context-dependent temperatures prevent it.

**Status.** Proofs are written in full and self-checked. **None is externally reviewed.** Novelty is
claimed only relative to the literature listed in `related_work.md`.

## Contents

| File | Results |
|---|---|
| `theorems_A_B_C.md` | Setup; **Thm A** (all-estimator information–exploration inequality, adaptive designs included); A′ (achievability sandwich); **Thm B** (single common temperature: loss ≳ n/log²(nδ²)); **Prop C** (context temperatures implement any design; optimal τ* grows with \|Δ\|); **Lemma R** (misspecified gaps, Kantorovich) |
| `theorem_D.md` | **Thm D**: boundary effect, Wald CI valid at β_0 while R_n → 0 for τ_n = n^{−α}, α ∈ (1/2, 1); full proof including variance-estimator consistency |
| `related_work.md` | Theorem-by-theorem comparison with prior results, with reading depth |

## Scope statements that must survive into the manuscript
1. The treatment is the **strategy choice**. The text-generation kernel, including token temperature, is fixed.
2. g is the deployer's **operational** gap (its own objective), not the human-outcome effect.
3. Thm A's impossibility holds in 𝓜(B, σ) **without extrapolation structure**. Constant or parametric
   effects remove the separation.
4. Thm B concerns **one finite common temperature**. Temperature mixtures with mass at τ = ∞ contain
   uniform mixing.
5. Thm D is one-dimensional (Δ(h) = h). Its error rate O_p((nR)^{−1/4}) is **achievable, not claimed optimal**.
6. The main gain is preventing divergence (common temperature vs uniform: ≈ 20× at n = 10⁵, δ = 0.1).
   Gap-based allocation saves a further 11% in the example, and Lemma R says when that is worth it.
7. Wald coverage is asymptotic. Finite-sample under-coverage appears when few observations are
   explored or the effective boundary sample is small:
   - optimal design at n = 10⁵, δ = .1 (≈ 130 explored): .915 over 400 replications;
   - boundary at nτ = 10: .887 over 1,000 replications.
   See `theorem_D.md` and `simulation/results/separation/designs*.csv`.

## Relation to the current manuscript (`paper/tex/main.tex`, commit b160d3d)
- **Prop. 4 (minimax collapse) is incorrect** as stated. The B-branch of the bound omits the mass
  factor; a counterexample has mass 1/n with p = n⁻⁴. It is superseded by Thm A and by the recoverability
  characterization (m_n(L) → 0 for all L), to be added as a lemma.
- The final sentence of Remark "Scope of Prop. 2" ("π > 0 everywhere ⇒ V < ∞") is false
  (e(H) = H, H ~ U(0, 1)).
- In App. C the kernel identity should read ω_τ = K(Δ/τ), without the 1/τ factor.
- `simulation/src/simulation.py`: truth uses the behaviour policy for other turns, while the paper
  defines a uniform reference.
- `simulation/results/continuous_h_results_uniform.csv`, row n = 32000, τ = 0.045: the MC SD of
  oracle AIPW (1.38) is far below the exact SD (79.35). Report exact moments.

## Reproducing
```bash
cd simulation/src/separation
python run.py finite        # seconds
python run.py kantorovich   # seconds
python run.py costs         # ~1 min
python run.py designs       # MC, minutes
python run.py designs --rate --ns 10000 100000 1000000 --reps 200
python run.py boundary      # MC
python run.py coverage      # MC, longest
```
Each run writes `simulation/results/separation/<name>.csv` and `<name>.json`. The JSON records
arguments, seed, git commit, numpy and python versions, and wall time. `log_*.txt` holds console
output with timing.
