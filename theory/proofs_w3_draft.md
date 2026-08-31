# W3 증명 (v0.2 — 2026-07-30, 통합됨)

> **지위: 통합 완료.** 사용자 지시("JCI 쪽 진행")로 nonidentification_note v0.5에 요약 반영. 이 파일은 전체 증명 원문 보관용이며, 말미 위임 결정 3건은 재검토 가능.
> 검토 통과 시: 1A 반례쌍 → nonidentification_note Prop 1A 절, Result A → 동 문서 Result A 절,
> Result B → Conjecture에서 **Proposition으로 승격** (outline §4 라벨 갱신).
> 필요한 신규 인용: Hahn (1998, Econometrica) — ATE semiparametric efficiency bound.
> 연속 H 시뮬레이션(simulation/src/continuous_h.py, 2026-07-30)이 세 결과 모두와 정합:
> 위상도 국면 경계가 실선 log E[1/p_τ]을 따라감, overlap 추정량은 β^ov에 대해 전 τ 불편.

---

## 1. Prop 1A 반례쌍의 완전한 구성

**설정 (최소 구성, T=1).** H ∈ {h₀, h₁}, P(H=h₁) = q ∈ (0,1). 행동 A ∈ {0,1}.
배치 정책: π^dep(A=1|h₀) = 1/2, **π^dep(A=1|h₁) = 0** (이력-결정적 성분).
잠재결과: Y(a) | H=h ~ N(μ_a(h), 1).

**두 DGP.** k ∈ {1,2}에 대해 DGP_k는 다음만 다르다:
μ₁^{(1)}(h₁) = c₁, μ₁^{(2)}(h₁) = c₂, c₁ ≠ c₂. 나머지 (P(H), π^dep, μ₀(·), μ₁(h₀)) 동일.

**관측분포 동일성.** 관측자료 (H, A, Y)의 결합분포는
P(H=h)·π^dep(A=a|h)·N(y; μ_a(h), 1)로 인수분해되는데, (a,h)=(1,h₁) 층은
π^dep(1|h₁)=0이라 결합분포에 **기여하지 않는다**. 따라서 두 DGP의 관측분포는 동일하다. ∎

**Estimand 불일치.** 균등 reference ρ 하의 excursion effect는
β = E_H[μ₁(H) − μ₀(H)] = (1−q)[μ₁(h₀)−μ₀(h₀)] + q[μ₁(h₁)−μ₀(h₁)]
이므로 β^{(2)} − β^{(1)} = q(c₂ − c₁) ≠ 0. 같은 관측분포, 다른 β → 비모수 비식별. ∎

**주 (U의 역할).** 위 구성은 미관측 U 없이도 성립한다 — 실패의 원천은 교란이 아니라
**support**다. nonidentification_note의 스케치가 U를 언급한 것은 다턴 버전(π^dep가
이력을 통해 과거 반응에 의존 → time-varying confounding과 결합)을 향한 것인데,
반례 자체는 최소 구성이 더 깨끗하다. 다턴 확장: H를 H_t = (X, R_{1:t−1})로 읽고
π^dep_t(a|h)=0인 (a,h) 층에 같은 논증을 적용하면 된다 (g-formula의 해당 적분 항 미정의).

**LLM 관련성 (v0.4 문구 유지).** 이 구조는 Robins(1986) 이래 표준. 본 논문의 주장은
저온 softmax 배치에서 π^dep(a|h) = σ(Δ(h)/τ) → 0이 **구조적으로 빈번**하고
(τ↓, RLHF가 Δ를 확대), 수치 0이 아니어도 Result A의 rate 문제가 이미 발생한다는 것.

---

## 2. Result A — (A1)–(A3) 하의 정식 하한

**정리 (초안).** 조건: (A1) P(𝓗_δ) > 0, 𝓗_δ = {h: |Δ(h)| ≥ δ};
(A2) σ̲² = inf_{h∈𝓗_δ, a} σ_a²(h) > 0;
(A3) outcome regression μ_a(·)가 비제약인 비모수 모델 클래스.
2-행동 softmax 정책 p_τ(h) = σ(Δ(h)/τ) 하에서, ATE형 excursion의
semiparametric efficiency bound V_τ는

  V_τ ≥ σ̲² · P(𝓗_δ) · exp(δ/τ).

