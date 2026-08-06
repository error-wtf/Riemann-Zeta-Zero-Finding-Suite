"""Small fail-closed Arb backend facade.

This module only certifies interval arithmetic operations. It does not claim
that a finite Theta truncation encloses the infinite series without explicit
tail bounds.
"""

from __future__ import annotations


def backend_status() -> dict[str, object]:
    try:
        import flint
        from flint import ctx
        return {"available": True, "python_flint": getattr(flint, "__version__", "unknown"), "precision": ctx.prec}
    except ImportError:
        return {"available": False, "python_flint": None, "precision": None}


def certified_exp_ball(text: str, precision: int = 256):
    """Return Arb's outward-rounded exponential of an input ball."""
    try:
        from flint import arb, ctx
    except ImportError as exc:  # pragma: no cover - exercised in certification env
        raise RuntimeError("install requirements-certify.txt for Arb certification") from exc
    ctx.prec = precision
    return arb(text).exp()


def definitely_positive(ball) -> bool:
    return ball.lower() > 0
