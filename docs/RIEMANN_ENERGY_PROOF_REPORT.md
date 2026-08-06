# Riemann energy proof report

This report records a conditional proof architecture, not an RH proof.

## Status table

| Lemma | Status | Evidence |
|---|---|---|
| Theta derivative tails | PROVED on certified boxes | Arb artefacts |
| Compact profile bounds | PROVED outward-rounded | compact certificate |
| Far remainder bounds | PROVED outward-rounded | far certificate |
| Profile/Schur production certificates | PROVED | compact, far, and Sturm artefacts |
| Matrix residual identification | CONDITIONAL | right identity proved; corrected-left identity open |
| Algebraic Green matching | PROVED under matched traces | symbolic matrix test |
| Xi transform identity | PROVED_FROM_SOURCE_MELLIN_FORMULA | source equation 2.2.1, x=log(t) |
| Trace existence | PROVED_UNDER_SOURCE_PROFILE_AND_OPEN_STRIP | analytic weighted-source majorant |
| Endpoint flux | OPEN | weighted limits |
| Strict nondegeneracy | OPEN | domain theorem |
| Global Weyl--Volterra contradiction | OPEN | depends on open lemmas |
| RH | OPEN | no public claim |

## Conditional final implication

If the open trace, endpoint, and nondegeneracy lemmas are proved for the
actual Volterra solutions, the finite-interval Green identity and global
positive production give a quantity that matching forces to zero but energy
forces to be strictly positive for \(\beta>0\).  This is a conditional
implication only; the missing analytic hypotheses are not hidden in the code.
