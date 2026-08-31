# Working Paper Outline (v0.3 — JCI-형, 10–15쪽, 8/26 arXiv v1 목표)

제목: When the Treatment Talks Back: Information Limits of Observational Logs from Adaptive Generative Political Communication (가제 — "Design-Based Causal Inference..." 부제 유지 여부는 W6 결정)

**이 outline은 JCI 논문의 골격이다 (docs/publication_map.md). G-MRT는 §5 해법 절로 등장하고, PA 실험 본체는 companion paper. Contribution = formal_framework §0의 1–2번 + 해법으로서의 3번 요약. 절대 늘리지 않는다.**

1. Introduction (2쪽)
   - 훅: Salvi/Hackenburg/Chen-Kalla-Le + 메타분석(g=0.02, I²=76% — 분해의 필요)
   - Hackenburg의 RM = turn-level 적응 정책 = 최강 지렛대의 내부가 블랙박스
   - 기여 3줄 (JCI 버전: estimand 체계 · overlap collapse and localization · 설계 처방)
2. **Related Work (1쪽) — 첫 단락에서 선 긋기 (필수)**
   - Nakamura & Imai 2026 "dynamic": 고정된 객체 **내부의 순서** 효과, 인간 피드백 없음, positivity 문제 없음 ↔ 우리: **인간 반응 피드백 루프 위의 적응 정책**, overlap collapse가 핵심
   - **OPE/deficient support (v0.2 신설 — 필수)**: Sachdeva–Su–Joachims 2020, Dudík 2011, Thomas & Brunskill 2016 ↔ 우리: 추정량 수준이 아닌 **efficiency bound 수준의 rate**, τ-지수화·닫힌형 위상 경계, 국소화(β^ov 극한 특성화 — OPE에 대응물 없음), 처방이 추정량이 아니라 **설계**
   - MRT(Qian/Boruvka): 사전정의 이산 행동 ↔ 우리: 생성 커널 + ill-defined labels
   - Stochastic interventions(Kennedy/Díaz): 정적 커널 ↔ 우리: 이력의존 생성커널 + 결정성 붕괴
   - Overlap weighting(Li–Morgan–Zaslavsky): β^ov의 준거
   - Dafoe: information equivalence → form/dose 분리 설계로 재해석
3. Generative Treatments (2쪽) ← framework §1–2 (2×2 표기 그대로)
4. Why Transcripts Are Not Enough (2–3쪽) ← **Prop 1A(반례쌍 완성) + Result A(정식 하한, Hahn 1998) + Result B(β^ov; 1-D Proposition — 증명 완료 2026-07-30) + 반례("고정 τ에서 target 불변") + (n,τ) 위상도 figure(phase_diagram.png 산출 완료)** + Study 0-a/c (동기화 언어)
5. The G-MRT Design as the Remedy (2쪽) ← framework §4 (fidelity 규약 포함; 실증은 companion으로 예고)
6. Estimation (1쪽): WCLS (known ρ), DR — scope 문장 포함
7. Simulation Evidence (2쪽) ← simulation/README 대응표 그대로: 2-상태 collapse(P1–P3, **"경계 estimand 이행" 서술 금지 — 편향-안정 국면으로 서술**) + 연속 H 배터리 + 위상도
8. Empirical Plan & Ethics (1쪽) · 9. Discussion (1쪽): 강등 목록 각 1단락 (transport/GPI/동시추론/policy learning) + PA companion 예고

집필 규칙: 각 절은 대응 문서에서만 가져온다. "theorem" 금지, "establishes" 금지(Study 0), "필연/inevitable" 금지(Prop 1A는 "structurally frequent and design-reinforced"), Result B = Conjecture 라벨 유지(1-D approximate-identity 증명 완료 시 Proposition 승격). §3은 일반 행동공간 𝒜로 서술하고 2×2는 running example(PA 구현)로만. §5의 Result 5는 illustrative trade-off 지위 — 독립 정리로 쓰지 않는다. 핵심 정리는 3개: support failure · efficiency-bound collapse · overlap localization. §7 지표 규율: Kish ESS(이론 객체)와 cell occupancy(희귀 crossover 진단)를 구분해 표기, E[p(1-p)]가 Result B 검증 객체, coverage는 conditional/unconditional 병기.
