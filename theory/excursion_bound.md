# Excursion Efficiency Bound (v0.5 — D-1 해결 + Result A의 decisiveness 재정식화)

> **지위**: 신규. `nonidentification_note.md:96` 위임결정 (ii) = `docs/review_packet_20260825.md` D-1을 해결한다.
> 이 파일이 닫는 것: (a) primary estimand β_t의 효율적 영향함수와 그 분산, (b) Result A를 ATE가 아닌
> **excursion effect에 대해** 정당하게 재진술, (c) softmax·τ를 제거한 policy-decisiveness 형태로의 일반화.
> 이 파일이 닫지 **못하는** 것: 고정 π의 점근분산 진술이라는 한계는 그대로다 (§5 참조).

---

## 1. 설정

관측 O = (H, A, Y). A ∈ 𝒜, |𝒜| = K < ∞. 행동정책 π(a|h) = P(A=a|H=h) > 0 (a.s.).
μ(a,h) = E[Y|A=a,H=h], σ²(a,h) = Var(Y|A=a,H=h). 모형은 **비모수**.

(다턴 설정에서는 H = H_t, Y = 근위 결과, 그리고 모든 진술을 가용층 {I_t=1} 위에서 읽는다.
원위 결과 · t 이후 ρ-전개는 §6.)

**목표 regime**: 결정적 행동이 아니라 **행동분포** q(·|h) 위의 확률적 개입 (stochastic intervention).

  ψ(q) = E[ Σ_a q(a|H) μ(a,H) ]

이는 stochastic/modified treatment policy 문헌(Muñoz & van der Laan 2012; Díaz & van der Laan 2013;
Kennedy 2019)의 파라미터이며, `formal_framework.md:33`의 커널 개입 규약과 동일한 대상이다.

**Primary estimand (2×2 form 효과).** ρ_D = dose 위 균등. `formal_framework.md:49`를 그대로 옮기면

  q₁(f,d | h) = 1{f = assertive}·ρ_D(d),   q₀(f,d | h) = 1{f = interrogative}·ρ_D(d)
  β^form = ψ(q₁) − ψ(q₀)

**중요 (여기서 갈린다)**: dose는 π가 아니라 **ρ로 주변화된다.** 따라서 관련 propensity는
form-marginal π(F=assertive|h)가 아니라 **셀 확률 π(f,d|h)들**이다. §4의 반례가 이 구분에 걸린다.

---

## 2. Proposition E (효율적 영향함수)

**Proposition E.** 위 비모수 모형에서 ψ(q)는 pathwise differentiable하고 그 효율적 영향함수는

  φ_q(O) = Σ_a q(a|H) μ(a,H) − ψ(q) + [ q(A|H) / π(A|H) ]·( Y − μ(A,H) ).

따라서 대비 β = ψ(q₁) − ψ(q₀)의 효율적 영향함수는 φ_{q₁} − φ_{q₀}이고, 그 분산 —
즉 semiparametric efficiency bound — 은

  V(β) = Var( m₁(H) − m₀(H) ) + E[ Σ_a ( q₁(a|H) − q₀(a|H) )² σ²(a,H) / π(a|H) ]   … (E1)

여기서 m_j(h) = Σ_a q_j(a|h) μ(a,h).

*증명.* ψ(q)는 관측분포의 (μ, H-주변분포)에만 의존한다. tangent space를
𝒯 = 𝒯_H ⊕ 𝒯_{A|H} ⊕ 𝒯_{Y|A,H}로 분해하고 각 성분에 대한 pathwise derivative를 취하면,
𝒯_H 성분이 Σ_a q μ − ψ, 𝒯_{Y|A,H} 성분이 (q/π)(Y−μ)를 준다. ψ가 π에 의존하지 않으므로
𝒯_{A|H} 성분은 0이다 (이것이 q가 h에 의존하더라도 성립하는 이유다 — q는 알려진 함수다).
E[φ_q] = 0과 φ_q ∈ 𝒯가 직접 확인되므로 φ_q가 EIF이다. 분산은 두 성분의 직교성에서
Var(m_q(H)) + E[(q/π)²σ²]이고, 후자를 a에 대해 전개하면 Σ_a q(a|H)²σ²(a,H)/π(a|H).
대비는 선형이므로 (q₁−q₀)로 치환된다. ∎

**부호 확인.** q₁, q₀의 support가 서로소일 때 (form 효과가 그렇다) (q₁−q₀)² = q₁² + q₀²이므로
(E1)의 합은 **네 셀 전부**를 훑는다.

