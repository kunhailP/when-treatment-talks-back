# 리뷰 패킷 (2026-08-25) — 5차 감사: 외부 재현 기반 전수 검증

> **지위: 진입점 갱신.** 20260730판은 HISTORICAL. 이 라운드는 서술 검토가 아니라 **산출물 재실행·재계산 기반 감사**다. 아래 C절의 모든 수치는 리포의 실제 CSV를 다시 읽거나 코드를 다시 돌려서 얻었고, 각 항목에 재현 경로를 적었다.
>
> **한 줄 판정: 연구는 끝나지 않았다. 다만 남은 것은 새 연구가 아니라 (i) 원고 조립, (ii) 서술 정정 7건, (iii) 이론 1건의 실질적 유도다.**

---

## A. 통과 항목 — 재현으로 확인된 것

이 절은 방어 자산이다. 심사에서 공격받으면 여기를 근거로 답한다.

| 검증 | 방법 | 결과 |
|---|---|---|
| numeric test 7종 | `tests/test_numeric.py` 전체 실행 | **7/7 통과** (닫힌형 E[1/p], Kish, overlap kernel 항등식, Result B 극한 방향, Dirichlet floor, strict fixture) |
| 전 스크립트 컴파일 | `py_compile simulation/src/*.py analysis/src/*.py` | 통과 |
| 부호 반전 시뮬 | `simulation/results/results.csv` | truth +0.0684, naive −0.2938, coverage 0.0 — 본문 §7(i)와 일치 |
| 온도 붕괴 시뮬 | `temperature_collapse.py --nsims 5 --n 500` 재실행 | naive 편향 −0.144 → −0.778, coverage 0.80 → 0.00, occupancy 0.169 → 0.000 (단조) |
| Study 0-c 전량 | `fidelity_audit_summary.txt` | n=22,262+16,674+17,895=**56,831** ✓ · η²=.2001/.1196/.3171 ✓ |
| Study 0-a | `reproduce_summary.csv` | n=750, crude OR 2.176 (최대) ✓ |
| judge 신뢰도 | `judge_confusion.csv` 재계산 | 원자료 일치도 .9032, κ=.1295, both-modal 제외 시 κ=−.016 ✓ |
| 모델 비교 | `model_comparison.csv` | modal share .945/.973/.986 ✓ · 엔트로피 중앙값 0 ✓ |
| 위상 경계 닫힌형 | 해석적 + 구적 + MC | **E[1/p_τ] = 1 + τ·sinh(1/τ)** 기계정밀도 일치 ✓ · τ↓0 점근 1/τ+log τ−log 2 ✓ |
| Result A 부등식 | 손 유도 | min(p,1−p) ≤ e^{−δ/τ} ⟹ 1/p+1/(1−p) ≥ e^{δ/τ} — 대수 정확 ✓ |
| Result B 커널 항등식 | 손 유도 | ω_τ = σ(σ−1) = 1/[4cosh²(Δ/2τ)], ∫K=1 — 정확 ✓ (approximate identity 논증 유효) |
| 배터리 핵심 수치 | `continuous_h_results_uniform.csv` | τ=.045에서 HT SD **2.9509** ✓ · Hájek 편향 **.4589**/SD **.2990** ✓ — 본문과 정확히 일치 |

**Result B(1-D)는 감사에서 유일하게 깨지지 않은 결과다.** `proofs_w3_draft.md §3`의 증명은 각 단계가 닫혀 있다 (역함수정리 → v=τu 변수변환 → 지배수렴 → 비율). ω_τ가 **정확히** approximate identity 커널이라는 관찰은 실제로 새롭고 깔끔하다.

---

## C. 확정 결함 — 원본 산출물로 직접 확인함

> 각 항목은 리포 파일을 다시 읽거나 코드를 다시 돌려서 확인했다. 재현 경로를 그대로 적는다.

### C-1 [P0] `main.tex:630` "oracle AIPW does not rescue coverage" — **자기 데이터가 반박한다**

본문: *"oracle AIPW does not rescue coverage (Result A is not an IPW artifact)"*

`simulation/results/continuous_h_results_uniform.csv`, `n=32000`, `beta=kink`의 `aipw_oracle_cover_uncond`:

