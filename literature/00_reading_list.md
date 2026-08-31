# Reading List (서지 검증 완료: 2026-07-22)

## 공식 세미나 5편 (각 논문이 최종 논문의 한 구성요소를 담당)

| # | 논문 | 게재 상태 | 담당 역할 | 데이터/코드 |
|---|---|---|---|---|
| 1 | Hackenburg, Tappin, Hewitt, et al. **The levers of political persuasion with conversational artificial intelligence.** *Science* (2025). DOI 10.1126/science.aea3884 · [arXiv:2507.13919](https://arxiv.org/abs/2507.13919) | Science 게재 | AI 정치설득의 최전선; 정보 밀도 = 핵심 지렛대; persuasion–accuracy trade-off | [github.com/kobihackenburg/scaling-conversational-AI](https://github.com/kobihackenburg/scaling-conversational-AI) |
| 2 | Salvi, Ribeiro, Gallotti, West. **On the conversational persuasiveness of GPT-4.** *Nature Human Behaviour* (2025). [s41562-025-02194-6](https://www.nature.com/articles/s41562-025-02194-6) | NHB 게재 | 개인화·다회차 대화 RCT; Study 0 재분석 대상 | 코드: [github.com/epfl-dlab/debategpt](https://github.com/epfl-dlab/debategpt) · 데이터: [huggingface.co/datasets/frasalvi/debategpt](https://huggingface.co/datasets/frasalvi/debategpt) (전략추출 스크립트 포함) |
| 3 | Imai, Nakamura. **Causal inference with generative artificial intelligence: Application to texts as treatments.** *JASA* (2026). [DOI 10.1080/01621459.2026.2689629](https://www.tandfonline.com/doi/full/10.1080/01621459.2026.2689629) · [arXiv:2410.00903](https://arxiv.org/abs/2410.00903) | JASA 게재 확정 | 정적 생성 텍스트 처치의 식별·추정 — 우리의 출발 경계선 | 소프트웨어: [gpi-pack](https://gpi-pack.github.io/) |
| 4 | Qian, Walton, Collins, Klasnja, Lanza, Nahum-Shani, Rabbi, Russell, Almirall, Murphy. **The microrandomized trial for developing digital interventions: Experimental design and data analysis considerations.** *Psychological Methods* 27(5) (2022). [arXiv:2107.03544](https://arxiv.org/abs/2107.03544) | 게재 (주의: 2021 아님) | turn-level randomization, causal excursion effect, WCLS | — |
| 5 | Dafoe, Zhang, Caughey. **Information equivalence in survey experiments.** *Political Analysis* 26(4): 399–416 (2018). [링크](https://www.cambridge.org/core/journals/political-analysis/article/information-equivalence-in-survey-experiments/8D134C6387CD7D845249B0712775AB79) | PA 게재 | information-locked generation의 이론적 근거; treatment integrity | — |

## 보조 필수문헌

- Chen, Kalla, Le. **Benchmarking political persuasion risks across frontier large language models.** [arXiv:2603.09884](https://arxiv.org/abs/2603.09884) (2026, preprint). n=19,145; 모델 간 이질성(정보형 프롬프트가 Claude·Grok ↑, GPT ↓) → generator transport estimand의 실증적 동기.
- Costello, Pennycook, Rand. **Durably reducing conspiracy beliefs through dialogues with AI.** *Science* 385 (2024). [DOI](https://www.science.org/doi/10.1126/science.adq1814) — 오정보 교정 도메인의 윤리적·실증적 선례.
- Tierney, Katta, Bail, Hillygus, Volfovsky. **A design-based solution for causal inference with text: Can a language model be too large?** [arXiv:2510.08758](https://arxiv.org/abs/2510.08758) (2025, preprint) — LLM 표현 기반 사후조정의 overlap bias; design-based 정신의 방증.
- Zeng et al. **Causal discovery and counterfactual reasoning to optimize persuasive dialogue policies.** [arXiv:2503.16544](https://arxiv.org/abs/2503.16544) · *Behaviour & Information Technology* (2025) — 비판 대상: policy optimization ≠ causal identification.
- Bai, Voelkel, Muldowney, Eichstaedt, Willer. **LLM-generated messages can persuade humans on policy issues.** *Nature Communications* 16 (2025). [s41467-025-61345-5](https://www.nature.com/articles/s41467-025-61345-5) — artifact effect의 대표.
- Matz, Teeny, Vaid, Peters, Harari, Cerf. **The potential of generative AI for personalized persuasion at scale.** *Scientific Reports* 14: 4692 (2024). [링크](https://www.nature.com/articles/s41598-024-53755-0)
- Boruvka, Almirall, Witkiewitz, Murphy. **Assessing time-varying causal effect moderation in mobile health.** *JASA* 113 (2018) — excursion effect와 WCLS의 원 논문. formal framework §2.3의 직접 기반.
- Robins. **A new approach to causal inference in mortality studies with a sustained exposure period.** *Mathematical Modelling* 7 (1986) — g-methods의 원류. Proposition 1에서 반드시 인용 (novelty 경계 설정).

## 읽기 순서 권고 (주차별 계획은 docs/project_plan.md)

1주차: Salvi + Hackenburg (현상과 데이터) → 2주차: Qian + Boruvka (설계 언어) → 3주차: Imai & Nakamura + Tierney (텍스트 처치의 식별) → 4주차: Dafoe (설계 세부) + Robins (이론 뿌리) → 상시: Chen–Kalla–Le, Costello, Zeng, Bai, Matz는 인용 목적 속독.
