"""Positive source-faithful far-range algebra.

This module contains the n=1 dominant profile and its exact derivative
formulae.  It intentionally does not claim the infinite-range remainder
bound; that remains a separate fail-closed obligation.
"""
from __future__ import annotations


def far_positive_theta_partial_ball(x_ball, terms: int = 30, precision: int = 256):
    """Evaluate the factored positive source series on x>=1/2.

    Every finite summand is positive because z=pi*exp(2x)>8.  The returned
    ball still includes the absolute tail symmetrically; callers needing only
    a lower bound may use ``far_positive_theta_lower_ball``.
    """
    from flint import arb, ctx
    from .theta_tail_bounds import tail_bound
    old = ctx.prec
    try:
        ctx.prec = precision
        x = arb(x_ball)
        if x.lower() < arb("0.5"):
            raise ValueError("far positive Theta requires x.lower() >= 1/2")
        z = arb.pi() * (2*x).exp(); total = arb(0)
        pi = arb.pi()
        for n in range(1, terms + 1):
            nn = arb(n)
            total += pi*nn**2*(arb(5)*x/2).exp() * (2*nn**2*z-3) * (-nn**2*z).exp()
        return total + arb(0, tail_bound(x, 0, terms, precision).upper())
    finally:
        ctx.prec = old


def far_positive_theta_lower_ball(x_ball, precision: int = 256):
    """Certified positive n=1 lower bound for x>=1/2."""
    from flint import arb, ctx
    old = ctx.prec
    try:
        ctx.prec = precision
        x = arb(x_ball)
        if x.lower() < arb("0.5"):
            raise ValueError("far positive Theta requires x.lower() >= 1/2")
        z = arb.pi()*(2*x).exp()
        return arb.pi()*(arb(5)*x/2).exp()*(2*z-3)*(-z).exp()
    finally:
        ctx.prec = old


def dominant_derivatives(z):
    """Return Phi_1', Phi_1'', Phi_1''' for z=pi*exp(2*x)."""
    phi1 = (8*z**2 - 30*z + 15) / (2*(2*z - 3))
    phi2 = 4*z*(4*z**2 - 12*z + 15) / (2*z - 3)**2
    phi3 = 8*z*(8*z**3 - 36*z**2 + 42*z - 45) / (2*z - 3)**3
    return phi1, phi2, phi3


def dominant_T(z):
    return 4*z*(16*z**3 - 92*z**2 + 168*z - 105) / (2*z - 3)**2


def dominant_positive_margins(z):
    """Return the dominant positive margins (Phi1'', T1-2)."""
    phi1, phi2, phi3 = dominant_derivatives(z)
    return {"Phi1_prime": phi1, "Phi1_second": phi2,
            "Phi1_third": phi3, "T1": dominant_T(z),
            "Phi1_second_margin": phi2, "T1_minus_2": dominant_T(z) - 2}


def dominant_polynomial_certificate():
    """Return exact coefficients of the shifted T1-2 numerator at z=8+w."""
    # (2z-3)^2 (T1-2) / 2, shifted by z=8+w.
    return (113038, 70644, 16408, 1680, 64)


def dominant_global_positive_certificate() -> dict[str, object]:
    """Exact algebraic certificate valid for every rational z>=8."""
    coeffs = dominant_polynomial_certificate()
    return {
        "threshold": 8,
        "phi1_second_identity": "4*(z-3/2)^2+6",
        "t1_minus_2_shifted_coefficients": coeffs,
        "all_shifted_coefficients_positive": all(c > 0 for c in coeffs),
        "status": "PROVED_EXACT_RATIONAL",
    }


def dominant_phi_prime_ratio_bounds():
    """Conservative rational far-field bounds for endpoint work.

    Direct polynomial division shows z <= Phi1' <= (9/2)z for z>=8;
    the certified remainder is far smaller than the available margin.
    """
    return {"lower_coefficient": 1, "upper_coefficient": 5,
            "domain": "z>=8", "status": "PROVED_EXACT_RATIONAL_FOR_DOMINANT"}


def dominant_phi_prime_minus_z_certificate():
    return {"shifted_polynomial": (79, 40, 4),
            "identity": "2*(2*z-3)*(Phi1_prime-z)=4*w^2+40*w+79, z=8+w",
            "status": "PROVED_EXACT_RATIONAL"}


def far_positive_theta_term(x, terms: int = 30, precision: int = 256):
    """Certified positive Theta enclosure for x>=1/2.

    Delegates to the positive source branch of theta_derivative_ball(order=0),
    whose absolute tail is attached symmetrically.  A caller still has to
    verify the requested box lies in the far range.
    """
    return far_positive_theta_partial_ball(x, terms, precision)
