# Study 0: DebateGPT 재분석 + 정책 엔트로피 측정 (v0.3 — 2026-07-30)

> v0.3: 4차 비판 반영 — 02 서열 수정 완료 표기, 08을 **전략별 n_eff 표 + Dirichlet smoothing**으로 교체, fidelity audit 시점을 데이터-의존으로 정정. estimand·설계는 theory/formal_framework.md(진실 원천), 트랙 구분은 docs/publication_map.md(Study 0 = JCI).
> **모든 산출물의 인식론적 지위: descriptive / motivating — "establishes"·"종결" 표현 금지.**

세 갈래:
- **0-a 재현·기술분석** (DebateGPT): 원 논문 방향 재현, 전략 선택의 반응 의존성
- **0-b 재질의 실험** (DebateGPT rebuttal): 배치 정책의 조건부 엔트로피/유효온도 proxy 실측 → Result 2 대입으로 "필요 대화 수" 하한 예시 산출 → G-MRT 필요성을 **동기화**
- **0-c fidelity audit** (Hackenburg): 무작위화된 전략 지시가 실제 발화에서 구현됐는지 — "무작위화된 것은 지시였지 행동이 아니다"의 실증. DebateGPT 특수성(구조화 토론)에서 일반 배치로의 외삽 간극을 메움

## 데이터

- DebateGPT: https://huggingface.co/datasets/frasalvi/debategpt (코드: github.com/epfl-dlab/debategpt)
- Hackenburg replication: github.com/kobihackenburg/scaling-conversational-AI
- **샌드박스에서 HF/일부 원격 차단** → 로컬에서 `src/01_download.py` 또는 브라우저로 받아 `data/raw/`에 넣을 것 **[사용자 액션 대기]**
- DebateGPT 구조: opening → rebuttal → conclusion. rebuttal이 반응-적응 단계 → 재질의 표적
- 주의: 결과변수는 1–5 서열 + partial proportional odds (02 재현 시 Ã 정렬 반영)

## 파이프라인 (src/)

| 스크립트 | 역할 | 상태 |
|---|---|---|
| 01_download.py | 데이터 다운로드 (로컬 실행) | 작성 완료 |
| 02_reproduce.py | 방향 재현 + `--strict` 방향 assertion | **fixture strict 통과 (2026-07-30 재생성 — `bash scripts/validate_repo.sh`로 검증)** |
| 06_extract_contexts.py | rebuttal 문맥 층화추출 (프롬프트를 Salvi 원형식 1–2문장 제약에 정렬) | fixture 통과 |
| 07_requery.py | 문맥당 k회 재생성, resume 캐시, manifest, --dry-run 비용 | dry-run 통과 (feasibility 지위; 강화 W5) |
| 08_policy_entropy.py | 전략 분류(LLM judge) → 엔트로피 → **전략별 n_eff(s)=n/E[1/p̂_s] 표 (Dirichlet α=0.5 smoothing + bootstrap 구간)** — 구 minority_p 혼합 방식은 고정 행동의 E[1/π(a\|H)]에 대응하지 않아 폐기 (2026-07-30) | 합성 라벨 스모크 통과, 데이터 대기 |
| 09_fidelity_audit.py (2026-07-30 작성·실행) | Hackenburg 지시-구현 감사 (공개본에 transcript 없음 → 원 저자 실현-행동 측정치 사용: fact 수 r=.87, compliance flags. 발화 수준 form audit은 PA 트랙) | **실행 완료 (3개 스터디, n=56,831)**: 배정 수사전략의 실현 dose 분산 설명력 η²=.12–.32 (68–88%는 within-assignment 변동), moral_reframing 배정의 52–56%가 fact 0개 실현, valence 준수 72.7%(study 1) — "무작위화된 것은 지시였지 행동이 아니다" 정량화 |
| 10_judge_sensitivity.py (2026-07-30 신설) | 두 judge 라벨의 κ·혼동행렬·전략별 n_eff 민감도 | **핵심 발견: 7B vs 32B raw agreement .90이나 κ=.13, both-REBT 제외 시 κ≈0** — 소수 전략의 정체는 인간 코딩 전 신뢰 불가; 단 전략별 n_req는 judge에 강건 (ratio .88–1.52) |
| 11_model_comparison.py (2026-07-30 신설) | 멀티모델 정책 결정성 비교 (동일 judge 통일) | Qwen2.5-7B·Mistral-7B-v0.3·Phi-3.5-mini 완료 — 3개 모델 모두 엔트로피 중앙값 0, modal REBT 94.5–98.6% ("structurally frequent" 실증) |
| 12_effective_temperature.py (2026-07-30 신설) | 문맥별 Δ̂/τ (식별되는 합성량 — τ 단독 비식별) → 위상도 배치 | **3개 모델 모두 중앙값 3.71 = k=20 해상도 상한에서 우측 중도절단 (58–89.5%)** — "결정성 측정 자체가 같은 정보 한계에 부딪힘" (재귀 논점, 논문 §4.4) |

## 전략 taxonomy와 2×2의 관계 (혼동 금지)

`strategy_taxonomy.md`(FACT/SOCR/COMG/…)는 **Study 0의 기존 대화 annotation용**이다. G-MRT 실험의 조작 축은 taxonomy가 아니라 **form(단언/질문) × dose(사실 4–5 vs 1–2)**다 (formal_framework §4). taxonomy의 FACT↔SOCR 대비는 form 축의 관찰 대응물로만 사용.

## 품질 관리

- LLM judge 분류: 인간 이중코딩 200턴, κ≥0.6 (발표 기준) — **논문 핵심 수치에는 민감도 범위 병기** (라벨 오분류의 π̂ 왜곡: simulation TODO 1과 연동)
- 프롬프트·모델 버전 manifest 자동 기록

## 산출 목표

1. reproduce_summary — 재현 신뢰 확보
2. policy_entropy_by_strategy 표 + 최희귀 전략 n_req 하한 — **G-MRT 동기화** (Prop의 증명 아님; 대비별 필요 표본은 두 전략 E[1/p]의 합 규모)
3. fidelity_audit 표 — 공격 Q1의 실증화
