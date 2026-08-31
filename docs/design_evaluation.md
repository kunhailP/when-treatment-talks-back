# 연구 설계 평가서

**When the Treatment Talks Back: Design-Based Causal Inference for Adaptive Generative Political Communication**

평가일: 2026-07-22 · 평가 목적: PA(Political Analysis)급 방법론 논문으로서의 기여 가능성, 식별 논리의 정합성, 실행 가능성 진단

---

## 총평

핵심 아이디어 — "생성형 AI 정치대화의 처치는 고정 텍스트가 아니라 (전략정책 π, 생성모델 G, 정보환경 E)의 결합인 확률적 동적 정책이다" — 는 실제로 좋은 estimand-first 기여이고, 문헌의 공백에 정확히 위치한다. Imai & Nakamura (JASA 2026)는 정적 텍스트 처치까지만 다루고, MRT 문헌(Qian et al. 2022)은 행동이 미리 정의된 이산 개입임을 전제한다. 그 사이 — "행동 자체가 매번 확률적으로 생성되는 자연어이고, 선택이 사용자 반응에 적응하는" 경우 — 는 아직 아무도 정식화하지 않았다. Hackenburg et al. (Science 2025)과 Chen, Kalla & Le (2026)의 결과는 이 estimand가 실무적으로도 필요함을 보여준다(모델·프롬프트에 따라 설득효과의 방향까지 달라짐 → policy와 generator를 분리해야 함).

그러나 현재 설계안에는 **논문의 생사를 가를 4개의 취약점**과 **실행상 과부하 1개**가 있다. 아래 순서는 심각도순이다.

---

## 1. "Strategy Non-Identification Theorem"은 현재 형태로는 정리가 아니다 (치명적, 그러나 고칠 수 있음)

시스템 단위 무작위화 하에서 턴별 전략효과가 식별되지 않는다는 주장은, 그 자체로는 **Robins (1986) 이래 알려진 time-varying confounding의 표준 사례**다. 전략 S_t가 이력 H_t(사용자 반응 포함)의 함수이고 H_t가 결과와 연관되면, S_t 조건부 비교는 post-treatment conditioning이다. PA 심사자는 이걸 "새 정리"로 제시하는 순간 논문 전체의 novelty를 의심하기 시작한다.

**살리는 방법**: 비식별의 *이유*를 더 정밀하게 쪼개면 실제로 새로운 내용이 나온다.

- (a) **Confounding 경로**: H_t가 관측되면 원칙적으로 g-formula로 조정 가능. 이건 표준.
- (b) **Positivity 위반 경로**: 배치된 LLM의 전략 선택은 이력에 대해 사실상 결정적(deterministic-in-history)이다. 온도가 있어도 특정 이력에서 특정 전략의 선택확률이 0에 수렴한다. 이 경우 **H_t를 완벽히 관측하고 전략 라벨을 완벽히 코딩해도** 식별이 실패한다. 이것이 "transcript 사후분석은 원리적으로 안 된다"의 정확한 형식적 근거이고, LLM이라는 대상 특유의 문제다(모바일헬스 MRT 문헌에는 이 형태가 없다 — 그쪽은 애초에 randomization을 전제하니까).
- (c) **처치 정의 실패 경로**: 전략 라벨이 관측되어도 실제 처치는 M_t ~ G(·|S_t, H_t)의 실현이며, G가 이력을 조건으로 하므로 같은 라벨이 이력마다 다른 처치분포를 의미한다. consistency/SUTVA 차원의 문제로, 라벨 기반 사후분석이 "무엇의 효과"를 추정하는지 자체가 미정의됨.

(b)+(c)를 묶어 "Proposition 1: 시스템 단위 무작위화 + 완전한 transcript 관측 하에서도 turn-level 전략효과는 (i) positivity 위반과 (ii) 처치분포의 이력의존성 때문에 비식별"로 쓰면, 표준 결과의 재진술이 아니라 **LLM 대화라는 새로운 대상에서 비식별의 구조를 분해한 결과**가 된다. 그리고 이 구조가 곧바로 G-MRT 설계의 각 요소(ρ_t > ε 보장 = positivity 복원, 전략 무작위화 = confounding 차단, information-lock = 처치 정의 고정)를 정당화한다. 정리→설계가 1:1로 대응되는 이 구조가 논문의 뼈대가 되어야 한다.

## 2. Information Equivalence와 Treatment Integrity는 트레이드오프다 — "해결"이 아니라 "선택"임을 인정해야 함 (치명적)

설계안은 Dafoe, Zhang & Caughey (2018)를 인용해 모든 전략 조건에 동일한 evidence bank를 잠그면 정보 등가성이 확보된다고 본다. 그러나:

- Socratic questioning은 **구조적으로 정보를 덜 전달하는 전략**이다. 질문은 주장을 하지 않는다. "같은 사실, 같은 개수, 같은 길이"를 강제하면 질문 전략은 더 이상 질문 전략이 아니게 된다(조작 파괴).
- 더 아픈 사실: Hackenburg et al.의 핵심 발견이 바로 **정보 밀도가 설득의 주요 지렛대**라는 것이다. 정보를 잠그면 전략 간 차이의 가장 큰 원천을 제거한 뒤 남는 잔차(수사적 형식)의 효과를 추정하게 된다. 그 효과는 작을 것이고, 파워 문제가 뒤따른다.

