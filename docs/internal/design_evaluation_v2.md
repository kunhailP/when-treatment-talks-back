# 연구 설계 재평가 v2 — Hackenburg 정독 반영

평가일: 2026-07-27 (D-30, W1 세미나 완료 시점) · 이전 평가: docs/internal/design_evaluation.md (7/22)

## 1. 정독 후 더 강해진 것

**(a) 우리 estimand의 표적이 "현존 최강 지렛대의 내부"임이 입증됐다.**
Hackenburg의 가장 효과적인 PPT인 Reward Modeling은 문자 그대로 turn-level adaptive policy다: 매 턴 12개 후보를 생성하고, 대화 이력을 조건으로 설득 확률을 예측해 최선을 고른다. 즉 그들이 발견한 최강 지렛대(+2.32pp)는 정확히 우리의 (π, G) 객체이고, 그 내부 — 어떤 턴의 어떤 선택이 효과를 만드는가 — 는 그들의 설계로 식별 불가. "우리가 풀려는 문제가 이 분야 최강 결과의 블랙박스"라는 서사가 완성됨.

**(b) 온도-붕괴 전제의 실증 근거를 그들이 제공했다.**
frontier 모델은 응답 변동성이 적어 RM 선택의 이득이 작다는 관찰(SM 2.10) = "배치 모델의 유효온도가 낮다"의 실측 사례. temperature_collapse.md의 전제를 인용으로 뒷받침 가능.

**(c) 방법론 부품 재사용 가능.**
정보 밀도 측정법(GPT 카운트 + 인간 팩트체커 r=.87)은 우리의 realized-content audit에 그대로 이식. 코드·데이터 공개(github.com/kobihackenburg/scaling-conversational-AI).

## 2. 새로 드러난 리스크

**(a) 효과크기 현실.** 프롬프트 수준 전략 격차가 2~4pp, 최강-차강 격차 ~1pp. turn-level form effect는 그보다 작을 가능성이 높고, n=1,500–2,500으로는 못 잡을 수 있다.
완화 요인: 우리 도메인(오정보 교정)의 효과크기는 정책설득보다 훨씬 크다(Costello: 음모론 믿음 ~20% 감소, 2개월 지속). 결과변수를 태도(0–100)가 아닌 belief accuracy로 두는 선택이 파워 측면에서도 옳았음. 단, power simulation에 Hackenburg 사전정보(전략효과 −1.5~+2.3pp 범위)를 반드시 반영해야 함.

**(b) form-only estimand의 null 위험.** 정보 밀도가 설득 분산의 44~75%를 설명한다면, 정보를 잠근 뒤 남는 순수 형식 효과는 0에 가까울 수 있다. "form effect = 0"이 나왔을 때 논문이 죽지 않도록, **정보량 자체를 실험 축으로 승격**하는 것이 안전하다 (→ §3).

## 3. 설계 개선 제안: turn-level 2×2 factorial

원안: 전략 2종(FACT vs SOCR) 무작위화 + information-lock.
개선안: 매 턴 **형식 × 정보용량** 2×2 무작위화.

- 축 1 형식(form): 단언형 교정 vs 질문형(소크라테스식)
- 축 2 정보용량(dose): 고밀도(사실 4–5개) vs 저밀도(사실 1–2개) — evidence bank 내에서 개수만 통제

기대 효과:
1. Hackenburg가 **상관으로만** 보인 정보 매개를 **인과로** 식별하는 최초 실험이 됨 (그들의 공격 지점 Q2를 우리가 해결)
2. form effect가 0이어도 dose effect와 상호작용이 결과 — null-proof 설계
3. fidelity 게이트가 쉬워짐: "주장 개수 세기"는 검증된 측정(r=.87), "소크라테스식인지 판정"보다 훨씬 신뢰 가능
4. estimand 확장: β_form, β_dose, β_form×dose — G-MRT 이론(WCLS, Proposition 1, 온도-붕괴)은 수정 없이 그대로 적용
5. factorial이라 셀 4개여도 주효과 파워는 2조건 설계와 동일

비용: 프롬프트 엔지니어링 복잡도 증가(용량 통제), evidence bank 설계 부담. sandbox fidelity 테스트(플랫폼 스펙의 사전 절차)로 검증 필요.

## 4. Study 0 재구성 제안: 데이터 2원화

| 데이터 | 역할 | 근거 |
|---|---|---|
| DebateGPT (Salvi) | 반응-적응성 입증 (04), 재질의 문맥 추출 (06–08) | rebuttal 구조가 유일하게 명시적 반응-적응 단계 |
| **Hackenburg replication 데이터 (추가)** | **fidelity audit** — 무작위화된 전략 지시가 실제 발화에서 구현됐는지 분류; 턴 수준 행동의 지시 간 분산 측정 | 전략이 무작위화된 유일한 대규모 코퍼스. 우리 공격 Q1(fidelity)을 실증 결과로 승격 |

fidelity audit는 새 스크립트 하나(전략 분류기를 그들 대화에 적용)로 가능하고, 결과는 그 자체로 발표 슬라이드 한 장 + 논문 §3의 실증 동기가 된다: "무작위화된 것은 지시였지 행동이 아니었다."

## 5. 일정 재점검 (D-30)

W1 완료: Hackenburg 세미나 (덱 v2 + 대본 + PDF). 남은 4주:

- **W2 (7/28–8/3)**: Salvi 세미나 준비 · **[사용자 액션 필요] DebateGPT + Hackenburg 데이터 다운로드** · 02 재현 실행
- **W3 (8/4–8/10)**: Study 0 실행 — fidelity audit + adaptive selection + 재질의(로컬 API) · Imai&Nakamura 세미나
- **W4 (8/11–8/17)**: Proposition 1 온도판 정식화 마무리 · 시뮬레이션에 2×2 DGP 확장 · Hackenburg 사전정보 기반 power simulation · Qian 세미나
- **W5 (8/18–8/26)**: working paper 10–15쪽 · 발표자료 · Dafoe 세미나 · 최종 발표

이연 유지: 플랫폼 구현·IRB (9월). Section 8(constrained policy learning)은 여전히 잘라둔 상태 유지.

## 6. 결정 대기 사항

1. G-MRT 1차 조작: 원안(전략 2종 + lock) vs **2×2 factorial (권고)**
2. Study 0 데이터: DebateGPT 단독 vs **+ Hackenburg fidelity audit (권고)**

결정되면 formal_framework §4, analysis/README, preregistration 골격에 반영.
