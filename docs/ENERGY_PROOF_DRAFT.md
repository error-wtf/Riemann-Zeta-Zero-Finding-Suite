# Conditional energy-proof draft (fail-closed)

This document writes the proposed argument as a complete lemma chain. It is
not a claim that the Riemann hypothesis has been proved. Every step whose
global hypotheses are not established is explicitly marked `OPEN`.

## Definitions

In logarithmic coordinates let

\[
D=-i\partial_x,\qquad L_\Phi=-i(\partial_x+\Phi'),\qquad
\vartheta=e^{-\Phi}.
\]

The source boundary equation is
\[
L_\Phi(D+\alpha)u_\alpha=0.
\]
Under the source convention and the stated endpoint conditions,
\[
u_\alpha(x)=e^{-i\alpha x}\int_{-\infty}^x e^{i\alpha y}\vartheta(y)\,dy.
\]

The condition \(\Xi(\alpha)=0\) is the source spectral boundary condition.

## Lemma 1 — formal weighted identity (`PROVED_FORMALLY`)

For real smooth \(a\), sufficiently regular \(u\), and vanishing Green
boundary terms,
\[
2\operatorname{Im}(\alpha)\int a|L_\Phi u|^2dx
=-\int a'|L_\Phi u|^2dx+\int R_a|u|^2dx,
\]
where
\[
R_a=(a\Phi'')'-2a\Phi'\Phi''.
\]
The repository verifies this identity symbolically. The endpoint hypotheses
are not inferred from the symbolic calculation.

## Lemma 2 — canonical reduction (`PROVED_ALGEBRAICALLY`)

If \(\Phi''>0\) and
\[
a_h=h\,e^{2\Phi}/\Phi'',
\]
then
\[
R_{a_h}=e^{2\Phi}h'.
\]
For \(h_b=e^{-2bx}\), \(b>0\), define
\[
S_\Phi=\frac{2\Phi'\Phi''-\Phi'''}{(\Phi'')^2}.
\]
The transformed identity for \(u=\vartheta w\) is formally
\[
\int_{\mathbb R}e^{-2bx}
\left(S_\Phi|w'|^2+2b|w|^2\right)dx=0.
\]

## Lemma 3 — global coefficient bounds (`OPEN`)

The required statement is
\[
\Phi''(x)>0\quad(x\in\mathbb R),\qquad
S_\Phi(x)>0\quad(x>0),
\]
with outward-rounded tail and compact-interval bounds. Finite-precision
scans support this statement but do not prove it. FLINT/Arb certification is
not available in the current environment.

## Lemma 4 — endpoint and trace control (`OPEN`)

All weighted boundary terms must vanish, and the half-line origin trace must
obey the required inequality. This has not been proved. The repository now
contains the exact trace formula \(w'(0)=1-i\alpha w(0)\) as a diagnostic.

## Lemma 5 — Volterra coercivity (`OPEN`)

The negative-half-axis contribution (or the equivalent half-line trace term)
must be controlled by the positive terms in Lemma 2. This is the central
remaining inequality; no numerical fit or finite-grid result substitutes for
it.

## Conditional theorem

If Lemmas 3–5 hold for every admissible complex \(\alpha\), and if
\(L_\Phi u_\alpha\ne0\), Lemma 2 gives a strictly positive left-hand energy
but zero by the identity, a contradiction whenever \(\operatorname{Im}\alpha>0\).
Conjugation symmetry excludes \(\operatorname{Im}\alpha<0\). Hence \(\alpha\in\mathbb R\), and the source parametrization \(s=\tfrac12+i\alpha\)
places every corresponding zero on the critical line.

This is a valid conditional proof, not an unconditional proof of RH until
Lemmas 3–5 are supplied with global proofs.
