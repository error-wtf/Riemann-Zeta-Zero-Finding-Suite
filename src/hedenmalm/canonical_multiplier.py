"""Canonical h_b multiplier and S_Phi reduction diagnostics."""

from __future__ import annotations

import mpmath as mp

from .profile_identification import Phi_log


def canonical_h(x: float, b: float) -> mp.mpf:
    if b <= 0:
        raise ValueError("b must be positive")
    return mp.exp(-2 * b * x)


def canonical_multiplier(x: float, b: float, *, dps: int = 50) -> mp.mpf:
    with mp.workdps(dps):
        phi = Phi_log(x, terms=100)
        phi2 = mp.diff(lambda y: Phi_log(y, terms=100), x, 2)
        if phi2 <= 0:
            raise ValueError("canonical multiplier requires Phi''>0 at x")
        return mp.exp(2 * phi - 2 * b * x) / phi2


def S_phi(x: float, *, dps: int = 50) -> mp.mpf:
    with mp.workdps(dps):
        f = lambda y: Phi_log(y, terms=100)
        p1, p2, p3 = mp.diff(f, x, 1), mp.diff(f, x, 2), mp.diff(f, x, 3)
        return (2 * p1 * p2 - p3) / (p2 * p2)


def canonical_multiplier_status() -> dict[str, str]:
    return {
        "reduction": "h_b=exp(-2*b*x), a_b=exp(2*Phi-2*b*x)/Phi''",
        "S_function": "S_Phi=(2 Phi' Phi''-Phi''')/(Phi'')^2",
        "positive_half_axis": "NUMERICALLY_SUPPORTED_ONLY",
        "negative_half_axis": "OPEN",
        "boundary_terms": "OPEN",
        "integrability": "OPEN",
        "status": "OPEN",
    }
