# Theorem-by-theorem comparison with the closest prior work

Compiled 2026-09-17 from literature checks. "Read" marks the depth at which the prior result was
inspected:
- **full**: theorem statements read in the paper;
- **abstract**: abstract or snippet only. These must be read in full before submission.

Absence claims mean only "not found in the papers we checked".

## Theorem A — information–exploration inequality (population ATE, no extrapolation structure)

| Prior result | Read | What it already gives | What A adds |
|---|---|---|---|
| Simchi-Levi & Wang (AISTATS 2023 / Mgmt Sci), Thm 1: inf max e·√R = Ω(1) | full | The 1/δ² trade-off between regret and ATE error, K-armed, **no contexts**, orders only | Contexts with heterogeneous operational gap g(h). The functional (E√g)² with an explicit constant. Model scope stated (no extrapolation). Adaptive designs covered via van Trees |
| Wan, Kveton & Song (ICML 2022), Lemma 1, Thm 1 | full | Variance-optimal exploration under a safety (value-loss) constraint, solved numerically | Closed form in g; lower bound over all estimators |
| Douglas, Persson & Provost (arXiv 2605.15108), Props 5–6 | full | Neyman-type optimal logging π ∝ π_t√μ for IPW; theory under several information conditions | They minimize variance with no loss price. A prices exploration in g and bounds all estimators |
| Koppel, Bhatt, Zeng & Ganesh (NeurIPS 2025 Constrained Optimization for ML workshop; listed at constrained-opt-ml.github.io/papers) | **abstract** | Inverse-gap-weighting contextual bandit with regret/ATE trade-offs | To be checked: whether a lower bound or a √g allocation appears |
| Cochran optimum allocation with costs | textbook | n_h ∝ N_h S_h/√c_h | The allocation form of A′ is this rule. **We do not claim the allocation as new** |
| Mou, Ding, Wainwright & Bartlett (arXiv 2301.06240), Thm 1 | full | Local minimax lower bound for off-policy linear functionals over convex classes; implies two-point bounds of our type | A couples the information bound to the exploration loss (the Cauchy–Schwarz step). Mou et al. has no loss |
| Hong, Leung & Li (Econometrics J 2020), Thm 1 | full | Finite strata with drifting propensity: n·a_n → ∞ gives a CLT | Superpopulation, general F, all-estimator lower bound |

## Theorem B — single common temperature

| Prior result | Read | What it already gives | What B adds |
|---|---|---|---|
| Douglas, Persson & Provost (2026), Fig. 6 | full | Simulation: softmax logging worse than top-k; MSE → ∞ as it approaches greedy | A rate: loss ≳ n/log²(nδ²) at fixed precision against a constant optimum. Scope limited to one deterministic common temperature per n; random mixtures of finite temperatures can avoid the rate |
| Cesa-Bianchi, Gentile, Lugosi & Neu (NeurIPS 2017), Thms 1–2 | full | Boltzmann exploration with a common schedule can have linear regret; arm-dependent schedules fix it | Different objective (population-effect precision, not regret). B concerns estimation cost at fixed precision |
| Khan & Tamer (Econometrica 2010) | **abstract** | Irregular identification with unbounded weights; slower-than-√n rates | Must read Thm 3.2/4.1 before submission |

## Proposition C and Lemma R

| Prior result | Read | Relation |
|---|---|---|
| Cesa-Bianchi et al. (2017) | full | Arm-dependent learning rates as the fix for Boltzmann exploration. C is the analogous context-dependent fix for estimation, with the explicit schedule τ* ∝ \|Δ\| |
| Kantorovich inequality | textbook | Lemma R is a direct application. The contribution is the decision rule E[g]/(E√g)² vs K(ρ) |

## Theorem D — boundary effect at vanishing exploration loss

| Prior result | Read | What it already gives | What D adds |
|---|---|---|---|
| Narita & Yata, *Algorithm as Experiment* (arXiv 2104.12909 v6), Prop 1, Thm 1, eq. (6) | full | e(1−e)-type weights on an approximate propensity score converge to a boundary estimand (Hausdorff measure). Needs undersmoothing nδ_n² → 0; equivalent to local linear RD | The bandwidth is a **system-chosen score-space temperature**, not an analyst-chosen X-space ball. Exploration loss R_n is computed jointly, giving valid inference with R_n → 0 |
| Eckles, Ignatiadis, Wager & Wu (Biometrika), noise-induced randomization | abstract | Known noise near a cutoff as a source of randomization | No exploration-loss accounting |
| Li, Morgan & Zaslavsky (JASA 2018) | abstract | Overlap weights and their target population | Source of the weight only |
| Cattaneo–Titiunik–Yu; Imbens & Wager (REStat 2019); Keele & Titiunik (2015) | abstract/full | Boundary RD estimation and rates | D uses no analyst bandwidth and claims no optimal rate |

## The separation (Corollary S; A with D) — the representative claim

Among the papers checked, we found none stating the following in one model (Corollary S), on the same
exploration-loss scale:
- a boundary effect admits valid inference with vanishing cumulative exploration loss;
- the same data cannot consistently estimate the population ATE across model members sharing that
  boundary effect;
- uniform consistency for the population ATE requires divergent loss. Every component has
close antecedents, listed above. The novelty claim is the comparison on a common cost scale and the
common-temperature consequence, **not** any single ingredient.

## Positioning against generative-AI causal work

| Paper | Read | How we position |
|---|---|---|
| Athey, Imbens & Ji (arXiv 2607.05792), Thm 1 and §9 | full | Randomization-based identification using logged unexposed candidates and probability ratios; logprobs or replays estimate assignment probabilities; trimming at κ. Their estimand averages over co-occurring pairs and is trimmed, so it does not contradict A. Our replay remark credits their §9 |
| Fresh & Shin (arXiv 2607.03597) | full | Taxonomy of conversational estimands (assignment, policy, messages, realized features). We cite it and work at the strategy-assignment level |
| Imai & Nakamura (arXiv 2410.00903); Nakamura & Imai (arXiv 2605.07834) | full/abstract | Text-as-treatment with deterministic decoding. We hold the generation kernel fixed and randomize strategies |
| Fong & Grimmer (AJPS 2023); Egami et al. (Sci Adv 2022) | abstract | Latent-treatment confounding in text. Motivates fixing the kernel |

## To read in full before submission
Khan & Tamer (2010); Koppel et al. (2025); Eckles et al.; Li–Morgan–Zaslavsky (for exact wording of
the target population).
