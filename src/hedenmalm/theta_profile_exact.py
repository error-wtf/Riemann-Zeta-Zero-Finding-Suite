"""Source-faithful Jacobi-theta derivative profile used by Hedenmalm.

This implements the positive real series for ``varTheta_00(i t^2)`` and its
inversion symmetry.  It is *not* silently identified with ``Phi``: the paper's
operator profile must be wired explicitly before Phi-asymptotics are claimed.
"""

from __future__ import annotations

import mpmath as mp


def vartheta00_it2(t: mp.mpf | float, *, terms: int = 80) -> mp.mpf:
    """Evaluate the positive real theta-derived profile for ``t>0``."""
    t = mp.mpf(t)
    if not t > 0:
        raise ValueError("t must be positive")
    u = max(t, 1 / t)  # exact inversion symmetry Theta(i t^2)=Theta(i/t^2)
    return mp.pi * u ** (mp.mpf(9) / 2) * mp.fsum(
        n**2 * (2 * mp.pi * n**2 - 3 / u**2) * mp.exp(-mp.pi * n**2 * u**2)
        for n in range(1, terms + 1)
    )


def vartheta00_bounds(t: mp.mpf | float, *, terms: int = 80) -> tuple[mp.mpf, mp.mpf]:
    """Return the published positive lower/upper series bounds for ``t>=1``."""
    t = mp.mpf(t)
    if t < 1:
        t = 1 / t
    lower = mp.pi * t ** (mp.mpf(9) / 2) * mp.fsum(
        n**2 * (2 * mp.pi * n**2 - 3) * mp.exp(-mp.pi * n**2 * t**2)
        for n in range(1, terms + 1)
    )
    upper = mp.pi * t ** (mp.mpf(9) / 2) * mp.fsum(
        2 * mp.pi * n**4 * mp.exp(-mp.pi * n**2 * t**2)
        for n in range(1, terms + 1)
    )
    return lower, upper


def theta_asymptotic_status() -> dict[str, str]:
    return {
        "profile": "varTheta_00(i t^2)",
        "inversion": "Theta(t)=Theta(1/t)",
        "endpoint_decay": "Gaussian in t^2 and 1/t^2",
        "phi_identification": "OPEN",
        "status": "PROVED_UNDER_SOURCE_FORMULA",
    }
