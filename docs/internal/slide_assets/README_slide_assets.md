# slide_assets — 8/26 발표 그림·수식 모음

slide_plan_20260826.md의 `[그림]` `[수식]` 자리에 넣는 파일들. 수식 PNG는 전부 **투명 배경·600dpi**(슬라이드에 그대로 붙여도 깨지지 않음), 그림은 300dpi. LaTeX 원본은 `equations_source.md`에 있으니 수정·재렌더가 필요하면 거기서.

## 제작한 그림 (3종)

| 파일 | 슬라이드 | 내용 |
|---|---|---|
| fig_S3_timeline.png | S3 | 2024–2026 타임라인: Science(Costello)·선거의 해·EU AI Act 적용·NHB(Salvi)·Science(Hackenburg)·PNAS → 본 연구. 색: 학계=파랑, 규제/배경=청록, 본 연구=주황 |
| fig_S5_pge_loop.png | S5 | (π, G, E) 합성 처치 다이어그램 — 정책→배정→생성기→발화→사용자, 반응이 이력으로 되먹임되는 주황 화살표 |
| fig_S11_overlap_localization.png | S11 | ω_τ(h)=1/[4cosh²(h/2τ)] 정규화 밀도, τ=1→0.03에서 결정경계로 집중 (실제 수식으로 계산한 곡선) |

## 리포에서 복사해 온 그림 (5종, simulation/results 원본)

| 파일 | 슬라이드 | 내용 |
|---|---|---|
| bias_plot.png | S6 | naive 부호 반전 (+0.068 vs −0.294) |
| phase_diagram.png | S12 | (n, τ) 세 국면 지도 |
| continuous_h_battery.png | S13 | 추정량 6종 배터리 |
| collapse_curve.png | (선택, S8 보조) | 온도 붕괴 P1–P3 |
| label_error.png | (백업 B5) | 라벨 오차 강건성 |

## 수식 PNG (11종)

| 파일 | 슬라이드 | 내용 |
|---|---|---|
| eq_S7_prop1A.png | S7 (또는 백업 B1) | 반례쌍: 관측분포 인수분해 + π=0 ⟹ β 차이 q(c₂−c₁) |
| eq_S8_resultA.png | S8 | V_τ ≥ σ̲²·P(𝓗_δ)·e^{δ/τ} — 본편 낭독 수식 |
| eq_S9_AT.png | S9 | A-T 다턴 복리 하한 + 복리 조건 |
| eq_S11_overlap.png | S11 | ω_τ 정의 + β^ov 정의 |
| eq_S12_boundary.png | S12 | 닫힌형 경계 곡선 log E[1/p_τ] = log(1+τ·sinh(1/τ)) |
| eq_B1_hahn.png | 백업 B1 | Hahn bound 전문 + min(p,1−p) ≤ e^{−δ/τ} |
| eq_B3_threshold.png | 백업 B3 | 복리 임계: K=2 → 1.386 < 3.71 ✓ / K=8 → 4.159 > 3.71 ✗ |
| eq_B4_kernel.png | 백업 B4 | 커널 항등식 + ∫K=1 + E[ω_τ]=τf(0)/|Δ′(0)|(1+o(1)) |
| eq_aux_softmax.png | S5/S8 보조 | softmax 정책·p_τ 정의 |
| eq_aux_kish.png | 백업 | arm-specific Kish 유효표본 |
| eq_aux_counterexample.png | S10 | 반례 수치: IPW 1.792 ≈ ATE 1.798 ≠ β^ov 1.356 |

## 주의

- 수식 표기: 논문의 σ̲(밑줄 시그마)를 그대로 썼습니다. 슬라이드에서 더 쉬운 표기를 원하면 equations_source.md에서 `\underline{\sigma}`를 `\sigma_{\min}`으로 바꿔 재렌더.
- 재렌더 방법: `python3 build_eqs.py` (pdflatex 필요), 그림은 `python3 build_figs.py`.
- S4의 두 논문 헤더 캡처는 저작권 있는 지면이라 직접 캡처해 넣으세요 (Science/NHB 홈페이지 헤더 스크린샷).