**증명.** (A3) 클래스에서 ATE의 efficiency bound는 (Hahn 1998)
V_τ = E[ σ₁²(H)/p_τ(H) + σ₀²(H)/(1−p_τ(H)) + (β(H) − β)² ].
마지막 항 ≥ 0을 버리고 𝓗_δ로 제한하면
V_τ ≥ E[ 1_{𝓗_δ}(H) · σ̲² · ( 1/p_τ(H) + 1/(1−p_τ(H)) ) ]
    ≥ σ̲² · E[ 1_{𝓗_δ}(H) / min(p_τ(H), 1−p_τ(H)) ].
𝓗_δ 위에서 |Δ(H)| ≥ δ이므로 min(p_τ, 1−p_τ) = σ(−|Δ|/τ) ≤ exp(−δ/τ), 즉
1/min ≥ 1 + exp(δ/τ) ≥ exp(δ/τ). 따라서 V_τ ≥ σ̲² P(𝓗_δ) exp(δ/τ). ∎

**함의 문장 (논문용).** convolution theorem에 의해 (A3) 클래스의 **어떤 정규(regular)
추정량도** 점근분산이 V_τ 미만일 수 없다 — "AIPW로 바꿔도 복구되지 않는다"의 정확한 형태.
파라메트릭 외삽은 (A3)를 깨는 것이므로 하한을 피할 수 있으나, 그것은 식별을 가정으로
사는 것이다.

**스코프 주의.** (i) 2-행동 케이스로 서술 — K-행동은 해당 대비에 관여하는 두 팔의
propensity로 동일 논증. (ii) 이 하한은 τ 고정의 점근 분산에 관한 것이고, 유한표본
편향-안정 국면은 위상도(반례 절)가 담당한다 — 두 주장을 섞지 않는다.

---

## 3. Result B — 1-D 정리 (변수변환 + approximate identity)

**정리 (초안, unique root).** 조건:
(B1) H ∈ ℝ, 연속밀도 f; (B2) Δ ∈ C¹, 유일한 root r=0이 simple (Δ(0)=0, Δ′(0)≠0),
그리고 **(B2′) 모든 ε>0에 대해 inf_{|h|≥ε} |Δ(h)| > 0**;
(B3) f와 c(h) := E[Y(1)−Y(0)|H=h]가 0 근방에서 연속, c는 유계;
(B4) f(0) > 0.
그러면 τ↓0에서:
(i) 정규화 측도 ν_τ(dh) = ω_τ(h)f(h)dh / ∫ω_τ f 는 δ₀로 약수렴;
(ii) E[ω_τ] = τ·[f(0)/|Δ′(0)|]·(1 + o(1)) — overlap 질량은 τ에 선형으로 소멸;
(iii) β^ov_τ → c(0) = E[Y(1)−Y(0)|H=0].

**증명.**
핵심 항등식: ω_τ(h) = p_τ(1−p_τ) = 1/[4cosh²(Δ(h)/2τ)]. K(u) := 1/[4cosh²(u/2)]로
두면 K ≥ 0, ∫_ℝ K(u)du = [½tanh(u/2)]_{−∞}^{∞} = 1 — approximate identity kernel.

임의의 유계 연속 g에 대해 I_τ(g) := ∫ g(h) K(Δ(h)/τ) f(h) dh를 분해한다.

*(tail)* (B2′)에 의해 |h| ≥ ε에서 |Δ| ≥ c(ε) > 0이므로 K(Δ/τ) ≤ e^{−c(ε)/τ}
(cosh²(x/2) ≥ e^{|x|}/4). 따라서 tail 기여 ≤ ‖g‖_∞ e^{−c(ε)/τ} — 어떤 τ 거듭제곱보다
빠르게 소멸.

