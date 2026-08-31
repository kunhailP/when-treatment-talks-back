# Temperature-Indexed Overlap Collapse and Localization (v0.4)

> v0.4 (2026-07-30): 3차 비판 반영 — 수학적 명칭을 "Overlap Collapse and Localization"으로 확정("정보"는 해석 층위), Result 2의 n_eff를 arm-specific Kish로 교체, "τ 절반→n 제곱"의 성립 범위를 고정-gap 층으로 제한, 시뮬레이션의 이론 곡선 명칭을 "scaled inverse-propensity diagnostic"으로 정정.
> v0.3 (2026-07-29): **기존 Result 4("추정량이 경계 estimand로 수렴") 폐기·교체.** 고정 τ에서 IPW는 모집단 효과를 겨냥함(수치 확인 완료). 새 프레임: Result A(정보 한계의 지수 폭발, efficiency bound 수준) + Result B(overlap 정보의 경계 국소화, β^ov 별도 정의). 상세는 nonidentification_note.md. 이 파일의 Result 1–3, 5는 유지(스코프 명시), 구 Result 4 절은 아래와 같이 재작성.

Proposition 1A의 정성적 비식별을 "정량적 붕괴율"로 승격시키는 결과들. 논문 §3의 본체이자 시뮬레이션(src/temperature_collapse.py)과 실증 브리지(analysis/06–08)의 이론적 뼈대. **지위 표기 (v0.5 갱신): Result 1–3, 5 = Proposition 후보(증명 스케치 있음), Result B = Proposition (1-D 증명 완료 2026-07-30, nonidentification_note v0.5 · proofs_w3_draft §3; 다차원 coarea는 appendix). 구 Result 4는 폐기됨.**

---

## 0. 왜 이것이 필요한가

배치된 LLM의 행동 선택을 softmax로 모형화한다: π_τ(a|h) ∝ exp(u(a,h)/τ), 점수격차 Δ(h). τ>0인 한 positivity는 **형식적으로는** 성립한다. 그래서 정성적 주장만으로는 "IPW 쓰면 되잖아"에 반박이 안 된다. 필요한 것은 rate다. **스코프: 이하의 하한은 known-propensity IPW/Hájek 클래스에 관한 것이다 (formal_framework §3).**

## Result 1 — Propensity의 지수 붕괴
π_τ(a|h) ≤ exp(−Δ(h)/τ). (softmax 분모 하한에서 즉시.)

## Result 2 — 분산 하한과 유효표본 (턴 수준)
IPW 분산 기여 ≥ σ²_min·E[exp(Δ(H)/τ)] / n. 유효표본 (v0.4 교체): **n_eff(a) = n / E[1/π_τ(a|H)]** (arm-specific Kish; 구 표기 n·E[exp(−Δ/τ)] 폐기). **"τ 절반 → 필요 n 제곱"은 점수격차 고정 층 내부에서만 성립** — 층별 gap 이질 시 전체 rate는 최대 gap 층이 지배 (nonidentification_note Result A).

## Result 3 — 다턴 복리 붕괴 (**v0.5.2: Proposition A-T로 승격**)
구 heuristic E[W²] ~ exp(2TΔ̄/τ)는 정식 하한으로 대체됨: (M1) 고갭 집합의 행동-균등 재귀성 + (M2) + (A3) 하에서 **V_eff ≥ σ̲²·P₁(𝓗_δ)·p_δ^{T−1}·[exp(δ/τ)/K²]^T** (Kallus–Uehara 2020 유한기간 OPE bound + backward induction; 증명 = proofs_w3_draft §4). 상수(K² 인자)는 비최적, excursion 버전은 corollary.

## Result B — Overlap collapse and localization (구 Result 4 교체; "정보 국소화"는 해석 층위)
ω_τ(H)=p_τ(1−p_τ)로 정규화된 overlap 질량은 τ↓0에서 결정면 {Δ(H)=0}으로 집중된다. **추정량의 목표가 바뀌는 것이 아니라, 안정적으로 관측 가능한 인과정보가 경계로 집중되는 것**이며, 경계 효과는 β^ov로 별도 정의한다 (nonidentification_note Result B; Li–Morgan–Zaslavsky overlap weighting과 연결).

> Adaptive systems generate the least population-wide causal information where they are most decisive; the stable information that remains is concentrated near the policy's learned decision boundary.

정치적 함의(유지): 정책이 확신하는 층(강반발 당파층)에서 모집단 효과의 정보가 0으로 수렴한다.

