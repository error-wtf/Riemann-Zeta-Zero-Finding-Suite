# Complete RH proof candidate

**Frozen candidate:** `f1c13d6`  
**Local tag:** `rh-candidate-v1`  
**Public status:** `CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW`

This is the self-contained linear statement of the canonical two-component
Weyl--Lyapunov candidate. The older scalar energy draft is not used.

## 1. Definitions

Define the completed zeta function

\[
\xi(s)=\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s),
\]

and

\[
\Xi(\alpha)=\xi\left(\frac12+i\alpha\right).
\]

Write \(\alpha=\eta+i\beta\), where \(\eta\in\mathbb R\) and
\(0<\beta<1/2\). Then

\[
s=\frac12+i\alpha=\frac12-\beta+i\eta.
\]

Thus \(\operatorname{Re}s=1/2-\beta\). The source profile is

\[
\theta(x)=\Theta_{00}(i e^{2x})>0,
\qquad \Phi(x)=-\log\theta(x),
\]

with

\[
P=\Phi'',
\qquad T=\frac{2\Phi'\Phi''-\Phi'''}{\Phi''}.
\]

## 2. Xi transform and Volterra states

The source Mellin formula, under \(t=e^x\), is exactly

\[
\Xi(\alpha)=\int_{\mathbb R}e^{i\alpha x}\theta(x)\,dx.
\]

The normalization factor is one. The analytic Gaussian majorant proves
absolute convergence for \(|\operatorname{Im}\alpha|<1/2\). Define

\[
u_-^\alpha(x)=e^{-i\alpha x}\int_{-\infty}^{x}e^{i\alpha y}\theta(y)\,dy,
\]

\[
u_+^\alpha(x)=-e^{-i\alpha x}\int_x^{\infty}e^{i\alpha y}\theta(y)\,dy.
\]

Differentiating the convergent integrals gives

\[
(u_\pm^\alpha)'+i\alpha u_\pm^\alpha=\theta.
\]

Subtraction gives

\[
u_-^\alpha-u_+^\alpha=e^{-i\alpha x}\Xi(\alpha).
\]

Consequently \(\Xi(\alpha)=0\) implies equality of the two states and,
by the common differential equation, equality of their derivatives.

## 3. First-order system

Set

\[
F=-i(u'+\Phi'u),
\qquad Y=(u,F)^T.
\]