| τ | 1.0 | .6 | .4 | .3 | .22 | .15 | .11 | .08 | .06 | .045 |
|---|---|---|---|---|---|---|---|---|---|---|
| AIPW coverage | .955 | .973 | .935 | .960 | .953 | .950 | .973 | .985 | .985 | **.995** |
| AIPW SD | .0119 | .0119 | .0157 | .0173 | .0272 | .0610 | .1739 | 1.160 | 2.046 | 1.381 |

**AIPW의 coverage는 모든 τ에서 명목 이상이고, τ가 작아질수록 오히려 보수적이 된다.** AIPW가 구제하지 못하는 것은 coverage가 아니라 **정밀도**(SD가 .012 → 1.38로 116배 폭발)다. 문장이 인용하는 바로 그 코드가 문장을 반박한다.

- **수정**: "oracle AIPW does not rescue **precision** --- its SD inflates from 0.012 to 1.38 across the τ grid while remaining nominally covered; the information deficit is a variance-bound phenomenon, not an IPW artifact." (이렇게 쓰면 Result A와 **더** 정합적이다. 하한은 분산에 관한 진술이지 coverage에 관한 진술이 아니었다.)
- 재현: `pd.read_csv(...uniform.csv).query("n==32000 and beta=='kink'")[["tau","aipw_oracle_cover_uncond","aipw_oracle_sd"]]`

### C-2 [P0] `main.tex:648-651` 위상도 "실선을 따라간다" — **격자가 그렇게 말하지 않는다**

본문: *"The empirical regime classification over the (n,τ) grid tracks the exact solid boundary log E[1/p_τ]; the dashed δ/τ heuristic is visibly off at small τ."*

`classify()`를 원본 그대로 적용해 재구성한 국면 격자 (uniform/kink, n=125…32,000):

| τ | .045 | .06 | .08 | .11 | .15 | .22 | ≥.30 |
|---|---|---|---|---|---|---|---|
| n=125 | 편향안정 | 편향안정 | 편향안정 | 분산폭발 | 분산폭발 | 분산폭발 | 추정가능 |
| n=4,000 | 편향안정 | 편향안정 | 분산폭발 | 분산폭발 | **추정가능** | 추정가능 | 추정가능 |
| n=32,000 | 편향안정 | 분산폭발 | 분산폭발 | 분산폭발 | 추정가능 | 추정가능 | 추정가능 |

경계 위치 비교 (log n 단위):

| τ | 실선 log E[1/p_τ] | 점선 1/τ | 실제 추정가능 전이 |
|---|---|---|---|
| .22 | 2.43 | 4.55 | **5.52** (n=125→250) |
| .15 | 4.09 | 6.67 | **8.29** (n=2,000→4,000) |
| .11 | 6.19 | 9.09 | **격자 내 없음** (n=32,000에서도 분산폭발) |

- **실선은 실제 경계보다 3.4–4.2 log 단위 아래**에 있다. τ=.15에서 실선은 n≈60이면 추정 가능하다고 예측하지만 실제 전이는 n≈4,000이다 (66배).
- **점선이 실선보다 모든 τ에서 더 가깝다** — 본문 주장의 정반대.
- 근본 원인은 **경계 기준식에 정밀도 상수가 빠진 것**이다. `log n = log E[1/p_τ]`에는 σ²/SE²가 없다. 같은 리포의 n_req 식은 ×2500(σ²=1, target SE=.02)을 곱한다. 그래서 §4.4는 같은 문맥에 "10⁵ 대화 필요"라 하고 `effective_temperature.csv`의 `implied_log_n_boundary`는 3.74(=n≈42)라 한다. **두 장치가 같은 대상에 3자릿수 다른 답을 낸다.**
- **수정**: (a) 경계를 `log n = log E[1/p_τ] + log(σ²/SE²)`로 정의하고 그 상수를 본문에 명시, 또는 (b) 실선을 "정성적 붕괴 척도"로 강등하고 "tracks"를 빼기. **어느 쪽이든 캡션의 "exact boundary"는 유지 불가** — 닫힌형은 정확하지만 *경계 기준*은 정확하지 않다. 세 국면의 존재와 τ 순서는 격자가 잘 지지하므로 그림 자체는 살아 있다.
- 재현: 본 문서 하단 스니펫

### C-3 [P0] `main.tex:493-495` Prop A-T 적용 — **자기 수치에서 조건이 깨진다**

