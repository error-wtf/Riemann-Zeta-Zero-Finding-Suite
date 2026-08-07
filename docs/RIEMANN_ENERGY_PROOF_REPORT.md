# Riemann energy proof report

This report records the canonical proof-candidate architecture. The obsolete
one-sided trace diagnostic is not used by the full two-sided Volterra matching
route; independent mathematical review remains required.

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
| Xi-zero origin matching | PROVED under full two-sided Volterra identity | Xi difference identity + common ODE + reflected trace matrix |
| Global Green limit | PROVED under endpoint theorem hypotheses | finite oriented identities + endpoint limits |
| Global Weyl--Volterra contradiction | PROVED under stated analytic hypotheses | \(0=E_-+E_+>0\) for \(0<\operatorname{Im}\alpha<1/2\) |
| RH parameter/symmetry bridge | PROVED under global contradiction | \(s=1/2+i\alpha\), \(\Xi(-\alpha)=\Xi(\alpha)\) |
| RH | CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW | no public claim of accepted proof |

## Dependency warning

The repository contains an exploratory one-sided trace diagnostic that fails
for generic complex parameters. It is diagnostic only. The final
origin-matching step uses the independent full two-sided identity
\(u_- - u_+=e^{-i\alpha x}\Xi(\alpha)\), absolute convergence, the common
ODE, and the reflected-state convention; it does not use the one-sided
cosine/sine inequality.

The endpoint and matrix-production blocks are recorded with their stated
quantifiers. Together with full Volterra matching they close the internal
contradiction; independent mathematical review remains outstanding.

## Interpretation

Passing tests demonstrate implementation consistency and certificate
reproducibility. They are not a substitute for the missing analytic lemma or
for independent mathematical review.
