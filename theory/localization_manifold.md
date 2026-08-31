# Decision-Manifold Localization (v0.5 — Result B의 다변량 완결)

> **지위**: 신규. `temperature_collapse.md:46`과 `paper/outline.md:25`가 "conjecture/appendix 상태"로
> 남겨둔 multivariate coarea 판을 정리로 닫는다. 1-D 판(`proofs_w3_draft.md:83-100`)은 d=1 특수사례가 된다.
> **참고**: 이 정리는 *어디에* overlap 질량이 남는지를 말한다. *얼마나* 남는지는 §4를 볼 것 — 그것도 사라진다.

---

## 1. 설정

H ∈ ℝ^d (d ≥ 1), 밀도 f. 점수함수 Δ : ℝ^d → ℝ.
p_τ(h) = σ(Δ(h)/τ), ω_τ(h) = p_τ(h){1 − p_τ(h)}.

**결정경계(decision manifold)**  ℬ := {h ∈ ℝ^d : Δ(h) = 0}.

**정규화 overlap 측도**  ν_τ(dh) := ω_τ(h) f(h) dh / ∫ ω_τ f.

**커널 항등식 (1-D와 동일, 차원 무관).**

  ω_τ(h) = 1 / [ 4 cosh²( Δ(h) / 2τ ) ] =: (1/τ)·K( Δ(h)/τ ),  K(u) = 1/[4cosh²(u/2)]

K는 ∫_ℝ K(u) du = 1, K(u) ≤ e^{−|u|}인 approximate identity다.

## 2. 가정

- **(C1)** Δ ∈ C¹(ℝ^d), f는 유계이고 ℬ의 근방에서 연속.
- **(C2)** **0이 Δ의 regular value**: ∇Δ(h) ≠ 0 for all h ∈ ℬ.
  (1-D의 "simple root" Δ′(r) ≠ 0의 정확한 일반화. 이것이 ℬ를 C¹ 매끄러운
  (d−1)차원 초곡면으로 만든다 — 음함수정리.)
- **(C3)** ℬ는 compact이거나, 아래 (C4)와 함께 ∫_ℬ f/‖∇Δ‖ dH^{d−1} < ∞를 보장할 만큼 f가 빠르게 감소.
- **(C4)** **꼬리 분리**: 모든 ε > 0에 대해 inf_{ dist(h,ℬ) ≥ ε } |Δ(h)| > 0.
- **(C5)** 0 < ∫_ℬ f/‖∇Δ‖ dH^{d−1} < ∞.   ← **(B4)의 다변량 판. 이것이 빠지면 정리가 공허해진다.**

## 3. Theorem L (decision-manifold localization)

**Theorem L.** (C1)–(C5) 하에서, τ ↓ 0일 때

  **(i)** ∫ ω_τ f dh = τ · [ ∫_ℬ f(h)/‖∇Δ(h)‖ dH^{d−1}(h) ] · (1 + o(1)),

  **(ii)** ν_τ ⇒ ν₀ (약수렴), 여기서 ν₀는 ℬ 위에 지지되고 (d−1)차원 Hausdorff 측도에 대해

  **dν₀/dH^{d−1} (h) ∝ f(h) / ‖∇Δ(h)‖,  h ∈ ℬ,**

  **(iii)** c(h) = E[Y(1) − Y(0) | H = h]가 유계이고 ℬ 근방에서 연속이면

  β^ov_τ = E[ω_τ c(H)]/E[ω_τ] → ∫_ℬ c · f/‖∇Δ‖ dH^{d−1} / ∫_ℬ f/‖∇Δ‖ dH^{d−1} =: c̄(ℬ).

*증명.* g를 유계연속이라 하고 I_τ(g) := ∫ ω_τ(h) g(h) f(h) dh를 본다.

**단계 1 (coarea).** (C1)–(C2)에 의해 ℬ 근방 U_ε = {|Δ| < ε₀}에서 ‖∇Δ‖ > 0이므로
coarea formula (Federer; Evans–Gariepy Thm 3.4.2)가 적용된다:

  ∫_{U_ε} Φ(h) dh = ∫_ℝ [ ∫_{Δ^{-1}(s)} Φ(h)/‖∇Δ(h)‖ dH^{d−1}(h) ] ds.

Φ = ω_τ g f로 두면 ω_τ는 Δ의 함수이므로 level set 위에서 상수로 빠져나온다:

  I_τ^{U}(g) = ∫_{−ε₀}^{ε₀} (1/τ) K(s/τ) · G(s) ds,  G(s) := ∫_{Δ^{-1}(s)} g f/‖∇Δ‖ dH^{d−1}.

**단계 2 (G의 연속성).** (C1)–(C2)와 음함수정리에 의해 s ↦ Δ^{-1}(s)는 s = 0 근방에서
ℬ의 C¹ 정상류(normal flow)로 매끄럽게 변형되고, g, f는 연속, ‖∇Δ‖는 연속이며 0에서 이탈해 있다.
따라서 G는 s = 0에서 연속이고 G(0) = ∫_ℬ g f/‖∇Δ‖ dH^{d−1}.

