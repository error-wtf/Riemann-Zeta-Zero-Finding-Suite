"""Source boundary-solution formulas without using L^{-1}."""

from __future__ import annotations


def boundary_solution_formula() -> dict[str, str]:
    return {
        "equation": "u_alpha'(x)+i*alpha*u_alpha(x)=theta(x)",
        "solution": "u_alpha(x)=exp(-i*alpha*x)*int_{-infty}^x exp(i*alpha*y)*theta(y)dy",
        "spectral_boundary": "Xi(alpha)=0 makes the +infinity boundary integral vanish",
        "inverse_used": "False",
        "status": "PROVED_FROM_FIRST_ORDER_VARIATION_UNDER_SOURCE_CONVENTION",
    }
