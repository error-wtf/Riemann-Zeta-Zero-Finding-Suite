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
    left = left_residual_identity()
    right = right_residual_identity()
    return {
        "right_residual_identity": right["status"],
        "left_residual_identity": left["status"],
        "left_schur_identification": left["schur_status"],
        "certificate_formula_match": left["schur_status"],
        "global_lyapunov_production": "PROVED_EXACT_SYMBOLIC"
        if right["status"] == "PROVED_EXACT_SYMBOLIC"
        and left["status"] == "PROVED_EXACT_SYMBOLIC"
        and left["schur_status"] == "PROVED_EXACT_SYMBOLIC"
        else "CONDITIONAL_ON_RESIDUE_IDENTIFICATION",
    }


def reflected_system_matrix():
    """Return the reflected matrix for ``Z(t)=P0*Y(-t)``."""
    p, q, xi, beta = sp.symbols("phi_prime phi_second xi beta", real=True)
    alpha = xi + sp.I * beta
    return sp.Matrix([[-p, sp.I], [-sp.I * q, sp.I * alpha]])


def left_residual_identity():
    """Derive the corrected-left residual and Schur complement exactly."""
    p, q, r = sp.symbols("phi_prime phi_second phi_third", real=True)
    xi, beta, k, kp, f = sp.symbols("xi beta k k_prime factor", real=True)
    alpha = xi + sp.I * beta
    A = sp.Matrix([[-p, sp.I], [-sp.I * q, sp.I * alpha]])
    J = f * sp.diag(-1, (1 + k) / q)
    # f' = 2(Phi' - beta)f and q' = r.
    J_prime = f * sp.diag(
        -2 * (p - beta),
        2 * (p - beta) * (1 + k) / q + kp / q
        - (1 + k) * r / q**2,
    )
    direct = sp.simplify(J_prime + sp.conjugate(A.T) * J + J * A)
    T = (2 * p * q - r) / q
    expected = f * sp.Matrix([
        [2 * beta, sp.I * k],
        [-sp.I * k, ((1 + k) * (T - 4 * beta) + kp) / q],
    ])
    difference = sp.simplify(direct - expected)
    normalized = direct / f
    schur = sp.factor(normalized[1, 1] - normalized[1, 0]
                      * normalized[0, 1] / normalized[0, 0])
    G = (1 + k) * (T - 4 * beta) + kp - q * k**2 / (2 * beta)
    schur_difference = sp.simplify(schur - G / q)
    return {
        "matrix": direct,
        "expected": expected,
        "difference": difference,
        "schur": schur,
        "schur_difference": schur_difference,
        "status": "PROVED_EXACT_SYMBOLIC"
        if difference == sp.zeros(2) else "CONTRADICTION_FOUND",
        "schur_status": "PROVED_EXACT_SYMBOLIC"
        if schur_difference == 0 else "CONTRADICTION_FOUND",
    }
