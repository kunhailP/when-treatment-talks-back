# Boundary side of the separation: Theorem D

Status (2026-09-17): full proof written and self-checked; **not externally reviewed**.

This is the one-dimensional score version (Δ(h) = h). A multivariate boundary would follow the
coarea argument of the manuscript's localization appendix. It is not claimed here.

Numerical checks: `simulation/src/separation/run.py boundary` and `run.py coverage`.

---

## Setup

For each n, (H_i, A_i, Y_i), i ≤ n, are iid (a triangular array).

**Assumptions**
- (D1) H has density f with f ≤ f̄. f is continuous at 0 and f(0) > 0.
- (D2) |μ_a| ≤ B, and μ_a is L-Lipschitz on [−u_0, u_0], where μ_a(h) = E[Y | A = a, H = h].
- (D3) σ_a²(h) = Var(Y | A = a, H = h) is continuous at 0 with σ_1²(0) + σ_0²(0) > 0, and E[Y⁴ | A, H] ≤ M.
- (D4) A | H ~ Bern(p_n(H)) with p_n(h) = σ(h/τ_n), known, and τ_n → 0.
  This is a **single common temperature**.
- (D5) Greedy action a*(h) = 1{h > 0}. The operational gap is g(h) = φ(|h|) with φ(u) ≤ κ̄u on
  [0, u_0] and g ≤ Ḡ. Strong form: φ is differentiable at 0 with φ′(0) = κ > 0.

No structure extrapolating c = μ_1 − μ_0 away from 0 is assumed. None is needed on this side.

**Notation**
- ω = p(1 − p) = K(H/τ), where K(u) = eᵘ/(1 + eᵘ)².
- Kernel facts: ∫K = 1, ∫|u|K = 2 log 2, ∫K(u)σ(u)du = 1/2, K(u) ≤ e^{−|u|}, and
  ∫_0^∞ vσ(−v)dv = π²/12.
- m_τ = E[ω].

**Targets**
- β_0 = c(0): the fixed boundary effect.
- β_ov,τ = E[ωc(H)]/m_τ: the temperature-indexed overlap effect.

**Estimator.** With w_1 = A(1 − p) and w_0 = (1 − A)p,
- D̂_a = n⁻¹Σ w_{a,i},
- m̂_a = Σ w_{a,i}Y_i / Σ w_{a,i},
- β̂ = m̂_1 − m̂_0.

**Variance estimator.** ŝ² = n⁻¹Σ ψ̂_i², where ψ̂ = w_1(Y − m̂_1)/D̂_1 − w_0(Y − m̂_0)/D̂_0.
The Wald interval is β̂ ± z ŝ/√n.

---

## Theorem D

Assume (D1)–(D5), τ_n → 0 and nτ_n → ∞.

1. **Asymptotic normality.** (β̂ − β_ov,τ_n) / (s_n/√n) ⇒ N(0, 1), where
   s_n² = (σ_1²(0) + σ_0²(0)) / (2τ_n f(0)) · (1 + o(1)).
2. **Bias.** |β_ov,τ − β_0| ≤ C_1τ_n for n large.
3. **Variance estimation.** ŝ²/s_n² →_p 1.
4. **Validity at the fixed boundary effect.** If also nτ_n³ → 0, then (β̂ − β_0)/(ŝ/√n) ⇒ N(0, 1), so
   the Wald interval for β_0 has asymptotic coverage 1 − α.
5. **Exploration loss.**
   R_n = nE[g(H)σ(−|H|/τ_n)] ≤ nτ_n²κ̄f̄π²/6 + nḠe^{−u_0/τ_n}.
   In the strong form, R_n = nτ_n²κf(0)π²/6 · (1 + o(1)).

**Corollary.** For τ_n = n^{−α} with α ∈ (1/2, 1), the Wald interval for β_0 is asymptotically valid and
R_n → 0 simultaneously. The three rate conditions are:

