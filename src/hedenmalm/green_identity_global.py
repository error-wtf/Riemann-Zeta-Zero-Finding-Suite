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
