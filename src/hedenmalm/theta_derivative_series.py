"""Direct termwise derivatives of the source Theta profile.

The series is split into two exponential terms per n and differentiated by an
exact polynomial recurrence. This avoids finite-differencing the summed
function; truncation and interval tails remain a separate proof obligation.
"""

from __future__ import annotations

import mpmath as mp


def _poly_derivative_factor(a: mp.mpf, k: mp.mpf, order: int, y: mp.mpf) -> mp.mpf:
    # P_0=1, P_{m+1}=a P_m + 2 y (P'_m-k P_m), for exp(a x-k exp(2x)).
    coeffs = [mp.mpf(1)]
    for _ in range(order):
        # Evaluate recurrence directly using polynomial coefficients in y.
        out = [mp.mpf(0)] * (len(coeffs) + 1)
        for j, c in enumerate(coeffs):
            out[j] += (a + 2 * j) * c
            out[j + 1] -= 2 * k * c
        coeffs = out
    return mp.fsum(c * y**j for j, c in enumerate(coeffs))


def theta_derivative_series(x: float, order: int = 0, terms: int = 100, dps: int = 50) -> mp.mpf:
    if order < 0 or order > 4:
        raise ValueError("order must be between 0 and 4")
    with mp.workdps(dps):
        x = mp.mpf(x)
        y = mp.exp(2 * x)
        total = mp.mpf("0")
        for n in range(1, terms + 1):
            k = mp.pi * n * n
            e = mp.exp(-k * y)
            total += 2 * mp.pi**2 * n**4 * mp.exp(mp.mpf(9) * x / 2) * e * _poly_derivative_factor(mp.mpf(9) / 2, k, order, y)
            total -= 3 * mp.pi * n**2 * mp.exp(mp.mpf(5) * x / 2) * e * _poly_derivative_factor(mp.mpf(5) / 2, k, order, y)
        return total


def phi_derivatives_from_series(x: float, terms: int = 100, dps: int = 50) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    t0, t1, t2, t3 = (theta_derivative_series(x, j, terms, dps) for j in range(4))
    r1 = t1 / t0
    return -r1, r1**2 - t2 / t0, -t3 / t0 + 3 * t1 * t2 / t0**2 - 2 * r1**3


def phi_fourth_from_series(x: float, terms: int = 100, dps: int = 50) -> mp.mpf:
    """Return Phi'''' from direct termwise Theta derivatives.

    This is an analytic quotient identity evaluated with high precision; it is
    not an interval certificate.  The fourth derivative is needed because
    S_Phi(0)=0 and its first nonzero Taylor coefficient is
    2 Phi''(0)^2 - Phi''''(0).
    """
    with mp.workdps(dps):
        t0, t1, t2, t3, t4 = (theta_derivative_series(x, j, terms, dps) for j in range(5))
        r1, r2, r3, r4 = t1 / t0, t2 / t0, t3 / t0, t4 / t0
        return -r4 + 4 * r1 * r3 + 3 * r2**2 - 12 * r1**2 * r2 + 6 * r1**4


def origin_slope_margin(terms: int = 100, dps: int = 50) -> mp.mpf:
    """Numerical value of 2 Phi''(0)^2 - Phi''''(0); status remains non-rigorous."""
    with mp.workdps(dps):
        _, p2, _ = phi_derivatives_from_series(0, terms, dps)
        return 2 * p2**2 - phi_fourth_from_series(0, terms, dps)


def s_phi_from_series(x: float, terms: int = 100, dps: int = 50) -> mp.mpf:
    p1, p2, p3 = phi_derivatives_from_series(x, terms, dps)
    return (2 * p1 * p2 - p3) / p2**2
