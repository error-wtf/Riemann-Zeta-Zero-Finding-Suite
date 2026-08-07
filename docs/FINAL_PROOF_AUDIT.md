# Final proof audit (current)

This report supersedes the earlier historical 46-test audit.

## Executed checks

* 103 unit/integration tests: passed; 5 optional certification tests skipped
  without FLINT in the default interpreter.
* Repository integrity test: passed.
* Direct fourth-derivative cross-check against independent high-precision
  differentiation: passed.
* Finite-precision scan on `[-4,4]`: `Phi''` and the right-half-axis
  `S_Phi` samples are positive.
* Exploratory origin-trace stress test: the proposed one-sided inequality is
  not valid for arbitrary complex `alpha` (for example the residual is
  approximately `-0.345` at `alpha=0.1i`). This diagnostic is not used by the
  canonical two-sided Volterra matching route.
* Proof ledger: the canonical internal chain is complete; independent review
  remains outstanding.

## What is actually proved

1. The source profile and normalization are identified.
2. The first-order boundary solution is derived without using `L^{-1}`.
3. The weighted energy identity is symbolically correct under convergence and
   vanishing-boundary assumptions.
4. The canonical multiplier algebraic reduction is exact.
5. The local-weight and global translation-invariant multiplier no-go results
   hold under their stated hypotheses.
6. Nondegeneracy holds under the cited source asymptotics.

## What is not proved

The remaining external obligation is independent mathematical review of the
complete RH candidate proof. The former one-sided trace implication is not a
dependency of the canonical route: absolute convergence gives both Volterra
tails, their full difference is (e^{-i\alpha x}\Xi(\alpha)), and an Xi zero
therefore gives equality of the actual states for every (x). The common ODE
then gives derivative and (F)-component matching.

The profile, far-range, correction-Sturm, weighted-source, absolute Volterra
convergence, fixed-parameter endpoint-decay, and oriented improper Green-limit
blocks are now certified and provenance-bound. The
source/ODE nondegeneracy implication is recorded as a theorem under its stated
hypotheses. The Xi-zero origin-matching composition and final Weyl
contradiction are assembled from the full two-sided Volterra identity; the
open one-sided diagnostic is not a live dependency. Xi normalization,
Volterra convergence, Xi evenness, standard nontrivial-zero strip
localization, and the parameter bridge are recorded separately. The
repository does not claim a publicly validated proof of RH; its status is
`CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW`.

The right- and corrected-left algebraic residual identities are now
independently verified. With \(q=e^{2\Phi-2\beta x}\),

$$
J_+'+A_\alpha^*J_++J_+A_\alpha
=q\,\operatorname{diag}(2\beta,S_\Phi).
$$

The corrected-left residual has Schur complement
(qG_\beta/\Phi''), so the profile/Sturm certificates are now connected to
both actual Hermitian residual matrices.
