# P0 Theta asymptotics theorem

This document records the part that follows directly from the published
Jacobi-theta series. It does **not** identify the operator profile `Phi` with a
logarithm of this function without an explicit definition.

For `t >= 1`, define

```text
Theta(t) = pi t^(9/2) sum_{n>=1} n^2 (2 pi n^2 - 3 t^(-2)) exp(-pi n^2 t^2).
```

The first term is positive and the series is positive. Termwise comparison
gives the explicit bounds

```text
pi t^(9/2) sum n^2 (2 pi n^2 - 3) exp(-pi n^2 t^2)
  <= Theta(t)
  <= pi t^(9/2) sum 2 pi n^4 exp(-pi n^2 t^2).
```

Jacobi inversion supplies `Theta(t)=Theta(1/t)`. Consequently the same
Gaussian decay holds at both ends: in `t` as `t -> infinity` and in `1/t` as
`t -> 0+`.

## Consequence and limitation

The implemented `vartheta00_it2` therefore has a source-level asymptotic
control. This does **not** yet prove asymptotics of the `Phi` appearing in
`L_Phi`, because the exact relation between that profile and `Theta` must be
declared first. Until then the `THETA_ASYMPTOTICS` ledger entry is
`PROVED_UNDER_SOURCE_FORMULA`, while the `Phi`-specific entry remains `OPEN`.
