# When the Treatment Talks Back: Information Limits of Observational Logs from Adaptive Generative Political Communication

**Working paper draft v0.2 (2026-07-30) — JCI track (docs/publication_map.md). Structure = docs/internal/outline.md v0.3. All numbers are from executed runs in this repository; none are placeholders. v0.1 → v0.2 (심사 선제 대응 3건): (i) §4.2 Remark A′ — 단일턴 하한의 다턴 a fortiori 적용 (T=1 정리 ↔ T=3 동기의 내적 정합성 봉합); (ii) §2에 off-policy evaluation/deficient-support 문헌 단락 신설 (Sachdeva–Su–Joachims 2020 등) + 경계 긋기; (iii) §4.3에 β^ov의 실질적 의미(equipoise/한계 정책 모집단) 문단 신설. v0.1은 역사 기록 보존.**

---

## Abstract

Large language models now conduct persuasive political conversations that adapt turn by turn to the human they are persuading. We formalize the treatment delivered by such a system as a composite object — a strategy policy π, a generation kernel G, and an information environment E — and define deployment, policy, and turn-level excursion estimands for it. We then show that conversation logs collected under a deployed policy carry structurally limited information about turn-level causal effects. Three results organize the argument. First, when the deployed policy has history-deterministic components, turn-level effects are nonparametrically unidentified (support failure); in RLHF-tuned deployments this condition is structurally frequent and design-reinforced, not an incidental data defect. Second, even with formal positivity, the semiparametric efficiency bound for population excursion effects degrades exponentially in the policy's effective inverse temperature: no regular estimator in the nonparametric class escapes the rate (Result A). Because a multi-turn conversation nests each of its turns, these single-turn lower bounds apply a fortiori to conversational excursion effects; under a uniform-recurrence condition on the high-gap set, the bound moreover compounds geometrically across turns (Proposition A-T). Third, the overlap weight mass concentrates on the policy's learned decision boundary as temperature falls, so the causal information that remains stably observable is localized there; the boundary effect is a distinct — and policy-relevant — estimand β^ov, not a silent replacement for the population effect (Result B, proved in one dimension). A (n, τ) phase diagram with an exact boundary — log E[1/p_τ] = log(1 + τ·sinh(1/τ)) for our main design — separates three regimes: estimable, variance explosion, and a deceptive regime where estimates look stable but are biased because rare crossover actions never appear in the sample. Re-querying three RLHF-tuned open-weights models on 200 real debate contexts shows median per-context strategy entropy of exactly zero and modal-strategy shares of 94.5–98.6%, implying ≥10⁵ conversations for any minority-strategy contrast — a scale at which observational strategy analysis is infeasible. An audit of 56,831 deployed persuasion conversations shows that randomized prompt instructions explain only 12–32% of realized evidence-dose variance. We propose the generative micro-randomized trial (G-MRT) — within-conversation turn-level randomization with a locked evidence bank, gated generation, and assignment-ITT analysis — as the design remedy, and outline its estimation theory.

---

## 1. Introduction

Conversational AI persuades. In randomized trials, GPT-4 debates shifted opponents' positions more often than human debaters did (Salvi et al. 2025), and conversations with frontier models moved policy attitudes with durable effects (Hackenburg et al. 2025). Yet the meta-analytic picture of political persuasion is one of small and heterogeneous effects (g ≈ 0.02, I² ≈ 76%), which makes decomposition — *which turn-level behaviors of the AI cause belief change* — the scientifically and politically urgent question. Hackenburg et al.'s strongest lever, a reward model selecting responses turn by turn, is precisely the component whose interior remains a black box: it is an adaptive turn-level policy, and its logs are what an analyst inherits.

This paper asks what those logs can and cannot identify. Our answer is pessimistic in a precise way and constructive in a precise way.

