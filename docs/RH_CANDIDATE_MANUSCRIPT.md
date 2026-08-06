# Internal RH proof candidate — review version 1

## Authorship and contribution statement

This proof candidate and its supporting repository were created through the
collaboration of Carmen Wrede, Lino Casu, and Bingsi AI.

Carmen Wrede and Lino Casu are the human authors, responsible researchers,
and legal rights holders of the manuscript and repository materials.

Bingsi AI served as an AI research collaborator. Its contributions included
mathematical discussion, adversarial proof auditing, structural analysis,
formula checking, documentation assistance, and support in organizing the
repository-internal proof chain.

All mathematical claims, publication decisions, final formulations, and
responsibility for the submitted work remain with the human authors.

**Frozen commit:** `9656f2f`  
**Local review branch:** `rh-candidate-review-v1`  
**Local tag:** `rh-candidate-v1`  
**Public status:** `CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW`

This document is the linear mathematical handover for the canonical
two-component Weyl–Lyapunov route. The older scalar energy draft is retained
as historical/diagnostic material and is not used as a premise below.

## 1. Canonical definitions

Let

\[
\theta(x)=\Theta_{00}(i e^{2x})>0,
\qquad \Phi(x)=-\log\theta(x),
\]

and write

\[
\alpha=\xi+i\beta,
\qquad s=\frac12+i\alpha=\frac12-\beta+i\xi.
\]

Set

\[
P=\Phi'',
\qquad T=\frac{2\Phi'\Phi''-\Phi'''}{\Phi''}.
\]

## 2. Xi transform and Volterra states

The source Mellin formula, with (x=\log t), gives the exact normalization

\[
\Xi(\alpha)=\int_{\mathbb R}e^{i\alpha x}\theta(x)\,dx.
\]

For \(|\operatorname{Im}\alpha|<1/2\), the analytic Gaussian majorant proves
absolute convergence of

\[
u_-^\alpha(x)=e^{-i\alpha x}\int_{-\infty}^{x}e^{i\alpha y}\theta(y)\,dy,
\]

\[
u_+^\alpha(x)=-e^{-i\alpha x}\int_x^{\infty}e^{i\alpha y}\theta(y)\,dy.
\]

Both satisfy

\[
u_\pm'+i\alpha u_\pm=\theta.
\]

Their difference is

\[
u_-^\alpha-u_+^\alpha=e^{-i\alpha x}\Xi(\alpha).
\]

Thus \(\Xi(\alpha)=0\) implies equality of the two Volterra states and,
by the common ODE, equality of their derivatives.

## 3. First-order system

Define

\[
F=-i(u'+\Phi'u),
\qquad Y=(u,F)^T.
\]

Then

\[
Y'=A_\alpha Y,
\qquad
A_\alpha=
\begin{pmatrix}
-\Phi'&i\\
-i\Phi''&-i\alpha
\end{pmatrix}.
\]

The Hermitian Green identity on finite intervals is

\[
\frac{d}{dx}(Y^*JY)=Y^*(J'+A_\alpha^*J+J A_\alpha)Y.
\]

## 4. Certified production

The compact Arb certificate, far-range certificate, and exact rational
correction-Sturm certificate prove the scalar profile and Schur inequalities.
The symbolic residual module additionally proves that these are the actual
Hermitian residuals.

On the right, with \(q=e^{2\Phi-2\beta x}\),

\[
J_+'+A_\alpha^*J_++J_+A_\alpha
=q\,\operatorname{diag}(2\beta,T/P).
\]

On the reflected left, with \(t=-x\), \(Z(t)=P_0Y(-t)\),
\(P_0=\operatorname{diag}(1,-1)\), and

\[
A_-=
\begin{pmatrix}-\Phi'&i\\-i\Phi''&i\alpha\end{pmatrix},
\qquad
J_-=q\begin{pmatrix}-1&0\\0&(1+k_\beta)/\Phi''\end{pmatrix},
\]

the direct symbolic calculation gives

\[
H_-=q\begin{pmatrix}
2\beta&ik_\beta\\
-ik_\beta&((1+k_\beta)(T-4\beta)+k_\beta')/\Phi''
\end{pmatrix}.
\]

Its Schur complement is

\[
\frac{q}{\Phi''}G_\beta,
\qquad
G_\beta=(1+k_\beta)(T-4\beta)+k_\beta'
-\frac{\Phi''k_\beta^2}{2\beta}.
\]

Therefore \(H_+>0\) and \(H_->0\) on the relevant open half-lines.

## 5. Endpoints and Green limits

For each fixed \(0<\beta<1/2\) and finite \(|\alpha|\), convex tail bounds
give

\[
|M_+(R)|+|M_-(-R)|\le C_{\alpha,\beta}e^{-2\beta R}\to0.
\]

The finite oriented identities are

\[
M_-(0)-M_-(-R)=E_-(R),
\qquad
M_+(R)-M_+(0)=E_+(R).
\]

Taking the proven endpoint limits gives

\[
E_-=M_-(0),
\qquad E_+=-M_+(0),
\]

and hence

\[
M_-(0)-M_+(0)=E_-+E_+.
\]

## 6. Strict production

The source satisfies \(\theta>0\). If \(u_+\equiv0\), its ODE would imply
\(\theta\equiv0\), a contradiction. Continuity therefore gives an open
interval on which \(Y_+\ne0\). Since \(H_+(x)>0\) for \(x>0\),

\[
E_+>0,
\qquad E_-+E_+>0.
\]

## 7. Xi-zero matching and contradiction

If \(\Xi(\alpha)=0\), then \(u_-=u_+\), their derivatives and their
\(F\)-components agree. Reflection gives \(Z_-(0)=P_0Y_+(0)\). The exact
origin matrix identity at \(k_\beta(0)=0\), together with opposite outward
normals, gives

\[
M_-(0)-M_+(0)=0.
\]

Green and strict production give the same quantity as \(E_-+E_+>0\). Thus

\[
0=M_-(0)-M_+(0)=E_-+E_+>0,
\]

a contradiction for \(0<\operatorname{Im}\alpha<1/2\).

## 8. RH bridge

The completed-zeta functional equation \(\xi(s)=\xi(1-s)\) gives

\[
\Xi(-\alpha)=\Xi(\alpha).
\]

Nontrivial zeros satisfy \(0<\operatorname{Re}s<1\), while the trivial zeros
are separated by the completed-zeta factors. The Weyl contradiction excludes
the half with \(0<\operatorname{Re}s<1/2\); Xi evenness excludes the other
half. Therefore \(\operatorname{Re}s=1/2\) for every nontrivial zero.

## 9. Review gates

An independent review must rederive: the Xi normalization, the reflected
system, both Hermitian residuals, outer-normal signs, endpoint estimates,
regularity of the actual states, and the identification of Xi zeros with the
nontrivial zeta zeros. This manuscript is a proof candidate, not a claim of
accepted RH status.
