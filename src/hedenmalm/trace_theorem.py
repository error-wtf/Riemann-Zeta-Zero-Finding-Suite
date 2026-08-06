"""Conditional trace/admissibility interface for Volterra solutions.

The implementation is deliberately fail-closed: it accepts a trace theorem
only when the caller supplies a certified weighted-L1 majorant.  No numerical
decay sample is treated as a proof of an improper integral.
"""
from __future__ import annotations


def require_weighted_l1_majorant(weighted_integral_bound):
    """Validate a supplied finite certified bound for ``∫ exp(-βx)θ``."""
    if weighted_integral_bound is None:
        raise RuntimeError("weighted L1 majorant is not certified")
    try:
        finite = bool(weighted_integral_bound < float("inf"))
    except Exception as exc:
        raise RuntimeError("weighted L1 majorant is not a certified scalar") from exc
    if not finite:
        raise RuntimeError("weighted L1 majorant is not finite")
    return True


def trace_theorem_status() -> dict[str, str]:
    return {
        "weighted_theta_integrability": "OPEN",
        "volterra_absolute_convergence": "OPEN",
        "trace_existence": "OPEN",
        "local_absolute_continuity": "CONDITIONAL_ON_WEIGHTED_L1",
    }
