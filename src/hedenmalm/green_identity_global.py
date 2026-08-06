"""Finite-interval Green/Lyapunov identity.

The identity is exact for AC solutions on a finite interval.  No improper
integral or endpoint limit is inferred here.
"""
from __future__ import annotations


def finite_matrix_green_identity_status() -> dict[str, str]:
    return {
        "interval": "finite [a,b]",
        "identity": "d(Y*JY)/dx = Y*(J' + A*J + JA)Y",
        "regularity": "CONDITIONAL_ON_Y_AC_LOCAL_AND_J_AC_LOCAL",
        "finite_interval_green_identity": "PROVED_ALGEBRAIC",
        "infinite_limit": "OPEN",
    }


def finite_boundary_balance(left_flux, right_flux, production_integral):
    """Return the exact balance ``right-left-production`` for diagnostics."""
    return right_flux - left_flux - production_integral


def oriented_halfline_balance(left_origin, left_endpoint, right_origin,
                              right_endpoint, left_production,
                              right_production):
    """Return the oriented outer-origin balance on [-R,0] and [0,R].

    The finite identities are
    ``left_origin-left_endpoint=left_production`` and
    ``right_endpoint-right_origin=right_production``.  Thus the outward
    origin sum is ``left_origin-right_origin`` and equals the sum of the two
    productions after endpoint terms vanish.  Keeping this bookkeeping
    explicit prevents a hidden sign change in the reflection step.
    """
    left_residual = left_origin - left_endpoint - left_production
    right_residual = right_endpoint - right_origin - right_production
    outward_origin_sum = left_origin - right_origin
    production_sum = left_production + right_production
    endpoint_sum = left_endpoint - right_endpoint
    return {
        "left_residual": left_residual,
        "right_residual": right_residual,
        "outward_origin_sum": outward_origin_sum,
        "production_sum": production_sum,
        "endpoint_sum": endpoint_sum,
        "endpoint_free_balance": outward_origin_sum - production_sum,
    }