Prop A-T는 τ < δ/log(K²/p_δ), 즉 **Δ/τ > log(K²/p_δ)**일 때만 복리한다.
`analysis/strategy_taxonomy.md`의 K = 8 (FACT/SOCR/COMG/SRCT/EMPA/REBT/CLAIM/META) ⟹ K² = 64 ⟹ 임계값이 최선의 경우(p_δ=1)에도 **log 64 = 4.159**.
`effective_temperature.csv`의 측정 중앙값은 **Δ̂/τ = 3.71**.

**3.71 < 4.159.** 턴당 계수 = 42/64·p_δ < 0.66 — 논문 자신의 헤드라인 수치에서 A-T는 복리가 아니라 **감쇠**한다. 그런데 본문은 *"via Proposition A-T the per-turn stratum factor E[1/p] ≥ 42 compounds across turns"*라고 쓴다. 심사자가 한 줄로 계산해 볼 수 있는 항목이다.

- **수정**: 이 문장을 삭제하거나, K를 대비에 관여하는 2팔로 환원(K=2 ⟹ 임계 log 4 = 1.386, 여유 있게 통과)하고 **그 환원을 명시**한다. 후자가 맞고 `nonidentification_note`의 "K-행동은 대비에 관여하는 두 팔로 환원" 규칙과도 일치하지만, **tex에는 그 환원이 적혀 있지 않다.**

### C-4 [P0] `main.tex:478` "every minority strategy ≥ ~1.1×10⁵" — **거짓**

| 파일 | 최소 소수전략 n_req |
|---|---|
| `policy_entropy_by_strategy.csv` (7B judge) | **FACT 77,473** |
| `..._mistral_judge32b.csv` | **COMG 88,609** |
| `..._phi_judge32b.csv` | **COMG 102,588** |
| `..._judge32b.csv` (Qwen/32B) | COMG 113,603 ✓ |

네 파일 중 하나만 주장을 만족한다. 1.1×10⁵은 사실 Qwen/7B 소수전략 7개의 **평균**(111,708)이며, 최솟값으로 보고되었다. 초록의 *"≥10⁵ conversations for **any** minority-strategy contrast"*도 같은 문제를 상속한다.

- **수정**: "on the order of 10⁵ (7.7×10⁴–1.2×10⁵ across judges and models)". 초록은 "conversation counts on the order of 10⁵".
- **추가 공개 필요**: SOCR·SRCT는 `mean_p_raw = 0.0000`이라 그 n_req는 **Dirichlet α=0.5와 K=8이 만든 값**이지 데이터의 값이 아니다 (0.5/(20+4) = 0.0208). 방향 hedge는 있으나 **크기가 prior가 정한다는 사실**은 공개되어 있지 않다.

### C-5 [P1] `main.tex:518` moral reframing "1.6--2.1" — 실제 1.6–2.2

`fidelity_audit.csv`: 1.620 (study 1) / **2.237** (study 2) / 2.086 (study 3). study 2의 최댓값이 빠졌다. → **1.6--2.2**로 수정.

### C-6 [P1] `main.tex:520` valence 준수율 선택 보고

`fidelity_audit_summary.txt`에는 study 1 = **0.727**과 study 3 = **0.896**이 둘 다 있다. 본문은 *"Where compliance flags exist, valence compliance is 72.7% (study 1)"* — 낮은 쪽만 보고하고, 표현이 마치 study 1에만 플래그가 있는 것처럼 읽힌다. study 3에는 `grammar .992`, `ontopic .966`도 있다.

같은 파일에서 유리한 숫자를 빼고 불리한 숫자만 싣는 것은 발견되는 순간 **다른 모든 수치의 신뢰도를 함께 깎는다.** → 둘 다 보고: "72.7% (study 1) and 89.6% (study 3)".

### C-7 [P0] `references.bib`에 `TODO:` 문자열 3건 — **PDF에 인쇄된다**

`plainnat`은 `note` 필드를 조판한다. 현재 상태로 컴파일하면 참고문헌에 이렇게 찍힌다:

> Hackenburg, Tappin, et al. The levers of political persuasion… *TODO: complete author list from published version*

- `references.bib:9` (hackenburg — **가장 중요한 인용**), `:89`, `:216`
- **수정**: 저자 목록을 채우고 `TODO:` 문자열 제거. 제목 각주의 *"none are placeholders"*와 직접 충돌한다.

### C-8 [P0] 부록이 없는데 부록을 두 번 참조한다

`main.tex`에 **`\appendix`가 없다.** 그런데:

