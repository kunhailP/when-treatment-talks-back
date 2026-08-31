# Proposition 1A + Results A/B — 비식별·overlap 붕괴의 정식화 (v0.5)

> v0.5 (2026-07-30, W3 증명 완료): 1A 반례쌍 완전 구성(U 없는 최소 구성 + 다턴 remark), Result A를 (A1)–(A3) 하의 정식 하한으로(Hahn 1998 인용), **Result B 1-D 증명 완료 → Proposition 승격** ((B2′) 정칙조건 추가). 전체 증명 = theory/proofs_w3_draft.md. 위임 결정 3건(§말미) 사용자 재검토 가능. 연속 H 시뮬레이션(continuous_h.py) 수치 검증 완료: 위상도 경계 = 실선 log E[1/p_τ], overlap 추정량 전 τ에서 β^ov 불편, β^ov_τ→β(0).
> v0.4 (2026-07-30): 3차 비판 반영 — Result A 성립 조건 (A1)–(A3) 명시, n_eff를 arm-specific Kish로 교체, Result B의 수학적 명칭 "overlap collapse and localization" 확정(정보는 해석 층위), Prop 1A "필연" 완화, 위상도 figure 사양 추가, 연속 H 시뮬레이션 주 DGP = Uniform(−1,1).
> v0.3 (2026-07-29): **"Hájek가 경계 estimand로 수렴한다"는 기존 1B(b) 주장 폐기** (고정 τ, n→∞에서 IPW는 모집단 효과를 겨냥함을 수치로 확인: τ=0.3, n=4M, IPW=1.792≈ATE=1.798≠β^ov=1.356). "theorem" 단어는 증명 완성 전까지 금지.

## 설정

시스템 수준 무작위화 Z ∈ {AI 대화, 통제}만 시행. Z=1군에서 배치 정책이 행동을 선택: A_t ~ π^dep_t(·|H_t), 발화 실현 M_t ~ G(·|A_t, H_t). 관측자료는 완전한 transcript (X, A_{1:T} 또는 그 추정 라벨 S̃_{1:T}, M_{1:T}, R_{1:T}, Y). 목표 estimand는 formal_framework §2.3의 experimental excursion β_t(a, a′; ρ).

---

## Proposition 1A (구조적 비식별 — LLM 배치에서의 구조적 빈발성)

**주장.** π^dep_t(a|h) = 0인 (a,h) 쌍이 양의 확률 이력 집합에서 존재하면, β_t(a, a′; ρ)는 관측분포로부터 비모수적으로 식별되지 않는다.

**"비식별"의 정확한 의미 (심사 질문 1에 대한 답).** 관측분포 P가 동일하지만 β 값이 다른 두 DGP가 존재한다는 뜻이다.

**반례쌍 (완전 구성 — v0.5, 증명 = proofs_w3_draft §1).** 최소 구성은 미관측 U조차 필요 없다 — 실패의 원천은 교란이 아니라 **support**다. T=1, H ∈ {h₀,h₁} (P(h₁)=q), π^dep(1|h₀)=1/2, **π^dep(1|h₁)=0**, Y(a)|H=h ~ N(μ_a(h),1)로 두고, 두 DGP가 μ₁(h₁) = c₁ vs c₂ (c₁≠c₂)에서만 다르다고 하자. 관측분포는 P(H)·π^dep(A|H)·N(y;μ_A(H),1)로 인수분해되는데 (1,h₁) 층은 확률 0이라 기여하지 않으므로 두 DGP의 관측분포는 동일하다. 반면 균등 ρ 하의 excursion β는 q(c₂−c₁)만큼 다르다. ∎ **다턴 remark**: H_t=(X,R_{1:t−1})로 읽고 π^dep_t(a|h)=0인 층에 같은 논증을 적용하면 time-varying 버전이 된다 (이때 U가 R을 매개로 개입하는 구 스케치의 형태가 회복됨).

**novelty 경계 (정직 서술 — v0.4 완화).** 이 구조 자체는 Robins(1986) 이후 time-varying confounding 문헌의 표준이다. 우리의 추가 주장은 하나뿐이다: **RLHF로 조각된 배치 LLM에서 π^dep의 이력-결정성은 우연한 데이터 결함이 아니라 구조적으로 빈번하며, 설계에 의해 강화된다** — 온도 τ가 낮게 배치되고 선호 최적화가 점수격차 Δ를 키우는 메커니즘이 이를 체계적으로 만든다. 따라서 "더 나은 로그 데이터"로 우회하기 어렵다. ("필연 inevitability"은 과잉 주장 — 모든 배치가 결정적이라는 증명은 없다. 주장 강도는 "structurally frequent and design-reinforced"까지.)

