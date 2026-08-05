"""Adversarial finite-precision scan for the scaled-correction bounds."""

from __future__ import annotations

import mpmath as mp

from .theta_derivative_series import phi_derivatives_from_series


def scan_profile_bounds(xmax: float = 0.5, points: int = 101, *, terms: int = 50, dps: int = 25) -> dict[str, object]:
    if xmax <= 0 or points < 3:
        raise ValueError("xmax must be positive and points >= 3")
    m = mp.inf
    M = mp.mpf("0")
    m_at = None
    with mp.workdps(dps):
        for j in range(1, points):
            t = mp.mpf(xmax) * j / (points - 1)
            p1, p2, p3 = phi_derivatives_from_series(t, terms, dps)
            T = 2 * p1 * p2 - p3
            ratio = T / t
            if ratio < m:
                m, m_at = ratio, t
            M = max(M, p2)
    return {
        "xmax": xmax,
        "points": points,
        "m_lower_sample": float(m),
        "m_at": float(m_at),
        "P_upper_sample": float(M),
        "definition": "T=2*Phi'*Phi''-Phi'''",
        "status": "NUMERICALLY_SUPPORTED_ONLY",
    }


def polynomial_lower_bound(tau: float, m: float, M: float, amplitude: float = 10.0, width: float = 1.0) -> float:
    """Evaluate the beta-independent q(tau) lower bound (diagnostic only)."""
    f = amplitude * tau * (1 - tau / width) ** 2
    fp = amplitude * (1 - tau / width) * (1 - 3 * tau / width)
    z = m * tau - 4
    return z + fp + f * min(z, 0.0) / 4.0 - M * f * f / 8.0