- `:342` *"The self-contained derivation of the quoted efficiency bound is **deferred to the appendix**"*
- `:381` *"The multivariate coarea version remains at **appendix**/conjecture status"*

그리고 네 개 결과의 증명 상태:

| | 증명 환경 | 상태 |
|---|---|---|
| Prop 1 (지지집합 실패) | **없음** | 반례가 본문 산문으로 흐름 |
| Prop 2 (Result A) | `proof` 4줄 | Hahn 인용만 |
| Prop 3 (A-T) | `proof sketch` | 인용 하한 미유도 |
| Prop 4 (Result B) | `proof idea` | 전문은 `theory/proofs_w3_draft.md`(한국어) |

**방법론 저널에 번호 붙은 명제를 내면서 증명이 원고 밖에 있는 것은 그 자체로 desk-reject 사유다.** 전문은 이미 존재하므로 이것은 연구가 아니라 **번역·조립 작업**이다.

### C-9 [P0] `main.tex:120-126` Imai 문단 — 사실 오류 + 논문 혼동 (원출처로 확인)

본문: *"\citet{imai2026causal} identify effects of generated texts as fixed objects; ordering effects within a fixed object involve no human-feedback loop and **no positivity problem**."*

원논문(arXiv:2410.00903 = JASA 2026, Imai & Nakamura)을 직접 확인한 결과:

> **Lemma 1 (OVERLAP)**: Under Assumptions 3–5, for any t ∈ {0,1} and u ∈ 𝒰, P(T_i = t | U_i = u) > 0.
> 저자들은 **분리가능성(가정 5)이 overlap을 함의하는 핵심 조건**이며, 이것이 외삽 없는 식별을 가능하게 한다고 명시한다.

즉 **그 논문의 중심 기술적 성취가 정확히 positivity를 확보하는 것**이다. "no positivity problem"은 반대로 쓴 것이다.

**추가로 발견된 것 — 두 논문이 섞였다.** `docs/internal/outline.md:12`은 이렇게 적고 있다:

> `Nakamura & Imai 2026 "dynamic": 고정된 객체 내부의 순서 효과, 인간 피드백 없음, positivity 문제 없음`

이 서술은 **다른 논문**(Kentaro Nakamura, *GenAI Powered Dynamic Causal Inference with Unstructured Data*, arXiv:2605.07834)에 대한 메모인데, tex에서 `imai2026causal`(JASA 텍스트-처치 논문)의 인용키에 붙었다. 저자 순서는 `references.bib`이 **맞다** (Imai, Kosuke and Nakamura, Kentaro — arXiv·JASA와 일치).

**그리고 그 dynamic 논문은 `references.bib`에도 `main.tex`에도 없다.** 제목만 보면 우리 연구와 가장 가까운 선행연구다. 인용 없이 지나가면 "가장 가까운 논문을 모른다"가 된다.

- **수정 (2단계)**:
  1. **먼저 arXiv:2605.07834를 읽어라.** 우리 기여 경계가 이 논문에 달려 있다. (2026-08-25 기준 이 세션에서 본문 확보 실패 — 직접 받아 확인 필요)
  2. 문단 교체:
     > Imai and Nakamura (2026) establish identification for generated texts as **fixed** treatment objects; their key device is a deconfounder f(R) whose separability restores the overlap their Lemma 1 requires. **Our setting differs in what fails and whether it can be repaired.** Their overlap failure is representational --- the treatment information is entangled in R, and discarding the entangled part recovers positivity. Ours is behavioral: the counterfactual utterance was never generated, so there is nothing to discard. The boundary is structural, not a matter of better representation learning.
  - 이 서술은 방어 가능하고, 상대 논문을 **딛고** 올라선다. 현재 문장은 심사자를 만들어내는 문장이다 (Imai는 JCI 심사위원 1순위).

### C-10 [P1] `main.tex:627` vs `:642` 표본크기 모순

본문 *"At n = 32,000"* ↔ 같은 배터리의 그림 캡션 *"at n = 4,000"*. 둘 중 하나가 틀렸다.

---

## D. 이론 감사 — 심사자가 먼저 칠 순서

> 이 절은 재계산이 아니라 논증 검토다. C절보다 확실성이 낮지만 무게는 더 크다.

**D-1 [최우선] Result A는 다른 estimand의 하한을 인용한다.**

`formal_framework.md:49`의 일차 estimand:

