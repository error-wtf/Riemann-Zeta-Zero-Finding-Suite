# Prior-art and novelty audit

**Date:** 2026-08-07  
**Purpose:** formula-level comparison before any peer-review novelty claim

This document is a research audit, not a priority claim and not evidence that
the repository proves the Riemann hypothesis.  It records what the cited
primary sources actually state, what is only structurally related, and which
repository implications still require an independent mathematical check.

## Primary sources inspected

### Hedenmalm (arXiv:2606.17494v1)

Haakan Hedenmalm, *Spectral interpretation of Riemann zeta zeros*, submitted
16 June 2026.

Source: <https://arxiv.org/abs/2606.17494>  
HTML source: <https://arxiv.org/html/2606.17494v1>

The paper defines the Jacobi theta function and the transformed profile
`\varTheta_{00}` (Section 1.2, equations (1.2.1)--(1.2.5)), states the Mellin
representation

```text
Xi(x) = integral_(0,+infinity) varTheta_00(i t^2) t^(i x) dt/t
```

(equation (2.2.1)), and uses

```text
xi(s) = 1/2 s(s-1) pi^(-s/2) Gamma(s/2) zeta(s).
```

It then introduces first-order operators and the boundary-value equation
`L_phi D^times u + alpha L_phi u = 0` (Section 3.2--3.3).  For a zero of
`Xi`, its one-sided Volterra expression is given in equation (3.3.8).  This is
close prior art for the source normalization, profile, spectral parameter and
one-sided Volterra mechanism.

It is not the same displayed construction as the repository's reflected
two-component system, corrected left multiplier, `G_beta` Schur expression,
or the repository's global production/Green/matching assembly.  That
non-identity is a comparison result, not a proof of novelty.

### Freedman (arXiv:2606.29555v1)

Marvin B. Freedman, *Finite-core Volterra reductions for a Weyl-positive
Riemann phase kernel*, submitted 28 June 2026.

Source: <https://arxiv.org/abs/2606.29555>  
HTML source: <https://arxiv.org/html/2606.29555v1>

The abstract explicitly describes a Weyl-positive Riemann phase kernel,
finite-core Volterra reductions, certificate machinery and a quotient Schur
factorization.  Its dependency map separates:

1. a Volterra Schur certificate;
2. the quotient-to-original Weyl lift;
3. uniform `|omega| < 1/2` coverage;
4. the KLM/de Branges/RH bridge.

The paper explicitly says that the latter external links remain requirements
and that the manuscript is not a complete RH proof.  It also records an
augmented Mellin-boundary trace repair and says that the continuum lift of
that repair remains to be established.  Therefore Freedman is close
methodologically (Volterra, Weyl, Schur, certificates), but the inspected
source does not display the repository's exact `A_-`, `J_-`, `H_-`,
`k_beta`, `G_beta` formula or the exact origin-flux contradiction below.

## Formula-level comparison

| Object | Repository candidate | Hedenmalm | Freedman | Audit classification |
|---|---|---|---|---|
| Theta/Mellin source | `Xi(alpha)=int_R exp(i alpha x) theta(x) dx` after `x=log(t)` | Explicit Mellin identity (2.2.1) | Riemann phase kernel and Mellin/Volterra reductions | **same family; normalization must be re-derived** |
| Spectral ODE | `Y'=A_alpha Y`, a two-component first-order form | `L_phi D^times u + alpha L_phi u=0` | Operator/Weyl quotient framework | **related, not shown identical** |
| Volterra states | two tails `u_-`, `u_+` on reflected half-lines | one-sided integral for a zero | Volterra boundary-plus-tail representations | **related; domains and orientations differ** |
| Reflected system | `A_-(t)=[[-p,i],[-i q,i alpha]]` | not this displayed matrix | no identical matrix found in inspected text | **candidate-specific, requires proof audit** |
| Right multiplier | `J_+=q diag(-1,1/P)` | no identical multiplier found | Schur positivity in a different quotient model | **not established as prior-identical** |
| Corrected left multiplier | `J_-=q diag(-1,(1+k_beta)/P)` | no identical construction found | related correction/trace ideas, but no identical formula found | **possible novelty candidate, not yet a novelty theorem** |
| Scalar Schur term | `G_beta=(1+k_beta)(T-4 beta)+k_beta' - P k_beta^2/(2 beta)` | no identical term found | Schur factorizations, different kernel/quotient notation | **requires line-by-line literature search** |
| Certified positivity | Arb/profile/Sturm certificates for the repository's formulas | not the same certificate chain | computer-assisted certificate framework, with external links separated | **related infrastructure; formula identity unproved** |
| Endpoint/Green assembly | `M_-(0)-M_+(0)=E_-+E_+` | boundary conditions, not this flux identity | quotient/trace limits, different orientation | **candidate-specific, adversarial sign audit required** |
| Xi-zero matching | `Xi=0 -> u_-=u_+ -> origin trace matching` | zero gives one-sided boundary solution | trace repair is explicitly an open bridge in the paper | **full two-sided route established here; independent review required** |
| Final contradiction | `0=E_-+E_+>0` | no such conclusion | paper explicitly does not claim complete RH proof | **internal candidate claim; external review required** |

## Repository consistency finding (resolved)

The repository previously contained two potentially confusing status surfaces.
The discrepancy is now resolved by separating the historical diagnostic from
the canonical proof route:

* `src/hedenmalm/spectral_boundary.py` states that the one-sided trace
  inequality is `OPEN` and that `Xi(alpha)=0` controls only the cosine part,
  leaving the sine transform uncontrolled.
* the canonical manuscript now derives origin matching from the full
  two-sided Volterra difference identity, rather than from that diagnostic.

The one-sided inequality remains an open negative control, but it is no longer
a dependency of the canonical chain. The current public scientific status is:

```text
CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW
```

and no novelty statement may imply that the RH contradiction is externally
validated.

## Required independent gates

1. Re-derive the exact Xi/Theta normalization from the classical `xi(s)` and
   Hedenmalm's equation (2.2.1), including every change-of-variable factor.
2. Reproduce the profile, Arb and Sturm certificates and verify that their
   domains cover every `0 < beta < 1/2` used by the matrix proof.
3. Prove `u_\pm`, `Y_\pm`, `J_\pm` regularity on every patch, including the
   support boundaries of `k_beta`.
4. Recompute reflection, `P_0`, outward normals, endpoint limits and every
   sign in the Green identity.
5. Resolve the `spectral_boundary.py` open sine-transform issue before
   upgrading origin matching from conditional to unconditional.
6. Compare `A_-`, `J_-`, `H_-`, `k_beta`, `G_beta`, `M_\pm` against the full
   texts of the closest prior papers, not only their abstracts.

## Permitted wording before review

Use:

> Building on the theta-kernel and spectral-operator tradition, we develop a
> distinct candidate construction based on reflected two-component Volterra
> systems, corrected Hermitian multipliers and a certified Schur reduction.

Do not use:

> We have established an entirely novel proof of the Riemann hypothesis.

The former describes a defensible research direction; the latter is not
supported by this audit.
