# Riemann energy proof report

This report records a conditional proof architecture, not an RH proof. Status
labels are dependency-aware: any statement depending on the unresolved
one-sided trace implication is explicitly marked conditional.

## Status table

| Lemma | Status | Evidence |
|---|---|---|
| Theta derivative tails | PROVED on certified boxes | Arb artefacts |
| Compact profile bounds | PROVED outward-rounded | compact certificate |
| Far remainder bounds | PROVED outward-rounded | far certificate |
| Profile/Schur production certificates | PROVED | compact, far, and Sturm artefacts |
| Matrix residual identification | PROVED | exact right/left symbolic identities and Schur match |
| Algebraic Green matching | PROVED under matched traces | symbolic matrix test |
| Xi transform identity | PROVED_FROM_SOURCE_MELLIN_FORMULA | source equation 2.2.1, \(x=\log t\) |
| Trace existence | PROVED_UNDER_SOURCE_PROFILE_AND_OPEN_STRIP | analytic weighted-source majorant |
| Endpoint flux for each fixed finite alpha, \(0<\operatorname{Im}\alpha<1/2\) | PROVED under stated hypotheses | convex-tail theorem + certified far bounds |
| Strict nondegeneracy | PROVED under stated hypotheses | positive source + inhomogeneous ODE + positive production |
| Xi-zero origin matching | CONDITIONAL_ON_TRACE_CLOSURE | Xi difference identity + reflected trace matrix |
| Global Green limit | CONDITIONAL_ON_TRACE_CLOSURE | finite oriented identities + endpoint limits |
| Global Weyl--Volterra contradiction | CONDITIONAL_ON_TRACE_CLOSURE | \(0=E_-+E_+>0\) for \(0<\operatorname{Im}\alpha<1/2\) |
| RH parameter/symmetry bridge | CONDITIONAL_ON_GLOBAL_CONTRADICTION | \(s=1/2+i\alpha\), \(\Xi(-\alpha)=\Xi(\alpha)\) |
| RH | CANDIDATE_PENDING_TRACE_CLOSURE_AND_INDEPENDENT_REVIEW | no public claim of accepted proof |

## Dependency warning

The repository contains an exploratory one-sided trace diagnostic that fails
for generic complex parameters. The final origin-matching step therefore may
not be labelled unconditionally proved unless either:

1. the required trace implication is proved for the actual matched
   (Xi)-zero parameters; or
2. a separate origin-matching argument is supplied that does not use that
   implication.

The endpoint and matrix-production blocks are recorded with their stated
quantifiers. They do not, by themselves, close the RH contradiction.

## Interpretation

Passing tests demonstrate implementation consistency and certificate
reproducibility. They are not a substitute for the missing analytic lemma or
for independent mathematical review.
