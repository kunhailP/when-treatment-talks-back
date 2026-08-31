# Formal Framework (v0.5 — SINGLE SOURCE OF TRUTH)

**When the Treatment Talks Back: Design-Based Causal Inference for Adaptive Generative Political Communication**

> **운영 규칙**: 이 파일이 프로젝트의 유일한 진실 원천이다. 설계·estimand·기여에 관한 모든 결정 변경은 이 파일을 먼저 수정한 뒤 다른 문서가 따라온다. (v0.3→v0.4: 2026-07-30, 3차 비판 반영 — Contribution 2의 수학적 명칭을 "overlap collapse and localization"으로 확정(정보는 해석 층위), Result A 성립 조건 명시, n_eff를 arm-specific Kish 형태로 교체, Prop 1A "필연"→"구조적으로 빈번·설계상 강화", 두-논문 분리(docs/publication_map.md) 신설. v0.2→v0.3: 2026-07-29, 2차 비판 — "추정량의 경계 수렴" 주장 폐기, proximal/distal 분리, novelty 축소, gate=생성커널)

> **두-논문 구조**: 이 framework는 프로그램 전체를 담지만, 산출물은 두 논문으로 분리된다 — **JCI 논문**(관측 로그의 정보 한계: Contribution 1–2 + 반례·위상도·연속 H 시뮬레이션, G-MRT는 해법 절)과 **PA 논문**(G-MRT 정치 실험: Contribution 3 + 2×2 실증). 경계·잠금은 `docs/publication_map.md`. **8/26 arXiv v1 = JCI-형 working paper.**

---

## 0. Contribution (잠금 — 3줄, 추가 금지)

1. **생성형 처치의 estimand 정식화 + 효율적 영향함수**: 처치를 (전략정책 π, 생성기 G, 정보환경 E)의
   결합으로 정의하고, deployment / policy / turn-level excursion 효과를 분해한다. **v0.5 신규**:
   turn-level excursion estimand의 EIF를 직접 유도한다 (`excursion_bound.md` Prop E) — Hahn(1998)의
   ATE bound를 인용하는 것이 아니라 그 일반형을 유도하고 Hahn을 특수사례로 회수한다.
   JCI 논문은 일반 행동공간 A_t ∈ 𝒜로 서술하고, 2×2(form × dose)는 running example이자 PA 트랙 사양.
2. **Policy-decisiveness collapse and localization** (v0.5: τ 중심 → D 중심으로 교체):
   지배량은 **D(h) = −log min_{a∈𝒜*} π(a|h)** 이며 행동정책만으로 정의되고 로그에서 식별 가능하다.
   softmax 온도는 그 특수사례다. (a) 효율경계가 E[e^D]로 지수적 악화 (`excursion_bound.md` Theorem A′),
   (b) **minimax 불가능성** — M(π_n)/n → ∞ 이면 risk가 0으로 안 감 (`minimax_collapse.md` Theorem C),
   (c) overlap 질량이 결정경계로 국소화 (`temperature_collapse.md` Result B, 다변량은
   `localization_manifold.md` Theorem L). **β^ov는 RD estimand다.**
   **주의: 국소화는 안정성이 아니다** — E[ω_τ] = O(τ)이므로 경계 estimand의 유효표본도 함께 소멸한다.
3. **G-MRT with generated-treatment fidelity**: 대화 내 턴별 micro-randomization + 잠긴 evidence bank
   + gated generation + 배정-ITT. 게이트는 처치커널의 일부이므로 ITT가 식별하는 것은
   "generate-and-gate 프로토콜에의 배정 효과"다. novelty는 "LLM×MRT 최초"가 아니다.

**명시적 강등 (본 논문의 기여가 아님)**: generator transport(Γ), GPI 내부표현 결합,
다중 비교 동시추론, epistemically constrained policy learning.

**미해결 (논문에 열린 문제로 명시)**: 달성(achievability) 쪽 상계. 하한 M과 oracle-IPW 분산인자
E[e^D]의 간격이 분포족 의존적(U(−1,1) 1.00 nat, N(0,1) 2.06 nats)이라 단일 함수형이
하한과 관측 전이를 동시에 예측하지 못한다.

---

## 1. Setup

개인 i = 1,…,n. 턴 t = 1,…,T (기본 T=3).

