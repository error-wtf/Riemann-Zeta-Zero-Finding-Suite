# P0 profile-identification theorem

The source definition is explicit:

$$
\phi_{00}(t)=-\log\!\bigl(\Theta_{00}(i t^2)\bigr),\quad t>0,
\qquad
\Phi(x)=\phi_{00}(e^x).
$$

Therefore the operator expression

$$
L_\phi f=D^{\times}f+fD^{\times}\phi
$$

uses the source profile `phi_00`, not a fitted potential. Since the source
Theta profile obeys `Theta(t)=Theta(1/t)`, the log-coordinate profile obeys

$$
\Phi(-x)=\Phi(x).
$$

The source asymptotic is

$$
\phi_{00}(t)=\pi t^2-\frac92\log t-\log(2\pi^2)+O(t^{-2})
\qquad(t\to\infty).
$$

Hence

$$
\Phi(x)=\pi e^{2x}-\frac92x-\log(2\pi^2)+O(e^{-2x})
\qquad(x\to+\infty).
$$

and the negative endpoint follows by even symmetry.

This proves the profile identification and its stated source asymptotic under
the source's normalization. It still does not prove closed range,
self-adjointness, or a Hilbert–Pólya theorem.