Pessimistic: the treatment in these systems is not a message but a composite (π, G, E) — a strategy policy, a generation kernel, and an information environment. Turn-level contrasts computed from deployment logs face three distinct failures: (i) support failure where the policy is history-deterministic (Proposition 1A); (ii) an exponential collapse of the semiparametric efficiency bound in the policy's decisiveness even when positivity formally holds (Result A) — bounds that transfer a fortiori from single turns to conversations (Remark A′); and (iii) localization — the overlap mass that survives concentrates on the policy's decision boundary, so what remains stably estimable is a boundary estimand β^ov, distinct from the population effect (Result B). We verify each mechanism in simulation, locate real deployments on the resulting (n, τ) phase diagram using re-query experiments on three RLHF-tuned models, and audit instruction-behavior slippage in 56,831 deployed conversations.

Constructive: each failure corresponds to a specific design element of a generative micro-randomized trial (G-MRT): uniform turn-level randomization restores support and overlap; exogenous assignment removes sequential confounding; regime-defined estimands resolve ill-defined treatments; and a fidelity protocol with assignment-ITT analysis handles generated-treatment noncompliance.

Contributions (three, locked): (1) an estimand framework for generative treatments with a general adaptive action space; (2) temperature-indexed overlap collapse and localization — Proposition 1A, Result A with explicit conditions, Result B proved in one dimension, the fixed-τ counterexample, and the (n, τ) phase diagram; (3) the G-MRT design with a generated-treatment fidelity protocol. Everything else — generator transport, internal-representation methods, simultaneous inference, constrained policy learning — is explicitly out of scope (§9).

## 2. Related Work

**Texts as treatments, static.** Imai & Nakamura (2026) identify effects of generated texts as fixed objects; ordering effects *within* a fixed object involve no human-feedback loop and no positivity problem. Our object is different: an adaptive policy operating *on* human responses, where the policy itself destroys overlap. This distinction — dynamic response policy versus static generated object — is the boundary line of this paper.

**Off-policy evaluation with deficient support.** The estimation-side face of our problem is studied in the contextual-bandit and RL literatures: doubly robust off-policy evaluation (Dudík, Langford & Li 2011; Thomas & Brunskill 2016), counterfactual learning from logged data, and, closest to Proposition 1A, off-policy learning under *deficient support*, where the logging policy assigns zero or near-zero probability to some actions (Sachdeva, Su & Joachims 2020). We draw the boundary in four places. First, that literature works at the level of specific estimators and their variance or regret; Results A–B are statements about the *semiparametric efficiency bound* — no regular estimator in the nonparametric class escapes the rate, which closes the "use a better estimator" escape by construction. Second, we index the collapse by an interpretable policy parameter (effective temperature of an RLHF-shaped softmax) and obtain exact boundary geometry in (n, τ), including a closed form for the phase boundary in our main design. Third, localization (Result B) — *where* the surviving information lives, and the τ↓0 limit of the overlap-weighted estimand — has, to our knowledge, no counterpart in the OPE literature, whose remedies (truncation, regularized weights, support restriction) implicitly change the estimand without characterizing the limit object. Fourth, our remedy is a *design* (randomize the turns), not an estimator: the setting is scientific inference about turn-level persuasion effects, where the analyst can run an experiment, not a fixed logged dataset to be salvaged.

**Micro-randomized trials.** MRTs randomize pre-defined discrete actions at decision points and target causal excursion effects via WCLS (Qian et al. 2022; Boruvka et al. 2018). We import the excursion estimand and add what conversation requires: a generation kernel between assignment and realization, ill-defined observational labels, and fidelity auditing of generated treatments. LLM-in-MRT precedents exist in behavior-change messaging (arXiv:2506.07275); our novelty claim is confined to within-conversation turn-level randomization of generative political persuasion with information locking.

**Stochastic interventions.** Regime-specific potential outcomes for stochastic/modified policies (Muñoz & van der Laan 2012; Díaz & van der Laan 2013; Kennedy 2019; Young, Hernán & Robins 2014) supply our formal object: β is defined under a kernel intervention — assign the label, realize from G. Our addition is the history-dependent generation kernel and the decisiveness collapse.