*(local)* Δ′(0) ≠ 0이므로 역함수 정리에 의해 어떤 ε>0에서 Δ: (−ε,ε) → Δ((−ε,ε))는
C¹ 미분동형. v = Δ(h) 변수변환 후 v = τu:
∫_{|h|<ε} g K(Δ/τ) f dh = τ ∫ K(u) · [(g·f)/|Δ′|](Δ⁻¹(τu)) · 1_{τu ∈ Δ((−ε,ε))} du.
피적분함수는 K(u)·sup_{|h|≤ε}|gf/Δ′|로 지배되고(적분가능), τ↓0에서 각 u마다
[(g·f)/|Δ′|](Δ⁻¹(τu)) → g(0)f(0)/|Δ′(0)| (연속성). 지배수렴에 의해
I_τ(g) = τ · g(0)f(0)/|Δ′(0)| + o(τ).

g ≡ 1로 (ii). 비율 I_τ(g)/I_τ(1) → g(0)로 (i) (약수렴의 정의). g = c로 (iii)
(β^ov_τ = I_τ(c)/I_τ(1); c의 유계·0-근방 연속이면 충분). ∎

**Corollary (multiple roots).** root {r_j}가 유한 개이고 각각 simple이면, 같은 분해로
ν_τ → Σ_j w_j δ_{r_j}, w_j = [f(r_j)/|Δ′(r_j)|] / Σ_k [f(r_k)/|Δ′(r_k)|],
β^ov_τ → Σ_j w_j c(r_j). (각 root에 국소화 논증을 적용하고 tail은 (B2′)의 자연 확장.)

**다차원 (appendix 지위 유지).** H ∈ ℝ^d, {Δ=0}이 정칙 초곡면이면 coarea 공식으로
ν_τ → {Δ=0} 위 f/|∇Δ| 비례 surface measure — v0.4.1 합의대로 appendix proposition
또는 conjecture로만 (본문 정리로 만들지 않는다).

**검증 (수치, 2026-07-30).** continuous_h.py: U(−1,1), Δ(H)=H, β(H)=1+|H|에서
β^ov_{τ=0.045} = 1.062 → c(0) = 1 방향 수렴 ✓; overlap mass의 τ-선형 소멸 ✓;
overlap 추정량은 전 τ에서 β^ov에 불편·명목 coverage ✓ ("경계 정보는 안정" 해석과 정합).

---

## 4. Result A-T — 다턴 복리 하한 (v0.3 신규, 2026-07-30: Result 3 heuristic의 Proposition 승격)

**설정.** T턴, 각 턴 행동 A_t ∈ {1,…,K}, 이력 H_t (H_1 ~ P_1), 로깅(배치) 정책
π_τ(a|h), 목표는 reference 정책 ρ (균등: ρ(a|h)=1/K)의 정책가치
V(ρ) = E_ρ[Y] (Y는 종결 결과). 관측자료는 π_τ 하의 trajectory.

**인용하는 기지 결과.** 유한기간·이력의존(NMDP) off-policy 평가의 semiparametric
efficiency bound (Kallus & Uehara 2020; 유한기간 형태는 Jiang & Li 2016의 EIF와 동일):

  V_eff = Var(V_1(H_1)) + Σ_{t=1}^{T} E_π[ (Π_{s=1}^{t} w_s)² · Var(V_{t+1} | H_t, A_t) ],

여기서 w_s = ρ(A_s|H_s)/π_τ(A_s|H_s), V_{t+1}은 ρ 하의 value function,
Var(V_{T+1}|H_T,A_T) = Var(Y|H_T,A_T) = σ²(H_T,A_T).

**추가 조건.**
- (M1) **고갭 집합의 균등 재귀성**: 𝓗_δ = {h: 최대 점수격차 ≥ δ}에 대해, 모든
  h ∈ 𝓗_δ, 모든 a에서 P(H_{s+1} ∈ 𝓗_δ | H_s = h, A_s = a) ≥ p_δ > 0.
  (행동에 균등해야 함 — 행동 선택이 조건화를 깨지 않도록.)
- (M2) 𝓗_δ 위 조건부 분산 하한: σ²(h,a) ≥ σ̲² (A2의 턴별 버전).
- (A3) 비모수 클래스 (동일).

**Proposition A-T (진술).** (M1)–(M2), (A3) 하에서

  V_eff ≥ σ̲² · P_1(𝓗_δ) · p_δ^{T−1} · [exp(δ/τ) / K²]^{T}.

