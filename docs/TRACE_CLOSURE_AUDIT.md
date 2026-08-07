# P0 trace-closure audit

**Repository status:**
`CANDIDATE_PROOF_PENDING_TRACE_CLOSURE_AND_INDEPENDENT_REVIEW`

**Purpose:** isolate the single unresolved dependency between an off-line
`Xi` zero and the origin-flux cancellation used by the Weyl--Volterra
contradiction. This document is fail-closed: an algebraic identity is not
promoted to a theorem about the actual Volterra traces.

## Target implication

For

$$
\alpha=\eta+i\beta,\qquad 0<\beta<\frac12,
$$

the intended contradiction requires the following implication:

$$
\Xi(\alpha)=0
\;\Longrightarrow\;
M_-(0)-M_+(0)=0.
$$

The independent positivity/Green route then supplies

$$
M_-(0)-M_+(0)=E_-+E_+,
\qquad E_-\ge 0,\quad E_+>0.
$$

Only if both routes are established for the **same actual states and traces**
may one conclude

$$
0=E_-+E_+>0.
$$

## Dependency ledger

| Step | Required hypotheses | Repository statement or source | Status | What is still required |
|---|---|---|---|---|
| 1. Xi zero | `Xi(alpha)=0`, open strip, finite `eta` | `src/hedenmalm/boundary_solution.py`, `trace_theorem.py` | **PROVED as an input condition** | None at this step; the zero is assumed for contradiction. |
| 2. Full transform identity | Even positive source, exact Mellin/Fourier normalization | `docs/RH_CANDIDATE_MANUSCRIPT.md`, `trace_theorem.py` | **PROVED under the stated source normalization** | Independent factor-by-factor derivation from the classical completed zeta function. |
| 3. Volterra absolute convergence | Weighted source majorant, `|Im(alpha)|<1/2` | `src/hedenmalm/trace_theorem.py` | **PROVED under source-profile hypotheses** | Verify the majorant for the exact canonical profile, not only a surrogate. |
| 4. Difference identity | Both improper integrals exist and share the same normalization | `docs/RH_CANDIDATE_MANUSCRIPT.md` | **PROVED under Steps 2--3** | Check all signs and the order of the two tails independently. |
| 5. Consequence of `Xi=0` | Difference identity only | `src/hedenmalm/boundary_solution.py` | **PROVED: `u_-=u_+` as functions where both are defined** | This does not yet identify every reflected boundary trace used by the Green argument. |
| 6. One-sided origin trace | A relation between the actual half-line trace and the full Xi transform | `src/hedenmalm/spectral_boundary.py` | **OPEN** | Prove the missing sine-transform control or replace it with an independent matching argument. |
| 7. Reflected state matching | Trace relation from Step 6, chain rule `t=-x`, `P_0=diag(1,-1)` | `src/hedenmalm/green_matching.py` | **CONDITIONAL_ON_TRACE_CLOSURE** | State the exact trace lemma and prove it for the actual complex-parameter solution. |
| 8. Origin flux equality | `k_beta(0)=0`, matched reflected traces, opposite outward normals | `green_matching.py` and symbolic tests | **PROVED ALGEBRAICALLY UNDER Step 7** | Do not treat the matrix calculation as proof of Step 7. |
| 9. Finite Green identity | Local absolute continuity of `Y` and `J`, residual identity | `src/hedenmalm/green_identity_global.py` | **PROVED FORMALLY / under regularity hypotheses** | Verify all regularity hypotheses for the actual states and correction. |
| 10. Endpoint limit | Fixed finite `alpha`, `beta>0`, certified tail bound | `docs/RH_CANDIDATE_MANUSCRIPT.md` | **PROVED CONDITIONALLY on the endpoint theorem** | Independently reproduce the bound and its quantifiers. |
| 11. Strict production | Nonzero source and positive residual on an open interval | `src/hedenmalm/strict_nondegeneracy.py` | **PROVED under stated source/residual hypotheses** | Confirm that the interval belongs to the actual right-half-line state. |
| 12. Global balance | Steps 8--11 with one orientation convention | `docs/RH_CANDIDATE_MANUSCRIPT.md` | **CONDITIONAL_ON_TRACE_CLOSURE** | Keep the boundary signs and outward normals explicit in the final proof. |

## The open statement, exactly

The diagnostic in `src/hedenmalm/spectral_boundary.py` decomposes the
one-sided trace as

$$
\int_0^\infty e^{i\alpha x}\theta(x)\,dx
=
\int_0^\infty\cos(\alpha x)\theta(x)\,dx
i\int_0^\infty\sin(\alpha x)\theta(x)\,dx.
$$

For an even profile, the full Fourier/Xi condition controls the cosine part.
It does not, by itself, control the sine part. Consequently the repository
records `trace_inequality = OPEN`. The following inference is **not** licensed
without a new lemma:

$$
\Xi(\alpha)=0
\;\Longrightarrow\;
\text{the one-sided trace has the value required by the reflected matching}.
$$

The failed unrestricted trace diagnostic in
`src/hedenmalm/volterra_closure.py` is a deliberate negative control. It must
not be reintroduced as an assumption merely because it would close the final
line.

## Accepted closure routes

The audit can be closed by either route, but the manuscript must name and
prove one of them:

1. **Trace lemma route.** Prove a theorem for the actual canonical source and
   complex `alpha` showing that `Xi(alpha)=0` implies the precise one-sided
   boundary relation used in the reflected state.
2. **Independent matching route.** Avoid the one-sided inequality entirely and
   derive `Z_-(0)=P_0Y_+(0)` directly from the full two-sided Volterra identity,
   including all trace-existence, reflection and endpoint hypotheses.

A numerical sample, a generic trace inequality, a finite truncation, or the
algebraic matrix identity alone is not an accepted closure.

## Reviewer checklist

- [ ] Re-derive the Xi--theta normalization, including every constant.
- [ ] Verify that the two Volterra tails are the actual improper integrals.
- [ ] Separate equality of functions from equality of reflected boundary traces.
- [ ] Identify the exact lemma that supplies the sine-transform component.
- [ ] Check `t=-x`, the `P_0` conjugation and both outward-normal signs.
- [ ] Verify `k_beta(0)=0` is sufficient only after trace matching is known.
- [ ] Reproduce endpoint decay for every fixed finite `alpha` and `beta>0`.
- [ ] Confirm strict positivity uses a nonzero state on an open interval.
- [ ] Ensure no step silently includes `beta=0`.
- [ ] Mark the final contradiction conditional until every box above is green.

## Current fail-closed conclusion

The repository has a substantial, internally tested Weyl--Volterra proof
candidate. The local residual algebra, source bounds, endpoint estimates and
finite Green identities are not evidence that the missing one-sided trace
implication is proved. Therefore the strongest justified public statement is:

$$
\boxed{
\text{RH candidate pending trace closure and independent review}
}.
$$

No accepted proof of the Riemann hypothesis is claimed by this audit.