> β_t^form = E[Y^{(F_t=assertive, D_t~ρ, 이후~ρ),G} − Y^{(...interrogative...)} **| I_t=1**]

가용성 조건부, **커널 개입** 하, **이후 턴을 π^dep에서 ρ로 교량**한 양이다. 그런데 `main.tex:277-282`의 증명은 Hahn(1998)의 **ATE** 하한 E[σ₁²/p + σ₀²/(1−p) + (β(H)−β)²]를 그대로 삽입한다. Hahn의 정리는 i.i.d. 단일시점 비교란 모형의 E[Y(1)−Y(0)]에 대한 것이다. **I_t와 ρ-continuation이 `formal_framework`와 `main.tex` 사이에서 조용히 사라진다.** 인과 excursion 효과의 효율 하한(Boruvka et al. 2018 계열)은 참조정책 가중과 continuation 항을 달고 나온다.

리포 자신의 위임 결정도 이걸 인정한다: *"Result A는 Hahn(1998) 인용 형태(자기완결 유도는 appendix 후보)"*.

이것이 남은 **유일한 실질 연구 과제**다. 필요한 것: **β_t(a,a′;ρ)의 효율적 영향함수를 유도하고, 그것이 Hahn 형태로 환원됨을 보이는 것.** 되면 Result A는 닫히고, 안 되면 Result A를 "단일턴 ATE의 하한"으로 강등하고 excursion이라는 말을 빼야 한다. 부록에 들어갈 §A가 정확히 이것이다.

**D-2 고정 τ 하한과 τ에 대한 rate 주장이 초록에서 섞인다.**

Prop 2는 **각 고정 τ**에 대한 진술이고, convolution 정리는 그 고정 τ에서 정규추정량을 제약한다. 초록의 *"no regular estimator in the nonparametric class escapes **the rate**"*는 τ_n ↓ 0인 표류수열에 대한 진술이고 local-asymptotic-minimax 논증을 요구한다 (Khan & Tamer 2010, *Econometrica*의 irregular identification이 직계 선행연구인데 **미인용**).

`theory/nonidentification_note.md:36`이 이미 규율을 적어놨다: *"이 하한은 고정 τ 점근 분산에 관한 것이고 … 두 주장을 섞지 않는다."* **초록이 그 규율을 어긴다.** 가장 싼 수정: 초록에서 "the rate"를 빼고 고정 τ 진술로 되돌리기.

**D-3 convolution 정리의 가정이 하나도 검증되지 않는다.**
`main.tex`와 이론 3파일 전체에서 pathwise differentiability, V_τ < ∞, strict overlap, LAN에 대한 언급이 **0회**다. 특히 V_τ = ∞이면 모수가 pathwise differentiable하지 않아 하한이 sharp가 아니라 vacuous가 된다. 그리고 정리는 **정규(regular)** 추정량만 덮는데, 논문 자신이 선호하는 overlap 가중이 바로 그 정리가 덮지 않는 비정규 탈출구다 (`:635-639`이 그 안정성을 자랑한다).

**D-4 Prop 1A의 가정이 논문 자신의 모형에서 공집합이다.**
1A는 π^dep = **정확히 0**을 요구한다. 그런데 `main.tex:234-238`은 정책을 softmax로 모형화하고, `nonidentification_note.md:25`는 *"τ > 0이면 … 형식적 positivity와 형식적 식별은 성립한다"*고 인정한다. 정확한 0을 만드는 기제 — **greedy decoding, top-k/top-p 절단, 제약 디코딩, 하드 필터** — 는 리포 어디에도 언급이 없다 (grep 결과 0건). **이것이 가장 값싼 수정이다**: 한 문단이면 1A의 가정이 실제 배치에서 채워진다.

**D-5 Result B는 `main.tex`에서 잘못 진술되어 있다.**
- `proofs_w3_draft.md:76`의 **(B4) f(0) > 0이 tex 가정 목록에서 빠졌다.** 없으면 결론 E[ω_τ] = τf(0)/|Δ′(0)|(1+o(1))이 0 = o(τ)로 퇴화한다. **인쇄된 명제가 거짓이다.**
- 가정은 "isolated simple root**s**"(복수)인데 결론은 "**a point mass**"(단수). 복수 근에서는 Σⱼ wⱼδ_{rⱼ} 혼합이다 — `proofs_w3_draft.md:102-104`는 이걸 맞게 적었다.
- 근 집합의 **유한성**이 tex에서 빠졌다.
- 꼬리 조건 (B2′)가 세 파일에서 세 가지로 다르게 적혀 있고, tex 버전(단일 r, 복수 근)이 깨진 것이다.