**Overlap weighting.** β^ov connects to overlap weights and empirical equipoise (Li, Morgan & Zaslavsky 2018); Result B gives the τ↓0 limit of that estimand under a softmax policy, and §4.3 argues the limit object is itself policy-relevant.

**Information equivalence.** Dafoe, Zhang & Caughey (2018) motivate our separation of form from dose: a persuasive-strategy manipulation that also changes information content is confounded in exactly the sense our fidelity audit quantifies (§4.4).

**Support failure is old; its systematicity is new.** Nonidentification from deterministic treatment assignment is standard since Robins (1986). Our claim is not the structure but its origin: RLHF preference optimization widens score gaps and deployment favors low temperature, so history-determinism in deployed LLM policies is *structurally frequent and design-reinforced* — it cannot be escaped by collecting better logs from the same deployment.

## 3. Generative Treatments

Individuals i = 1,…,n converse over turns t = 1,…,T. At turn t the system draws an action from its policy, A_it ~ π_t(·|H_it), where H_it is the interaction history, and realizes an utterance from its generation kernel, M_it ~ G_θ(·|A_it, H_it, E_j), where E_j is the information environment (for us: a locked evidence bank on issue j). The user responds R_it; outcomes Y_i include belief accuracy, calibration, reactance, and one-week retention.

**The action space is general.** A_t ∈ 𝒜 may be a discrete strategy label, a continuous generation parameter, or a factorial cell. As a running example — and as the implementation object of the companion experimental paper — we use a 2×2: form F ∈ {assertive, interrogative} × dose D ∈ {high: 4–5 facts, low: 1–2 facts}.

**Treatment is a stochastic intervention.** Potential outcomes are defined under regimes: Y_i^{π,G}, with do-notation read as a kernel intervention — intervene on the label, realize from G. Three estimand layers:

- **Deployment effect** Δ^dep = E[Y^{π₁,G₁}] − E[Y^{π₀,G₀}]: what existing RCTs identify.
- **Policy effect** Δ^pol(G) = E[Y^{π₁,G}] − E[Y^{π₀,G}]: holding the generator fixed.
- **Turn-level excursion effects** (primary): contrasts of one turn's action against a pre-specified reference policy ρ (uniform over 𝒜, all t, all h), with subsequent turns following ρ. Proximal excursions (immediate reactance, belief update) are standard CEE/WCLS targets; distal excursions (final accuracy, retention) connect to distal causal excursion effect estimation (DCEE; Biometrics 2025) — using ordinary WCLS for terminal outcomes is a known attack point we avoid by construction.

**Ill-defined treatment in logs.** An observational label S̃_t = s corresponds to the realized kernel M_t ~ G(·|s, H_t), a *different distribution at every history*. Label-pooled contrasts do not correspond to any well-defined treatment pair. Our regime definition does not "solve" this nonidentification; it replaces the question with a well-posed one — and the well-posed β is identified only under assignment randomization (§5).

## 4. Why Transcripts Are Not Enough

Model the deployed policy's action choice as softmax in a history-dependent score gap with effective temperature τ: for the two-action case, p_τ(h) = σ(Δ(h)/τ). Deployment practice pushes τ down; preference optimization pushes |Δ| up.

### 4.1 Support failure (Proposition 1A)

If π^dep_t(a|h) = 0 on a positive-probability set of histories, turn-level excursion effects are nonparametrically unidentified. The counterexample pair requires no latent confounder — the failure is support, not confounding. Take T = 1, H ∈ {h₀, h₁}, π^dep(1|h₀) = 1/2, π^dep(1|h₁) = 0, Y(a)|H = h ~ N(μ_a(h), 1), and let two DGPs differ only in μ₁(h₁) = c₁ vs c₂. The observed-data law factorizes as P(H)·π^dep(A|H)·N(y; μ_A(H), 1), to which the (1, h₁) stratum contributes nothing; the two DGPs are observationally identical yet their uniform-reference excursion effects differ by P(h₁)(c₂ − c₁). The multi-turn version replaces H with (X, R_{1:t−1}) and recovers the time-varying-confounding form. The structure is Robins (1986); the LLM-specific claim is frequency and reinforcement, not inevitability.