Solving the definition of \(F\) for \(u'\), differentiating \(F\), and
using the Volterra equation yields

\[
Y'=A_\alpha Y,
\qquad A_\alpha=
\begin{pmatrix}-\Phi'&i\\-i\Phi''&-i\alpha\end{pmatrix}.
\]

For locally absolutely continuous \(Y,J\), the product rule gives

\[
\frac{d}{dx}(Y^*JY)=Y^*(J'+A_\alpha^*J+J A_\alpha)Y.
\]

## 4. Right and reflected-left residuals

Let \(q=e^{2\Phi-2\beta x}\). On the right define

\[
J_+=q\begin{pmatrix}-1&0\\0&1/P\end{pmatrix}.
\]

Using \(q'=2(\Phi'-\beta)q\) and \(P'=\Phi'''\), direct multiplication gives

\[
H_+=J_+'+A_\alpha^*J_++J_+A_\alpha
=q\operatorname{diag}\left(2\beta,\frac{2\Phi'P-\Phi'''}{P^2}\right)
=q\operatorname{diag}(2\beta,T/P).
\]

For the left put \(t=-x\), \(P_0=\operatorname{diag}(1,-1)\), and
\(Z(t)=P_0Y(-t)\). Evenness gives \(\Phi'(-t)=-\Phi'(t)\) and
\(\Phi''(-t)=\Phi''(t)\), so

\[
A_-=-P_0A_\alpha(-t)P_0
=\begin{pmatrix}-\Phi'&i\\-i\Phi''&i\alpha\end{pmatrix}.
\]

Let \(k=k_\beta(t)\) be the compactly supported correction, with
\(k(0)=0\) and \(k=0\) beyond its support. Define

\[
J_-=q\begin{pmatrix}-1&0\\0&(1+k)/P\end{pmatrix}.
\]

The direct symbolic calculation is

\[
H_-=q\begin{pmatrix}
2\beta&ik\\
-ik&((1+k)(T-4\beta)+k')/P
\end{pmatrix}.
\]

Its Schur complement is

\[
\operatorname{Schur}(H_-)=\frac{q}{P}G_\beta,
\]

where

\[
G_\beta=(1+k_\beta)(T-4\beta)+k_\beta'
-\frac{P k_\beta^2}{2\beta}.
\]

The compact Arb certificate proves \(0<P<40\) and \(T>500x\) on
\([0,1/2]\). The far certificate proves \(P>0\), \(T>2\) for
\(x\ge1/2\). The exact rational Sturm certificate proves the two
conservative correction polynomials positive on \([0,1/125]\) and
\([1/125,1]\). Therefore \(H_+>0\) and \(H_->0\) on the open half-lines.

## 5. Endpoint and global Green limits

For each fixed finite \(|\alpha|\) and \(0<\beta<1/2\), the far certificate
gives \(m=8-B_{DR}>1/2\) and \(p_0=\inf P>0\). Convexity gives

\[
|u_+(R)|\le\frac{\theta(R)}{\Phi'(R)+\beta},
\qquad
|u_-(-R)|\le\frac{\theta(R)}{\Phi'(R)-\beta}.
\]

Since \(m-\beta>0\), the state and second-component bounds imply

\[
|M_+(R)|,|M_-(-R)|\le C_{\alpha,\beta}e^{-2\beta R},
\]

with

\[
C_{\alpha,\beta}=\frac1{(m-\beta)^2}
 +\frac1{p_0}\left(1+\frac m{m-\beta}
 +\frac{|\alpha|}{m-\beta}\right)^2<\infty.
\]

Hence both endpoint fluxes tend to zero. On finite intervals the oriented
identities are

\[
M_-(0)-M_-(-R)=E_-(R),
\qquad M_+(R)-M_+(0)=E_+(R).
\]

Taking \(R\to\infty\) gives

\[
E_-=M_-(0),\qquad E_+=-M_+(0),
\]

and therefore

\[
M_-(0)-M_+(0)=E_-+E_+.
\]

## 6. Strictness, matching, and contradiction

Since \(\theta>0\), the equation \(u_+'+i\alpha u_+=\theta\) excludes
\(u_+\equiv0\). Continuity gives an open interval on which \(Y_+\ne0\).
Because \(H_+>0\) there, \(E_+>0\), hence \(E_-+E_+>0\).

If \(\Xi(\alpha)=0\), the Volterra difference identity gives
\(u_-=u_+\), their derivatives agree, and so do their \(F\)-components.
Reflection gives \(Z_-(0)=P_0Y_+(0)\). Since \(k_\beta(0)=0\), direct
conjugation gives \(P_0^*J_-(0)P_0=J_+(0)\). Opposite outward normals then
give

\[
M_-(0)-M_+(0)=0.
\]

The global Green identity gives the same quantity as \(E_-+E_+>0\), so

\[
0=E_-+E_+>0.
\]

Therefore \(\Xi(\alpha)\ne0\) for \(0<\operatorname{Im}\alpha<1/2\).

## 7. RH symmetry bridge

The completed-zeta functional equation \(\xi(s)=\xi(1-s)\) implies

\[
\Xi(-\alpha)=\xi\left(\frac12-i\alpha\right)
=\xi\left(1-\left(\frac12+i\alpha\right)\right)=\Xi(\alpha).
\]

Nontrivial zeta zeros are the zeros of \(\xi\) in
\(0<\operatorname{Re}s<1\); the trivial zeros are separated by the
completed factors. The Weyl contradiction excludes the left half of this
strip, and evenness excludes the right half. Hence every nontrivial zero has
\(\operatorname{Im}\alpha=0\), which is exactly \(\operatorname{Re}s=1/2\).

## Appendices

The exact matrix calculations are implemented in
`src/hedenmalm/residue_identification.py`. The three certificates are:

* `compact_profile_m500_M40.json`, SHA-256
  `51f36fe953984b8da3e9d5c0ec1c67df76ebf918d0b835c26cf7db0200572aab`;
* `far_asymptotic_profile.json`, SHA-256
  `acc733efee2765fe2ca3633ab405f02735ef2f2e65ccc88d8ab11b2d8a580de3`;
* `correction_sturm_q_m500_M40.json`, SHA-256
  `6bba83172c4291c688f0337a8aaa0cdc9f3758bdb5b002c76db58e2dc419e9fe`.

Reproduction commands are `pytest -q` and the certificate commands listed in
`docs/RIEMANN_ENERGY_PROOF_HANDOVER.md`. The manuscript remains a candidate
pending independent review; it is not a public claim that RH has been
accepted or proved by the mathematical community.
