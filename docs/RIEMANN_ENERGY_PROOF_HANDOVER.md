# Riemann energy proof handover

## Scope

The repository studies the source-faithful profile
\(\theta(x)=\Theta_{00}(i e^{2x})>0\), \(\Phi=-\log\theta\),
\(P=\Phi''\), and \(T=2\Phi'\Phi''-\Phi'''\).  The parameter convention is

\[
\alpha=\xi+i\beta,\qquad s=\tfrac12+i\alpha=	frac12-\beta+i\xi.
\]

Thus \(\beta>0\) denotes a point left of the critical line.

## Closed constructive block

The Arb certificates prove \(0<P<40\) and \(T>500x\) on
\([0,1/2]\), and the positive n=1/remainder certificate proves \(P>0\) and
\(T>2\) for \(x\ge1/2\).  Together with the exact Sturm certificate this
proves the explicit right and reflected-left Lyapunov production matrices
(strictly for \(x>0\), semidefinite at the isolated origin point).

The certificate artefacts are:

* `artifacts/certificates/compact_profile_m500_M40.json`;
* `artifacts/certificates/far_asymptotic_profile.json`.

## Green matching

The state is \(Y=(u,F)^T\), \(F=L_\Phi u=-i(u'+\Phi'u)\), with
\(Y'=A_\alpha Y\) and
\[
A_\alpha=\begin{pmatrix}-\Phi'&i\\-i\Phi''&-i\alpha\end{pmatrix}.
\]
The actual symbolic calculation in `green_matching.py` verifies
\(P_0^*J_-(0)P_0-J_+(0)=\operatorname{diag}(0,a k_\beta(0))\),
where \(P_0=\operatorname{diag}(1,-1)\).  Hence the algebraic trace identity
holds iff \(k_\beta(0)=0\), with opposite outward normals.

## Open analytic obligations

The repository now records the Xi normalization from the source Mellin
formula (unit factor after `x=log(t)`, `dt/t=dx`).  It does **not** claim
trace existence,
Volterra admissibility, endpoint flux decay, strict nondegeneracy, or the RH
contradiction.  These require actual improper-integral estimates and a
functional-analytic domain theorem; passing tests cannot substitute for them.

## Reproduction

```bash
python3 -m pytest -q
python3 test_suite_integrity.py
.venv-cert/bin/python scripts/certify_compact_profile.py --precision 256 --terms 30 --origin-cut 1/256 --max-depth 30 --max-boxes 100000 --output artifacts/certificates/compact_profile_m500_M40.json
.venv-cert/bin/python scripts/certify_far_remainder.py --precision 256 --output artifacts/certificates/far_asymptotic_profile.json
```

## Review checklist

The next human review must independently check the Xi transform normalization,
the left/right normal signs, the improper-integral limit, and the mapping
\(s=\tfrac12+i\alpha\).  No public RH status may be upgraded before those
lemmas are written and checked.
