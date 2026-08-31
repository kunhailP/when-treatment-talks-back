# G-MRT 실험 플랫폼 사양 (v0.4 — 2026-07-30 framework 동기화, 구현: 9월~)

> 기준: theory/formal_framework.md v0.4 (2×2 form×dose) · **PA 트랙** 소속 (docs/publication_map.md) · 표본: pilot 80–120 → demo 180–250 (preregistration 참조).

## 흐름
사전조사(믿음·확신·당파성) → 쟁점 배정 → T=3턴 대화 (턴별 proximal 측정 포함 여부는 reactivity 검증 설계) → 사후조사 → 1주 follow-up

## 무작위화
- conversation-level: generator Z_i ∈ {G_a(API snapshot 고정), G_b(open-weights)}
- **turn-level: A_it = (form, dose) ~ 균등 2×2** — 배정·확률·구현·게이트 판정 전부 로깅

## Evidence bank (고갈 방지 규격 — framework §4.3)
- 쟁점당 **fact unit ≥20**: {id, 원문, 출처, 허용 paraphrase, 방향성, 난이도, 중복관계}
- 턴별 서브뱅크 또는 비복원 sampling — **sampling 규칙 자체가 treatment regime의 일부**
- bank 외부 사실 사용 금지 프롬프트 + 누출 검출기

## Fidelity 게이트 (= 생성커널 G̃의 일부 — framework §4.4)
- 송출 전 검사: form 분류기 + dose 사실 카운트 → 불일치 시 1회 재생성 → 재실패 시 기록 후 송출 (ITT 보존)
- 게이트 판정 로그 공개 · 셀별 fidelity 실시간 모니터링 (하한 80%)
- sandbox 사전 테스트: pilot 전 form/dose fidelity ≥90% 달성 확인

## 로깅 manifest
model id+snapshot, 프롬프트 해시, 디코딩 파라미터, 배정 A_t, 구현 라벨, 게이트 결과, refusal, bank 버전, seed

## 기술 스택
Prolific/CloudResearch + FastAPI/WebSocket 챗 + vLLM(open-weights 팔) · pod 운영은 docs 참조 (이론·시뮬 단계는 GPU 불필요)
