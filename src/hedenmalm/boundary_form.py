"""Green-boundary forms for the first-order logarithmic operators.

The formulas use the convention ``<f,g>=integral(conj(f)*g)`` and finite
endpoints ``a,b`` as a transparent proxy for endpoint limits.  On the real
line the displayed brackets must be replaced by justified limits; no decay is
assumed automatically.
"""

from __future__ import annotations

import sympy as sp


def endpoint_bracket(expr: sp.Expr, a: sp.Expr, b: sp.Expr) -> sp.Expr:
    return sp.simplify(expr.subs({sp.Symbol("x"): b}) - expr.subs({sp.Symbol("x"): a}))


def dilation_green_form(u: sp.Expr, v: sp.Expr, x: sp.Symbol, a: sp.Expr, b: sp.Expr) -> sp.Expr:
    """Return ``<D u,v>-<u,D v>`` after integration by parts."""
    return sp.simplify(-sp.I * (sp.conjugate(u) * v).subs(x, b) + sp.I * (sp.conjugate(u) * v).subs(x, a))


def weighted_L_green_form(
    u: sp.Expr, v: sp.Expr, Phi: sp.Expr, W: sp.Expr, x: sp.Symbol, a: sp.Expr, b: sp.Expr
) -> dict[str, sp.Expr]:
    """Return boundary term and formal volume residual for ``L_phi``.

    For real ``Phi`` and ``W``, formal symmetry requires ``W'=2 Phi'``.  The
    returned residual makes that condition inspectable rather than silently
    imposing it.
    """
    w = sp.exp(W)
    boundary = sp.simplify(-sp.I * w * sp.conjugate(u) * v).subs(x, b) - sp.simplify(-sp.I * w * sp.conjugate(u) * v).subs(x, a)
    residual = sp.simplify(sp.I * (sp.diff(W, x) - 2 * sp.diff(Phi, x)) * w * sp.conjugate(u) * v)
    return {"boundary": boundary, "volume_residual": residual}


def pair_status() -> dict[str, object]:
    """State what the current Green calculation does and does not establish."""
    return {
        "minimal_core": "C_c^infinity(R)",
        "boundary_form": "available for D and weighted L",
        "pair_form": "not reduced without a declared inverse domain for L",
        "deficiency_indices": "not computed",
        "self_adjointness": "unproven",
    }