**D-6 β^ov의 실질 주장 하나가 반례를 가진다.**
`:390-394`는 *"a regulation, a guardrail, a reward-model update, **a temperature change**"* 모두에 대해 β^ov가 1차 항이라고 한다. 점수 섭동 Δ→Δ+εg에서 ∂p/∂ε = ωg/τ이므로 이는 **g가 h에 상수일 때만** 성립한다. 특히 명시된 온도 변화에서는 ∂p/∂τ = −ωΔ/τ²이고, **ω(h)|Δ(h)|는 경계에서 0**이다(|Δ|≈2.4τ에서 최대). β^ov는 그 문장이 이름을 댄 바로 그 섭동의 1차 항이 아니다.
→ "uniform score shifts"로 한정하거나 목록에서 온도를 빼라.

**D-7 Remark A′의 지위가 문서마다 다르다.**
`draft_jci_v02.md:169`: *"the factorization argument is a **sketch pending** the multi-turn envelope result"*. 그런데 `main.tex:91`은 *"with bounds that **transfer a fortiori**"*라고 사실로 쓴다. `temperature_collapse.md:47`은 그 envelope 항목을 **여전히 미해결 TODO**로 올려두고 있다.

---

## E. 오탐 — 무시할 것

감사 과정에서 파일 일부만 옮겨 생긴 착시다. **원본에는 전부 존재한다. 대응 불필요.**

- `paper/tex/figs/` 4개 PNG 없음 → **있다** (bias_plot, collapse_curve, continuous_h_battery, phase_diagram, 전부 7/30 생성)
- `simulation/results/continuous_h_results_uniform.csv` 없음 → **있다** (167,977 bytes)
- `analysis/src/01_download.py`, `06_extract_contexts.py`, `07_requery.py` 없음 → **있다**
- Imai 저자 순서가 틀렸다 → **맞다** (Imai, Kosuke and Nakamura, Kentaro — arXiv·JASA와 일치)

---

## F. 남은 작업

### P0 — arXiv v1 전 (기계적, 1–2일)

- [ ] C-7 `references.bib`의 `TODO:` 3건 제거 + hackenburg 저자 목록 완성
- [ ] C-9 Imai 문단 교체 (**단, arXiv:2605.07834를 먼저 읽을 것**) + 그 논문 bib 추가·인용
- [ ] C-1 AIPW 문장을 coverage → precision으로 수정
- [ ] C-2 위상도 "tracks"·"exact boundary" 문구 수정 (정밀도 상수 명시 또는 강등)
- [ ] C-3 A-T 적용 문장 삭제 또는 K=2 환원 명시
- [ ] C-4 n_req 하한 "1.1×10⁵" → "10⁵ 규모(7.7×10⁴–1.2×10⁵)"; 초록도 함께
- [ ] C-8 `\appendix` 신설 — §A Result A 유도, §B A-T 자기완결, §C Result B 전문, §D coarea(추측으로 명시). `proofs_w3_draft.md` 번역·조립
- [ ] C-10 n=32,000 / n=4,000 모순 해결
- [ ] `\author` / `\thanks` 실명·소속, `\date` 갱신
- [ ] **Limitations 절 신설** — 대리모델 치환, REBT 동어반복 위험, judge 신뢰도 범위, k=20 절단, 고정 τ vs rate, Study 0-c는 원저자 파생변수 사용
- [ ] **Data & Code Availability 문장** (URL/DOI)
- [ ] C-5, C-6 수치 정정

### P1 — JCI 투고 전 (실질 작업)