| Condition | Needed for | Holds when |
|---|---|---|
| nτ_n → ∞ | effective boundary sample grows | α < 1 |
| nτ_n³ → 0 | bias negligible relative to SE | α > 1/3 |
| nτ_n² → 0 | cumulative exploration loss vanishes | α > 1/2 |

The achievable error is |β̂ − β_0| = O_p((nτ_n)^{−1/2}) = O_p((nR_n)^{−1/4}). **We state this as
achievable, not optimal.** No lower bound on the boundary side is claimed.

**Remark (smoother effects).** If c and f are differentiable at 0, the symmetry of K makes the bias
O(τ²), and condition 4 relaxes to nτ⁵ → 0.

---

## Proof

### Step 1: kernel integrals
Let q be bounded and continuous at 0, and let j ≥ 1, r, s ≥ 0. Substitute h = τu. The integrand is
dominated by ‖q‖_∞ f̄ K(u), so dominated convergence gives

  E[K(H/τ)^j (1 − p)^r p^s q(H)] = τ f(0) q(0) ∫K^j σ(−u)^r σ(u)^s du + o(τ).

In particular m_τ = τf(0)(1 + o(1)).

### Step 2: bias
β_ov,τ − β_0 = E[ω(c(H) − c(0))]/m_τ. Split the expectation:
- On |H| ≤ u_0: |c(h) − c(0)| ≤ 2L|h|, and E[ω|H|] ≤ f̄τ²∫|u|K = 2 log 2 · f̄τ².
- On |H| > u_0: ω ≤ e^{−u_0/τ}, and |c| ≤ 2B.

So |β_ov,τ − β_0| ≤ (4 log 2 · Lf̄τ² + 2Be^{−u_0/τ})/m_τ = (4 log 2 · Lf̄/f(0))τ(1 + o(1)). ∎

### Step 3: linearization
Let μ̄_a = E[ωμ_a]/m_τ. Since E[w_1 | H] = ω and E[w_1Y | H] = ωμ_1, we have E[w_1(Y − μ̄_1)] = 0, and
likewise for arm 0. Define

  T_a = n⁻¹Σ_i w_{a,i}(Y_i − μ̄_a)/m_τ,  ξ_i = [w_{1,i}(Y_i − μ̄_1) − w_{0,i}(Y_i − μ̄_0)]/m_τ.

Then m̂_a − μ̄_a = (m_τ/D̂_a)T_a, μ̄_1 − μ̄_0 = β_ov,τ, and Eξ = 0.

Because w_1w_0 = 0 and E[A(1 − p)² | H] = ω(1 − p),

  s_n² := Var(ξ) = m_τ⁻² E[ω{(1 − p)(σ_1² + (μ_1 − μ̄_1)²) + p(σ_0² + (μ_0 − μ̄_0)²)}].

- μ̄_a → μ_a(0) by Step 1.
- (μ_a(τu) − μ̄_a)² → 0 pointwise and is bounded by 4B², so those terms are o(τ).
- The σ² terms equal τf(0)σ_a²(0)·½ + o(τ), since ∫K(1 − σ) = ∫Kσ = ½.

Therefore s_n² = (σ_1²(0) + σ_0²(0))/(2τf(0)) · (1 + o(1)).

Numerical check: σ_a² = 1 and f(0) = ½ give SD(β̂) ≈ (2/(nτ))^{1/2}.

### Step 4: central limit theorem
- *Fourth moment.* w_a⁴ ≤ w_a ≤ A(1 − p) or (1 − A)p, and E[(Y − μ̄_a)⁴ | A, H] ≤ C(M, B). So
  E[w_a⁴(Y − μ̄_a)⁴] ≤ Cm_τ, hence Eξ⁴ ≤ C′m_τ⁻³ ≍ τ⁻³.
- *Lyapunov.* n⁻¹Eξ⁴/s_n⁴ ≍ n⁻¹τ⁻³/τ⁻² = (nτ)⁻¹ → 0. Therefore n^{−1/2}Σξ_i/s_n ⇒ N(0, 1).
- *Denominators.* Var(D̂_a)/m_τ² ≤ E[w_a²]/(nm_τ²) ≤ 1/(nm_τ) → 0, so D̂_a/m_τ →_p 1 and
  m_τ/D̂_a − 1 = O_p((nτ)^{−1/2}).
