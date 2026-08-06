# Endpoint-flux status after the far-field ratio audit

## Scope

This report checks the endpoint argument against the current repository
artifacts. It does not claim an unconditional endpoint theorem or an RH
proof.

## Verified algebra

For `z = pi*exp(2*x)` and `z >= 8`, the dominant profile satisfies

\[
\Phi_1'(z)-z=
\frac{4z^2-24z+15}{2(2z-3)}.
\]

With `z = 8+w`, the numerator is

\[
4w^2+40w+79>0.
\]

Hence `Phi1_prime >= z >= 8`. The published far remainder certificate
provides an outward-rounded bound `B_DR` for `|D R| = |L'|`, with

\[
|L'|\le B_{DR}<4.896\cdot 10^{-8}.
\]

Therefore the certified global lower bound used by the endpoint helper is

\[
m=8-B_{DR}>7.99999995.
\]

The same far certificate gives

\[
p_0=\inf_{x\ge 1/2}\Phi''(x)>19.999996.
\]

## Ratio lemma

For fixed `beta > 0`, the function

\[
f\mapsto \frac{f}{f-\beta}
\]

is strictly decreasing on `f > beta`. Consequently, from `Phi' >= m > beta`
alone,

\[
\frac{\Phi'}{\Phi'-\beta}
\le \frac{m}{m-\beta}.
\]

No global upper bound for `Phi'` is needed. The Arb implementation
`certified_phi_prime_ratio_bound` computes this bound and rejects invalid
`beta` or nonpositive denominators fail-closed. At `beta=1/2` it returns an
upper bound below `1.067` at 128-bit Arb precision.

## Full flux constant

The legacy ratio helper returned only a bound for the second state component.
It is therefore not a complete bound for `|Y*JY|`. The certified helper now
uses the full estimate

\[
C_{\rm flux}
=\frac{1}{(m-\beta)^2}
 +\frac{1}{p_0}
 \left(1+\frac{m}{m-\beta}
 +\frac{|\alpha|}{m-\beta}\right)^2.
\]

The first term bounds the `u` component and the second bounds the `F`
component. Certified calls reject Python floats and require exact or Arb-
compatible inputs.

## Implementation changes

* `far_positive_theta_term` now calls the genuinely factorized positive
  source branch rather than the older difference representation.
* `full_phi_prime_far_bounds` records the proven dominant lower coefficient as
  `1`, not the former unexplained `0.9`.
* `certified_phi_prime_ratio_bound` exposes the monotonic ratio lemma as an
  outward-rounded Arb result.
* Endpoint constants remain fail-closed for `beta <= 0`, nonpositive
  `Phi''`, and `Phi' - beta <= 0`.
* `endpoint_theorem.py` now isolates the convex-tail and state-bound lemma;
  it now also records the actual Volterra endpoint certificate, including the
  finite support cutoff of the left correction. The global contradiction still
  remains explicitly open.
* `oriented_halfline_balance` records the finite-interval signs separately:
  `left_origin-left_endpoint=left_production` and
  `right_endpoint-right_origin=right_production`.  Endpoint terms are not
  discarded until an explicit zero-limit theorem is supplied.

## What is and is not proved

| Statement | Status |
|---|---|
| Dominant inequality `Phi1' > z` for `z >= 8` | `PROVED_EXACT_RATIONAL` |
| Far remainder `B_DR` and `Phi''` lower bound | `PROVED_OUTWARD_ROUNDED` |
| Ratio bound `Phi'/(Phi'-beta) <= m/(m-beta)` | `PROVED_OUTWARD_ROUNDED` under the far certificate |
| Full algebraic flux constant | `PROVED` as a conditional bound |
| Absolute convergence of the actual Volterra tails | `PROVED_ANALYTICALLY_IN_OPEN_STRIP` |
| Vanishing endpoint flux for the actual Weyl solutions | `PROVED_CONDITIONALLY_FOR_DEFINED_VOLTERRA_INTEGRALS` |
| Global Weyl--Volterra contradiction | `OPEN` |
| RH | `OPEN` |

The remaining gap is not a missing upper bound for `Phi'`: the endpoint limit
is now certified for the defined Volterra integrals under the stated profile
bounds. What remains is the global assembly with the oriented Green identity,
matching, and strict nondegeneracy.

## Validation

The default test suite passes with `84 passed, 5 skipped`; optional Arb tests
are skipped when the system interpreter has no `python-flint`. In the pinned
certification environment, the ratio helper returns a strictly positive
denominator and an upper bound below `1.067` for `beta=1/2`.
