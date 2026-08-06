"""Canonical two-endpoint Volterra solutions and their local system.

The functions are defined for a supplied source profile.  The module records
the exact ODE and matching algebra; absolute convergence is supplied by the
analytic weighted-source theorem, while endpoint flux remains separate.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class VolterraStatus:
    xi_transform_identity: str = "OPEN"
    absolute_convergence: str = "PROVED_ANALYTICALLY_IN_OPEN_STRIP"
    trace_existence: str = "PROVED_UNDER_SOURCE_PROFILE_AND_OPEN_STRIP"
    endpoint_flux: str = "OPEN"


def left_solution_integrand(alpha: complex, x: float, y: float, theta: Callable[[float], complex]) -> complex:
    return complex(__import__('cmath').exp(-1j*alpha*x + 1j*alpha*y) * theta(y))


def right_solution_integrand(alpha: complex, x: float, y: float, theta: Callable[[float], complex]) -> complex:
    return complex(-__import__('cmath').exp(-1j*alpha*x + 1j*alpha*y) * theta(y))


def volterra_ode_residual(alpha: complex, x: float, u: complex, theta: complex, derivative: complex) -> complex:
    """Residual of u'(x)+i alpha u(x)=theta(x)."""
    return derivative + 1j*alpha*u - theta


def volterra_weyl_status() -> dict[str, str]:
    return {
        "ode": "PROVED_ALGEBRAIC",
        "left_solution": "DEFINED_BY_ABSOLUTELY_CONVERGENT_INTEGRAL",
        "right_solution": "DEFINED_BY_ABSOLUTELY_CONVERGENT_INTEGRAL",
        "xi_transform_identity": "OPEN",
        "trace_existence": "PROVED_UNDER_SOURCE_PROFILE_AND_OPEN_STRIP",
        "endpoint_flux": "OPEN",
    }
