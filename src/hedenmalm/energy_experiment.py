"""Finite-precision exploration of the Theta energy coefficients.

This module deliberately accepts no zero list and never labels a sign scan as
proof. It is a reproducible guide for where analytic interval bounds are still
needed.
"""

from __future__ import annotations

import mpmath as mp

from .profile_identification import Phi_log
from .canonical_multiplier import S_phi


def scan_energy_coefficients(points: int = 81, radius: float = 4.0, dps: int = 40) -> dict[str, object]:
    if points < 3 or radius <= 0:
        raise ValueError("points must be >=3 and radius must be positive")
    xs = [(-radius + 2 * radius * i / (points - 1)) for i in range(points)]
    phi2 = []
    s_right = []
    with mp.workdps(dps):
        for x in xs:
            f = lambda y: Phi_log(y, terms=100)
            phi2.append(float(mp.diff(f, x, 2)))
            if x > 1e-12:
                s_right.append(float(S_phi(x, dps=dps)))
    return {
        "grid": {"points": points, "radius": radius, "dps": dps},
        "phi2_min": min(phi2),
        "s_right_min": min(s_right),
        "phi2_positive_on_grid": min(phi2) > 0,
        "s_positive_on_right_grid": min(s_right) > 0,
        "status": "NUMERICALLY_SUPPORTED_ONLY",
    }
