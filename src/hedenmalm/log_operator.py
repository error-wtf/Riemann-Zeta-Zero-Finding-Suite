"""Symbolic, domain-aware form of the logarithmic operator pair.

This file encodes identities and diagnostics only.  It does not assert that
the pair is self-adjoint, nor does it insert a list of zeta zeros.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import sympy as sp


@dataclass(frozen=True)
class LogCoordinateMap:
    t: sp.Expr
    x: sp.Symbol
    relation: sp.Equality
    dilation_identity: sp.Equality


def log_coordinate_map(x: sp.Symbol | None = None) -> LogCoordinateMap:
    x = x or sp.symbols("x", real=True)
    t = sp.exp(x)
    return LogCoordinateMap(t, x, sp.Eq(t, sp.exp(x)), sp.Eq(t * sp.Derivative(sp.Function("f")(t), t), sp.Derivative(sp.Function("f")(sp.exp(x)), x)))


def dilation_operator(f: sp.Expr, x: sp.Symbol) -> sp.Expr:
    """Return ``D^× f = -i d f/dx`` after ``x=log(t)``."""
    return -sp.I * sp.diff(f, x)


def L_phi(f: sp.Expr, Phi: sp.Expr, x: sp.Symbol) -> sp.Expr:
    """Return ``L_Phi f = -i (f' + Phi' f)`` for real Phi."""
    return -sp.I * (sp.diff(f, x) + sp.diff(Phi, x) * f)


def null_vector(Phi: sp.Expr) -> sp.Expr:
    """The formal null vector of ``L_Phi``; domain membership is separate."""
    return sp.exp(-Phi)


def pair_equation(u: sp.Expr, alpha: sp.Expr, Phi: sp.Expr, x: sp.Symbol) -> sp.Expr:
    """Return ``L_Phi D^×u + alpha L_Phi u``.

    The equation is represented without forming ``L_Phi^{-1}``; inverse-domain
    and boundary questions are intentionally left explicit to later modules.
    """
    return sp.simplify(L_phi(dilation_operator(u, x), Phi, x) + alpha * L_phi(u, Phi, x))


def operator_spec() -> dict[str, object]:
    """Machine-readable assumptions for the non-circular operator audit."""
    return {
        "coordinate": "x=log(t), t>0",
        "dilation_operator": "D^×=-i*d/dx",
        "L_operator": "L_Phi=-i*(d/dx+Phi')",
        "pair_equation": "L_Phi D^× u + alpha L_Phi u = 0",
        "core_domain": "C_c^infinity(R) before closure",
        "boundary_status": "must be proved for each closure",
        "inverse_status": "L_Phi^{-1} is not assumed globally; nullspace/domain required",
        "zero_data_allowed": False,
        "proof_status": "symbolic identity only",
    }


def spec_json() -> dict[str, object]:
    """Alias kept for scripts that expect a serialisable specification."""
    return operator_spec()