**수치 검증.** π = (.48, .02, .02, .48) (셀 순서 (a,hi),(a,lo),(i,hi),(i,lo)), σ²=1, ρ_D=(½,½),
n = 4×10⁶ Monte Carlo:

  MC Var( (q₁−q₀)/π · (Y−μ) ) = 25.98      해석식 ρ_min²·Σ_a 1/π(a) = 26.04      ✓

---

## 3. Theorem A′ (policy-decisiveness 형태의 하한) — Result A의 교체

**정의 (policy decisiveness).** 𝒜* = supp(q₁) ∪ supp(q₀) ⊆ 𝒜에 대해

  **D(h) := − log min_{a ∈ 𝒜*} π(a|h)**                                        … (D)

즉 대비에 관여하는 행동 중 **가장 희귀한 것의 로그-희귀도**. D는 행동정책만으로 정의되며
**관측로그에서 식별 가능**하다. τ도 Δ도 softmax도 등장하지 않는다.

**가정.** (A1′) 𝓗_d = {h : D(h) ≥ d}에 대해 P(H ∈ 𝓗_d) ≥ c > 0.
(A2′) σ̲² := inf_{h ∈ 𝓗_d, a ∈ 𝒜*} σ²(a,h) > 0.
(A3) 비모수 모형 — outcome regression의 파라메트릭 외삽을 허용하지 않는다 (기존과 동일).

**Theorem A′.** (A1′)–(A3) 하에서, ρ_min := min_{a ∈ 𝒜*} q_j(a|h) 의 하한을 ρ_min이라 두면

  V(β) ≥ σ̲²·ρ_min²·E[ e^{D(H)} ] ≥ σ̲²·ρ_min²·c·e^{d}.                        … (A′)

*증명.* (E1)의 둘째 항만 유지(첫 항 ≥ 0). 𝓗_d 위에서
Σ_a (q₁−q₀)²σ²/π ≥ σ̲²ρ_min² Σ_{a∈𝒜*} 1/π(a|H) ≥ σ̲²ρ_min²/min_{a∈𝒜*}π(a|H) = σ̲²ρ_min² e^{D(H)}.
𝓗_d 위에서 e^{D} ≥ e^d이고 P(𝓗_d) ≥ c. ∎

**Hahn(1998)으로의 환원.** K=2, q₁=δ₁, q₀=δ₀ (ρ_min=1)이면 (E1)은
Var(μ₁−μ₀) + E[σ₁²/π(1|H) + σ₀²/π(0|H)] — 정확히 Hahn(1998)의 ATE bound.
**즉 우리는 Hahn의 bound를 인용하는 것이 아니라, excursion estimand에 대해 그 일반형을 유도하고
Hahn을 특수사례로 회수한다.** (D-1이 요구한 것이 이것이다.)

**softmax는 특수사례다.** π가 온도 τ의 softmax이고 K=2이면 D(h) = |Δ(h)|/τ + O(e^{−|Δ|/τ}),
따라서 (A′)는 기존 Result A의 exp(δ/τ)를 회수한다. **역은 성립하지 않는다** — (A′)는
softmax가 아닌 임의의 sharply adaptive policy(top-k, nucleus, 규칙기반 gating, 학습된 argmax)에
적용된다. 이것이 "Hahn bound에 softmax 대수를 넣은 것 아닌가"라는 반론이 성립하지 않는 이유다.

**정확한 항등식 (K=2).** p = π(1|h)일 때 1/(p(1−p)) = 2 + 2cosh(logit p) — 근사가 아니라 항등식
(상대오차 3×10⁻¹³로 수치확인). 논문에서 지수적 폭발을 그림 없이 한 줄로 보일 때 쓴다.

---

## 4. 반례 기각 — form-marginal은 하한을 구하지 못한다

"셀 propensity가 붕괴해도 form-marginal π(F=assertive|h)는 비퇴화일 수 있으므로 Theorem A′가
β^form에 적용되지 않는다"는 반론이 자연스럽다. **성립하지 않는다.**

π = (½−ε, ε, ε, ½−ε)로 두면 P(F=assertive) ≡ ½ (ε에 무관):

| ε | P(F=assert) | marginal 기반 오독 | **(E1)의 참값** |
|---|---|---|---|
| 0.10 | 0.500 | 4.00 | 6.2 |
| 0.05 | 0.500 | 4.00 | 11.1 |
| 0.02 | 0.500 | 4.00 | 26.0 |
| 0.005 | 0.500 | 4.00 | **101.0** |

