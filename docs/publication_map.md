# Publication Map — 두-논문 분리 (v1, 2026-07-30)

> 3차 비판 수용으로 신설. framework v0.4 §0의 두-논문 구조를 실행 수준으로 잠근다. **한 결과는 정확히 한 논문에 속한다** — 겹치면 JCI가 우선하고 PA는 인용한다.

## Paper 1 — JCI (몸통, 8/26 arXiv v1)

**가제**: When the Treatment Talks Back: Information Limits of Observational Logs from Adaptive Generative Political Communication
**타깃**: Journal of Causal Inference (가을 2026) · 대안 PSRM · stretch PA(methods note)

**기여 잠금 (3개, 추가 금지)**
- J1. 생성형 처치 (π, G, E)의 estimand 정식화 — **일반 적응 생성 행동공간 A_t ∈ 𝒜** (이산 전략·연속 생성 파라미터·form×dose는 특수사례), deployment/policy/turn-level excursion, 커널 개입, ill-defined treatment (framework §1–2). 의료 챗봇·교육·상담·정치대화에 공통 적용되는 일반 방법론으로 서술; **2×2는 running example로만**
- J2. Temperature-indexed overlap collapse and localization — Prop 1A(반례쌍) + Result A(조건 (A1)–(A3), Kish n_eff) + Result B(β^ov, 1-D Laplace) + 반례(고정 τ target 불변) + (n,τ) 위상도
- J3. 설계 처방 — G-MRT를 정보 한계의 해법으로 제시 (Result 5는 **illustrative trade-off/design corollary 지위**로만 포함 — 독립 정리 아님; 실증은 Paper 2 예고)

**증거 자산**: simulation.py(부호 반전) · temperature_collapse.py(P1–P3) · 연속 H 배터리 + 위상도(W4) · Study 0-a/b(동기화 지위)

## Paper 2 — PA (참가자·펀딩 확보 후)

**가제**: The G-MRT: Micro-Randomizing Generative Political Persuasion
**타깃**: Political Analysis · 대안 AJPS(letter) — 실험 결과가 본체

**기여 잠금 (3개)**
- P1. 대화 내 턴별 2×2(form × dose) micro-randomization 프로토콜 — **2×2가 이 논문의 중심 실험 객체** (JCI의 일반 𝒜를 정치설득에 구현), evidence bank 잠금(≥20 fact units), gated kernel G̃, 배정-ITT
- P2. β^form, β^dose, β^form×dose의 proximal(WCLS)/distal(DCEE) 추정 + 직전 반발 moderation
- P3. Generated-treatment fidelity 방법론 — 차별 비순응 감사, 게이트 오차 민감도, fidelity ≥80%/셀 규약

**표본 (현실화, 3차 비판 수용)**: pilot n=80–120 (기능 검증: 배정 작동·fidelity·bank 누출·dropout·분산 — 효과 발견 아님) → PA demo n=180–250 (사전등록 소수 대비) → confirmatory는 power sim 후 별도.

**증거 자산 (PA 트랙 전용)**: 2×2 form×dose DGP · WCLS 추정기 · differential fidelity 시뮬 · 플랫폼(platform/design_spec) · pilot_prereg

## 자산 배분 규칙

| 자산 | 트랙 |
|---|---|
| Prop 1A, Result A/B, 반례, 위상도, 연속 H 시뮬, 라벨 오차 축 | JCI |
| temperature_collapse.py, simulation.py | JCI |
| Study 0-a/b/c (동기화 지위) | JCI (§4 동기화 + PA의 design 근거로 재인용) |
| 2×2 DGP, WCLS 코드, differential fidelity, prereg, platform | PA |
| transport Γ, GPI, 동시추론, policy learning | 어느 쪽도 아님 (후속) |

## 일정 상호작용

8/26 arXiv v1 = JCI-형 working paper (G-MRT는 §5). JCI 투고 시 PA companion을 "in preparation"으로 인용. PA는 pilot 데이터 확보 전 투고하지 않는다.
