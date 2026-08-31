> ⚠️ **역사 기록 — 현재 상태가 아님.** 2026-07-30 리뷰 진입점
>
> **폐기됨.** 후속 감사 `review_packet_20260825.md`가 이 문서가 놓친 결함 17건을 추가로 확정했다.
>
> 현재 진실 원천: `theory/formal_framework.md` (v0.5) · 현재 원고: `paper/tex/main.tex`
> 이 디렉터리는 replication package가 아니다 (`docs/internal/README.md` 참조).

---

# 리뷰 패킷 (2026-07-30) — 3차 비판 반영 완료 보고 · 현재 진입점

이 문서 하나로 리포의 현재 상태를 파악한다. 구판(20260728)은 historical.

---

## A. 3차 비판에 대한 판정 (수용 근거)

3차 비판은 새 오류 지적이 아니라 **정밀화 패스**다: 비판자가 직접 코드를 실행해 v0.3 수정(--strict 통과, ESS 단조, 1/p 수정)을 확인했고, 남은 문제는 (i) 리포 전반 동기화 미완, (ii) 이론 서술의 조건·명명 정밀도, (iii) 두-논문 구조의 실물화였다. 전부 검증 가능했고 전부 수용했다. 점수 6.3 → 7.7–8.0 상승과 무관하게, 반영 안 할 이유가 있는 항목은 없었다.

**수용하되 조정한 것**: 없음 (이번 라운드는 전 항목 수용). **이연 합의 유지**: Docker/CI, RunPod 사용.

## B. 반영 내역 (2026-07-30, v0.4)

| 항목 | 파일 | 내용 |
|---|---|---|
| stale 문서 4개 동기화 | README, simulation/README, paper/outline, docs/project_plan | Contribution 2 갱신 · **"경계-국소 estimand로 조용히 이행" 문장 폐기** → "희귀 crossover 미실현에 의한 편향-안정 overlap collapse (n≪exp(δ/τ) 국면)" · outline v0.3 = JCI-형 (Prop 1B/Result 4 제거) · project_plan v2 = 새 W3–W6 |
| Result A 조건 잠금 | formal_framework §3, noniden | (A1) 𝓗_δ 양의 측도 · (A2) σ̲²>0 · (A3) 비모수 클래스(파라메트릭 외삽 배제 — "가정으로 식별을 사는 것" 문장 포함) |
| n_eff 교체 | framework, noniden, temp_collapse(이론·코드) | **arm-specific Kish: n_eff(a)=n/E[1/π_τ(a|H)]** (구 n·E[exp(−Δ/τ)] 폐기) · "τ 절반→n 제곱"은 고정-gap 층 내부로 제한 |
| 명명 확정 | 이론 3파일, README | 수학적 명칭 = **"overlap collapse and localization"** · "정보 국소화"는 efficiency bound와 연결되는 해석 층위로만 |
| Prop 1A 완화 | framework, noniden | "설계상 필연" → **"구조적으로 빈번하며 설계에 의해 강화"** (structurally frequent and design-reinforced) |
| 두-논문 실물화 | **docs/publication_map.md (신설)** | JCI(J1–J3) / PA(P1–P3) 기여 잠금 · 자산 배분 규칙표 · 8/26 = JCI-형 working paper |
| 표본 현실화 | pilot_prereg v0.4 | pilot 80–120 (기능 검증) · PA demo 180–250 · 구 300–500 폐기 |
| 시뮬 사양 | noniden TODO, simulation/README | 주 DGP **H~Uniform(−1,1)** (경계 밀도 상수 → Laplace 검증 깨끗) · N(0,1)은 robustness · **(n,τ) 위상도 figure** 사양 추가 |
| diagnostic 재명명 | temperature_collapse.py, 이론 | theory_se = **"scaled inverse-propensity diagnostic"** (정식 bound 아님 — legend·docstring 명시) |
| 트랙 분리 | noniden TODO, simulation/README, project_plan | 2×2 DGP·WCLS·differential fidelity → PA 트랙 이관 |

## C. 읽는 순서 (약 30분)

① publication_map(두 논문 경계) → ② framework v0.4 §0·§3 → ③ nonidentification_note v0.4 → ④ simulation/README v0.3 → ⑤ paper/outline v0.3 → ⑥ project_plan v2

## D. 현재 결정 대기 (사용자)

