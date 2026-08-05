"""Exact source identification of the operator profile.

The cited source defines ``phi_00(t) = -log(Theta_00(i t^2))``.  In log
coordinates the operator profile is therefore ``Phi(x)=phi_00(exp(x))``.
No fitted or alternative normalization is used here.
"""

from __future__ import annotations

import mpmath as mp

from .theta_profile_exact import vartheta00_it2


def phi00(t: mp.mpf | float, *, terms: int = 80) -> mp.mpf:
    t = mp.mpf(t)
    if not t > 0:
        raise ValueError("t must be positive")
    return -mp.log(vartheta00_it2(t, terms=terms))


def Phi_log(x: mp.mpf | float, *, terms: int = 80) -> mp.mpf:
    """Return ``Phi(x)=phi_00(exp(x))`` in logarithmic coordinates."""
    return phi00(mp.exp(mp.mpf(x)), terms=terms)


def profile_identification_status() -> dict[str, str]:
    return {
        "status": "PROVED_FROM_SOURCE",
        "t_profile": "phi_00(t)=-log(Theta_00(i*t^2))",
        "log_profile": "Phi(x)=phi_00(exp(x))",
        "normalization": "source normalization; no fitted constants",
        "inversion": "Phi(-x)=Phi(x)",
        "source": "Hedenmalm, arXiv:2606.17494v1, Sections 1.2 and 3.2",
    }


def asymptotic_leading_terms() -> dict[str, str]:
    return {
        "t_to_infinity": "phi_00(t)=pi*t^2-(9/2)*log(t)-log(2*pi^2)+O(t^-2)",
        "x_to_plus_infinity": "Phi(x)=pi*exp(2x)-(9/2)*x-log(2*pi^2)+O(exp(-2x))",
        "x_to_minus_infinity": "Phi(x)=Phi(-x)",
        "status": "PROVED_FROM_SOURCE_ASYMPTOTIC",
    }
