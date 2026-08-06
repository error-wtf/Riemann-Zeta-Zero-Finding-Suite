"""Outward-rounded Theta derivative enclosures using python-flint Arb.

The finite sum is augmented by a *symmetric* ball whose radius is the
absolute Gaussian tail majorant.  This is an enclosure of the infinite
series, not an assertion about the sign of its remainder.
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
    if not 0 <= order <= 4:
        raise ValueError("order must be between 0 and 4")
    if terms < 1:
        raise ValueError("terms must be positive")
    old_precision = ctx.prec
    try:
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
        from .theta_tail_bounds import tail_bound
        bound = tail_bound(x, order, terms, precision)
        # tail_bound is an absolute-value majorant: attach [-B, B], never +B.
        tail_error = arb(0, bound.upper())
        return total + tail_error
    finally:
        ctx.prec = old_precision


def finite_phi_derivative_balls(x, terms: int = 40, precision: int = 256):
    p1, p2, p3, p4, t0 = profile_derivative_balls(x, terms, precision)
    return p1, p2, p3


def profile_derivative_balls(x_ball, terms: int = 40, precision: int = 256):
    """Return (Phi', Phi'', Phi''', Phi'''', Theta) on an Arb box.

    The source profile is positive.  A merely nonzero or negative enclosure
    is therefore not accepted: all quotient formulae fail closed unless
    ``Theta.lower() > 0``.
    """
    try:
        from flint import ctx
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("install requirements-certify.txt") from exc
    old_precision = ctx.prec
    try:
        ctx.prec = precision
        t = [theta_derivative_ball(x_ball, j, terms, precision) for j in range(5)]
        t0, t1, t2, t3, t4 = t
        if t0.lower() <= 0:
            raise RuntimeError("Strict positivity of Theta was not certified; subdivide the box")
        r1 = t1 / t0
        phi1 = -r1
        phi2 = r1**2 - t2 / t0
        phi3 = -t3 / t0 + 3*t1*t2/t0**2 - 2*r1**3
        phi4 = -t4/t0 + 4*t1*t3/t0**2 + 3*(t2/t0)**2 - 12*t1**2*t2/t0**3 + 6*r1**4
        return phi1, phi2, phi3, phi4, t0
    finally:
        ctx.prec = old_precision


def profile_margin_balls(x_ball, terms: int = 40, precision: int = 256):
    """Return certified profile margins on an Arb box."""
    from flint import arb
    phi1, phi2, phi3, phi4, theta = profile_derivative_balls(x_ball, terms, precision)
    x = arb(x_ball)
    T = 2*phi1*phi2 - phi3
    F = T - 500*x
    F_prime = 2*phi2**2 + 2*phi1*phi3 - phi4 - 500
    return {
        "theta": theta,
        "P": phi2,
        "40_minus_P": arb(40) - phi2,
        "T": T,
        "F": F,
        "F_prime": F_prime,
    }


def finite_profile_status() -> dict[str, str]:
    return {
        "backend": "python-flint/Arb",
        "outward_rounding": "TRUE",
        "theta_tail": "GAUSSIAN_MAJORANT_INCLUDED",
        "status": "TAIL_INCLUDED_NOT_PROFILE_CERTIFIED",
    }
