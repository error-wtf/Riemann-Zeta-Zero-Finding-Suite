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
        "weighted_theta_integrability": "PROVED_UNDER_GLOBAL_GAUSSIAN_BOUND",
        "volterra_absolute_convergence": "PROVED_UNDER_GLOBAL_GAUSSIAN_BOUND",
        "trace_existence": "CONDITIONAL_ON_GLOBAL_GAUSSIAN_BOUND",
        "local_absolute_continuity": "PROVED_UNDER_WEIGHTED_L1",
    }


def certify_gaussian_weighted_integrability(beta: float, gaussian_rate: float) -> bool:
    """Check the sufficient tail hypotheses for |beta|<1/2."""
    if abs(beta) >= 0.5:
        raise RuntimeError("trace theorem requires |Im(alpha)| < 1/2")
    if gaussian_rate <= 0:
        raise RuntimeError("positive Gaussian decay rate is not certified")
    return True