- X_i ∈ 𝒳: 사전 공변량 · b_i0: 사전 믿음 · E_j: 쟁점 j의 잠긴 evidence bank (사실 명제 유한집합, fact-check 절차로 고정)
- **A_{it} = (F_{it}, D_{it})**: 턴 t의 배정 행동 — **form** F ∈ {assertive(단언), interrogative(질문)} × **dose** D ∈ {high(사실 4–5개), low(사실 1–2개)}. **2×2가 기본 실험 객체다.**
- M_{it} ∈ ℳ: 실현된 발화. S̃_{it}: 발화에서 측정된 구현 행동 (fidelity 감사용)
- R_{it}: 사용자 반응 · H_{it}: 턴 t 직전 이력 · Y_i: 결과 벡터 (belief accuracy, calibration, reactance, 1주 retention)

**생성형 처치의 2단 구조.**
행동 배정: A_{it} ~ π_t(·|H_{it}) · 발화 실현: M_{it} ~ G_θ(·|A_{it}, H_{it}, E_j)

**처치는 확률적 개입(stochastic intervention)이다.** 잠재결과는 개별 문장이 아니라 **regime (π, G) 하의 잠재결과** Y_i^{π,G}로 정의한다. 이는 stochastic/modified treatment policy 문헌(Muñoz & van der Laan 2012; Díaz & van der Laan 2013; Kennedy 2019; Young, Hernán & Robins 2014)의 regime-specific potential outcome과 동일한 형식 객체이며, β의 do-표기는 "라벨에 대한 개입 + 실현은 G에서 추출"이라는 **커널 개입**으로 읽는다. (시뮬레이션의 do(S_t)가 정확히 이 커널 개입을 구현함을 simulation/README에 명시할 것.)

## 2. Estimands

### 2.1 Deployment effect
Δ^dep = E[Y^{π₁,G₁}] − E[Y^{π₀,G₀}]. 기존 RCT(Salvi 2025; Hackenburg 2025)가 식별하는 것.

### 2.2 Policy effect (생성기 고정)
Δ^pol(G) = E[Y^{π₁,G}] − E[Y^{π₀,G}].

### 2.3 Turn-level causal excursion effects — **primary 계열 (proximal/distal 분리)**

**Proximal excursion** (턴 직후 결과: reactance, 즉시 belief update, 지속 여부): 표준 CEE/WCLS 대상.
**Distal excursion** (최종 belief accuracy, 1주 retention): 최종 시점 결과이므로 일반 WCLS가 아니라 **distal causal excursion effect(DCEE) 문헌(Biometrics 2025)의 estimand·추정법과 명시적으로 연결**한다. 이 구분 없이 최종 Y에 WCLS만 쓰면 표준 공격점이 된다.
**Reference policy 사전지정: ρ = 균등 (각 form 1/2 × 각 dose 1/2), 모든 t, 모든 h에서.** primary estimand는 "experimental excursion under ρ":

- **Form 효과**: β_t^form = E[Y^{(F_t=assertive, D_t~ρ, 이후~ρ),G} − Y^{(F_t=interrogative, D_t~ρ, 이후~ρ),G} | I_t=1]
- **Dose 효과**: β_t^dose = E[Y^{(D_t=high, F_t~ρ, 이후~ρ),G} − Y^{(D_t=low, F_t~ρ, 이후~ρ),G} | I_t=1]
- **상호작용**: β_t^{form×dose} = 표준 factorial 대비의 차이-의-차이
- Moderation: 위 각각을 H_t 요약통계(직전 반발 등) 조건부로.

배치-정책-기준 excursion(ρ = π^dep)은 **secondary**로만 보고한다 (positivity·해석 문제를 명시). I_t는 가용성 지표.

**구분 (혼동 금지)**: information mediation β^{free} − β^{lock}(잠금 체제 간 비교)과 β^dose(잠긴 bank 안의 용량 조작)는 **다른 과학적 질문**이다. 본 실험의 primary는 후자다. 전자는 G^lock vs G^free 체제 비교가 별도로 설계될 때만 다룬다.

### 2.4 정책가치 V(π,G)
사전지정된 2–3개 정책 쌍에 한해 secondary로 비교 (분산 폭발 때문).

## 3. Identification (요약 — 상세 증명은 nonidentification_note.md)

**Prop 1A (표준 구조의 LLM 관련성).** 시스템 수준 무작위화 하에서 배치 정책이 이력-결정적 성분을 가지면(∃(a,h): π^dep(a|h)=0), 해당 층의 g-formula 항이 미정의 → turn-level 효과 비모수 비식별. 구조 자체는 Robins(1986) 이래 알려진 것; 우리의 주장은 **LLM 배치에서 이 조건이 우연한 데이터 결함이 아니라 구조적으로 빈번하며, RLHF 선호 최적화(점수격차 확대)와 저온 배치 관행에 의해 설계상 강화된다**는 것이다. ("필연"이라는 표현은 쓰지 않는다 — 모든 배치가 결정적이라는 증명은 없으며, 주장의 강도는 빈도·강화 메커니즘까지다.)

