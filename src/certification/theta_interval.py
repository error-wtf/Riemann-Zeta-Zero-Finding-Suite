"""Outward-rounded finite Theta derivative sums using python-flint Arb.

This module intentionally does not include an infinite-series tail. Every
result is therefore marked FINITE_TRUNCATION_ONLY until analytic tail bounds
are supplied.
"""

from __future__ import annotations


def _poly_factor(a, k, order, y, arb):
    coeffs = [arb(1)]
    for _ in range(order):
        out = [arb(0)] * (len(coeffs) + 1)
        for j, c in enumerate(coeffs):
            out[j] += (a + 2 * j) * c
            out[j + 1] -= 2 * k * c
        coeffs = out
    return sum((c * y**j for j, c in enumerate(coeffs)), arb(0))


def theta_derivative_ball(x, order: int = 0, terms: int = 40, precision: int = 256):
    try:
        from flint import arb, ctx
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("install requirements-certify.txt") from exc
    ctx.prec = precision
    x = arb(x)
    y = (2 * x).exp()
    total = arb(0)
    pi = arb.pi()
    for n in range(1, terms + 1):
        nn = arb(n)
        k = pi * nn * nn
        e = (-k * y).exp()
        total += 2 * pi**2 * nn**4 * (arb(9) * x / 2).exp() * e * _poly_factor(arb(9) / 2, k, order, y, arb)
        total -= 3 * pi * nn**2 * (arb(5) * x / 2).exp() * e * _poly_factor(arb(5) / 2, k, order, y, arb)
    return total


def finite_phi_derivative_balls(x, terms: int = 40, precision: int = 256):
    t0, t1, t2, t3 = (theta_derivative_ball(x, j, terms, precision) for j in range(4))
    r1 = t1 / t0
    return (-r1, r1**2 - t2 / t0, -t3 / t0 + 3 * t1 * t2 / t0**2 - 2 * r1**3)


def finite_profile_status() -> dict[str, str]:
    return {
        "backend": "python-flint/Arb",
        "outward_rounding": "TRUE",
        "theta_tail": "NOT_INCLUDED",
        "status": "FINITE_TRUNCATION_ONLY",
    }
