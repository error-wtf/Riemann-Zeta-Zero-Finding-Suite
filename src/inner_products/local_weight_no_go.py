"""Symbolic local-weight diagnostics.

The result is intentionally a *condition*, not a no-go theorem for the full
operator pair.  The inverse of ``L_Phi`` and its closed domain are not encoded
by a scalar weight calculation.
"""

from __future__ import annotations

import sympy as sp


def local_weight_condition(Phi: sp.Expr, W: sp.Expr, x: sp.Symbol) -> dict[str, object]:
    """Derive the formal ``L_Phi`` symmetry condition in weight ``w=e^W``.

    For real Phi and compactly supported test functions, formal symmetry of
    ``L_Phi`` alone requires ``W'=2 Phi'``.  This is not the pair condition.
    """
    equation = sp.Eq(sp.diff(W, x), 2 * sp.diff(Phi, x))
    residual = sp.simplify(sp.diff(W, x) - 2 * sp.diff(Phi, x))
    return {
        "equation": equation,
        "residual": residual,
        "weight_solution": sp.exp(2 * Phi),
        "scope": "formal symmetry of L_Phi on compactly supported functions",
        "pair_status": "undecided_without_inverse_domain",
    }


def pair_probe_status(Phi: sp.Expr, x: sp.Symbol) -> dict[str, object]:
    """Probe a commonly suggested local obstruction without overclaiming."""
    curvature_like = sp.simplify(sp.diff(Phi, x) ** 2 - sp.diff(Phi, x, 2))
    is_constant = not curvature_like.has(x)
    return {
        "expression": curvature_like,
        "constant_expression": is_constant,
        "status": "diagnostic_only",
        "interpretation": "A nonconstant expression rules out only this restricted ansatz, not all positive kernels.",
    }
