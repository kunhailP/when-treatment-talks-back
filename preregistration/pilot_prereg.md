# Pilot G-MRT Preregistration 골격 (v0.4 — 2026-07-30, PA 트랙)

> 기준: theory/formal_framework.md v0.4 · 두-논문 경계: docs/publication_map.md (이 문서는 **PA 트랙** 소속). 충돌 시 framework를 따른다.

## 1. 연구질문
정치적 오정보 교정 대화에서 턴별 **form(단언 vs 질문) × dose(고정보 vs 저정보 패키지)** 배정의 proximal·distal excursion 효과는 무엇이며, 직전 반발 상태에 따라 조절되는가?

## 2. 설계
- **표본 (v0.4 현실화)**: pilot n = 80–120 (Prolific, 미국 성인, 당파 층화) — 목적이 기능 검증이므로 이 규모로 충분 · **PA demo 단계 n = 180–250** (사전등록 소수 대비) · confirmatory 표본은 pilot 분산 기반 power sim 후 별도 결정 (구 표기 300–500은 pilot 규모로는 과대, confirmatory 규모로는 미정 상태였음 — 폐기)
- 쟁점 2개 · T = 3턴 · **쟁점 사용 규칙 (v0.4.1)**: pilot에서는 issue-specific treatment effect를 추정하지 않는다 — **issue는 blocking factor로만** 사용 (쟁점당 40–60명은 효과 추정에 불충분). demo(180–250)에서도 primary는 form·dose main effect의 **pooled 추정 + issue fixed effect**이며, issue별 효과·issue×treatment 상호작용은 exploratory로 사전지정.
- **턴별 2×2 균등 무작위화** (ρ = 각 셀 1/4, 모든 이력에서) · generator 1–2개 (최소 한 팔 open-weights)
- Evidence bank: 쟁점당 fact unit ≥20, 턴별 서브뱅크/비복원 sampling 규칙 명시 (framework §4.3)
- Fidelity 게이트 = 생성커널 G̃의 일부 (framework §4.4)
- pilot 1차 목적: 효과 발견이 아니라 배정 작동·fidelity·bank 누출·dropout·분산 측정

## 3. Estimands (사전지정)
- **Primary (proximal)**: β_t^form, β_t^dose — ITT(배정 기준), 턴 풀링 WCLS (known ρ)
- **Secondary**: β_t^{form×dose} 상호작용 · 직전 반발 조절 · **distal excursion(최종 accuracy·1주 retention)은 DCEE 추정법으로** (일반 WCLS 금지)
- 정책가치 비교는 confirmatory로 이연 · ~~simultaneous CI primary~~ → **companion 과제로 강등(v0.3)**, pilot은 사전지정 소수 대비 + 표준 보정만

## 4. 결과변수 (proximal/distal 분리)
- Proximal (턴 직후): reactance, perceived respect/informativeness, 즉시 belief update, 지속 여부
- Distal (종료 시): belief accuracy, 확신도, AI 신뢰 / (1주 후): retention, 태도 지속, 출처 회상

## 5. Fidelity·제외·결측 규칙
- **fidelity 하한: 셀당 ≥80%** — 미달 셀이 있으면 해당 대비를 exploratory로 강등 (사전지정)
- form fidelity: 분류기 + 인간 이중코딩 / dose fidelity: 사실 개수 카운트 (r=.87 방식)
- 게이트 미적용 민감도 분석 사전지정 · 대화 중단은 I_t로 처리 · attrition은 IPW-for-attrition

## 6. 윤리
즉시 종료권·전액 보상 · evidence bank fact-check 문서 첨부 · debrief에 무작위화 고지 · IRB [기관/번호]

## 7. Power
Hackenburg 사전정보(효과 2–4pp 스케일) + Costello(교정 도메인 d≈0.8–1.1) 기반 시뮬레이션으로 confirmatory 표본 결정. 파워 미달 대비의 fallback(강등) 사전지정.
