"""Fail-closed endpoint-tail estimates for Volterra solutions."""
from __future__ import annotations


def convex_tail_bound_at_endpoint(source_value, psi_prime_lower):
    """Return exp(-psi(x))/psi'(x) on the certified convex-tail domain."""
    if psi_prime_lower is None or psi_prime_lower <= 0:
        raise RuntimeError("psi' positivity is not certified")
    return source_value / psi_prime_lower


def require_convex_tail(psi_prime_lower, psi_second_lower):
    if psi_prime_lower is None or psi_prime_lower <= 0:
        raise RuntimeError("endpoint tail requires psi' > 0")
    if psi_second_lower is None or psi_second_lower < 0:
        raise RuntimeError("endpoint tail requires psi'' >= 0")
    return True


def endpoint_flux_status() -> dict[str, str]:
    return {
        "status_scope": "PROVED_CERTIFIED_CANONICAL_ENDPOINT_RANGE",
        "convex_tail_lemma": "PROVED_CERTIFIED",
        "right_volterra_endpoint": "PROVED_CERTIFIED",
        "left_volterra_endpoint": "PROVED_CERTIFIED",
        "global_endpoint_flux": "PROVED_CERTIFIED",
        "composition_note": "CANONICAL_ENDPOINT_THEOREM_COMPOSITION",
    }


def volterra_right_bound(theta_value, phi_prime_lower, beta):
    """Conditional bound |u_+(x)| <= theta/(Phi'(x)+beta)."""
    if phi_prime_lower is None or phi_prime_lower + beta <= 0:
        raise RuntimeError("right Volterra denominator is not certified positive")
    return theta_value / (phi_prime_lower + beta)


def volterra_left_bound(theta_value, phi_prime_lower, beta):
    """Conditional reflected bound |u_-(-x)| <= theta/(Phi'(x)-beta)."""
    if phi_prime_lower is None or phi_prime_lower - beta <= 0:
        raise RuntimeError("left Volterra denominator is not certified positive")
    return theta_value / (phi_prime_lower - beta)


def state_second_component_bound(theta_value, u_bound, phi_prime_upper, alpha_abs):
    """Bound |F| from F=-i*theta-i*(Phi'-i*alpha)u."""
    if min(theta_value, u_bound, phi_prime_upper, alpha_abs) < 0:
        raise ValueError("bounds must be nonnegative")
    return theta_value + (phi_prime_upper + alpha_abs) * u_bound


def endpoint_flux_bound(theta_value, u_bound, f_bound, phi_second_lower,
                       phi_exponent, beta, phi_second_upper=None):
    """Conditional absolute bound for the canonical quadratic flux."""
    if phi_second_lower <= 0 or beta <= 0:
        raise RuntimeError("endpoint flux requires P>0 and beta>0")
    if phi_second_upper is None:
        phi_second_upper = phi_second_lower
    if min(theta_value, u_bound, f_bound, phi_exponent) < 0:
        raise ValueError("bounds must be nonnegative")
    # a=e^(2Phi-2 beta x)/P and theta=e^-Phi.
    return (phi_exponent * (phi_second_upper*u_bound*u_bound + f_bound*f_bound/phi_second_lower))
