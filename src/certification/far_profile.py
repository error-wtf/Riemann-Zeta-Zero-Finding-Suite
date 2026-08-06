"""Positive source-faithful far-range algebra.

This module contains the n=1 dominant profile and its exact derivative
formulae.  It intentionally does not claim the infinite-range remainder
bound; that remains a separate fail-closed obligation.
"""
from __future__ import annotations


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


def far_positive_theta_term(x, terms: int = 30, precision: int = 256):
    """Certified positive Theta enclosure for x>=1/2.

    Delegates to the positive source branch of theta_derivative_ball(order=0),
    whose absolute tail is attached symmetrically.  A caller still has to
    verify the requested box lies in the far range.
    """
    from .theta_interval import theta_derivative_ball
    return theta_derivative_ball(x, 0, terms, precision)