**Theorem A′ (policy-decisiveness collapse — v0.5, 구 Result A 교체).** 𝒜*를 대비에 관여하는
행동집합, D(h) = −log min_{a∈𝒜*} π(a|h)로 두면, 조건 (A1′) P{D(H) ≥ d} ≥ c > 0,
(A2′) 𝓗_d 위 조건부분산 하한 σ̲² > 0, (A3) 비모수 outcome 모형(파라메트릭 외삽 불허) 하에서

  V(β) ≥ σ̲²·ρ_min²·E[e^{D(H)}] ≥ σ̲²·ρ_min²·c·e^{d}.

전문·증명은 `excursion_bound.md`. **τ도 softmax도 등장하지 않으며**, softmax는 D = |Δ|/τ인
특수사례다. K=2·ρ 퇴화에서 Hahn(1998) ATE bound를 회수한다.
**factorial에서 지배하는 것은 대비 factor의 marginal이 아니라 셀 확률이다** (§4의 반례 참조).

**Theorem C (minimax 불가능성 — v0.5 신규).** M(π) := sup_d P{D(H) ≥ d}·e^d 로 두면

  inf_{β̂} sup_P E|β̂ − β| ≥ (1/4)·min{ B·ρ_min , ρ_min·σ·√(M(π)/n) }.

따라서 표류수열에서 M(π_n)/n → ∞ 이면 minimax risk가 0으로 가지 않는다. 이것이
"정보 한계"라는 표현을 정당화하는 근거이며, Theorem A′ 단독으로는 정당화되지 않는다
(A′는 고정 π의 상수 진술). 증명(Le Cam 두 점)과 독립 재검증 3종은 `minimax_collapse.md`.
**위상도의 "편향된 채 안정" 국면은 two-point 구별불가능성이다.**

**유효표본 (arm-specific Kish — v0.4 교체).** n_eff(a) = n / E[1/π_τ(a|H)] (Kish 형태; 구 표기 n·E[exp(−Δ/τ)]는 폐기). "τ 절반 → 필요 n 제곱" 문장은 **점수격차가 고정된 층 내부에서만** 성립한다 (층별 gap이 다르면 혼합 rate).

**Result B (localization — v0.5 조건 수정).** ω_τ(H) = p_τ(1−p_τ)로 정의된 overlap 가중은
τ↓0에서 결정면 {Δ(H)=0}으로 집중된다. **조건 (구 진술은 불충분했다)**: (B1) 밀도 f가 근 근방에서
연속, (B2) Δ ∈ C¹이고 근 집합이 **유한**이며 모든 근이 **simple** (Δ′(r) ≠ 0), (B2′) 꼬리 분리,
(B3) c 유계·연속, (B4) **f(r) > 0** — (B4)가 없으면 결론이 0 = o(τ)로 퇴화한다.
복수근이면 극한은 Σ_j w_j δ_{r_j}, w_j ∝ f(r_j)/|Δ′(r_j)|.
다변량(H ∈ ℝ^d)은 `localization_manifold.md` Theorem L: (C2) 0이 Δ의 regular value이면
표면측도로 수렴하고 밀도가 f/‖∇Δ‖에 비례한다.

경계 효과는 별도 estimand β^ov_τ = E[ω_τ(Y(1)−Y(0))]/E[ω_τ]로 정의하며,
**이는 회귀불연속(RD) estimand다** — d=1에서 E[Y(1)−Y(0) | Δ(H)=0], 다변량에서 boundary RD.
**"안정적으로 관측 가능"은 틀린 표현이다**: E[ω_τ] = O(τ)이므로 β^ov의 유효표본도 O(nτ)로 소멸한다.
정확한 진술은 "가장 오래 살아남는 것이 경계 정보이나 그것도 사라진다".

**반례 (논문에 반드시 포함).** 고정된 τ>0에서 true propensity를 아는 IPW는 n→∞에서 여전히 모집단 효과를 추정한다 — 정책이 날카롭다는 이유만으로 추정량의 목표가 경계 효과로 "자동으로 바뀌지 않는다" (수치 확인 완료: τ=0.3, n=4M에서 IPW=1.792≈ATE=1.798 ≠ β^ov=1.356). 문제는 n과 τ의 **공동극한**이며, n이 exp(δ/τ)보다 느리게 자라면 희귀 crossover 미관측 → 편향된 채 안정돼 보이는 붕괴가 일어난다. **한 문장 잠금: 형식적 식별과 실용적 추정가능성은 다르며, 본 논문의 주장은 정보 한계의 rate와 정보의 국소화이지, 추정량 target의 변화가 아니다.**

