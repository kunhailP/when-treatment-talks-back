> ⚠️ **역사 기록 — 현재 상태가 아님.** 설계 결정 v3 (2026-07-27)
>
> 역사 기록.
>
> 현재 진실 원천: `theory/formal_framework.md` (v0.5) · 현재 원고: `paper/tex/main.tex`
> 이 디렉터리는 replication package가 아니다 (`docs/internal/README.md` 참조).

---

# 설계 확정 v3 — Salvi·Imai&Nakamura 정독 + 딥리서치(87개 주장, 60건 적대검증) 종합

작성일: 2026-07-27 · 선행: design_evaluation.md (v1), design_evaluation_v2.md

---

## A. 딥리서치 결과: 4개 질문에 대한 판정

| # | 질문 | 판정 | 근거 |
|---|---|---|---|
| 1 | turn-level / micro-randomized 설계를 LLM 대화 설득에 적용한 연구? | **부재** | Salvi·Hackenburg·Costello 전부 대화/참가자 수준 무작위화. MRT는 여전히 mHealth(Liu et al. AJPH 2023)와 IS 분야 소개 논문(Pieper et al. JIT 2024/25)까지만 — 대화·설득 적용 사례 없음. turn-level "분석"은 존재하나(Jaipersaud et al. 2025, linear probe) 관찰적·상관적 |
| 2 | 정보 밀도의 설득 매개효과를 무작위화로 식별한 연구? | **부재** | Hackenburg조차 정보 밀도는 사후 측정된 매개변수(2단계 회귀). 2025년 말 기준 LLM 설득 실험은 거의 전부 결과지표만 보고, 기제의 실험적 식별 부재 |
| 3 | 수사 형식 × 정보량 factorial 분리 조작? | **부재** | 존재하는 factorial은 상대×개인화(Salvi), 정체성×어조, 모드×대화유형뿐. Timm et al. 2025(Tailored Truths)가 조작통계+개인화 혼합전략 비교로 근접하나 직교 분리 아님 |
| 4 | I&N 프레임의 동적/적응형 대화 확장? | **부분 존재 — 주의** | **Nakamura & Imai (2026): 정적 텍스트 내부의 문장 시퀀스(위치) 효과로 확장** (MSM 적용, 홍콩 시위 실험 재분석). 단, 사람 반응에 적응하는 상호작용형 turn-level 처치는 명시적으로 미해결 |

**결론: 우리의 2×2 G-MRT 설계는 선점되지 않았다. 그러나 4번 — I&N 그룹이 이미 "동적"으로 이동 중 — 은 시계가 돌고 있다는 뜻이다.** 그들의 동적 = 객체 내부 순서(고정된 텍스트, 피드백 없음, positivity 문제 없음). 우리의 동적 = 인간 반응 피드백 루프 위의 적응 정책(positivity 붕괴가 핵심 문제). 구분은 명확하지만, working paper의 관련연구 절에서 이 구분을 **명시적으로** 그어야 하고, 빠르게 내야 한다.

부수 확보 문헌: LLM vs 인간 설득 메타분석(7편, n=17,422, g=0.02 전체 무차이, I²=76% — "무엇이 효과를 만드는지 분해가 필요하다"는 우리 문제의식의 완벽한 도입 인용), Costello 후속(GPT-4o, n=955, 음모론 확신 −11.8%, 정체성·어조 무관), Timm et al. 2025, Jaipersaud et al. 2025.

## B. Salvi 정독에서 얻은 것 (세미나 #2 대비 겸)

1. **구조**: opening(4분)–rebuttal(3분)–conclusion(3분)의 시간제한 단계형. GPT-4는 "1–2문장만, 상대를 직접 호명하지 말 것" 프롬프트 → LIWC에서 분석적·논리적 스타일 두드러짐. **함의: 재질의 실험(06–08)의 rebuttal 프롬프트를 이 형식에 맞출 것(1–2문장 제약 포함).**
2. **결과 정밀화**: 개인화 AI vs Human–Human 오즈 +81.2% [26.0, 160.7] — CI가 매우 넓다(n=150/조건). 비개인화 AI(+21.9%, n.s.), 인간 개인화(−15.7%, n.s.). **개인화 AI 조건만 backfire가 없었다**는 절대변화 결과가 발표용으로 강력.
3. **Hackenburg와의 개인화 모순 해소 단서**: Salvi 개인화 = 6개 인구정보를 "빈틈을 파고들라"는 지시와 함께 + 상대적 벤치마크(vs 인간) + 구조화 토론. Hackenburg = 절대효과(pp) + 자유대화 + 3개 방식 평균. 모순이 아니라 **estimand와 세팅이 다른 것** — 세미나 토론 포인트.
4. **재현 스크립트(02) 수정 필요**: 결과변수가 0–100이 아니라 1–5 서열 + partial proportional odds. 현재 fixture 기반 스크립트의 crude OR 방향 확인은 유효하나, 서열 스케일 정렬(Ã 변환식) 반영해야 함.

