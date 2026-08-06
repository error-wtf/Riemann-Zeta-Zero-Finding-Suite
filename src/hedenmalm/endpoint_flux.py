"""Fail-closed endpoint-tail estimates for Volterra solutions."""
from __future__ import annotations


def convex_tail_bound_at_endpoint(source_value, psi_prime_lower):
    """Return exp(-psi(x))/psi'(x) under certified convex-tail hypotheses."""
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
        "convex_tail_lemma": "PROVED_CONDITIONALLY",
        "right_volterra_endpoint": "OPEN",
        "left_volterra_endpoint": "OPEN",
        "global_endpoint_flux": "OPEN",
    }