**Ill-defined treatment (구 명칭 "consistency 실패" — 용어 교체).** 관측 라벨 S̃=s의 실제 처치는 M~G(·|s,H)로 이력마다 다른 분포다. 라벨 풀링 대비는 잘 정의된 처치쌍의 효과에 대응하지 않는다. **정직한 서술**: 우리의 estimand 재정의(생성분포 평균화)는 이 비식별을 "푸는" 것이 아니라 **질문을 잘 정의된 것으로 바꾸는 것**이며, 그렇게 정의된 β는 G-MRT 하에서만 식별된다.

**설계 대응 (2×2 갱신).** ρ(a|h)=1/4 ≥ ε → positivity 복원 · A_t 외생 무작위화 → sequential ignorability · regime 정의 → ill-defined treatment 해소.

## 4. Design: G-MRT (2×2 factorial)

1. **모델 수준 무작위화** (conversation-level): Z_i ∈ {G_a, G_b}, 최소 한 팔은 open-weights (재현성).
2. **턴별 2×2 무작위화**: A_{it} = (F_{it}, D_{it}) ~ 균등, 배정·확률·구현 전부 로깅.
3. **Evidence bank 잠금 — 고갈 방지 규격**: T=3 × high dose 4–5개 = 총 12–15개 사실 소요 → **쟁점당 최소 20개 fact unit**(ID·원문·출처·허용 paraphrase·방향성·중복관계 명세)을 준비하고, 턴별 서브뱅크 또는 비복원 sampling 규칙을 **treatment regime의 일부로 명시**한다. dose의 정직한 명명: 사실 수를 조작하면 길이·구체성·인지부하가 동반 변동하므로, 이 논문에서는 dose를 "순수 정보량"이 아니라 **high-information communication package** 효과로 정의한다 (길이 통제 설계는 후속 옵션).
4. **Fidelity 게이트와 noncompliance 규약** — **게이트는 품질관리 장치가 아니라 처치 생성커널의 일부다**: 실제 처치커널은 base G가 아니라 재생성 절차가 결합된 G̃(gated kernel)이며, ITT가 식별하는 것은 "실현된 발화 형식의 효과"가 아니라 **"해당 형식 생성을 지시하고 게이트를 적용하는 프로토콜에 배정된 효과"**다. 논문 본문에 이 문장을 그대로 쓴다.
   - Primary는 **배정-ITT** (배정 A_t 기준 분석). 게이트: 송출 전 검사 → 불일치 시 1회 재생성 → 재실패 시 기록 후 송출.
   - **차별 비순응 경고**: form fidelity와 dose fidelity의 실패율이 다르면(예: 질문형이 더 자주 실패) 셀 간 비교가 오염된다. → 사전등록에 **fidelity 하한 ≥80%/셀**과 미달 시 분석 계획(해당 대비 강등)을 명시.
   - **게이트 분류기의 측정오차가 배정과 상관되면 게이트 자체가 처치를 왜곡** → 게이트 판정 로그를 공개하고, 게이트 미적용 민감도 분석 사전지정.
   - dose fidelity는 사실 개수 세기(검증된 측정, Hackenburg r=.87 방식 재사용), form fidelity는 분류기 + 인간 이중코딩 표본.

## 5. Estimation

- **Proximal excursion (primary)**: WCLS (known ρ). **Distal excursion**: DCEE 추정법 (§2.3 분리 참조).
- **정책가치 (secondary)**: cross-fitted DR, 사전지정 쌍만.
- 분산·다중비교: 사전지정 family에 대한 보정(방법은 pilot 후 확정). simultaneous confidence region은 **companion 과제로 강등**.

## 6. 강등된 확장 (본 논문 discussion 1단락씩만)

Generator transport Γ / GPI 내부표현 결합 / constrained policy learning / 동시추론 이론. 각각 후속 논문 후보.

## 7. 미해결 질문 (galley — 결정되면 §들로 승격)

1. R_t 측정의 reactivity: pilot에서 측정 유무 자체를 무작위화해 검증 (설계 확정, 파라미터 미정).
2. 1주 follow-up attrition의 estimand 처리: IPW-for-attrition 사전지정 예정, composite 여부 미정.
3. G^lock 구현 충실도: pilot 전 sandbox 테스트 (companion/platform_design_spec.md).
4. ~~reference policy 선택~~ → **해결됨(v0.2): ρ=균등 primary, 배치-기준 secondary.**