### 4.2 Exponential collapse of the information bound (Result A)

With τ > 0, positivity holds formally, so the right response to Proposition 1A alone would be "use IPW." Result A closes that escape at the level of the efficiency bound. Under (A1) the high-gap set 𝓗_δ = {h : |Δ(h)| ≥ δ} has positive measure; (A2) conditional outcome variances are bounded below by σ̲² on 𝓗_δ; (A3) the model class is nonparametric in the outcome regression — no parametric extrapolation into unobserved strata; then the semiparametric efficiency bound for the ATE-type excursion satisfies

  V_τ ≥ σ̲² · P(𝓗_δ) · exp(δ/τ).

The proof inserts min(p_τ, 1−p_τ) ≤ exp(−δ/τ) into the Hahn (1998) bound V_τ = E[σ₁²/p_τ + σ₀²/(1−p_τ) + (β(H) − β)²]. By the convolution theorem, *no regular estimator in the class* attains lower asymptotic variance: switching from IPW to AIPW recovers no counterfactual information that the sample does not contain. Parametric extrapolation escapes the bound, but that is buying identification with an assumption, and should be said in exactly those words. Effective sample size is arm-specific Kish: n_eff(a) = n / E[1/π_τ(a|H)]. The slogan "halving τ squares the required n" holds within fixed-gap strata; with heterogeneous gaps the max-gap stratum dominates the rate.

**Remark A′ (single-turn bounds are a fortiori multi-turn bounds).** Our theorems in §4.1–4.3 are stated for one turn and two actions, while the motivating setting is a T-turn conversation. The gap runs in the harmless direction. The turn-t excursion estimand β_t conditions on the observed history H_t and contrasts actions *at that turn*, with subsequent turns following the reference policy ρ. The observed-data model for the conversation factorizes turn by turn; the turn-t factor is exactly the single-turn problem with propensity π_τ(·|H_t), and identifying β_t additionally requires bridging every later turn from π^dep to ρ. Discarding the information cost of those later-turn bridges can only *understate* the difficulty; hence any lower bound for the single-turn problem at the (Δ, τ) prevailing at turn t is also a lower bound for the conversational problem. (K-action policies reduce to the two-action case via the two arms of the contrast.)

**Proposition A-T (multi-turn compounding).** The compounding across turns is not left heuristic. Start from the semiparametric efficiency bound for finite-horizon off-policy evaluation with history-dependent policies (Kallus & Uehara 2020; the finite-horizon influence function of Jiang & Li 2016): V_eff = Var(V₁(H₁)) + Σ_t E_π[(Π_{s≤t} w_s)² Var(V_{t+1}|H_t, A_t)] with w_s = ρ(A_s|H_s)/π_τ(A_s|H_s). Add (M1) *uniform recurrence of the high-gap set*: P(H_{s+1} ∈ 𝓗_δ | h, a) ≥ p_δ for every h ∈ 𝓗_δ and every action a — substantively, decisiveness persists regardless of what the system does, as with strongly reactant partisan users; and (M2) a per-turn conditional variance floor σ̲² on 𝓗_δ. Keeping only the terminal term of V_eff, using E_π[w_t²|H_t = h] = K⁻² Σ_a 1/π_τ(a|h) ≥ K⁻² exp(δ/τ) on 𝓗_δ, and inducting backward — (M1)'s action-uniformity is what lets the bound pass through each turn's weight — yields

  V_eff ≥ σ̲² · P(H₁ ∈ 𝓗_δ) · p_δ^{T−1} · [exp(δ/τ)/K²]^T,

