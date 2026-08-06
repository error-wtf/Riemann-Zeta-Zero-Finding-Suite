"""Exact algebraic checks for the Lyapunov residual matrices.

The profile certificates control scalar expressions.  This module checks the
missing algebraic bridge from those expressions to the actual first-order
system.  The right-hand identity is complete; the corrected reflected-left
system is intentionally not guessed here and remains open until its matrix
is defined canonically.
"""
from __future__ import annotations

import sympy as sp


def right_residual_identity():
    """Return the exact symbolic identity for the canonical right matrix.

    With ``alpha = xi + i beta``, ``q = exp(2 Phi - 2 beta x)``,
    ``A = [[-Phi', i], [-i Phi'', -i alpha]]`` and
    ``J = q*diag(-1, 1/Phi'')``, direct differentiation gives
    ``J' + A.H*J + J*A = q*diag(2 beta, S_phi)``.
    """
    p, p2, p3 = sp.symbols("phi_prime phi_second phi_third", real=True)
    xi, beta, q = sp.symbols("xi beta q", real=True)
    alpha = xi + sp.I * beta
    A = sp.Matrix([[-p, sp.I], [-sp.I * p2, -sp.I * alpha]])
    J = q * sp.diag(-1, 1 / p2)
    # q' = 2(Phi' - beta)q and (Phi'')' = Phi'''.
    J_prime = q * sp.diag(
        -2 * (p - beta),
        2 * (p - beta) / p2 - p3 / p2**2,
    )
    residual = sp.simplify(J_prime + sp.conjugate(A.T) * J + J * A)
    target = q * sp.diag(2 * beta, (2 * p * p2 - p3) / p2**2)
    return {
        "residual": residual,
        "target": target,
        "difference": sp.simplify(residual - target),
        "status": "PROVED_EXACT_SYMBOLIC"
        if residual == target else "CONTRADICTION_FOUND",
    }


def matrix_residue_identification_status() -> dict[str, str]:
    """Report the exact state of the matrix-to-certificate bridge."""
    right = right_residual_identity()
    return {
        "right_residual_identity": right["status"],
        "left_residual_identity": "OPEN_LEFT_MATRIX_NOT_CANONICALLY_DEFINED",
        "left_schur_identification": "OPEN",
        "certificate_formula_match": "OPEN",
        "global_lyapunov_production": "CONDITIONAL_ON_LEFT_IDENTIFICATION",
    }
