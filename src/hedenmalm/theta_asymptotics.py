"""Asymptotic diagnostics for the formal null vector ``exp(-Phi)``.

The Hedenmalm profile must be supplied by a later, source-faithful module.
These helpers never infer an asymptotic from a finite numerical fit.
"""

from __future__ import annotations

import sympy as sp


def null_vector_integrability(Phi: sp.Expr, x: sp.Symbol) -> dict[str, object]:
    """Report symbolic endpoint limits relevant to ``exp(-Phi) in L2``."""
    plus = sp.limit(Phi, x, sp.oo)
    minus = sp.limit(Phi, x, -sp.oo)
    status = "OPEN"
    if plus is sp.oo and minus is sp.oo:
        status = "PROVED_FORMALLY"
    elif plus is -sp.oo or minus is -sp.oo:
        status = "CONTRADICTION_FOUND"
    return {
        "phi_plus": plus,
        "phi_minus": minus,
        "null_vector": sp.exp(-Phi),
        "square_density": sp.exp(-2 * Phi),
        "status": status,
        "scope": "endpoint growth is necessary; a complete integral proof may need bounds",
    }


def even_profile_check(Phi: sp.Expr, x: sp.Symbol) -> sp.Equality:
    """Return the exact symbolic parity identity for a proposed profile."""
    return sp.Eq(sp.simplify(Phi.subs(x, -x) - Phi), 0)