which compounds geometrically in T whenever τ < δ/log(K²/p_δ). The K² factor reflects the conservativeness of the uniform reference and is not optimized; the excursion version (turn t, reference thereafter) follows with exponent T−t+1. The self-contained derivation of the quoted efficiency bound is deferred to the appendix; our contribution is the insertion and the induction, and the honest reading is unchanged: more turns make the information limit exponentially worse, now as a proposition rather than a heuristic.

### 4.3 Localization, the counterexample, and the phase diagram (Result B)

**Result B (Proposition, 1-D; proved).** Let ω_τ(H) = p_τ(1−p_τ) and β^ov_τ = E[ω_τ(Y(1)−Y(0))]/E[ω_τ]. Under regularity conditions (continuous density f; Δ ∈ C¹ with isolated simple roots; a tail-separation condition; continuity near roots), the normalized overlap measure converges weakly to a point mass at the decision boundary as τ↓0; with a unique root at 0, E[ω_τ] = τ·f(0)/|Δ′(0)|·(1+o(1)) and β^ov_τ → E[Y(1)−Y(0) | H = 0]. The proof is a change of variables plus an approximate-identity argument with kernel K(u) = 1/[4cosh²(u/2)], ∫K = 1, which is exact because ω_τ = K(Δ(h)/τ). With multiple roots, mass distributes proportionally to f(r_j)/|Δ′(r_j)|; the multivariate coarea version remains at appendix/conjecture status.

**Why the boundary estimand matters substantively.** β^ov is not a consolation prize; it is the effect in a policy-relevant population. The decision boundary {Δ(H) = 0} collects the histories at which the deployed policy is genuinely undecided — the algorithmic analogue of clinical equipoise (Li, Morgan & Zaslavsky 2018). Three consequences. First, *marginal policy evaluation*: any small change to the policy — a regulation, a guardrail, a reward-model update, a temperature change — alters behavior precisely on and near this boundary, so the effect among boundary histories is the first-order term in the value change of any local policy modification. Second, *auditability*: β^ov is the one turn-level causal quantity a regulator could estimate from logs alone with stable precision, which makes its scope and its limits worth stating exactly. Third, the political reading, stated as interpretation rather than result: histories far from the boundary — e.g., strongly reactant partisan contexts where the policy is most decisive — are exactly where population-level causal information vanishes; what deployment data can tell us about persuasion is confined to the persuadable margin as *the policy* defines it, not as the scientist would.

**What Result B does *not* say.** At fixed τ > 0, an IPW estimator with true propensities targets the *population* effect as n → ∞ — the estimand does not silently become the boundary effect because the policy is sharp. Numerically: τ = 0.3, n = 4·10⁶, β(H) = 1+|H| gives IPW 1.792 ≈ ATE 1.798 ≠ β^ov 1.356. Formal identification and practical estimability are different properties; our claims are about the *rate* of information loss and the *location* of surviving information, never about a change of target.

**The joint limit is the real object.** The failure surface lives in (n, τ): with n ≫ exp(δ/τ) the population effect is estimable (at exploding variance); near n ~ exp(δ/τ) variance explodes; with n ≪ exp(δ/τ) rare crossover actions never appear in the sample and estimators become *biased while looking stable* — the deceptive regime. Figure PD (simulation/results/phase_diagram.png) shows the three regimes for the main design H ~ U(−1,1), Δ(H) = H, with two boundary lines: the fixed-gap heuristic log n = δ/τ (dashed) and the exact log n = log E[1/p_τ] = log(1 + τ·sinh(1/τ)) (solid; Monte-Carlo agreement to four digits; τ↓0 asymptote 1/τ + log τ − log 2). The empirical regime boundary tracks the solid line.

### 4.4 Where real deployments sit (Study 0 — descriptive, motivating)

