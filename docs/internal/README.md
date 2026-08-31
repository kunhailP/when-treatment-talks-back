# Internal record — not part of the replication package

Every file in this directory is a dated historical document. None of it
describes the current state of the project, and nothing here should be cited.

- Current source of truth: `theory/formal_framework.md` (v0.5)
- Current manuscript: `paper/tex/main.tex`
- What is verified where: the table in the top-level `README.md`

The files are kept rather than deleted because this project's corrections are
part of its record: several claims that appeared in early drafts were later
disproved by the project's own outputs, and the sequence in which that
happened is worth being able to reconstruct. Each file carries a banner
saying what superseded it, and the drafts additionally list which of their
claims did not survive.

## What is here

**Audits.** `review_packet_20260728.md`, `review_packet_20260730.md`,
`review_packet_20260825.md`, `errata_20260729.md`. The 8/25 packet is the
substantive one: it identified seventeen defects (C-1 to C-10 in the
manuscript, D-1 to D-7 in the theory), all resolved on 2026-08-31.

**Superseded drafts.** `draft_jci_v01.md`, `draft_jci_v02.md`, `outline.md`.
The v0.2 draft is the most misleading file in the repository if read without
its banner: it contains the exact-boundary claim, the `E[1/p] >= 42` lower
bound, the `>= 1.1e5` figure, and the zero-entropy headline, all of which
were later shown to be wrong or unsupported.

**Design history.** `design_evaluation.md`, `design_evaluation_v2.md`,
`design_decision_v3.md`, `project_plan.md`. How the two-paper split and the
2x2 factorial were arrived at.

**Presentation, 2026-08-26.** `slide_plan_20260826.md`,
`presentation_script_20260826.md`, `presentation_outline.md`,
`slide_assets/`. Worth one note: the slides incorporated the 8/25 audit while
the manuscript did not, so for five days the talk was more accurate than the
paper. That gap is what the audit trail is for.

**Reading notes.** `literature/`.

**`writing_rules_compliance.md`.** An internal list of phrasings deliberately
avoided in the manuscript. Kept for continuity, not for publication.

## Claims in this directory that are known false

Do not carry any of these forward.

| Claim | Where it appears | Status |
|---|---|---|
| The regime boundary tracks `log E[1/p_tau]`, an exact boundary | v0.2 draft, slide plan, old README | Disproved by this project's own CSVs. That line is the `n_eff = 1` contour, a necessary condition; measured onsets sit 3-5 nats above it |
| `E[1/p] >= 42` as a lower bound | v0.2 draft | It is the arithmetic ceiling of `k = 20`, not a bound. Clopper-Pearson gives `>= 7.2` |
| Every minority strategy needs `>= 1.1e5` conversations | v0.2 draft | That is the mean over seven strategies; the minimum is 77,473. The magnitude is set by the Dirichlet prior, not by data |
| Median per-context entropy of exactly zero | v0.2 draft, slides | A judge artifact. The second judge in this repository gives 0.286 |
| No regular estimator escapes the rate | v0.2 draft | Unproved when written. Now established, but as a minimax bound along drifting policy sequences (Prop. 4), which is a different statement |
| Multi-turn compounding of `42^3` | slide plan, script | Drops the `rho_min^2` and `p_delta` factors; `p_delta` is not estimated anywhere |
| `simulation/results/` figures reproduce | all pre-08-31 files | They did not: `continuous_h.py` seeded population targets from `hash()`, which Python salts per process. Fixed and regenerated |