**살리는 방법**: 이걸 결함이 아니라 estimand의 선택 문제로 명시적으로 정식화하라. 두 estimand를 구분해 정의하면 된다.

- **Form effect** (information-locked): 전달되는 사실 집합을 고정했을 때 수사적 형식의 효과. 작지만 해석이 깨끗함.
- **Bundle effect** (information-free): 전략이 자연스럽게 수반하는 정보량 차이까지 포함한 효과. 크지만 "전략"과 "정보"가 섞임.

실험은 information-locked를 primary로 하되, 실현된 메시지의 정보 밀도·사실 개수·길이를 사후 측정해 **realized-content audit**을 manipulation check로 보고한다. "우리는 form effect를 추정하며, bundle effect와의 차이가 곧 정보 매개분이다"라고 쓰면 심사자 공격이 기여로 바뀐다.

## 3. Turn-level 식별의 novelty 과장 — 방법론적 신규성은 다른 곳에 있다 (중요)

전략 S_t를 알려진 확률로 무작위화하면, 문장 M_t ~ G(·|S_t, H_t)의 확률적 실현은 형식적으로는 그냥 결과생성과정의 일부다. 즉 **turn-level causal excursion effect의 식별과 WCLS 추정은 기존 MRT 이론(Boruvka et al. 2018; Qian et al. 2022)이 이미 커버한다.** "생성형이라 새로운 식별이론이 필요하다"고 쓰면 반례를 맞는다.

실제로 새로운(그래서 논문이 힘을 실어야 할) 방법론적 문제는 세 개다.

- (a) **구현 충실도/거부(refusal)**: 배정된 전략이 safety filter나 모델 거부로 구현되지 않으면 턴 수준 noncompliance다. 배정을 도구변수로 한 turn-level ITT vs per-protocol, 그리고 fidelity 모니터링 설계 — MRT 문헌에 정식화가 얇은 부분.
- (b) **Generator transport**: 처치커널 G_a → G_b 교체 시 정책가치의 안정성. 이건 "처치분포 자체의 distribution shift"라는, 기존 transportability 문헌(공변량 shift 중심)과 다른 구조다. 진짜 새 문제 맞음.
- (c) **다중 전략×턴×집단×결과에 대한 동시추론**: max-t/multiplier bootstrap 기반 simultaneous confidence region. 네 기존 강점과 접속되는 지점.

**권고**: Section 구성을 "식별은 설계가 해결(기존 이론 활용을 명시) → 신규 기여는 (a)(b)(c)"로 재배치. 겸손한 곳에서 겸손하고 새로운 곳에서 새로움을 주장하는 논문이 심사를 통과한다.

## 4. 정책가치 추정의 파워 문제 (중요)

전략 4개 × 3턴이면 결정적 정책의 시퀀스 공간이 4³ = 64. 특정 대안 정책 π의 V(π)를 IPW로 추정하면 importance weight가 턴별 확률의 곱(균등 무작위화면 4³ = 64배)이라 분산이 폭발한다. n = 1,500–2,500에서 쟁점 3–4개·하위집단까지 자르면 정책가치 비교는 사실상 파워가 없을 가능성이 높다.

**권고**:

- Primary 추정대상을 **turn-level excursion effect**(이력 전체에 대해 풀링되므로 파워 양호)로 두고, 정책가치 비교는 2–3개의 사전지정 정책 쌍으로 제한.
- DR 추정과 cross-fitting으로 분산을 줄이되, pilot에서 effect size와 ICC를 재고 **power simulation을 confirmatory 설계의 전제조건**으로 명시(현재 계획에도 있으나, "파워가 안 나오면 정책가치 비교를 포기하고 excursion effect만 사전등록한다"는 fallback까지 써야 함).
- 전략 4개가 아니라 **첫 실험은 2–3개**로 시작하는 것도 진지하게 고려. 대비되는 전략 2개(직접 교정 vs 소크라테스식)의 깨끗한 비교가 4개의 노이즈보다 논문에 유리하다.

## 5. 실행 범위: 5주 안에 다 못 한다 (실행상 치명적)

7/22 기준 8/26까지 5주. 제시된 산출물(working paper 20–25쪽, Study 0 재분석, 시뮬레이션 패키지, 플랫폼 프로토타입, preregistration, IRB 초안, repo)은 풀타임 연구자 기준으로도 과하다. 전부 벌리면 전부 미완성이 된다.

**권고 우선순위** (발표의 설득력 기준):

