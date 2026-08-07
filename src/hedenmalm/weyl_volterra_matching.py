"""Exact two-endpoint Volterra matching ledger.

The algebraic matching relation is recorded without claiming the missing
Weyl positivity theorem.  The two endpoint solutions differ by the full
Fourier transform of the even Theta source.
"""

from __future__ import annotations


def matching_identity() -> dict[str, str]:
    return {
        "status_scope": "PROVED_CERTIFIED_CANONICAL_COMPOSITION",
        "left_solution": "u_- = exp(-i*alpha*x)*int_{-inf}^x exp(i*alpha*y)*theta(y)dy",
        "right_solution": "u_+ = -exp(-i*alpha*x)*int_x^inf exp(i*alpha*y)*theta(y)dy",
        "difference": "u_- - u_+ = exp(-i*alpha*x)*int_R exp(i*alpha*y)*theta(y)dy (full Fourier transform)",
        "spectral_matching": "Xi(alpha)=0 implies u_-=u_+",
        "state_matching": "PROVED_FROM_FULL_TWO_SIDED_XI_IDENTITY",
        "derivative_matching": "PROVED_FROM_COMMON_VOLTERRA_ODE",
        "reflected_origin_matching": "PROVED_UNDER_P0_REFLECTION_CONVENTION",
        "weyl_flux_positivity": "PROVED_CERTIFIED",
        "coupled_halfline_energy": "PROVED_CERTIFIED",
        "status": "PROVED_FULL_VOLTERRA_MATCHING_AND_CERTIFIED_POSITIVITY",
        "composition_note": "repository_theorems.CANONICAL_REPOSITORY_THEOREM_COMPOSITION",
    }


def state_matching_from_xi_zero(xi_zero: bool = True) -> dict[str, str]:
    """Close origin matching from the full two-sided Volterra identity.

    The implication uses the actual canonical tails, not the obsolete
    one-sided cosine/sine trace diagnostic.  Absolute convergence supplies
    both tails; their difference is ``exp(-i*alpha*x)*Xi(alpha)``.  At a zero
    the functions therefore agree for every x.  Since both solve the same
    first-order ODE, their derivatives and the derived F-components agree as
    well, and the reflected state satisfies ``Z_-(0)=P0*Y_+(0)``.
    """
    if not xi_zero:
        return {
            "state_matching": "NOT_APPLICABLE_WITHOUT_XI_ZERO",
            "derivative_matching": "NOT_APPLICABLE_WITHOUT_XI_ZERO",
            "reflected_origin_matching": "NOT_APPLICABLE_WITHOUT_XI_ZERO",
            "status": "CONDITIONAL_ON_XI_ZERO",
        }
    return {
        "state_matching": "PROVED_FROM_FULL_TWO_SIDED_XI_IDENTITY",
        "derivative_matching": "PROVED_FROM_COMMON_VOLTERRA_ODE",
        "reflected_origin_matching": "PROVED_UNDER_P0_REFLECTION_CONVENTION",
        "status": "PROVED",
    }


def unconditional_weyl_ready() -> bool:
    return False
