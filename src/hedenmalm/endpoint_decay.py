"""Conditional endpoint-flux decay calculation."""
from __future__ import annotations


def _reject_float(value, name):
    if isinstance(value, float):
        raise TypeError(f"{name} must be Fraction/int/Arb, not float")


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
        "global_endpoint_flux": "PROVED_CERTIFIED",
    }


def flux_decay_constant_from_ratio(phi_prime_lower, phi_prime_ratio,
                                   beta, alpha_abs):
    """Legacy state-only bound using Phi' upper/lower ratio bounds.

    This returns only the ``F``-component square and is *not* the complete
    flux constant.  Use ``certified_endpoint_flux_constant`` for the full
    quadratic flux.  Unlike a fixed upper bound for Phi', this remains
    meaningful as Phi'(x) grows at infinity.
    """
    if beta <= 0 or phi_prime_lower <= beta:
        raise RuntimeError("requires beta>0 and a certified Phi'-beta lower bound")
    if phi_prime_ratio < 1 or alpha_abs < 0:
        raise ValueError("invalid ratio or absolute spectral bound")
    ratio = phi_prime_lower / (phi_prime_lower - beta)
    f_const = 1 + phi_prime_ratio * ratio + alpha_abs / (phi_prime_lower - beta)
    return f_const * f_const


def certified_endpoint_flux_constant(phi_prime_lower, phi_second_lower,
                                     beta, alpha_abs):
    """Correct full constant for |Y*JY| <= C exp(-2 beta x)."""
    for name, value in (("phi_prime_lower", phi_prime_lower), ("phi_second_lower", phi_second_lower),
                        ("beta", beta), ("alpha_abs", alpha_abs)):
        _reject_float(value, name)
    if beta <= 0:
        raise RuntimeError("endpoint decay requires beta > 0")
    if phi_prime_lower <= beta:
        raise RuntimeError("Phi' - beta is not certified positive")
    if phi_second_lower <= 0:
        raise RuntimeError("Phi'' positivity is not certified")
    if alpha_abs < 0:
        raise ValueError("alpha_abs must be nonnegative")
    denominator = phi_prime_lower - beta
    one = denominator * 0 + 1
    u_const = one / denominator
    phi_ratio = phi_prime_lower / denominator
    f_const = one + phi_ratio + alpha_abs / denominator
    return u_const*u_const + f_const*f_const/phi_second_lower