## Result A (Temperature-indexed collapse of the efficiency bound — 본 기여)

τ > 0이면 π^dep_t(a|h) > 0이므로 **형식적 positivity와 형식적 식별은 성립한다.** Result A는 그럼에도 정보가 붕괴한다는 rate 주장이며, **IPW 클래스가 아니라 semiparametric efficiency bound 수준에서 서술한다** — "outcome regression 쓰면 되잖아"라는 반론을 원천 차단하기 위함.

**성립 조건 (v0.4 잠금 — 증명은 이 조건 하에서만 쓴다):**
- (A1) 𝓗_δ = {h : |Δ(h)| ≥ δ}가 양의 측도, 어떤 δ > 0에 대해.
- (A2) 분산 비퇴화: σ̲² = inf_{h∈𝓗_δ, a} σ_a²(h) > 0. (결과가 결정적이면 반사실 정보가 필요 없어 하한이 폭발하지 않음 — 이 조건 없이는 거짓.)
- (A3) **비모수/semiparametric 모델 클래스**: outcome regression의 파라메트릭 외삽(희귀 층의 E[Y(a)|H]를 모형으로 보간)을 배제. 파라메트릭 가정을 사면 하한을 피할 수 있으나 그것은 식별을 가정으로 사는 것 — 논문에 명시.

**정식 하한 (v0.5, 증명 = proofs_w3_draft §2).** (A3) 클래스에서 ATE형 excursion의 efficiency bound는 (Hahn 1998) V_τ = E[σ₁²/p_τ + σ₀²/(1−p_τ) + (β(H)−β)²]. 셋째 항을 버리고 𝓗_δ로 제한한 뒤, 𝓗_δ 위에서 min(p_τ,1−p_τ) = σ(−|Δ|/τ) ≤ exp(−δ/τ)를 대입하면

  **V_τ ≥ σ̲² · P(𝓗_δ) · exp(δ/τ).**

convolution theorem에 의해 (A3) 클래스의 어떤 정규 추정량도 이 하한 미만의 점근분산을 가질 수 없다 — "AIPW로 바꿔도 복구되지 않는다"의 정확한 형태. (2-행동 서술; K-행동은 해당 대비의 두 팔에 동일 논증. 이 하한은 고정 τ 점근 분산에 관한 것이고, 유한표본 편향-안정 국면은 위상도가 담당 — 두 주장을 섞지 않는다.)

**유효표본 (v0.4 교체 — arm-specific Kish).** n_eff(a) = n / E[1/π_τ(a|H)]. (구 표기 n·E[exp(−Δ/τ)] 폐기 — 층 혼합에서 Jensen 방향이 달라 과대평가할 수 있음.) **"τ 절반 → 필요 n 제곱"은 점수격차가 고정된 층 내부에서만** 성립: 그 층에서 1/p_τ ≈ exp(δ/τ)이므로 τ→τ/2가 exp(δ/τ)→exp(δ/τ)²을 준다. 층별 gap이 이질적이면 전체 rate는 최대 gap 층이 지배.

**핵심 문장: 추정량을 IPW에서 AIPW로 바꿔도 근본적으로 관측되지 않는 반사실 정보는 복구되지 않는다.** T턴 복리화(E[W²]~exp(2TΔ̄/τ))의 정확한 차수는 경로 의존성 때문에 heuristic으로 표기 (envelope 정리 TODO).

**Proposition A-T (다턴 복리 하한 — v0.5.2 신규, 증명 = proofs_w3_draft §4).** (M1) 고갭 집합의 행동-균등 재귀성 P(H_{s+1}∈𝓗_δ|h,a) ≥ p_δ, (M2) 턴별 분산 하한, (A3) 하에서, Kallus–Uehara(2020)/Jiang–Li(2016) 유한기간 OPE efficiency bound에 backward induction을 적용하면 T턴 정책가치의 효율 하한은 **V_eff ≥ σ̲²·P₁(𝓗_δ)·p_δ^{T−1}·[exp(δ/τ)/K²]^T** — τ < δ/log(K²/p_δ)에서 T에 기하급수 복리. **구 Result 3의 heuristic이 정식 하한으로 대체됨** (excursion 버전은 지수 T−t+1의 corollary). (M1)은 실질 가정(강반발층의 지속성)이며 논문에 해석 명시.

