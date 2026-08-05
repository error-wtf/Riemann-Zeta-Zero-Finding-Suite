"""Exact two-endpoint Volterra matching ledger.

The algebraic matching relation is recorded without claiming the missing
Weyl positivity theorem.  The two endpoint solutions differ by the full
Fourier transform of the even Theta source.
"""

from __future__ import annotations


def matching_identity() -> dict[str, str]:
    return {
        "left_solution": "u_- = exp(-i*alpha*x)*int_{-inf}^x exp(i*alpha*y)*theta(y)dy",
        "right_solution": "u_+ = -exp(-i*alpha*x)*int_x^inf exp(i*alpha*y)*theta(y)dy",
        "difference": "u_- - u_+ = exp(-i*alpha*x)*int_R exp(i*alpha*y)*theta(y)dy (full Fourier transform)",
        "spectral_matching": "Xi(alpha)=0 implies u_-=u_+",
        "weyl_flux_positivity": "OPEN",
        "coupled_halfline_energy": "OPEN",
        "status": "PROVED_MATCHING_IDENTITY_OPEN_POSITIVITY",
    }


def unconditional_weyl_ready() -> bool:
    return False