**단계 3 (Laplace / approximate identity).** s = τu로 치환:

  I_τ^{U}(g) = τ · ∫_{−ε₀/τ}^{ε₀/τ} K(u) · G(τu) · (1/τ) · τ du → 정확히는
  I_τ^{U}(g) = ∫ K(u) G(τu) du · τ / τ … 계산을 명시하면
  (1/τ)K(s/τ) ds = K(u) du 이므로  I_τ^{U}(g) = ∫_{|u| ≤ ε₀/τ} K(u) G(τu) du.

G가 0에서 연속·유계이고 ∫K = 1, K(u) ≤ e^{−|u|}이므로 지배수렴에 의해

  I_τ^{U}(g) → G(0)  … (단위 질량으로 정규화된 형태)

원래 스케일로 되돌리면 ∫ω_τ g f dh = τ·G(0)·(1+o(1)).

**단계 4 (꼬리).** (C4)에 의해 dist(h,ℬ) ≥ ε에서 |Δ| ≥ η(ε) > 0이므로
ω_τ ≤ e^{−η/τ}이고, f 유계·g 유계에서 그 영역의 기여는 O(e^{−η/τ}) = o(τ). 따라서 U_ε 밖은 무시된다.

**결론.** g ≡ 1로 두면 (i). 일반 g에 대해 비율을 취하면
I_τ(g)/I_τ(1) → G(0)/G_1(0) = ∫_ℬ g f/‖∇Δ‖ / ∫_ℬ f/‖∇Δ‖ 이고,
(C5)가 분모의 0 < · < ∞를 보장한다. 이것이 (ii)의 약수렴이다. g = c로 두면 (iii). ∎

**d = 1 환원.** ℬ = {r_j} (유한, (C2)+(C3)), H⁰ = 셈측도, ‖∇Δ‖ = |Δ′|이므로
가중이 f(r_j)/|Δ′(r_j)|에 비례 — `proofs_w3_draft.md:103`의 복수근 따름정리와 일치.
단일근이면 점질량, E[ω_τ] = τ f(0)/|Δ′(0)|(1+o(1)) — 1-D 정리 그대로.

## 4. 정직 절 — 국소화는 안정성이 아니다

Theorem L (i)이 곧바로 말한다: **E[ω_τ] = O(τ).**
따라서 β^ov_τ의 유효표본은 O(nτ)이고 τ ↓ 0에서 함께 소멸한다.
"정보가 결정경계로 국소화된다"는 참이지만 "거기서는 안정적으로 관측된다"는 **거짓**이다.
정확한 진술: **가장 오래 살아남는 것이 경계 정보이나, 그것도 사라진다.**
(`temperature_collapse.md:24`와 `proofs_w3_draft.md:112`의 "안정적으로"는 이에 맞춰 수정할 것.)

## 5. 해석 — 이 정리가 정치방법론에서 갖는 의미

**β^ov는 회귀불연속(RD) estimand다.** d = 1에서 극한은 E[Y(1)−Y(0) | Δ(H) = 0] —
정확히 처치 배정 규칙의 문턱에서의 조건부 처치효과, 즉 Hahn–Todd–van der Klaauw (2001)의 대상이다.
다변량에서는 **경계 위의 f/‖∇Δ‖-가중 평균**, 즉 다차원 RD / boundary RD (Keele & Titiunik 2015,
지리적 RD)의 estimand와 같은 형식 객체다.

이 프레이밍이 현재 문서들의 "overlap weighting과 연결"(Li–Morgan–Zaslavsky)보다 강하다:

- 배치 로그에서 비모수적으로 안정 추정 가능한 것은 **모집단 효과가 아니라 정책의 결정경계에서의 효과**다.
- 즉 적응형 시스템의 로그는 **관측연구가 아니라 (그 시스템이 스스로 만든 문턱에서의) 자연실험**처럼
  행동한다. 그리고 그 문턱은 연구자가 고른 것이 아니라 **정책이 학습한 것**이다.
- 외적 타당도 함의가 즉각적이다: 그 추정치는 "정책이 결정을 망설이는 이력"에만 해당하고,
  정책이 확신하는 이력 — 즉 배치에서 **대부분의 트래픽** — 에는 해당하지 않는다.

**따라서 RD 문헌을 인용해야 한다** (현재 리포 전체 grep 0회):
Hahn, Todd & van der Klaauw (2001); Imbens & Lemieux (2008); Calonico, Cattaneo & Titiunik (2014);
Keele & Titiunik (2015, 다차원/지리적 RD); Cattaneo, Titiunik & Vazquez-Bare (경계 RD).
인용하지 않으면 심사자는 (a) 이미 알려진 것으로 읽거나 (b) 더 강한 주장을 놓쳤다고 볼 것이다.

## 6. 상류 문서 반영

- `formal_framework.md:69`: Result B 조건에 **(B2) simple root** 누락 — 수정 필요(별건).
  다변량 판은 (C2) "0이 regular value"로 진술.
- `temperature_collapse.md:46`, `paper/outline.md:25`: "conjecture/appendix 상태" 표기 해제.
- `paper/tex/main.tex`: Result B 뒤에 Corollary로 배치, 증명은 부록 §C.
- `references.bib`: RD 5건 + Federer/Evans–Gariepy (coarea) 추가.
