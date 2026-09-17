<!--
DRAFT. Every [TO CONFIRM] item must be checked by the author before submission.
Do not add suggested reviewers, funding, or affiliations that have not been confirmed.
-->

[TO CONFIRM: date]

Editors
Journal of Causal Inference

Dear Editors,

I submit the research article **"The exploration cost of learning boundary and population causal effects"** for consideration in the *Journal of Causal Inference*.

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

**Scope.** The results concern one decision per unit with a known assignment policy and a score that
is not learned from outcomes. The boundary results are one-dimensional; boundary coverage holds uniformly
over a model with Gaussian outcomes and Lipschitz mean functions. The separation requires an operational
cost that vanishes at the decision boundary: with a fixed cost per deviation, boundary inference under a
common-temperature design also incurs divergent loss. The population-side impossibility excludes models in which boundary data
identify the population effect. These limits are stated in the abstract and the introduction.

**Reproducibility.** No new data were collected. Simulation code, result files with seeds and code
commits, plain-text proofs, and the script that generates every reported number are available at
https://github.com/kunhailP/exploration-cost-boundary-population (tagged submission version jci-submission-v1).

**Declarations.**
- The manuscript has not been published previously, in any language, and is not under simultaneous
  consideration by another journal. No preprint has been posted.
- Related work by the author: [TO CONFIRM — state that there is none, or describe any related
  submission].
- Conflicts of interest: none. Funding: this research received no external funding.
- Use of AI-assisted tools: [TO CONFIRM against De Gruyter's policy; the manuscript contains a draft
  disclosure].

Thank you for considering this submission.

Sincerely,

Kunwoo Park
Department of Political Science and International Relations, Kookmin University
77 Jeongneung-ro, Seongbuk-gu, Seoul 02707, Republic of Korea [TO CONFIRM postal address]
pkw6094@kookmin.ac.kr · ORCID 0009-0007-9067-8964
