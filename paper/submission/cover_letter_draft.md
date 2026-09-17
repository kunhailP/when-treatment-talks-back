<!--
DRAFT. Every [TO CONFIRM] item must be checked by the author before submission.
Do not add suggested reviewers, funding, or affiliations that have not been confirmed.
-->

[TO CONFIRM: date]

Editors
Journal of Causal Inference

Dear Editors,

I submit the research article **"The exploration cost of boundary and population effects"** for consideration in the *Journal of Causal Inference*.

**Question.** Systems that assign treatments adaptively, including conversational AI systems that choose
persuasive strategies, generate logs in which the assignment policy is known but increasingly
deterministic. Analysts then face a design question before any estimation question: which causal
target can such logs deliver, and what must be paid to learn a different target?

**Main result.** The paper proves a separation between two causal targets **within a single outcome
model**, with the cost of learning measured on one scale: the deployer's cumulative exploration loss.
- Under a common softmax temperature that shrinks with the sample size, the effect at the policy's
  decision boundary admits asymptotically valid Wald inference while the exploration loss tends to zero.
- In the same model, outcome laws with equal boundary effects but different population average effects
  become indistinguishable whenever the exploration loss tends to zero.
- Uniformly consistent estimation of the population effect requires divergent worst-case exploration loss.

In a model without extrapolation structure, an information–exploration inequality valid for all
estimators and adaptive designs shows that uniform precision δ requires worst-case loss of order at
least (E√g)²/δ², independent of the sample size. For small fixed δ, one deterministic common
temperature requires loss of order at least n/log²(nδ²), whereas uniform mixing keeps it bounded.

**How this advances the discussion.** Limited overlap is known to make average effects hard to
estimate, and boundary estimands from algorithmic assignment are known (e.g. Narita and Yata). What the
paper adds is to place the two targets **in the same model and on the same cost scale**. It shows that
the choice of target determines the exploration a design must pay for, and draws consequences for a
design lever that practitioners use: temperature. The contribution is this comparison and its design
consequence. The paper does not claim novelty for any single ingredient, such as the boundary limit of
overlap weights, regret–estimation trade-offs in bandits, or cost-weighted allocation. The manuscript
positions each against the closest prior work.

**Fit with the journal.** The paper concerns research design, target-parameter specification,
identifiability and statistical estimation under known assignment. These are core topics of the
journal. The motivating application (political persuasion by conversational AI) links causal inference
with machine learning and political science.

**Scope.** The results concern one decision per unit with a known assignment policy. The boundary
results are one-dimensional and pointwise in the outcome law. The population-side impossibility excludes
models in which boundary data identify the population effect. These limits are stated in the abstract
and the introduction.

**Reproducibility.** No new data were collected. Simulation code, result files with seeds and code
commits, plain-text proofs, and the script that generates every reported number are available at
https://github.com/kunhailP/when-treatment-talks-back ([TO CONFIRM: tagged submission version]).

**Declarations.**
- This manuscript is not published and is not under consideration elsewhere. [TO CONFIRM]
- Related work by the author: [TO CONFIRM — e.g. whether an earlier version of this manuscript or a
  companion empirical/experimental paper has been posted or submitted anywhere; describe the
  relationship if so, or state that there is none].
- Conflicts of interest: [TO CONFIRM]. Funding: [TO CONFIRM].
- Use of AI-assisted tools: [TO CONFIRM against De Gruyter's policy; the manuscript contains a draft
  disclosure].
- Article processing charge: I intend to request a waiver or discount. [TO CONFIRM — see
  `apc_waiver_request_draft.md`; send to jci_editorial@degruyter.com at or right after submission.]

Thank you for considering this submission.

Sincerely,

Kunwoo Park
[TO CONFIRM: department], Kookmin University, Seoul, Republic of Korea
[TO CONFIRM: e-mail]
