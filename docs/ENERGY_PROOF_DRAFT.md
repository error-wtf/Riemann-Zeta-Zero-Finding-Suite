# Conditional energy-proof draft (fail-closed)

This document writes the proposed argument as a complete lemma chain. It is
not a claim that the Riemann hypothesis has been proved. Every step whose
global hypotheses are not established is explicitly marked `OPEN`.

## Definitions

In logarithmic coordinates let

$$
D=-i\partial_x,\qquad L_\Phi=-i(\partial_x+\Phi'),\qquad
\vartheta=e^{-\Phi}.
$$

The source boundary equation is
$$
L_\Phi(D+\alpha)u_\alpha=0.
$$
Under the source convention and the stated endpoint conditions,
$$
u_\alpha(x)=e^{-i\alpha x}\int_{-\infty}^x e^{i\alpha y}\vartheta(y)\,dy.
$$

The condition \(\Xi(\alpha)=0\) is the source spectral boundary condition.

## Lemma 1 — formal weighted identity (`PROVED_FORMALLY`)

For real smooth \(a\), sufficiently regular \(u\), and vanishing Green
boundary terms,
$$
2\operatorname{Im}(\alpha)\int a|L_\Phi u|^2dx
=-\int a'|L_\Phi u|^2dx+\int R_a|u|^2dx,
$$
where
$$
R_a=(a\Phi'')'-2a\Phi'\Phi''.
$$
The repository verifies this identity symbolically. The endpoint hypotheses
are not inferred from the symbolic calculation.

## Lemma 2 — canonical reduction (`PROVED_ALGEBRAICALLY`)

If \(\Phi''>0\) and
$$
a_h=h\,e^{2\Phi}/\Phi'',
$$
then
$$
R_{a_h}=e^{2\Phi}h'.
$$
For \(h_b=e^{-2bx}\), \(b>0\), define
$$
S_\Phi=\frac{2\Phi'\Phi''-\Phi'''}{(\Phi'')^2}.
$$
The transformed identity for \(u=\vartheta w\) is formally
$$
\int_{\mathbb R}e^{-2bx}
\left(S_\Phi|w'|^2+2b|w|^2\right)dx=0.
$$

## Lemma 3 — global coefficient bounds (`PROVED_CERTIFIED`)

The required statement is
$$
\Phi''(x)>0\quad(x\in\mathbb R),\qquad
S_\Phi(x)>0\quad(x>0),
$$
with outward-rounded tail and compact-interval bounds. The compact Arb
certificate, positive far-range majorant, and exact rational correction-Sturm
certificate are independently validated and provenance-bound by the ledger.
These certificates do not by themselves prove the endpoint or improper-limit
lemmas below.

## Lemma 4 — endpoint and trace control (`CONDITIONAL_REPOSITORY_THEOREM`)

Weighted source integrability, absolute convergence of both Volterra
integrals, and local trace existence are proved from the analytic Gaussian
majorant. The convex-tail estimate and certified far-range margins give an
endpoint-decay theorem under those hypotheses. The repository has not yet
promoted that conditional theorem to a self-instantiating theorem for the
actual matched complex-\(\alpha\) solution, so the improper Green boundary
limit remains open. The old unrestricted trace inequality is not used: it
fails for generic complex \(\alpha\).

## Lemma 5 — global Green limit and nondegeneracy (`OPEN`)

The finite oriented Green identities are implemented, including endpoint
terms and outer-normal signs. What remains is the improper-limit theorem for
the actual Volterra states, strict right-production from the nonzero source,
and the connection from the Xi-zero identity to matched origin traces. No
numerical fit or finite-grid result substitutes for these functional-analytic
implications.

## Conditional theorem

If Lemmas 3–5 hold for every admissible complex \(\alpha\), and if
\(L_\Phi u_\alpha\ne0\), Lemma 2 gives a strictly positive left-hand energy
but zero by the identity, a contradiction whenever \(\operatorname{Im}\alpha>0\).
Conjugation symmetry excludes \(\operatorname{Im}\alpha<0\). Hence \(\alpha\in\mathbb R\), and the source parametrization \(s=\tfrac12+i\alpha\)
places every corresponding zero on the critical line.

This is a valid conditional proof, not an unconditional proof of RH until
Lemmas 3–5 are supplied with global proofs.