1. **JCI 논문 가제** — "Information Limits of Observational Logs..." 확정 여부 (outline v0.3 참조)
2. **[유일한 외부 병목] 데이터 다운로드** — DebateGPT(HF: frasalvi/debategpt) + Hackenburg replication(github: kobihackenburg/scaling-conversational-AI) → analysis/data/raw/
3. 구판 packet의 D-5건 중 미결 2건 유지: fidelity 80% 숫자, dose 4–5/1–2 수치 (sandbox 검증 후 — PA 트랙이라 급하지 않음)

## E. 다음 단계 = W3 (8/4–)

증명 주간: 1A 반례쌍 · Result B 1-D approximate-identity 증명(unique root → multiple-root corollary → 다차원은 appendix) · Result A 정식 하한. 데이터 도착 시 Study 0 병렬 실행. 세미나 #3 (Imai & Nakamura) 덱은 요청 시 착수.

---

## F. 4차 비판 대응 (같은 날, 2026-07-30 — v0.4.1)

**판정**: 전 항목 수용. 특히 1·2·3번은 비판자가 실행으로 잡아낸 실제 결함이었고, 전부 검증 후 수정했다.

| # | 지적 | 검증 | 수정 |
|---|---|---|---|
| 1 | 패키지 fixture로 strict 실패 | **재현됨** (1.355 < 1.609, 비판자 수치와 일치) — 코드는 맞았으나 구 fixture가 패키징됨 | fixture·summary 재생성(3.610 최대, strict 통과) + **`scripts/validate_repo.sh` 신설** (compile→fixture→strict→smoke를 배포 전 1커맨드 검증) |
| 2 | 구 ESS 지표는 Kish가 아니라 셀 점유율 | **맞음** — 층 내 p 상수 → 셀 Kish=셀 크기 | `min_cell_occupancy`로 개명 + **전역 arm-specific Kish**(이론 객체) 별도 추가. 부수 발견: collapse 국면에서 실현 Kish가 비단조 반등(0.028→0.53) — zero-cell rate와 병기 규칙 신설 (simulation/README) |
| 3 | overlap 정의 불일치 (p(1−p) vs 2min) | **맞음** | `overlap_weight_mass`(Result B 객체) / `overlap_coefficient`(진단) 분리, W4 중심 지표는 전자 |
| 4 | Result B 정칙조건 부족 | 수용 | (B1)–(B4) 잠금: 고립 simple root·Δ′≠0, 다중 root 질량 f(r_j)/\|Δ′(r_j)\|, 다차원은 f/\|∇Δ\| surface measure. 증명 경로 = **cosh⁻² kernel 변수변환 + approximate identity** (ω_τ=1/[4cosh²(Δ/2τ)]) |
| 5 | 위상도 경계 δ/τ는 층별 heuristic | **수치 확인** — Uniform(−1,1)에서 정확한 닫힌형 발견: **E[1/p_τ]=1+τ·sinh(1/τ)** (MC 일치 4자리) | 위상도 2선 사양: 점선 δ/τ(직관) + 실선 log E[1/p_τ](정확) |
| 6 | NaN 제거가 실패 은폐 | 수용 | estimable/zero-treated/zero-control/zero-cell rate + median·p95 max weight + coverage **conditional/unconditional 병기**, 전체 재실행 완료 |
| 7 | JCI Contribution 1의 2×2 층위 | 수용 | framework §0: JCI는 일반 행동공간 𝒜, **2×2는 PA의 실험 구현 객체** (publication_map J1/P1 갱신) |
| 8 | Result 5 과대 지위 | 수용 | **design corollary / illustrative trade-off로 강등** — JCI 핵심 정리는 1A·A·B 3개 |
| 9 | 08의 minority_p 혼합 | **맞음** — 문맥마다 minority 전략이 달라 고정 행동의 E[1/π(a\|H)] 아님 | **전략별 n_eff(s)=n/E[1/p̂_s] 표** + Dirichlet(α=0.5) smoothing + bootstrap 95% 구간, 합성 라벨 스모크 통과 |
| 10 | 잔여 동기화 6건 | 확인 | noniden 제목 "필연성" 제거, analysis/README v0.3, platform v0.4 기준, errata HISTORICAL 표기, prereg에 **issue=blocking factor 규칙** 추가 |

**다음 리뷰 진입점은 이 문서 그대로** (같은 날 갱신이므로 새 파일 만들지 않음).
