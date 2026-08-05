"""Fail-closed guards for the final weighted-energy contradiction."""

from __future__ import annotations


def contradiction_status(*, multiplier_positive: bool, residual_nonpositive: bool, boundary_terms_zero: bool, nondegenerate: bool) -> dict[str, object]:
    ready = multiplier_positive and residual_nonpositive and boundary_terms_zero and nondegenerate
    return {
        "ready": ready,
        "status": "PROVED_UNDER_ASSUMPTIONS" if ready else "OPEN",
        "missing": tuple(name for name, ok in (
            ("a_b>0", multiplier_positive),
            ("energy residual<=0", residual_nonpositive),
            ("boundary terms vanish", boundary_terms_zero),
            ("L u_alpha != 0", nondegenerate),
        ) if not ok),
    }
