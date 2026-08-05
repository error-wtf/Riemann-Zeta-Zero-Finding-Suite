"""Two-component Weyl/Lyapunov algebra for the operator pair.

The module derives the first-order system and exposes the matrix residual that
would have to be made positive for a genuine Weyl-Volterra proof.  Existence
of such a positive matrix field is deliberately left open.
"""

from __future__ import annotations

import sympy as sp


def system_matrix(phi_prime: sp.Expr, phi_second: sp.Expr, alpha: sp.Expr) -> sp.Matrix:
    """A_alpha for Y=(u,L_Phi u)^T with Y'=A_alpha Y."""
    return sp.Matrix([[-phi_prime, sp.I], [-sp.I * phi_second, -sp.I * alpha]])


def diagonal_flux_matrix(a: sp.Expr, phi_second: sp.Expr) -> sp.Matrix:
    """The directly visible scalar Green-flux matrix J_a."""
    return a * sp.diag(-phi_second, 1)


def lyapunov_residual(J: sp.Matrix, A: sp.Matrix, x: sp.Symbol) -> sp.Matrix:
    """Return J' + A^*J + JA; positivity is not inferred."""
    return sp.simplify(J.diff(x) + sp.conjugate(A.T) * J + J * A)


def weyl_lyapunov_status() -> dict[str, str]:
    return {
        "system_matrix": "PROVED_ALGEBRAICALLY",
        "visible_diagonal_flux": "PROVED_FORMALLY_UNDER_GREEN_ASSUMPTIONS",
        "common_origin_trace": "OPEN",
        "positive_J_or_H": "OPEN",
        "coupled_halfline_flux": "OPEN",
        "rh_conclusion": "CONDITIONAL_ONLY",
    }