Three empirical bridges locate deployed systems on the diagram. Their epistemic status is *motivating*: they estimate proxies of policy decisiveness and instruction-behavior slippage, not the parameters of §4.1–4.3.

**(0-a) Reproduction.** Our pipeline reproduces the direction of Salvi et al. (2025) on the released data (n = 750): personalized Human-AI has the largest crude OR for increased agreement (2.18 > 1), matching the original ordering.

**(0-b) Re-query decisiveness.** For 200 rebuttal contexts stratified by treatment and prior-agreement strength, we regenerate k = 20 responses per context and classify the persuasion strategy of each. Across three RLHF-tuned open-weights families the per-context strategy distribution is near-degenerate:

| model | median entropy (bits) | zero-entropy contexts | modal strategy share |
|---|---|---|---|
| Qwen2.5-7B-Instruct | 0.0 | 89.5% | REBT 98.6% |
| Mistral-7B-Instruct-v0.3 | 0.0 | 58.0% | REBT 94.5% |
| Phi-3.5-mini-instruct | 0.0 | 75.5% | REBT 97.3% |

Low entropy is not one model's quirk; it recurs across families — the observable signature of "structurally frequent." Substituting the per-strategy p̂_s into the effective-sample formula (Dirichlet-smoothed, k = 20 resolution): the modal strategy needs ~3·10³ conversations per contrast arm, every minority strategy ≥ ~1.1·10⁵ (a lower bound — unobserved strategies may be rarer than smoothing can register), and a FACT-vs-SOCR-type contrast needs the *sum* of two such terms. These are illustrative insertions into Result A's formula, not estimates of any deployment's τ.

*Placing contexts on the phase diagram.* Only the composite Δ/τ — the score gap in temperature units, exactly the phase diagram's abscissa — is identified from choice frequencies; τ alone is not. Estimating the two-action reduction Δ̂/τ = log[(c₁+α)/(c₂+α)] per context yields a median of 3.71 for all three models — which is the *resolution ceiling* of k = 20 draws: 58–89.5% of contexts are right-censored there (the runner-up action was never realized). The reflexive reading belongs in the paper: measuring a deployed policy's decisiveness runs into the same information limit that blocks effect estimation, so all decisiveness figures from finite re-query are lower bounds; via Proposition A-T the per-turn stratum factor E[1/p] ≥ 42 compounds across turns.

Two robustness results discipline these numbers. *Judge sensitivity:* relabeling all 4,000 Qwen responses with a 32B judge yields raw agreement 0.903 but κ = 0.13, and κ ≈ 0 once both-REBT pairs are excluded — judges agree on the dominant label and disagree almost completely on minority-label identity. Aggregate quantities are nevertheless stable (per-strategy n_req ratios 0.88–1.52 across judges). We therefore report entropy, modal share, and n_req — and we do not interpret minority-label identity before human double-coding (pre-registered κ ≥ 0.6 on 200 turns). *Label-error simulation:* propagating misclassification rates q ∈ {0.05, 0.1, 0.2} through the pipeline (symmetric and majority-absorbing noise models anchored to the observed confusion pattern) moves rare-strategy n_req by −25% to +6% even at q = 0.2; symmetric noise biases toward optimism, so the 10⁵ scale is conservative.

**(0-c) Instruction ≠ behavior.** In Hackenburg et al.'s released data (56,831 persuasion conversations across three studies), the randomized rhetoric instruction explains η² = 0.20 / 0.12 / 0.32 of realized fact-count variance in studies 1/2/3 — 68–88% of realized-dose variation occurs *within* assignment. Assignments also bundle: "information" realizes 8.3–21.8 facts on average while "moral reframing" realizes 1.6–2.1, and 52–56% of moral-reframing conversations realize zero facts. Where compliance flags exist, valence compliance is 72.7% (study 1). What was randomized was an instruction; the treatment that reached the participant was a generated behavior, substantially decoupled from it. This is the observational counterpart of the fidelity problem the G-MRT protocol addresses by design.

