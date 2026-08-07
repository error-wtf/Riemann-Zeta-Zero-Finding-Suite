# P0 Theta asymptotics theorem

This document records the part that follows directly from the published
Jacobi-theta series. It does **not** identify the operator profile `Phi` with a
logarithm of this function without an explicit definition.

For \(t\ge1\), define

$$
\Theta(t)=\pi t^{9/2}\sum_{n\ge1}n^2
\left(2\pi n^2-3t^{-2}\right)e^{-\pi n^2t^2}.
$$

The first term is positive and the series is positive. Termwise comparison
gives the explicit bounds

$$
\pi t^{9/2}\sum_{n\ge1}n^2(2\pi n^2-3)e^{-\pi n^2t^2}
\le\Theta(t)
\le\pi t^{9/2}\sum_{n\ge1}2\pi n^4e^{-\pi n^2t^2}.
$$

Jacobi inversion supplies \(\Theta(t)=\Theta(1/t)\). Consequently the same
Gaussian decay holds at both ends: in \(t\) as \(t\to\infty\) and in \(1/t\)
as \(t\to0^+\).

## Consequence and limitation

The implemented `vartheta00_it2` therefore has a source-level asymptotic
control. This does **not** yet prove asymptotics of the `Phi` appearing in
`L_Phi`, because the exact relation between that profile and `Theta` must be
declared first. Until then the `THETA_ASYMPTOTICS` ledger entry is
`PROVED_UNDER_SOURCE_FORMULA`, while the `Phi`-specific entry remains `OPEN`.