1. **P0 — formal framework + Proposition 1** (theory/): 논문의 심장. 이것 없이는 나머지가 응용 리포트.
2. **P0 — 시뮬레이션** (simulation/): response-adaptive confounding의 편향을 그림 한 장으로 보여주는 것. 발표 임팩트 최대.
3. **P1 — Study 0: DebateGPT 재분석** (analysis/): 전략 선택의 반응 의존성(adaptive selection)을 실데이터로 보여주면 Proposition 1의 실증적 동기가 됨. 재현은 핵심 계수 2–3개만.
4. **P1 — working paper 10–15쪽** (paper/): 20–25쪽 욕심 버리기. Intro–setup–proposition–design–simulation이면 충분.
5. **P2 — pilot preregistration 골격** (preregistration/): 템플릿 수준.
6. **P3 — 플랫폼 프로토타입, IRB**: 세션 이후(9월)로 이연. 발표에는 design spec 문서로 대체.

Section 8의 epistemically constrained policy learning은 **그 자체로 두 번째 논문**이다. 이번 논문에는 discussion 한 단락으로만 남기고 잘라내는 것을 강하게 권고.

## 6. 기타 지적사항

- **모델 스냅샷 재현성**: API 모델은 deprecate된다. generator transport 실험은 최소 한 축을 open-weights 모델(예: Llama 고정 체크포인트)로 두어야 재현 가능성 주장이 성립. 프롬프트·모델 버전·디코딩 파라미터의 manifest를 repo에 커밋할 것.
- **전략 annotation의 측정오차**: Study 0에서 LLM으로 전략을 코딩하면 측정오차가 대화 내용과 상관될 수 있음. 인간 이중코딩 표본(예: 200턴)으로 신뢰도(κ)를 보고하고, Study 0의 모든 결과에 "기술적(descriptive)" 라벨을 명시.
- **결과변수**: belief accuracy + calibration + 1주 retention 구성은 좋다. 다만 1주 follow-up의 attrition이 정책과 상관될 수 있음(불쾌한 대화 → 이탈). missingness를 estimand 정의에 포함하거나(composite), IPW-for-attrition을 사전지정할 것.
- **윤리 프레임**: 오정보 교정 도메인 선택은 옳다. Costello, Pennycook & Rand (Science 2024)가 선례. 단 "교정 방향이 참"임을 보증하는 evidence bank의 fact-check 절차를 프로토콜에 명문화해야 IRB와 심사 양쪽에서 방어됨.
- **세미나 5편 선정**: 2차안(Hackenburg/Salvi/Imai&Nakamura/Qian/Dafoe)이 1차안보다 명백히 우수. 각 논문이 최종 논문의 한 구성요소를 담당하는 구조도 좋음. Zeng et al.과 Tierney et al.은 보조문헌으로 강등하는 것에 동의(Zeng은 비판 대상, Tierney는 design-based 정신의 방증).

## 7. 서지 검증 결과 (2026-07-22 웹 확인)

| 논문 | 상태 | 비고 |
|---|---|---|
| Hackenburg et al. | **Science 게재 확정** (2025.12, DOI 10.1126/science.aea3884) | 코드: github.com/kobihackenburg/scaling-conversational-AI |
| Salvi et al. 2025 | Nature Human Behaviour 게재 | 데이터: huggingface.co/datasets/frasalvi/debategpt, 코드: github.com/epfl-dlab/debategpt (분석·전략추출 스크립트 포함) |
| Imai & Nakamura | **JASA 게재 확정** (2026, DOI 10.1080/01621459.2026.2689629) | 소프트웨어: gpi-pack (GenAI-Powered Inference) |
| Qian et al. | Psychological Methods 2022 (arXiv 2107.03544) | 인용연도 2021→2022로 수정 필요 |
| Dafoe, Zhang & Caughey 2018 | Political Analysis 26(4) | 확인 |
| Tierney et al. 2025 | arXiv 2510.08758 (미게재 preprint) | 저자: Tierney, Katta, Bail, Hillygus, Volfovsky |
| Zeng et al. 2025 | arXiv 2503.16544 + Behaviour & Information Technology 게재 | PersuasionForGood 데이터 사용 |
| Chen, Kalla & Le 2026 | arXiv 2603.09884 (preprint) | "et al./alphabetical" — 저자 3인: Zhongren Chen, Joshua Kalla, Quan Le; n=19,145 |
| Bai et al. 2025 | Nature Communications 16 (s41467-025-61345-5) | 확인 |
| Matz et al. 2024 | Scientific Reports 14:4692 | 확인 |
| Costello et al. 2024 | Science 385 (durably reducing conspiracy beliefs) | 확인 |

## 결론

이 설계는 "적응형 LLM 설득 실험"이라는 응용 아이디어를 넘어, **생성형 처치의 인과추론이라는 방법론적 프레임**으로 발전할 잠재력이 실제로 있다. 단, (1) 비식별 결과를 positivity + 처치정의 실패로 재정식화하고, (2) 정보등가성-조작충실성 트레이드오프를 estimand 선택으로 명시화하고, (3) 신규성 주장을 fidelity/transport/동시추론으로 옮기고, (4) 파워 현실에 맞게 전략 수와 정책 비교를 줄이고, (5) 5주 산출물을 P0–P1으로 자르는 다섯 가지 수정이 선행되어야 한다. 이 수정을 반영한 형식화가 `theory/formal_framework.md`에 있다.
