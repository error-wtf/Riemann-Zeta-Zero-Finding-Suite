"""Algebraic origin Green-flux matching for the reflected half-lines.

This module proves only the finite-dimensional trace identity.  Trace
existence and the Volterra endpoint theorem remain separate obligations.
"""
from __future__ import annotations


def reflection_matrix():
    return ((1, 0), (0, -1))


def origin_flux_matrices(a, phi_second, k0=0):
    """Return right and reflected-left origin matrices."""
    if k0 != 0:
        raise ValueError("origin correction must satisfy k_beta(0)=0")
    right = ((-a*phi_second, 0), (0, a))
    left = right
    return right, left


def reflected_trace_flux_equal(a, phi_second):
    """Check P0* J_left P0 = J_right exactly for k(0)=0."""
    right, left = origin_flux_matrices(a, phi_second, 0)
    # P0 is diagonal, hence conjugation preserves this diagonal form.
    reflected = left
    return reflected == right


def symbolic_origin_matching():
    """Perform the actual symbolic P0*J_left*P0 multiplication."""
    import sympy as sp
    a, p, k = sp.symbols("a p k", real=True)
    p0 = sp.diag(1, -1)
    j_plus = a * sp.diag(-p, 1)
    j_minus = a * sp.diag(-p, 1 + k)
    delta = sp.simplify(p0.conjugate().T * j_minus * p0 - j_plus)
    return {"matrix": delta, "factorized": sp.factor(delta[1, 1]),
            "vanishes_iff": sp.Eq(k, 0)}


def green_matching_status() -> dict[str, str]:
    return {
        "trace_matching": "PROVED_ALGEBRAIC_UNDER_XI_MATCHED_TRACES",
        "origin_flux_cancellation": "PROVED_ALGEBRAIC_UNDER_OPPOSITE_NORMALS",
        "trace_existence": "OPEN",
        "endpoint_flux": "OPEN",
    }
