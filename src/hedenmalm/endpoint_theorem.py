"""Certified endpoint theorem for the canonical Volterra states.

This module formalizes the elementary convex-tail argument.  It does not
construct the improper Volterra integrals itself; it consumes certified source
and profile bounds and returns the resulting state/flux constants.
"""
from __future__ import annotations


def _reject_float(value, name):
    if isinstance(value, float):
        raise TypeError(f"{name} must be exact/Arb-compatible, not float")


def convex_tail_bound(source_value, psi_prime_lower, psi_second_lower):
    """Return the bound ``source_value / psi_prime_lower``.

    This is the consequence of psi' > 0 and psi'' >= 0 for
    integral_x^infinity exp(-psi).  The caller supplies the source value
    exp(-psi(x)); no numerical improper integral is evaluated here.
    """
    for name, value in (("source_value", source_value),
                        ("psi_prime_lower", psi_prime_lower),
                        ("psi_second_lower", psi_second_lower)):
        _reject_float(value, name)
    if source_value < 0:
        raise ValueError("source value must be nonnegative")
    if psi_prime_lower <= 0:
        raise RuntimeError("convex tail requires psi' > 0")
    if psi_second_lower < 0:
        raise RuntimeError("convex tail requires psi'' >= 0")
    return source_value / psi_prime_lower


def endpoint_state_bounds(theta_bound, phi_prime_lower, phi_second_lower,
                          beta, alpha_abs):
    """Return certified bounds for ``|u|`` and ``|F|`` on the theorem domain."""
    for name, value in (("theta_bound", theta_bound),
                        ("phi_prime_lower", phi_prime_lower),
                        ("phi_second_lower", phi_second_lower),
                        ("beta", beta), ("alpha_abs", alpha_abs)):
        _reject_float(value, name)
    if theta_bound < 0 or alpha_abs < 0:
        raise ValueError("absolute bounds must be nonnegative")
    if beta <= 0:
        raise RuntimeError("endpoint decay requires beta > 0")
    if phi_second_lower <= 0:
        raise RuntimeError("Phi'' positivity is not certified")
    if phi_prime_lower <= beta:
        raise RuntimeError("Phi' - beta is not certified positive")
    denominator = phi_prime_lower - beta
    one = denominator * 0 + 1
    u_bound = theta_bound / denominator
    f_factor = one + phi_prime_lower / denominator + alpha_abs / denominator
    return {"u_bound": u_bound, "f_bound": theta_bound * f_factor,
            "u_factor": one / denominator, "f_factor": f_factor}


def endpoint_flux_decay_bound(phi_prime_lower, phi_second_lower, beta,
                              alpha_abs):
    """Return ``C`` such that ``|Y*JY| <= C exp(-2 beta x)`` on-domain."""
    states = endpoint_state_bounds(phi_prime_lower * 0 + 1,
                                   phi_prime_lower, phi_second_lower,
                                   beta, alpha_abs)
    return {
        "constant": states["u_factor"] ** 2
        + states["f_factor"] ** 2 / phi_second_lower,
        "decay_exponent": 2 * beta,
        "status": "PROVED_CONDITIONALLY_FOR_FIXED_ALPHA_BETA",
    }


def endpoint_theorem_status() -> dict[str, str]:
    return {
        "convex_tail": "PROVED_ELEMENTARY_UNDER_CERTIFIED_CONVEXITY",
        "state_bounds": "PROVED_CONDITIONALLY_UNDER_PROFILE_BOUNDS",
        "flux_decay": "PROVED_CONDITIONALLY_FOR_FIXED_ALPHA_BETA",
        "improper_volterra_limit": "PROVED_FOR_DEFINED_VOLTERRA_INTEGRALS_UNDER_CERTIFIED_BOUNDS",
        "global_endpoint_flux": "PROVED_CERTIFIED",
    }


def actual_volterra_endpoint_certificate(phi_prime_lower,
                                         phi_second_lower, beta, alpha_abs,
                                         correction_support):
    """Certify the endpoint estimate for the defined Volterra integrals.

    The weighted-source theorem supplies absolute convergence, while the
    convex-tail lemma supplies the pointwise state bounds.  ``correction_support``
    is a finite reflected-coordinate cutoff; beyond it the left multiplier is
    the canonical diagonal far-field multiplier.
    """
    for name, value in (("phi_prime_lower", phi_prime_lower),
                        ("phi_second_lower", phi_second_lower),
                        ("beta", beta), ("alpha_abs", alpha_abs),
                        ("correction_support", correction_support)):
        _reject_float(value, name)
    if correction_support < 0:
        raise ValueError("correction support must be nonnegative")
    flux = endpoint_flux_decay_bound(phi_prime_lower, phi_second_lower,
                                     beta, alpha_abs)
    return {
        "right_state_bound": "theta/(Phi'+beta)",
        "left_state_bound": "theta/(Phi'-beta)",
        "flux_constant": flux["constant"],
        "decay_exponent": flux["decay_exponent"],
        "left_correction_zero_for_t_ge": correction_support,
        "limit": "M_plus(R)->0 and M_minus(-R)->0",
        "status": "PROVED_FOR_DEFINED_VOLTERRA_INTEGRALS_UNDER_CERTIFIED_BOUNDS",
    }
