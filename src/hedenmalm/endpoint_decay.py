"""Conditional endpoint-flux decay calculation."""
from __future__ import annotations


def flux_decay_constant(phi_prime_lower, phi_prime_upper, phi_second_lower,
                        beta, alpha_abs):
    """Return C in |Y*JY| <= C exp(-2 beta x).

    This is the algebraic substitution of |u|,|F| <= C_source*theta into
    a=exp(2 Phi-2 beta x)/Phi''.  The source-tail constant is normalized to 1;
    callers must supply its certified value separately.
    """
    if beta <= 0:
        raise RuntimeError("decay requires beta > 0")
    if phi_prime_lower <= beta or phi_second_lower <= 0:
        raise RuntimeError("required positive far-field denominators are open")
    if min(phi_prime_upper, alpha_abs) < 0:
        raise ValueError("absolute bounds must be nonnegative")
    u_const = 1.0 / (phi_prime_lower - beta)
    f_const = 1.0 + (phi_prime_upper + alpha_abs) * u_const
    return phi_second_lower*u_const*u_const + f_const*f_const/phi_second_lower


def endpoint_decay_status() -> dict[str, str]:
    return {
        "decay_calculation": "PROVED_ALGEBRAIC_UNDER_FAR_BOUNDS",
        "right_endpoint_limit": "CONDITIONAL_ON_BOUNDS",
        "left_endpoint_limit": "CONDITIONAL_ON_BOUNDS",
        "global_endpoint_flux": "OPEN",
    }
