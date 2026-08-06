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
        "weighted_theta_integrability": "PROVED_ANALYTICALLY_IN_OPEN_STRIP",
        "volterra_absolute_convergence": "PROVED_ANALYTICALLY_IN_OPEN_STRIP",
        "trace_existence": "PROVED_UNDER_SOURCE_PROFILE_AND_OPEN_STRIP",
        "local_absolute_continuity": "PROVED_UNDER_SOURCE_PROFILE",
    }


def certify_gaussian_weighted_integrability(beta: float, gaussian_rate: float) -> bool:
    """Check the sufficient tail hypotheses for |beta|<1/2."""
    if abs(beta) >= 0.5:
        raise RuntimeError("trace theorem requires |Im(alpha)| < 1/2")
    if gaussian_rate <= 0:
        raise RuntimeError("positive Gaussian decay rate is not certified")
    return True


def weighted_theta_l1_bound_formula() -> dict[str, str]:
    """Return the analytic majorant used for the weighted source."""
    return {
        "source_bound": "2*pi^2*exp(-pi)/(1-16*exp(-3*pi))",
        "decay_rate": "2*pi-9/2",
        "weighted_l1_bound": "4*pi^2*exp(-pi)/((1-16*exp(-3*pi))*(2*pi-9/2-|beta|))",
        "domain": "|beta| < 1/2",
        "proof": "evenness + e^(2x)-1 >= 2x + geometric n-tail",
    }


def certified_weighted_theta_l1_bound(beta, precision: int = 256):
    """Evaluate the analytic L1 majorant with outward-rounded Arb."""
    from flint import arb, ctx
    old = ctx.prec
    try:
        ctx.prec = precision
        b = arb(beta)
        abs_b = abs(b)
        if abs_b.upper() >= arb(1) / 2:
            raise RuntimeError("trace theorem requires |Im(alpha)| < 1/2")
        geometric_den = 1 - 16 * (-3 * arb.pi()).exp()
        if geometric_den.lower() <= 0:
            raise RuntimeError("geometric theta tail denominator is not positive")
        decay_den = 2 * arb.pi() - arb(9) / 2 - abs_b
        if decay_den.lower() <= 0:
            raise RuntimeError("weighted decay denominator is not positive")
        c_theta = 2 * arb.pi()**2 * (-arb.pi()).exp() / geometric_den
        bound = 2 * c_theta / decay_den
        if bound.lower() <= 0:
            raise RuntimeError("weighted L1 bound is not strictly positive")
        return {"bound": bound, "source_constant": c_theta,
                "decay_rate": 2 * arb.pi() - arb(9) / 2,
                "status": "PROVED_OUTWARD_ROUNDED"}
    finally:
        ctx.prec = old
