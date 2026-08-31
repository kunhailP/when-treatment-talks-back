> ⚠️ **역사 기록 — 현재 상태가 아님.** 2026-07-28 리뷰 패킷
>
> **폐기됨.** 이후 v0.4·v0.5에서 설계·이론이 크게 바뀌었다.
>
> 현재 진실 원천: `theory/formal_framework.md` (v0.5) · 현재 원고: `paper/tex/main.tex`
> 이 디렉터리는 replication package가 아니다 (`docs/internal/README.md` 참조).

---

# 리뷰 패킷 — 동기화 상환 완료 보고 (2026-07-28)

> **[HISTORICAL — 2026-07-30 대체됨]** 이 문서는 2·3차 비판 이전 상태의 기록이다. 일부 주장("동기화 완료", Prop 1B, Result 4)은 이후 정정되었다 (errata_20260729). **현재 진입점은 `review_packet_20260730.md`.** 이 파일은 수정하지 않고 보존한다.

네(박건우)가 리뷰를 시작하기 위한 단일 문서. 이것만 읽고 아래 순서로 파일을 열면 된다.

---

## A. 무엇이 바뀌었나 (v0.2 동기화 상환)

| 파일 | 버전 | 핵심 변경 |
|---|---|---|
| theory/formal_framework.md | **v0.2** | 진실 원천 승격 · Contribution 3줄 잠금(§0) + 강등 목록 · 2×2(form×dose)가 기본 객체, β^form/β^dose/β^form×dose · ρ=균등 사전지정 · stochastic intervention 연결 · "consistency 실패"→ill-defined treatment · fidelity 규약(차별 비순응·게이트 오차·80% 하한) |
| theory/nonidentification_note.md | **v0.2** | Prop 1A/1B 분리 · 1A 반례쌍 스케치 · 1B 스코프 제한(known-propensity IPW/Hájek) · Result 4 = Conjecture 라벨 · "재정의는 질문 전환" 정직 문장 · "theorem" 금지 조항 |
| theory/temperature_collapse.md | **v0.2** | Result별 지위 표기(Prop 후보/Conjecture/heuristic) · 시뮬레이션 동일-객체 선언 · 실증 브리지의 인식론적 지위("동기화", "종결" 금지) · 라벨 오차 주의 |
| simulation/README.md | **신규** | 이론↔DGP 대응표 · τ=1 캘리브레이션 명문화 · 커널 개입으로서의 do(S) · 해석 주의 2건 · W4 TODO(라벨 노이즈, 2×2 DGP) |
| analysis/README.md | **v0.2** | "종결"→"동기화" · Study 0-c(Hackenburg fidelity audit, 09 스크립트) 추가 · taxonomy ≠ 2×2 조작 축 혼동 금지 문단 · κ 민감도 병기 규칙 |
| docs/internal/outline.md | **v0.2** | Related Work 절 신설(Nakamura–Imai 피드백 유무 선 긋기 필수) · 집필 금지어 목록 |

**변경 안 한 것 (의도적)**: docs/internal/design_evaluation*.md, design_decision_v3.md는 **역사적 기록**으로 보존 — 진실 원천은 framework이며, 과거 문서와 충돌 시 framework가 우선한다는 규칙이 §0에 명시됨.

## B. 편집위원 비판 7개 항목 대비 상태

| # | 항목 | 상태 |
|---|---|---|
| 1 | Contribution 3줄 고정 + 강등 | ✅ framework §0 |
| 2 | Prop 1A/1B 분리, theorem 금지 | ✅ (증명 자체는 TODO) |
| 3 | 2×2를 estimand 기본 객체로 | ✅ framework §1–2, §4 |
| 4 | ρ 사전지정 | ✅ 균등 primary / 배치 secondary |
| 5 | Study 0 언어 규율 | ✅ temp_collapse·analysis README |
| 6 | 시뮬에 τ 축 또는 라벨 노이즈 | ✅ τ 축은 기존 완료(동일-객체 선언 추가) · 라벨 노이즈는 W4 예약 |
| 7 | Related work 선 긋기 | ✅ outline에 지침 고정 (본문 집필 시 이행) |

## C. 정합성 검증 결과 (내가 확인한 것)

1. **2×2 일관성**: framework·noniden·outline·analysis 모두 form×dose 기준. 잔존 충돌 1건 발견·해소 — strategy_taxonomy는 annotation용으로 재정의(analysis README에 명시).
2. **ρ 일관성**: framework §2.3 ↔ noniden Corollary ↔ outline §6 일치.
3. **지위 라벨 일관성**: Result 4 = Conjecture가 세 문서에서 동일. "theorem" 단어 잔존 0건(이론 파일 기준).
4. **시뮬↔이론**: τ=1 캘리브레이션(0.85/0.30)의 동일-객체 관계가 코드와 문서 양쪽에 존재.
5. **미해소 잔존 (역사 문서 내)**: presentation_outline.md의 "킬러 슬라이드" 서술과 project_plan.md의 옛 K=2 표현 — 발표자료 제작 시점(W5)에 outline v0.2 기준으로 재작성 예정이라 지금은 방치가 맞다고 판단.

## D. 네 리뷰 가이드 — 읽는 순서와 판단 요청

**읽는 순서 (약 40분)**: ① framework §0(기여 3줄) → ② framework 전체 → ③ nonidentification_note → ④ temperature_collapse → ⑤ simulation/README → ⑥ analysis/README → ⑦ paper/outline.

**리뷰에서 결정해줘야 하는 것 (5건)**:
1. **Contribution 3줄 문안** — 이대로 잠가도 되는가? (특히 2번 문장의 범위)
2. **ρ=균등 primary** — 동의하는가? (배치-기준을 primary로 바꾸면 해석은 정책적, 추정은 어려워짐)
3. **Result 4의 Conjecture 라벨** — 8/26 arXiv v1에 Conjecture로 실어도 되는가, 증명 완성까지 미룰 것인가? (내 권고: Conjecture로 싣기 — 정직 라벨이면 오히려 신뢰 신호)
4. **fidelity 하한 80%/셀** — 이 숫자로 사전등록할 것인가? (sandbox 테스트 후 조정 여지)
5. **dose 조작 수치** — 고=4–5, 저=1–2 사실 개수. 근거는 Hackenburg의 평균 5.6/최대 22 claims 분포인데, sandbox에서 검증 전 임시값.

## E. 남은 작업 (우선순위·주차)

| 우선순위 | 작업 | 주차 | 성격 |
|---|---|---|---|
| P0 | 1A 반례쌍 완전 구성 + 1B 라플라스 증명 | W3–4 | 이론(증명) |
| P0 | **[사용자] DebateGPT + Hackenburg 데이터 다운로드** → Study 0 실행 | W3 | **유일한 외부 병목** |
| P1 | 02 재현 서열 스케일 수정 · 09 fidelity audit 스크립트 | W3 | 코드 |
| P1 | 시뮬 라벨 노이즈 축 + 2×2 DGP + WCLS 추정기 | W4 | 코드 |
| P1 | Hackenburg 사전정보 power simulation | W4 | 코드 |
| P0 | working paper 초고 (outline v0.2 순서) | W5 | 집필 |
| P2 | 세미나 #3(Imai&Nakamura) 덱 — 설명형 스타일 | W3 | 발표 |

## F. 리뷰 후 다음 단계

네 리뷰에서 D의 5건이 결정되면 → framework에 반영(변경 시 §0 규칙대로 이 파일부터) → W3 진입: 증명 작업과 Study 0 실행이 병렬로 시작된다.