**Remark A′ (단일턴 하한의 다턴 a fortiori 적용 — v0.5.1, draft_jci_v02 §4.2와 동일).** 본 문서의 정리들은 단일턴·2행동으로 서술되지만, 관측모형이 턴별로 인수분해되고 turn-t excursion의 식별은 turn-t 단일턴 문제 + 이후 턴들의 π^dep→ρ 교량을 모두 요구하므로, **이후 턴의 정보비용을 버리는 것은 난이도를 과소평가하는 방향**이다. 따라서 turn-t의 (Δ,τ)에서의 단일턴 하한은 대화 문제의 하한이기도 하다 — "한 턴만 봐도 이만큼 나쁘다"가 Result A의 올바른 다턴 독해. 다턴 복리의 정확한 차수는 여전히 열린 문제(envelope TODO)이며 증명에 사용하지 않는다. K-행동은 대비에 관여하는 두 팔로 환원.

## Result B (Overlap collapse and localization — 본 기여, **v0.5 Proposition 승격**)

> 명칭 규율 (v0.4): 수학적 결과의 이름은 "overlap collapse and localization"이다 — 증명되는 것은 overlap 질량/가중의 붕괴와 집중이지 "정보" 그 자체가 아니다. "인과정보의 국소화"는 efficiency bound와 연결되는 **해석** 층위에서만 쓴다.

ω_τ(H) = p_τ(H){1−p_τ(H)},  β^ov_τ = E[ω_τ(H){Y(1)−Y(0)}] / E[ω_τ(H)].

**정칙조건 (v0.5 — 1-D Proposition은 이 조건 하에서 증명됨):**
- (B1) H가 연속밀도 f를 가짐 (1-D: H ∈ ℝ)
- (B2) Δ ∈ C¹, Δ(h)=0의 해가 고립된 simple root들 {r_j}: Δ′(r_j) ≠ 0
- **(B2′, v0.5 추가) 모든 ε>0에 대해 inf_{dist(h,{r_j})≥ε} |Δ(h)| > 0** (tail 차단; U(−1,1)·N(0,1) 주/robustness DGP 모두 충족)
- (B3) f와 조건부 효과함수 c(h) = E[Y(1)−Y(0)|H=h]가 각 root 근방에서 연속, c 유계
- (B4) 정규화 상수 E[ω_τ] > 0 유한, root에서 f(r_j) > 0

**진술 (unique root r=0인 경우).** 정규화 측도 ω_τ(h)f(h)/∫ω_τ f 는 τ↓0에서 δ₀로 약수렴하고, β^ov_τ → E[Y(1)−Y(0)|H=0]. **다중 root면 한 점이 아니라 각 r_j에 f(r_j)/|Δ′(r_j)| 비례 질량이 배분**된다. 다차원에서는 결정면 {Δ=0} 위에 f/|∇Δ| 비례 surface measure가 남는다 — "경계로 집중"은 특정 경계점이 아니라 **결정면 전체에 걸친 분포**를 뜻한다 (서술 시 이 구분 유지).

**증명 (v0.5 완료 — 변수변환 + approximate identity; 전문 = proofs_w3_draft §3).** 핵심 항등식 ω_τ = 1/[4cosh²(Δ(h)/2τ)]에서 K(u)=1/[4cosh²(u/2)]는 ∫K=1인 approximate identity kernel. (B2′)로 tail 기여가 e^{−c(ε)/τ}로 소멸하고, root 근방에서 v=Δ(h), v=τu 변수변환 + 지배수렴으로 I_τ(g) = τ·g(0)f(0)/|Δ′(0)| + o(τ). 이로부터 (i) ν_τ ⇒ δ₀, (ii) **E[ω_τ] = τ·f(0)/|Δ′(0)|·(1+o(1))** (overlap 질량의 τ-선형 소멸 — 정확한 상수 포함), (iii) β^ov_τ → c(0). multiple-root corollary: 질량 f(r_j)/|Δ′(r_j)| 비례 배분. **다차원 coarea는 appendix proposition/conjecture 지위 유지** (본문 정리로 만들지 않는다). 수치 검증(continuous_h.py): β^ov_{τ=0.045}=1.062→c(0)=1, overlap 추정량 전 τ 불편. **주장의 정확한 형태: 전체 ATE가 경계 효과로 "바뀌는" 것이 아니라, 안정적으로 관측 가능한 인과정보가 경계로 집중되는 것이며, 경계 효과는 β^ov라는 별도 estimand로 정의된다.** overlap weighting의 empirical equipoise 해석(Li–Morgan–Zaslavsky 2018)과 연결. 정치학적 함의(유지): 정책이 확신 있게 행동을 고르는 층 — 강반발 당파층 — 에서 모집단 효과에 대한 정보가 0으로 수렴한다.

## 반례 (논문에 반드시 포함 — 잘못된 직관 차단)