이유: 목표 regime이 F를 고정한 뒤 **D를 ρ로 뽑으므로**, assertive 팔 안에서 (a,low) 셀이
반드시 필요하다. 그 셀이 희귀해지면 하한은 발산한다. marginal 기반 읽기는 dose를 π로
주변화하는 **다른 estimand**에 해당하며, 그것은 `formal_framework.md:49`가 정의한 대상이 아니다.

**따라서 K→2 축약은 무효가 아니라 불필요하다.** (A′)는 K개 행동에 대해 직접 진술되며,
지배하는 것은 두 행동의 점수격차가 아니라 **대비에 관여하는 행동 중 최희귀 셀**이다.
이는 기존 진술보다 강하다.

---

## 5. 이 정리가 하지 **않는** 것 (정직 절)

1. **(A′)는 고정 π에서의 점근분산 진술이다.** 모든 h에서 π(a|h) > 0이면 V(β) < ∞이고
   β는 여전히 regular하게 √n-추정 가능하다. (A′)는 impossibility가 아니라 **상수 인자**다.
   초록·본문에서 "no regular estimator escapes **the rate**"라고 쓰려면 π_n이 n과 함께
   날카로워지는 표류수열 위의 **local asymptotic minimax 논증**이 필요하다. 그것은 이 파일에 없다.
   (직계 선행연구: Khan & Tamer 2010, *Econometrica* — irregular identification. `references.bib`에 추가할 것.)
2. **다턴 복리는 §6의 미완성 항목이다.** Prop A-T는 정책가치 V(ρ)의 하한이며 excursion 버전이 아니다.
3. **유한표본 붕괴(위상도의 "편향된 채 안정" 국면)는 (A′)가 설명하지 않는다.** (A′)는 E[e^D] —
   즉 D의 **평균** — 을 지배량으로 갖는데, 유한표본 support 실패는 D의 **상위꼬리**가 지배한다
   (수치 확인: U(−1,1)과 N(0,1)에서 평균 기반 임계는 후자를 4 log 단위 틀린다).
   **두 임계는 다른 양이며 같은 그림에 한 선으로 그려서는 안 된다.** → `joint_regimes.md` (미작성)

---

## 6. 다턴 확장 (미완성 — 작업 항목)

t 이후 ρ-전개를 포함하는 원위 excursion의 EIF는 순차 가중

  W_t = [ q(A_t|H_t) / π(A_t|H_t) ] · Π_{s>t} [ ρ(A_s|H_s) / π(A_s|H_s) ]

을 갖는 sequential DR 형태다 (Robins g-formula / MSM). E[W_t²|H_t]가 턴마다
Σ_a ρ(a|H_s)²/π(a|H_s) ≥ ρ_min² e^{D(H_s)} 인자를 곱하므로, **Prop A-T의 복리는 여기서
정당하게 살아난다** — 단 인자는 e^{D}가 아니라 ρ_min² e^{D}이고, 층 지속확률 p_δ가 곱해진다.
현재 발표자료의 "42³"은 이 두 인자를 소거한 값이다 (K=2, p_δ=½이면 턴당 42·½/4 = 5.25).

**남은 작업**: (i) 위 EIF의 정식 유도, (ii) (M1) 없이 성립하는 형태 탐색 —
현재 (M1)("모든 행동에서 이력이 고갭층에 잔류")은 논문 제목 *When the Treatment Talks Back*의
전제와 정면으로 충돌한다, (iii) p_δ의 실증 추정 또는 하한.

---

## 7. 상류 문서에 반영할 변경

- `formal_framework.md` §3: Result A를 **Theorem A′**로 교체, (A1)(A2)를 (A1′)(A2′)로 교체,
  D의 정의 (D)를 §1에 추가. SSOT를 v0.5로 올린다.
- `formal_framework.md:69`: Result B 조건에 **(B2) simple root (Δ′(r) ≠ 0)** 가 누락되어 있다.
  현재 문장("Δ가 연속이고 0 근방에 밀도")만으로는 결론이 성립하지 않는다 — 반드시 수정.
- `paper/tex/main.tex`: §4.2를 D 기반으로 재작성. Hahn 인용을 "우리 (E1)의 특수사례"로 재배치.
- `references.bib`: Khan & Tamer (2010), Muñoz & van der Laan (2012), Kennedy (2019),
  Liu et al. (2018, curse of horizon), Hahn–Todd–van der Klaauw (2001, RD) 추가.
