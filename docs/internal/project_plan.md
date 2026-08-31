> ⚠️ **역사 기록 — 현재 상태가 아님.** 프로젝트 계획 (2026-07-30)
>
> **폐기됨.** 일정·목표가 이후 변경되었다 (JCI 트랙 확정, Study 0 부록 강등).
>
> 현재 진실 원천: `theory/formal_framework.md` (v0.5) · 현재 원고: `paper/tex/main.tex`
> 이 디렉터리는 replication package가 아니다 (`docs/internal/README.md` 참조).

---

# 실행 계획 v2 (2026-07-30 갱신 — W1–W2 완료, W3–W6 재편)

원칙: P0 없이는 발표가 서지 않는다. **8/26 산출물 = JCI-형 working paper (arXiv v1)** — 관측 로그의 정보 한계가 몸통, G-MRT는 해법 절 (docs/publication_map.md). 구 5주 계획(W1–W2 골격·재현)은 완료되어 역사 기록.

## 완료 (W1–W2, 7/22–8/3)
- formal_framework v0.4 잠금 (2×2, ρ=균등, Result A/B, 조건 (A1)–(A3), Kish n_eff)
- 시뮬 2종 검증 (naive 부호 반전 · temperature collapse P1–P3, ESS 층별 수정, --strict)
- Study 0 파이프라인 fixture 검증 · 세미나 #1 Hackenburg, #2 Salvi
- 외부 비판 3회 수용·검증 (errata_20260729, review_packet_20260730)

## W3 (8/4–8/10) — JCI 수학 객체 잠금 + 증명 완료 (증명을 "시작"하는 주가 아님)
- [P0] Prop 1A 반례쌍 완전 구성 (U 분포·두 DGP 결합 명세)
- [P0] Result B **1-D Laplace 증명** (H∈ℝ, f(0)>0, Δ′(0)≠0) — 다차원 coarea는 corollary로만
- [P0] Result A를 (A1)–(A3) 하의 정식 하한으로
- [P1] **[사용자 병목] 데이터 도착 시** Study 0-a/b 실행 (02 --strict, 06–08)
- 세미나 #3: Imai & Nakamura (설명형 덱)

## W4 (8/11–8/17) — JCI 시뮬레이션
- [P0] 연속 H 시뮬레이션: 주 DGP H~Uniform(−1,1), robustness N(0,1), β(H) 3종, 추정량 배터리, arm-specific Kish ESS·overlap mass
- [P0] **(n,τ) 위상도 figure** (x=1/τ, y=log n, 경계 log n≈δ/τ) — 논문 핵심 그림
- [P1] 라벨 측정오차 축 (q∈{0,.1,.2}) — Study 0 방어
- 세미나 #4: Qian

## W5 (8/18–8/23) — 실증·인프라 정리
- [P1] requery(07) 강화: 개인화 복원, manifest 호환성 검사, 실패 기록, judge 캐시 해시 (feasibility 지위 유지)
- [P1] 최소 테스트 골격: pytest numeric tests(1/p 버그 재발 방지), seed 관리, config (Docker/CI는 이연 합의)
- [P2] PA 트랙 준비 문서만: prereg N 확정(pilot 80–120, demo 180–250), 2×2 DGP 사양 (구현은 9월)

## W6 (8/24–8/26) — 통합
- [P0] JCI-형 working paper 10–15쪽 (paper/outline v0.3 순서) — 중심 메시지 1개 + 그림 4개(bias_plot, collapse_curve, 연속 H 배터리, 위상도)
- [P0] 발표자료 (outline v0.3 기준으로 presentation_outline 재작성)
- 세미나 #5: Dafoe → 8/26 최종 발표

## PA 트랙으로 이관 (9월 이후, publication_map 참조)
2×2 form×dose DGP · WCLS 추정기 · differential fidelity 시뮬 · 플랫폼 구현 · IRB · pilot(80–120) → demo(180–250) · generator transport
