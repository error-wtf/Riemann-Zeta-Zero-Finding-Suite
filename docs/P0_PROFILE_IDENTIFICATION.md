# P0 profile-identification theorem

The source definition is explicit:

```text
phi_00(t) = -log(Theta_00(i t^2)),  t>0
Phi(x)    = phi_00(exp(x)).
```

Therefore the operator expression

```text
L_phi f = D^× f + f D^× phi
```

uses the source profile `phi_00`, not a fitted potential. Since the source
Theta profile obeys `Theta(t)=Theta(1/t)`, the log-coordinate profile obeys

```text
Phi(-x)=Phi(x).
```

The source asymptotic is

```text
phi_00(t) = pi t^2 - (9/2) log(t) - log(2 pi^2) + O(t^-2)
```

as `t -> infinity`. Hence

```text
Phi(x) = pi exp(2x) - (9/2)x - log(2 pi^2) + O(exp(-2x))
```

as `x -> +infinity`, and the negative endpoint follows by even symmetry.

This proves the profile identification and its stated source asymptotic under
the source's normalization. It still does not prove closed range,
self-adjointness, or a Hilbert–Pólya theorem.