**고정 τ>0, true propensity, n→∞이면 IPW는 여전히 모집단 효과를 추정한다.** 정책이 날카롭다는 이유만으로 estimand가 자동으로 경계 효과로 변하지 않는다. 수치 확인(2026-07-29): τ=0.3, n=4,000,000, β(H)=1+|H| DGP에서 IPW=1.792 ≈ ATE=1.798, β^ov=1.356. 문제는 n×τ **공동극한의 위상도**다:
- n ≫ exp(δ/τ): 전체 효과 추정 가능 (분산 큼)
- n ~ exp(δ/τ): 분산 폭발 구간
- n ≪ exp(δ/τ): 희귀 crossover 미관측 → **편향된 채 안정돼 보이는** 붕괴 (기존 2-상태 시뮬레이션의 극단 τ 현상이 정확히 이것 — Result B의 증거가 아님)

**위상도 figure 사양 (W4 — 논문 핵심 그림, v0.4.1 갱신).** x축 = 1/τ, y축 = log n, 격자 셀 색 = 세 국면(추정 가능/분산 폭발/편향-안정), RMSE·coverage 각 한 판. **경계선은 2개**: 점선 = 층별 직관 기준 log n = δ/τ (고정-gap heuristic), 실선 = 해당 DGP의 정확한 log E[1/p_τ(H)] (또는 두 arm 중 큰 쪽). **주 DGP Uniform(−1,1), Δ(H)=H에서는 닫힌 형태가 존재: E[1/p_τ] = 1 + τ·sinh(1/τ)** (수치 확인 2026-07-30: τ=0.3에서 MC 5.197 vs 닫힌형 5.199), τ↓0 점근으로 log E[1/p_τ] ≈ 1/τ + log τ − log 2. 임의의 δ/τ만 그리면 DGP 전체의 경계로는 부정확하다.

## Ill-defined treatment (구 "(ii) consistency 실패" — 용어 교체)

관측 라벨 S̃_t = s의 실제 처치는 M_t ~ G(·|s, H_t)이며 G가 H_t를 조건으로 하므로, 같은 라벨이 이력마다 다른 발화분포를 의미한다. 이력 층화 없는 라벨 풀링 대비는 **잘 정의된 처치쌍에 대응하지 않는다** (ill-defined treatment; stochastic intervention 문헌의 언어로는 "개입 분포가 미지정"). 

**정직한 서술 (심사 질문 2에 대한 답).** 우리는 estimand를 "G의 생성분포에 대해 평균화된 효과"로 재정의함으로써 이 문제를 다룬다. 이 재정의는 비식별을 **푸는 것이 아니라 질문을 잘 정의된 것으로 바꾸는 것**이다: 관측 라벨 대비는 우리가 원하는 β에 대응하지 않고, 우리가 정의한 β는 G-MRT(배정 무작위화)에서만 식별된다.

## Corollary — 설계 요소와 실패 경로의 대응 (2×2 갱신)

| G-MRT 요소 | 제거하는 실패 |
|---|---|
| ρ_t(a|h) = 1/4 (모든 form×dose 셀, 모든 h) | 1A의 support 실패 + Result A의 정보 붕괴 |
| A_t = (F_t, D_t) 외생 무작위화 | sequential confounding |
| regime-정의 estimand (커널 개입) | ill-defined treatment |
| 배정-ITT + fidelity 규약 | turn-level noncompliance (형·용량 차별 비순응은 §4.4 경고 참조) |

## TODO 상태 (v0.5 갱신)

1. ~~1A 반례쌍의 완전한 구성~~ → **완료 (v0.5, 본 문서 + proofs_w3_draft §1)**
2. ~~Result B 1-D 증명~~ → **완료·Proposition 승격 (v0.5, proofs_w3_draft §3)**; 다차원 coarea는 appendix 지위
3. ~~Result A 정식 하한~~ → **완료 (v0.5, proofs_w3_draft §2)**
4. ~~연속형 결정경계 시뮬레이션~~ → **완료 (2026-07-30, simulation/src/continuous_h.py)**: 위상도·battery·robustness 전부 산출, 국면 경계가 실선 log E[1/p_τ]와 정합
5. 전략 라벨 측정오차 하의 π̂ 왜곡 분석 — W4 (JCI 부록) [진행 중]
6. **[PA 트랙으로 이관]** differential fidelity(배정 vs 실현) 시뮬레이션, 2×2 form×dose DGP, WCLS 추정기 — publication_map 참조

**위임 결정 3건 (2026-07-30, 사용자 재검토 가능 — proofs_w3_draft 말미 참조):** (i) (B2′) 정칙조건 채택, (ii) Result A는 Hahn(1998) 인용 형태(자기완결 유도는 appendix 후보), (iii) 1A는 U 없는 최소 구성을 본문으로, U-매개 다턴은 remark로.
