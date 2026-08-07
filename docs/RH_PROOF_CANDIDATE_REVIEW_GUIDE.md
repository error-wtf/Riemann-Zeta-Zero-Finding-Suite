# Adversarial review guide for the RH candidate

Review the frozen candidate at tag `rh-candidate-v1` (local branch
`rh-candidate-review-v1`). The public status is
`CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW`.

Before making any novelty or completeness claim, read
[`PRIOR_ART_AND_NOVELTY_AUDIT.md`](PRIOR_ART_AND_NOVELTY_AUDIT.md).  It records
the inspected Hedenmalm and Freedman primary sources and the fail-closed status
distinction between the historical one-sided trace diagnostic and the
canonical full two-sided Volterra origin-matching route.

The former P0 question is documented in
[`TRACE_CLOSURE_AUDIT.md`](TRACE_CLOSURE_AUDIT.md). Read that ledger before
reviewing the final contradiction: it separates the historical one-sided
diagnostic from the proved full two-sided Volterra implication that an Xi zero
supplies the actual matched states.

## Priority checks

1. Re-derive the source Mellin/Fourier normalization, including every factor
   in \(\Xi(\alpha)=\int e^{i\alpha x}\theta(x)dx\).
2. Re-derive the first-order system from
   \(F=-i(u'+\Phi'u)\), checking the sign of \(-i\alpha\).
3. Recompute both \(J'+A^*J+JA\) matrices independently. In particular,
   check the reflected variable \(t=-x\), the matrix \(P_0\), and the
   lower-right term \(i\alpha=i\eta-\beta\).
4. Check that the Sturm-certified expression is exactly the Schur complement
   of the computed left residual, not merely an equivalent-looking formula.
5. Check that the endpoint estimate applies to the actual improper Volterra
   integrals, not only to a formal source expression.
6. Check local absolute continuity and all hypotheses of the finite Green
   identity before taking limits.
7. Check the outward-normal convention: the manuscript uses
   \(M_-(0)-M_+(0)\), not an untracked sum with an implicit sign.
8. Check strictness: \(u_+\not\equiv0\) must imply positive production on a
   genuine open interval.
9. Check the exact relation between zeros of the completed zeta function and
   nontrivial zeros of \(\zeta\); separate trivial zeros and the pole.
10. Check that \(\beta=0\) is never excluded by an endpoint argument requiring
    \(e^{-2\beta R}\to0\).

## Deliberate break tests

The proof should fail if any of the following is introduced:

* replace \(A_-\)'s lower-right entry \(i\alpha\) by \(-i\alpha\);
* use \(A^T\) instead of \(A^*\);
* omit the chain-rule minus in \(t=-x\);
* omit \(k_\beta'\) or replace \(T-4\beta\) by \(T-2\beta\);
* use the same outward normal at both origins;
* set \(\beta=0\) in the endpoint theorem;
* replace the full Fourier transform by a one-sided integral;
* infer a uniform bound in \(\eta\) from a single spectral parameter;
* replace the exact Arb/Sturm certificates by floating-point samples.

## Reproduction

```bash
pytest -q
python test_suite_integrity.py
```

Run the pinned certification environment as described in
`docs/RIEMANN_ENERGY_PROOF_HANDOVER.md`. Verify all three certificate hashes
against the frozen manuscript and the JSON artifacts.

## Required independent sign-off

The candidate should be reviewed independently by specialists in analytic
number theory, first-order ODE/Green identities, and computer-assisted proof.
No single green test or repository status is a substitute for that review.