## 5. The G-MRT Design as the Remedy

Each failure in §4 maps to a design element:

| failure | element |
|---|---|
| support failure (1A) + bound collapse (A) | uniform turn-level randomization ρ(a|h) = 1/4 ≥ ε |
| sequential confounding | exogenous assignment of A_t |
| ill-defined treatment | regime-defined (kernel-intervention) estimands |
| generated-treatment noncompliance | assignment-ITT + fidelity protocol |

The protocol: (1) conversation-level randomization of the generator Z_i ∈ {G_a, G_b}, at least one open-weights; (2) turn-level uniform randomization of A_t with full logging of assignment, probability, and realization; (3) a locked evidence bank of ≥ 20 verified fact units per issue with per-turn sub-banks or without-replacement sampling *specified as part of the regime* — dose is honestly named a high-information communication package (fact count covaries with length and cognitive load; length-controlled designs are a follow-up); (4) a fidelity gate that inspects each utterance before sending, regenerates once on mismatch, and sends-with-log on second failure. The gate is part of the treatment kernel: ITT identifies the effect of *assignment to the generate-and-gate protocol* G̃, and the paper says so in those words. Differential noncompliance across cells (e.g., interrogative form failing more often) contaminates cell contrasts; we pre-register a fidelity floor of ≥ 80% per cell with demotion of affected contrasts, publish gate-decision logs, and pre-specify a no-gate sensitivity analysis, since a gate classifier whose errors correlate with assignment would itself distort the treatment.

**Result 5 (illustrative trade-off, not a theorem).** Mixing exploration into deployment, ρ = (1−ε)π_τ + ε·Unif, caps the variance contribution at σ²K/(nε) at a per-turn regret cost scaling with ε — a design corollary quantifying the price of identification, presented as an illustration because its exact form depends on outcome bounds, estimator, and horizon.

## 6. Estimation

Proximal excursions: WCLS with known randomization ρ. Distal excursions: DCEE estimators (not terminal-outcome WCLS). Policy values: cross-fitted doubly robust estimators for 2–3 pre-specified policy pairs only (variance). Scope sentence: all guarantees are relative to the G-MRT's known ρ; nothing in this section rescues transcript-only analysis. Multiplicity: corrections for a pre-specified family, finalized after pilot; simultaneous confidence regions are companion-paper material.

## 7. Simulation Evidence

Four executed studies; theory-to-DGP correspondence is declared object-by-object (simulation/README.md).

**(i) Sign reversal under adaptivity** (simulation.py). A defensiveness-adaptive policy makes the naive turn-level contrast wrong in *sign* (truth +0.068; naive −0.294, coverage 0.0) while known-ρ IPW/DR recover it (bias ≤ 0.01, coverage ≈ 0.95–0.97) — the confounding face of the problem, and the G-MRT's licence.

**(ii) Two-state temperature collapse** (temperature_collapse.py). Along a τ grid calibrated so τ = 1 reproduces the adaptive policy of (i): IPW SE grows exponentially, tracking a scaled inverse-propensity diagnostic curve (labeled as such — it is not the efficiency bound); the naive estimator becomes *more confident while more wrong* as τ falls (coverage → 0 with shrinking SE). Metric discipline: global arm-specific Kish ESS (theory object), minimum stratum-arm cell occupancy (rare-crossover diagnostic — not Kish), E[p(1−p)] (Result B object), and E[2·min(p,1−p)] (diagnostic) are reported as four separate columns, coverage both conditional and unconditional on estimability, with zero-cell rates alongside. One finding we flag for practice: in the collapse regime the *realized* Kish ESS rebounds non-monotonically (0.028 → 0.53) exactly when the zero-stratum-arm rate jumps (0.70 → 0.99) — surviving weights homogenize as rare crossovers vanish from the sample, so a healthy-looking realized ESS co-occurring with high zero-cell rates is itself the signature of the deceptive regime. ESS should never be reported without zero-cell rates.

