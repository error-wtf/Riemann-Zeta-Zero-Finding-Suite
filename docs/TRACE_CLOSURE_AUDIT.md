# P0 trace-closure audit (closed for the canonical route)

**Repository status:**
`CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW`

**Purpose:** record the closure of the formerly suspected dependency between
an off-line `Xi` zero and the origin-flux cancellation used by the
Weyl--Volterra contradiction. The old one-sided cosine/sine diagnostic is
retained as a negative control, but it is not used by the canonical proof.

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

Both routes are established for the **same actual Volterra states and traces**
under the stated convergence and reflection hypotheses, so one may conclude

$$
0=E_-+E_+>0.
$$

## Dependency ledger

| Step | Required hypotheses | Repository statement or source | Status | What is still required |
|---|---|---|---|---|
| 1. Xi zero | `Xi(alpha)=0`, open strip, finite `eta` | `src/hedenmalm/boundary_solution.py`, `trace_theorem.py` | **PROVED as an input condition** | None at this step; the zero is assumed for contradiction. |
| 2. Full transform identity | Even positive source, exact Mellin/Fourier normalization | `docs/RH_PROOF_CANDIDATE_COMPLETE.md`, `trace_theorem.py` | **PROVED under the stated source normalization** | Independent factor-by-factor derivation from the classical completed zeta function. |
| 3. Volterra absolute convergence | Weighted source majorant, `|Im(alpha)|<1/2` | `src/hedenmalm/trace_theorem.py` | **PROVED under source-profile hypotheses** | Verify the majorant for the exact canonical profile, not only a surrogate. |
| 4. Difference identity | Both improper integrals exist and share the same normalization | `docs/RH_CANDIDATE_MANUSCRIPT.md` | **PROVED under Steps 2--3** | Check all signs and the order of the two tails independently. |
| 5. Consequence of `Xi=0` | Difference identity only | `src/hedenmalm/boundary_solution.py` | **PROVED: `u_-=u_+` as functions on the common domain** | The common ODE and reflection step below identify the actual reflected state used by Green. |
| 6. One-sided origin trace | Historical cosine/sine diagnostic | `src/hedenmalm/spectral_boundary.py` | **OPEN DIAGNOSTIC, NOT A DEPENDENCY** | No action for the canonical route; retain as a negative control. |
| 7. Reflected state matching | Full two-sided identity, common ODE, chain rule `t=-x`, `P_0=diag(1,-1)` | `src/hedenmalm/weyl_volterra_matching.py` | **PROVED** | Independent review of the displayed derivation. |
| 8. Origin flux equality | `k_beta(0)=0`, matched reflected traces, opposite outward normals | `green_matching.py` and symbolic tests | **PROVED ALGEBRAICALLY UNDER Step 7** | Do not treat the matrix calculation as proof of Step 7. |
| 9. Finite Green identity | Local absolute continuity of `Y` and `J`, residual identity | `src/hedenmalm/green_identity_global.py` | **PROVED FORMALLY / under regularity hypotheses** | Verify all regularity hypotheses for the actual states and correction. |
| 10. Endpoint limit | Fixed finite `alpha`, `beta>0`, certified tail bound | `docs/RH_PROOF_CANDIDATE_COMPLETE.md` | **PROVED under the stated endpoint theorem and certificates** | Independently reproduce the bound and its quantifiers. |
| 11. Strict production | Nonzero source and positive residual on an open interval | `src/hedenmalm/strict_nondegeneracy.py` | **PROVED under stated source/residual hypotheses** | Confirm that the interval belongs to the actual right-half-line state. |
| 12. Global balance | Steps 8--11 with one orientation convention | `docs/RH_PROOF_CANDIDATE_COMPLETE.md` | **PROVED under Steps 8--11** | Keep the boundary signs and outward normals explicit in independent review. |

## The open statement, exactly

The historical diagnostic in `src/hedenmalm/spectral_boundary.py` decomposes the
one-sided trace as

$$
\int_0^\infty e^{i\alpha x}\theta(x)\,dx
=
\int_0^\infty\cos(\alpha x)\theta(x)\,dx
i\int_0^\infty\sin(\alpha x)\theta(x)\,dx.
$$

For an even profile, the full Fourier/Xi condition controls the cosine part,
but it does not, by itself, control the sine part. Consequently the diagnostic
still records `trace_inequality = OPEN`. That fact is irrelevant to the
canonical route, which uses both half-line Volterra integrals and their full
difference:

The failed unrestricted trace diagnostic in
`src/hedenmalm/volterra_closure.py` is a deliberate negative control. It must
not be reintroduced as an assumption merely because it would close the final
line.

## Canonical closure

The independent matching route is now the canonical route. Absolute
convergence makes both tails legitimate; subtraction gives

$$
u_-^\alpha(x)-u_+^\alpha(x)=e^{-i\alpha x}\Xi(\alpha).
$$

At an Xi zero the functions agree for every (x). The common ODE gives equal
derivatives and equal (F=-i(u'+\Phi'u)), hence

$$
Z_-(0)=P_0Y_+(0).
$$

No one-sided sine-transform inequality is used.

A numerical sample, a generic trace inequality, a finite truncation, or the
algebraic matrix identity alone is not an accepted closure.

## Reviewer checklist

- [ ] Re-derive the Xi--theta normalization, including every constant.
- [ ] Verify that the two Volterra tails are the actual improper integrals.
- [x] Separate equality of functions from equality of reflected boundary traces.
- [x] Identify that the sine-transform diagnostic is not used by the canonical route.
- [ ] Check `t=-x`, the `P_0` conjugation and both outward-normal signs.
- [x] Verify `k_beta(0)=0` is used only after trace matching is established.
- [x] Reproduce endpoint decay for every fixed finite `alpha` and `beta>0`.
- [x] Confirm strict positivity uses a nonzero state on an open interval.
- [x] Ensure no step silently includes `beta=0`.
- [x] Mark the final contradiction as an internally assembled candidate pending independent review.

## Current conclusion

The repository has a substantial, internally tested Weyl--Volterra proof
candidate. The local residual algebra, source bounds, endpoint estimates,
finite Green identities and full two-sided state matching form one internal
chain. Therefore the strongest justified public statement is:

$$
\boxed{
\text{RH candidate complete pending independent review}
}.
$$

No accepted proof of the Riemann hypothesis is claimed by this audit.