## C. Imai & Nakamura 정독에서 얻은 것 (세미나 #3 대비 겸)

1. **프레임 요약**: 프롬프트 무작위화 → LLM이 X 생성 → T=g_T(X)(처치 특징), U=g_U(X)(교란 특징) → **분리가능성(separability) 가정**(T와 U가 서로의 결정적 함수가 아님)이 overlap을 함의 → 오픈소스 모델의 내부 표현 R로 deconfounder 학습(TarNet) → DML로 ATE + 유효 신뢰구간. gpi-pack 공개.
2. **우리와의 결합점 (이건 새 발견)**: 우리 G-MRT가 open-weights generator(Llama)를 쓰면 **모든 생성 발화의 내부 표현 R_t를 관측**할 수 있다 → (a) R_t를 공변량으로 쓰는 분산 감소(효율 개선), (b) 실현된 발화의 잔여 교란 특징(길이·어조) 조정, (c) form/dose의 조작 검증(manipulation check)을 표현 공간에서 수행. **design-based 식별(우리) + representation-based 효율(GPI)의 결합은 아무도 안 했다** — 논문 §5 추정 절의 차별점으로 추가.
3. **경계의 정확한 위치**: 그들의 Assumption 2(프롬프트 무작위 배정)가 우리 세팅에서 정확히 깨지는 지점 — 턴 t의 "프롬프트"(전략 배정)가 H_t에 의존. 논문에서 이 가정 번호를 직접 인용하며 확장 지점을 특정할 것.
4. **v5(2026.6) 결론부 확인**: 향후 과제로 이미지·비디오만 언급. 대화형 확장은 그들의 지도에 없음(단, 위 A-4의 별도 논문 주의).

## D. 확정 사항

1. **G-MRT 1차 조작 = 턴별 2×2 factorial** (형식: 단언 vs 질문 × 정보용량: 고 vs 저) — 사용자 확정(7/27). formal_framework §4에 반영할 것.
2. **Study 0 = DebateGPT + Hackenburg 이원화** — DebateGPT: 반응-적응성·재질의(rebuttal 형식을 Salvi 원 프롬프트에 정렬), Hackenburg: fidelity audit("무작위화된 것은 지시였지 행동이 아니다"). *사용자 데이터 다운로드 대기 중.*
3. **generator 축 확정**: 최소 한 팔은 open-weights(Llama 계열) — 재현성 + GPI 결합 가능성 확보.
4. **관련연구 절 필수 인용 추가**: Nakamura & Imai 2026(동적 확장 — 구분 명시), Timm et al. 2025, Jaipersaud et al. 2025, LLM 설득 메타분석, Pieper et al.(MRT의 IS 도입 — "대화 적용은 없음" 근거).

## E. 리스크 갱신

- **스쿱 리스크 상향**: I&N 그룹의 동적 이동 확인 → working paper 초안을 8/26 전에 arXiv 가능한 수준으로 다듬는 것을 목표로 상향 (기존: 발표용 10–15쪽).
- 개인화 논쟁(Salvi vs Hackenburg)은 우리 논문의 주전선이 아님 — 세미나 토론용으로만 소비하고 논문에서는 각주 처리.

## F. 남은 4주 (수정 없음, 세부만 갱신)

- W2 (7/28–8/3): Salvi 세미나(위 B 반영) · **[사용자] DebateGPT·Hackenburg 데이터 다운로드** · 02 재현(서열 스케일 수정)
- W3 (8/4–8/10): Study 0 실행(fidelity audit 추가) · I&N 세미나(위 C 반영)
- W4 (8/11–8/17): 2×2 DGP 확장 시뮬레이션 · Hackenburg 사전정보 power simulation · Qian 세미나
- W5 (8/18–8/26): working paper(관련연구 절에 A·C 반영, arXiv 수준 목표) · 발표 · Dafoe 세미나
