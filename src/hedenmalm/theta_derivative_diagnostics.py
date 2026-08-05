"""Numerical diagnostics for Phi', Phi'' and Phi''' from the source profile.

These evaluations help locate a possible coercive multiplier but do not prove
global signs or interval bounds.
"""

from __future__ import annotations

import mpmath as mp

from .profile_identification import Phi_log


def phi_derivatives(x: float, *, dps: int = 50) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    with mp.workdps(dps):
        f = lambda y: Phi_log(y, terms=100)
        return mp.diff(f, x, 1), mp.diff(f, x, 2), mp.diff(f, x, 3)


def residual_value(x: float, a: callable, *, dps: int = 50) -> mp.mpf:
    """Evaluate R_a numerically; derivative signs remain uncertified."""
    with mp.workdps(dps):
        p1, p2, p3 = phi_derivatives(x, dps=dps)
        aa = mp.mpf(a(x))
        ap = mp.diff(a, x)
        return ap * p2 + aa * (p3 - 2 * p1 * p2)


def diagnostic_status() -> dict[str, str]:
    return {
        "P1_SIGN_STRUCTURE": "NUMERICALLY_SUPPORTED_ONLY",
        "P2_COERCIVE_MULTIPLIER": "OPEN",
        "P3_BOUNDARY_VANISHING": "OPEN",
        "P4_COMPLEX_ALPHA_CONTRADICTION": "OPEN",
    }
