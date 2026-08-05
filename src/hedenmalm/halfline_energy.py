"""Half-line energy and origin-trace diagnostics.

The half-line reduction is an exact formal target for the remaining proof,
not a proof itself.  These helpers deliberately return diagnostic statuses and
do not accept a zero list or fit any parameter to one.
"""

from __future__ import annotations

import mpmath as mp

from .theta_derivative_series import phi_derivatives_from_series


def origin_trace(alpha: complex, w0: complex) -> complex:
    """w'(0)=1-i*alpha*w(0) under the fixed source convention."""
    return 1 - 1j * alpha * w0


def origin_trace_residual(alpha: complex, w0: complex, *, terms: int = 100, dps: int = 50) -> mp.mpf:
    """Residual of |w'(0)|² >= Phi''(0)|w(0)|² (positive means passes)."""
    with mp.workdps(dps):
        _, phi2, _ = phi_derivatives_from_series(0, terms, dps)
        wp0 = origin_trace(alpha, w0)
        return abs(wp0) ** 2 - phi2 * abs(w0) ** 2


def halfline_energy_status() -> dict[str, str]:
    return {
        "phi2_global": "OPEN",
        "s_phi_positive_on_open_halfline": "NUMERICALLY_SUPPORTED_ONLY",
        "infinity_boundary_term": "OPEN",
        "origin_trace_inequality": "OPEN",
        "volterra_coercivity": "OPEN",
        "status": "OPEN",
    }
