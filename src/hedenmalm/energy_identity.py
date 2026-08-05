"""Symbolic weighted energy identity for the actual pair equation."""

from __future__ import annotations

from dataclasses import dataclass
import sympy as sp


@dataclass(frozen=True)
class EnergyIdentity:
    identity: str
    residual: sp.Expr
    assumptions: tuple[str, ...]
    status: str


def multiplier_residual(a: sp.Expr, Phi: sp.Expr, x: sp.Symbol) -> sp.Expr:
    """Return R_a=(a Phi'')' - 2 a Phi' Phi'' exactly."""
    return sp.simplify(sp.diff(a * sp.diff(Phi, x, 2), x) - 2 * a * sp.diff(Phi, x) * sp.diff(Phi, x, 2))


def weighted_energy_identity(a: sp.Expr, Phi: sp.Expr, x: sp.Symbol) -> EnergyIdentity:
    residual = multiplier_residual(a, Phi, x)
    return EnergyIdentity(
        "2 Im(alpha) int a|L_Phi u|^2 = -int a'|L_Phi u|^2 + int R_a|u|^2",
        residual,
        (
            "u solves L_Phi D u + alpha L_Phi u=0",
            "a is real smooth",
            "all displayed integrals converge",
            "all Green boundary terms vanish",
        ),
        "PROVED_FORMALLY_UNDER_BOUNDARY_ASSUMPTIONS",
    )


def energy_ledger() -> dict[str, str]:
    return {
        "P0_ENERGY_IDENTITY": "PROVED_FORMALLY_UNDER_BOUNDARY_ASSUMPTIONS",
        "P1_SIGN_STRUCTURE": "OPEN",
        "P2_COERCIVE_MULTIPLIER": "OPEN",
        "P3_BOUNDARY_VANISHING": "OPEN",
        "P4_COMPLEX_ALPHA_CONTRADICTION": "OPEN",
    }
