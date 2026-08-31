# Simulation (v0.3.1 — 2026-07-30, 4차 비판 반영: 지표 객체 분리)

이론(theory/)과 시뮬레이션의 대응 관계 문서. estimand·설계 정의는 formal_framework.md(진실 원천)를 따른다. JCI/PA 트랙 구분은 docs/publication_map.md.

## 파일

| 스크립트 | 검증하는 이론 | 산출물 |
|---|---|---|
| `src/simulation.py` | Prop 1A의 confounding 직관: 적응 정책 하 naive 부호 반전, known-ρ IPW/DR 복원 | results/results.csv, bias_plot.png |
| `src/temperature_collapse.py` | Result A의 rate 직관: (P1) IPW SE 지수 성장 — **scaled inverse-propensity diagnostic** 곡선과 일치(정식 efficiency bound 아님, legend에 명시), (P2) 유효표본·overlap 붕괴 — **4개 지표를 구분 보고** (아래), (P3) naive의 확신-오류 동반 상승 — coverage는 conditional/unconditional 병기, zero-cell·estimability rate·max weight 동시 출력 | results/collapse_results.csv, collapse_curve.png |
| `src/continuous_h.py` (2026-07-30 신설, W4) | 연속 H 시뮬레이션: 주 DGP H~Uniform(−1,1) + robustness N(0,1), β(H) 3종(const/smooth/kink), 추정량 배터리(HT/Hájek/trunc/AIPW-oracle/OR-oracle/overlap — **overlap의 target은 β^ov**), (n,τ) 격자 400 sims/cell → **위상도 figure** (점선 δ/τ + 실선 log E[1/p_τ]=log(1+τ·sinh(1/τ)), `--selftest`로 닫힌형 MC 대조). 국면 분류 임계값(상대편향 .10/.20, coverage .85)은 presentation 선택 — RMSE·coverage 판 병기로 방어 | results/continuous_h_results_{uniform,normal}.csv, continuous_h_battery.png, phase_diagram.png |

**지표 객체 구분 (2026-07-30 — 혼동 금지):**

| 컬럼 | 객체 | 지위 |
|---|---|---|
| `kish_ess1_frac`, `kish_ess0_frac` | 전역 arm-specific Kish ESS/n → 1/E[1/p_a] | **이론(Result A) 대응 객체** |
| `min_cell_occupancy` (구명 ess_frac) | 최소 층×팔 셀 점유율 — 이 DGP는 층 내 p가 상수라 셀 Kish=셀 크기 | Kish ESS 아님; **희귀 crossover 소멸의 직접 진단** |
| `overlap_weight_mass` | E[p(1−p)] | **Result B의 정리 객체** — W4 연속 시뮬의 중심 지표 |
| `overlap_coefficient` | E[2min(p,1−p)] | 별도 진단 (Result B 검증용 아님) |

## 동일-객체 선언 (이론 ↔ DGP)

`temperature_collapse.py`의 배치 정책은 softmax(gap(d)/τ)이며, gap은 τ=1에서 `simulation.py`의 적응 정책(P(evidence|defensive)=0.85, 아니면 0.30)이 정확히 재현되도록 캘리브레이션됨 (GAP_DEF=log(0.85/0.15), GAP_REC=log(0.30/0.70)). **따라서 두 DGP는 별개가 아니라 τ=1 단면과 τ 축 전체의 관계이고, 시뮬레이션의 τ는 이론의 Δ/τ와 동일 파라미터다.**

`do(S_t)`의 의미: 라벨 개입 후 실현은 생성분포(Q_t ~ N(1,σ_g))에서 추출 — formal_framework §1의 커널 개입(stochastic intervention)을 구현한 것.

## 해석 주의

- IPW가 "사는" 것은 **true propensity를 아는 경우**다. 이는 G-MRT 정당화이지, transcript 사후분석의 구제가 아니다 (관측 세팅의 공격은 H 부분관측·라벨 오분류이며 아래 TODO).
- **극단 τ에서 경험적 분산이 감소해 보이는 현상은 경계 estimand로의 수렴이 아니다** (구 서술 폐기, 2026-07-29 정정). 이 DGP는 이산 2-상태라 연속 결정경계 자체가 없다. 정확한 해석: 희귀 crossover가 표본에 실현되지 않아 **추정량이 편향된 채 안정적으로 보이는 유한표본 overlap collapse**다 — nonidentification_note의 (n,τ) 공동극한 위상도에서 n ≪ exp(δ/τ) 국면. Result B(연속 경계 국소화)의 증거로 쓰지 않는다; Result B 검증은 연속 H 시뮬레이션(W4)에서.
- **실현된(realized) 전역 Kish ESS 자체도 collapse 국면에서 오도적일 수 있다** (2026-07-30 신규 관측, nsims=300·n=2000): τ≤0.22에서 `zero_stratum_arm_rate`가 0.70→0.99로 뛰는 순간 `kish_ess0_frac`이 0.028→0.37→0.53으로 **비단조 반등**한다 — 희귀 crossover가 표본에서 사라지면 남은 가중치가 균질해져 실현 Kish가 "건강해 보이는" 것. 모집단 객체 1/E[1/p]는 계속 붕괴하는데 실현 지표만 회복되는 이 간극이 곧 "편향된 채 안정" 국면의 signature다. **따라서 ESS 보고는 반드시 zero-cell rate와 병기한다** (논문 §7에 이 문장 사용).

## TODO

**JCI 트랙 (W4)**
1. ~~연속 H 시뮬레이션 신설~~ → **완료 (src/continuous_h.py, 2026-07-30)** — 위 표 참조
2. ~~전략 라벨 측정오차 축~~ → **완료 (src/label_error.py, 2026-07-30)**: 참 분포 = Study 0-b 실측(judge32b), symmetric·absorbing 두 노이즈 모델, q∈{0,.05,.1,.2}. **결과: q=0.2에서도 희귀 전략 n_req 변동 −25%(sym)/+6%(abs) — 10⁵ 스케일 결론은 judge 노이즈에 강건, symmetric은 낙관 방향(실제 필요량은 더 큼)** (results/label_error.csv, label_error.png)

**PA 트랙 (참가자 확보 후 — publication_map 참조)**
3. 2×2 form×dose DGP 확장: β^form, β^dose, β^form×dose + 차별 비순응(form/dose fidelity 상이) 시나리오
4. WCLS 추정기 추가 (현재 naive/IPW/DR)

## 재현

pip install numpy pandas matplotlib
python src/simulation.py --nsims 500 --n 2000
python src/temperature_collapse.py --nsims 300 --n 2000
