# When the Treatment Talks Back (v0.4)

**Design-Based Causal Inference for Adaptive Generative Political Communication**

X:AI 7기 ADV Session · Research Track · 8/26 발표 = **JCI-형 working paper (arXiv v1)** · 이후 JCI/PSRM → PA

> **운영 규칙**: `theory/formal_framework.md`가 유일한 진실 원천이다. 설계·estimand·기여의 변경은 그 파일부터 수정한다. 두 논문의 경계는 `docs/publication_map.md`. 지금 리뷰를 시작한다면 `docs/review_packet_20260730.md`부터 열 것.

## Contribution (3줄 — framework §0에서 잠금, v0.4)

1. 생성형 처치 (π, G, E)의 estimand 정식화 + 턴별 2×2(form × dose) 분해
2. **Temperature-indexed overlap collapse and localization** (Result A: efficiency bound의 지수 악화 — 조건 (A1)–(A3) 하; Result B: overlap 질량의 결정경계 집중, β^ov 별도 estimand. "정보 국소화"는 해석 층위. 고정 τ에서 추정량 target은 바뀌지 않음 — 반례 포함)
3. G-MRT 설계와 generated-treatment fidelity·turn-level noncompliance 규약

강등(본 논문 기여 아님): transport · GPI 결합 · 동시추론 · constrained policy learning

## 두-논문 구조 (docs/publication_map.md)

- **JCI 논문** (8/26 arXiv v1의 몸통): 관측 로그의 정보 한계 — Contribution 1–2 + 반례·(n,τ) 위상도·연속 H 시뮬레이션. G-MRT는 해법 절로 등장.
- **PA 논문** (참가자 확보 후): G-MRT 2×2 정치 실험 — Contribution 3 + 실증. pilot 80–120, demo 180–250.

## 구조

```
theory/        formal_framework v0.4(진실 원천) · nonidentification_note(Prop 1A + Result A/B) · temperature_collapse(Results 1–3, 5, B)
simulation/    README(이론↔DGP 대응) · src/ 2종 · results/ (bias_plot, collapse_curve)
analysis/      Study 0-a/b/c 파이프라인 (데이터 다운로드 대기)
paper/         outline v0.3 (JCI-형) · references.bib (검증 2026-07-22)
docs/          publication_map(두 논문 경계) · review_packet_20260730(리뷰 진입점) · errata · design_evaluation v1–v3(역사 기록)
platform/ preregistration/   PA 트랙 (프레임은 유지, 실행은 9월 이후)
```

## 상태 (2026-07-30 저녁 — JCI 트랙 일괄 실행 완료)

- 이론: **v0.5 — W3 증명 3개 완료** (1A 반례쌍 완전 구성, Result A 정식 하한(Hahn 1998), **Result B 1-D Proposition 승격**; 전문 = theory/proofs_w3_draft.md, 위임 결정 3건 재검토 가능)
- 시뮬레이션: P1–P3 + **연속 H 배터리·(n,τ) 위상도 완료** (continuous_h.py — 국면 경계가 실선 log E[1/p_τ]=log(1+τ·sinh(1/τ))와 정합) + **라벨 오차 축 완료** (label_error.py — q=0.2에서도 n_req −25%/+6%)
- Study 0: **0-a strict 실데이터 통과** (personalized AI OR 2.18 최대) · **0-b 3개 모델 완료** (Qwen/Mistral/Phi 각 4000건 — 전부 엔트로피 중앙값 0, modal REBT 94.5–98.6%; judge 민감도 κ=.13, n_req는 강건) · **0-c 완료** (n=56,831: 배정의 dose 분산 설명력 η²=.12–.32)
- 논문: **draft v0.2 + LaTeX 완성** — paper/draft_jci_v02.md (Remark A′·**Prop A-T 다턴 기하복리**·OPE 경계·β^ov equipoise) → **paper/tex/main.pdf (13쪽, 그림 4종, 컴파일 0 에러)**. v01은 HISTORICAL
- 신규 실증: 12_effective_temperature — 3개 모델 Δ̂/τ 중앙값 = k=20 해상도 상한 (58–89.5% 우측 중도절단; "측정 자체가 같은 한계" 재귀 논점)
- 인프라: tests/ pytest 7종(닫힌형·kernel 항등식·Kish·B극한·overlap mass·strict·smoothing), validate_repo [3b] 실데이터 복원, 02 --out 옵션
- 대기 (사람 필요): 인간 이중코딩 — analysis/human_coding/ (샘플 200턴 + 지침 준비 완료)
- 세미나: #1 Hackenburg, #2 Salvi 완료 · #3 Imai&Nakamura 예정

## 재현

pip install numpy pandas matplotlib
python simulation/src/simulation.py && python simulation/src/temperature_collapse.py