## Result 5 — 식별의 가격 (지위 강등 v0.4.1: **design corollary / illustrative trade-off**)
ρ = (1−ε)π_τ + ε·Unif ⇒ 분산 ≤ σ²K/(nε). 목표 SE*에 필요한 최소 ε* ≈ σ²K/(n·SE*²); 탐색 비용은 턴당 ε(1−1/K)E[Δ regret]. **지위 (4차 비판 수용): 독립 기여·정식 정리가 아니다** — 이 형태의 bound에는 결과 상한/조건부 분산 상한, 추정량 종류, 단일/다턴, stabilized 여부 등의 조건이 필요하고 다턴 regret은 history transition으로 복잡해진다. 8월 JCI 논문에서는 G-MRT 절의 **예시적 트레이드오프 곡선**으로만 쓰고, 조건 명시 정식화는 후속. JCI 핵심 정리는 3개로 충분: support failure(1A) · efficiency-bound collapse(A) · overlap localization(B).

## 시뮬레이션과의 관계 (동일-객체 선언)

src/temperature_collapse.py의 DGP는 **이론과 같은 객체를 구현한다**: 배치 정책을 softmax(gap(d)/τ)로 두고, gap을 τ=1에서 기존 적응 정책(0.85/0.30)이 정확히 재현되도록 캘리브레이션했다(GAP_DEF=logit(0.85), GAP_REC=logit(0.30)). 따라서 시뮬레이션의 τ 축은 이론의 Δ/τ와 동일한 파라미터다. 검증된 예측: (P1) IPW SE의 지수 성장이 **scaled inverse-propensity diagnostic** 곡선(√(E[1/p]+E[1/(1−p)])에 최대-τ 지점에서 상수 캘리브레이션 — 진짜 efficiency bound가 아니라 진단 곡선임을 figure legend에 명시)과 일치, (P2) 유효표본·overlap 붕괴 — 지표 4종 구분 보고(2026-07-30): 전역 arm-specific Kish(이론 객체) / min cell occupancy(Kish 아님 — 희귀 crossover 진단) / E[p(1−p)](Result B 객체) / E[2min(p,1−p)](진단), (P3) naive는 τ↓에서 더 확신 있게 더 틀림(coverage conditional/unconditional 병기, zero-cell rate 동시 보고). **정정(2026-07-29): 극단 τ에서 경험 SD가 이론 하한 아래로 떨어지는 현상은 "국소화의 흔적"이 아니다 — 이 DGP는 이산 2-상태라 연속 결정경계 자체가 없다. 정확한 해석: 희귀 crossover가 표본에서 사라져 추정량이 편향된 채 안정돼 보이는 overlap collapse의 증거.** Result B 검증에는 연속 H 시뮬레이션 신설이 필요 (nonidentification_note TODO 3). 미구현 축: 라벨 측정오차, differential fidelity (W4).

## 실증 브리지 (analysis/06–08) — 인식론적 지위

재질의 실험이 추정하는 것은 **배치 정책의 조건부 엔트로피 / 유효온도의 proxy**다. 이는 Prop 1A나 Result A/B의 증명도, β 비식별의 증명도 아니다. 산출되는 "필요 대화 수"는 Result 2 공식에 실측 엔트로피를 대입한 **하한의 예시**이며, 논문과 발표에서의 역할은 G-MRT 설계의 필요성을 **동기화(motivate)**하는 것이다 — "종결한다"는 표현 사용 금지. 추가 주의: LLM judge 전략 분류 오차는 π̂을 왜곡할 수 있으므로(κ≥0.6은 발표용 기준), 핵심 수치에는 인간 이중코딩 표본과 민감도 범위를 함께 보고한다. DebateGPT rebuttal의 특수성(구조화 토론) 때문에 일반 배치(Hackenburg RM)로의 외삽에는 별도 논증이 필요하며, 이 간극은 Hackenburg fidelity audit(Study 0-c)가 메운다.

절차: 문맥 N≈200 추출 → 모델당 k≈20 재생성 → 전략 분류 → 문맥별 엔트로피/최빈 점유율 → Result 2 대입.

## 남은 이론 TODO (nonidentification_note와 동기화됨)

1. Result 2를 명시된 스코프(IPW/Hájek)의 정식 하한으로 — 또는 semiparametric bound로 상향 (JCI 트랙에서만)
2. Result B 라플라스 수렴 증명 → Conjecture에서 Proposition으로 승격 (연속 H 시뮬레이션과 함께)
3. Result 3 envelope 정리
4. 유효온도 τ의 식별: 재생성 실험으로 τ̂ 직접 추정 절차