- [ ] **D-1: β_t(a,a′;ρ)의 효율적 영향함수 유도** ← 남은 유일한 진짜 연구 과제
- [ ] D-2 초록에서 "the rate" 제거 또는 LAM 논증 추가 + Khan & Tamer (2010) 인용
- [ ] D-4 절단 샘플링(greedy/top-k/top-p) 한 문단 — 1A의 가정을 실제 배치에 착지
- [ ] D-5 Result B 명제 재진술 ((B4) 복원, 단일근+따름정리, 유한성, (B2′) 통일)
- [ ] D-6 β^ov 1차 항 주장을 uniform shift로 한정
- [ ] **k=200 재질의** (7B 모델 로컬, 주말 작업) — 58–89.5% 우측절단을 제거. 현재 Δ̂/τ 중앙값 3.71은 **모든 모델에서 log(41)로 산술적으로 강제된 값**이라 모델 정보가 0이다. 이걸 풀면 가장 약한 절이 가장 흥미로운 절이 된다
- [ ] Mistral·Phi에 2차 judge 실행 (현재 judge 민감도는 Qwen만 있음)
- [ ] **REBT 동어반복 방어**: rebuttal 턴을 뽑아 judge가 REBT라 라벨한 것이므로, REBT 제외 시 또는 rebuttal 내부 분할(form×dose) 시에도 엔트로피 결과가 살아남는지 보이기. 못 하면 Table 2는 부록행
- [ ] Kennedy(2019) incremental intervention을 estimand 측 대안으로 정면 대응하는 한 문단
- [ ] 인간 이중코딩 200턴 (κ≥0.6은 이미 본문 `:505`에 공약됨)
- [ ] 재질의 **생성 온도**와 **1–2문장 프롬프트 제약**을 본문에 공개 (온도가 주제인 논문에서 자기 실험 온도가 미기재)
- [ ] `qian2022microrandomized` 저자 정정 (Almirall 오기재, Maureen A. Walton·Hyesun Yoo 누락)
- [ ] 미인용 3건 정리: `bai2025llm`, `matz2024potential`, `zeng2025causal`

### P2

- [ ] 버전관리 복구 — 현 폴더는 `when-treatment-talks-back 2`이고 **`.git`이 없다**. 7/30 이후 이력 없음
- [ ] 제목 확정 (20260730 packet D-1 미결)
- [ ] envelope 정리 (열린 문제로 표기되어 있어 무방)

---

## G. 판정

**arXiv v1**: P0 12건. 전부 기계적·서술적이며 새 연구가 필요 없다. **1–2일.**

**JCI 투고**: 아직 아니다. 결정적인 것은 두 개다 —
1. **부록이 없어 네 개 명제 중 어느 것도 원고 안에 완결된 증명이 없다.** 조립 작업이지만 필수다.
2. **Result A가 excursion estimand가 아니라 ATE의 하한을 인용한다.** 이건 조립이 아니라 유도다.

셋째로 무거운 것은 Study 0-b다. 대리모델 + REBT 동어반복 + 417개 표본 위의 κ≈0이 곱해진다. 셋 중 둘(k=200, 2차 judge)은 각각 주말 하나면 되고, REBT 건은 생각이 필요하다.

**연구가 끝났는가**: 이론의 뼈대와 시뮬레이션은 섰다. Result B는 깨끗하고 새롭다. 위상도의 닫힌형 경계는 실제 기여다. 반례로 오독을 선제 차단한 `:403-410`은 심사자 신뢰를 버는 종류의 자기규율이다. **끝나지 않은 것은 D-1 하나와, 원고가 아직 조립되지 않았다는 사실이다.**

---

## 부록 — 재현 스니펫

```python
import pandas as pd, math
d = pd.read_csv("simulation/results/continuous_h_results_uniform.csv")
sub = d[(d.dgp=="uniform") & (d.beta=="kink")].copy()

def classify(row):                                   # continuous_h.py:161 원본
    ref = abs(row["ate"]); rb, sd = row["hajek_bias"]/ref, row["hajek_sd"]
    if abs(rb) >= 0.20 and sd < abs(row["hajek_bias"]): return "biased-stable"
    if abs(rb) <= 0.10 and row["hajek_cover_uncond"] >= 0.85: return "estimable"
    return "variance-explosion"

sub["regime"] = sub.apply(classify, axis=1)
print(sub.pivot_table(index="n", columns="tau", values="regime", aggfunc="first"))

for t in sorted(sub.tau.unique()):                   # C-2 경계 비교
    solid = math.log(1 + t*math.sinh(1/t))
    est = [n for n in sorted(sub.n.unique())
           if (sub[(sub.tau==t)&(sub.n==n)].regime == "estimable").any()]
    print(f"tau={t}: solid={solid:.2f} dashed={1/t:.2f} "
          f"empirical={math.log(min(est)) if est else float('nan'):.2f}")

# C-1
print(sub[sub.n==32000][["tau","aipw_oracle_cover_uncond","aipw_oracle_sd"]])
```