- *Decomposition.* β̂ − β_ov = (T_1 − T_0) + (m_τ/D̂_1 − 1)T_1 − (m_τ/D̂_0 − 1)T_0.
  Here T_1 − T_0 = n⁻¹Σξ_i and T_a = O_p((nτ)^{−1/2}). The remainder is O_p((nτ)⁻¹) = o_p(s_n/√n).

Slutsky gives Part 1. ∎

### Step 5: variance estimator
Write ξ_{a,i} = w_{a,i}(Y_i − μ̄_a)/m_τ, so ξ = ξ_1 − ξ_0.

(i) n⁻¹Σξ_i²/s_n² has mean 1 and variance ≤ Eξ⁴/(ns_n⁴) ≍ (nτ)⁻¹ → 0. So it converges to 1 in
probability.

(ii) For arm 1, ψ̂_{1,i} − ξ_{1,i} = w_1(Y − μ̄_1)(1/D̂_1 − 1/m_τ) + w_1(μ̄_1 − m̂_1)/D̂_1. Hence
- n⁻¹Σ[w_1(Y − μ̄_1)(1/D̂_1 − 1/m_τ)]² = (n⁻¹Σξ_{1,i}²)(m_τ/D̂_1 − 1)² = O_p(s_n²) · O_p((nτ)⁻¹);
- n⁻¹Σ[w_1(μ̄_1 − m̂_1)/D̂_1]² ≤ (m̂_1 − μ̄_1)² D̂_1/D̂_1² = O_p((nτ)⁻¹)/O_p(τ) = O_p(1/(nτ²)),
  using w_1² ≤ w_1. Relative to s_n² ≍ τ⁻¹ this is O_p((nτ)⁻¹).

Arm 0 is identical. By Minkowski, n⁻¹Σ(ψ̂_i − ξ_i)² = o_p(s_n²). Then Cauchy–Schwarz gives
|n⁻¹Σψ̂_i² − n⁻¹Σξ_i²| = o_p(s_n²), which is Part 3. ∎

### Step 6: centering at β_0
(β_ov,τ − β_0)/(s_n/√n) = O(τ) · O((nτ)^{1/2}) = O((nτ³)^{1/2}) → 0. Together with Parts 1 and 3 and
Slutsky, this gives Part 4. ∎

### Step 7: exploration loss
The off-greedy probability is σ(−|h|/τ).
- On |h| ≤ u_0: nE[φ(|H|)σ(−|H|/τ)] ≤ nκ̄f̄ · 2τ²∫_0^∞ vσ(−v)dv = nκ̄f̄τ²π²/6.
- Outside, the contribution is ≤ nḠe^{−u_0/τ}.
- Strong form: on v ≤ u_0/τ we have φ(τv)/τ → κv and f(τv) → f(0), dominated by κ̄vf̄σ(−v). Dominated
  convergence gives the asymptotic equality, and the region v > u_0/τ is the exponentially small term
  above.

For τ_n = n^{−α}: nτ² → 0 iff α > 1/2, and ne^{−u_0n^α} → 0 always. ∎

---

## Monte Carlo evidence

Source: `simulation/results/separation/coverage.csv`, with settings and seeds in the matching `.json`.
DGP: H ~ U(−1, 1), μ_0(h) = h, c(h) = 1 + |h|, σ = 1, α = 0.6. The kink makes the bias O(τ).

**Wording for the manuscript:**
> A lower coverage observed with few replications (0.91 with 200 replications at n = 10⁶) did not recur
> with more replications. In the enlarged experiment coverage is close to nominal. At the smallest sample
> size a slight under-coverage remains, consistent with the standard error underestimating the sampling
> SD by about 1–1.5%.

For reference, a bias-free normal estimator whose SE is 0.986 × SD has coverage
2Φ(1.96 × 0.986) − 1 ≈ 0.9467.