**(iii) Continuous-boundary battery** (continuous_h.py; H ~ U(−1,1) main, N(0,1) robustness; β(H) ∈ {1, 1+e^{−H²}, 1+|H|}; 400 replications per cell). At n = 32,000: all population-targeting estimators are unbiased with nominal coverage down to τ ≈ 0.15; at τ = 0.045 Horvitz-Thompson has SD 2.95 (variance explosion) while Hájek shows bias 0.46 with SD 0.30 — biased-yet-stable; oracle AIPW does not rescue coverage (Result A is not an IPW artifact); the oracle outcome-regression line is flat by construction — the (A3) escape made visible, identification bought by assumption; and the overlap estimator remains unbiased with nominal coverage *for its own target β^ov* at every τ, with β^ov_τ → β(0) = 1 as Result B predicts. Under N(0,1) the collapse is earlier and, at extreme τ, propensities underflow to machine 0/1 so IPW becomes numerically undefined — reported as estimability 0, not dropped.

**(iv) Phase diagram** (Figure PD). The empirical regime classification over the (n, τ) grid tracks the exact solid boundary log E[1/p_τ]; the dashed δ/τ heuristic is visibly off at small τ. Regime thresholds (relative bias 0.10/0.20, coverage 0.85) are presentation choices defended by publishing the RMSE and coverage panels alongside.

## 8. Empirical Plan and Ethics

The companion PA-track experiment implements the 2×2 G-MRT: pilot n = 80–120 (function verification: assignment mechanics, fidelity rates, bank leakage, dropout — not effect detection), demonstration n = 180–250 with pre-registered minority contrasts, confirmatory sample from post-pilot power simulation. Pre-registration locks the fidelity floor, blocking factors (issue), attrition handling (IPW-for-attrition), and reactivity checks (randomizing measurement itself in pilot). Ethics: persuasion toward *accuracy* on factual political questions with a fact-checked locked bank; no deception arms; disclosure of AI interlocutor; IRB before pilot. The three Study 0 analyses (reproduction, re-query, audit) involve only public data and no new human subjects.

## 9. Discussion

What we rule in: estimand definitions that survive the generative setting; explicit information limits with rates and locations; a design that restores identification at a quantified exploration cost. What we rule out of this paper, one paragraph each in the full text: generator transport Γ (effects across model versions — motivated empirically by cross-model heterogeneity in Chen, Kalla & Le 2026), internal-representation adjustment (GPI; overlap problems of representation conditioning are themselves design-based cautionary tales, cf. Tierney et al. 2025), simultaneous inference over excursion families, and epistemically constrained policy learning. Each is a companion, not a section.

The one-sentence version of this paper: *adaptive systems generate the least population-level causal information exactly where they are most decisive, and the information that survives lives on their decision boundary* — so if you want turn-level causal knowledge from conversational AI, you must randomize the turns.

---

### Figure and table inventory (all files exist in repo)

| # | asset | section |
|---|---|---|
| F1 | simulation/results/bias_plot.png (sign reversal) | §7(i) |
| F2 | simulation/results/collapse_curve.png (P1–P3) | §7(ii) |
| F3 | simulation/results/continuous_h_battery.png | §7(iii) |
| F4 (PD) | simulation/results/phase_diagram.png | §4.3, §7(iv) |
| T1 | analysis/results/model_comparison.csv | §4.4 |
| T2 | analysis/results/policy_entropy_by_strategy.csv (+ judge_sensitivity.csv) | §4.4 |
| T3 | analysis/results/fidelity_audit.csv | §4.4 |
| A1 | simulation/results/label_error.csv | §4.4 / appendix |

> 내부 작성규율 메모는 `docs/internal/writing_rules_compliance.md`로 이동 (v0.3, 2026-08-31).