특히 τ < δ / log(K²/p_δ)이면 하한은 T에 대해 **기하급수적으로 복리**된다 —
구 Result 3의 E[W²] ~ exp(2TΔ̄/τ) heuristic이 efficiency bound 수준의
정식 하한으로 대체된다 (지수는 Tδ/τ − T·log(K²/p_δ)).

**증명 (backward induction).** V_eff의 모든 항이 비음이므로 t = T 항만 남긴다:

  V_eff ≥ E_π[ (Π_{s=1}^{T} w_s)² σ²(H_T, A_T) ]
        ≥ σ̲² · E_π[ Π_{s=1}^{T} w_s² · 1(H_1 ∈ 𝓗_δ, …, H_T ∈ 𝓗_δ) ].

핵심 계산: h ∈ 𝓗_δ에서 π_τ의 최희귀 행동 a*(h)는 π_τ(a*|h) ≤ exp(−δ/τ)이므로

  E_π[ w_t² | H_t = h ] = Σ_a π_τ(a|h) · ρ(a|h)²/π_τ(a|h)²
                        = (1/K²) Σ_a 1/π_τ(a|h) ≥ (1/K²) exp(δ/τ).   (★)

t = T부터 후진 귀납: tower property로

  E[ w_T² 1(H_T ∈ 𝓗_δ) | H_{T−1}, A_{T−1} ]
    = E[ 1(H_T ∈ 𝓗_δ) · E[w_T²|H_T] | H_{T−1}, A_{T−1} ]
    ≥ p_δ · (1/K²) exp(δ/τ)      (H_{T−1} ∈ 𝓗_δ일 때, (M1)+(★))

이고, 이 하한이 (M1)의 행동-균등성 덕분에 A_{T−1}에 의존하지 않으므로 앞 턴의
w_{T−1}²와의 곱에 그대로 통과한다. 같은 단계를 t = T−1, …, 2에 반복하면 각 턴이
인자 p_δ·exp(δ/τ)/K²를 기여하고, 마지막 턴 t = 1은 (★)과 P(H_1 ∈ 𝓗_δ) = P_1로
인자 P_1 · exp(δ/τ)/K²를 기여한다. 곱하면 진술의 하한. ∎

**정직성 주석.** (i) 인용한 V_eff 공식 자체의 자기완결 유도(EIF 계산)는 appendix
TODO — 본 증명은 그 공식 위의 초등 부등식·귀납이다. (ii) (M1)은 실질 가정이다:
"어떤 행동을 하든 다음 이력이 고갭 층에 남을 확률이 균등히 양수" — 강반발
사용자층의 지속성 같은 실질 서사와 대응하며, 논문에서는 이 가정의 해석을 한
문단으로 밝힌다. (iii) 하한의 K² 인자는 균등 ρ의 보수성에서 오며 open — 상수
최적화는 하지 않는다. (iv) excursion 버전(턴 t 대비, 이후 ρ)은 t 이후 턴의
교량만 남기는 같은 논증으로 지수 T−t+1을 얻는다 (corollary).

**신규 인용**: Kallus & Uehara (2020, JMLR) — double reinforcement learning /
finite-horizon OPE efficiency bound; Jiang & Li (2016, ICML) — doubly robust OPE의 EIF.

---

## 남은 검토 포인트 (사용자 판단 필요)

1. (B2′)는 기존 (B1)–(B4)에 없던 **추가 정칙조건**이다 (unbounded support에서 tail
   차단용; U(−1,1)·N(0,1) 주/robustness DGP 모두 충족). nonidentification_note의
   조건 목록에 추가할지, compact support로 제한할지 결정 필요.
2. Result A 증명이 Hahn(1998) bound를 인용 형태로 쓴다 — 자기완결 증명(influence
   function 유도)을 appendix에 둘지 여부.
3. 1A 반례에서 U 없는 최소 구성을 본문으로, U-매개 다턴 버전을 remark로 두는 배치가
   nonidentification_note의 기존 서술("U가 (i) H를 통해…")과 다르다 — 문서 쪽을
   최소 구성으로 교체할지 결정 필요.
