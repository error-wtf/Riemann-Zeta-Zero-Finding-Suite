"""Declared test domains for the logarithmic differential operators.

These are domain *specifications*, not a claim that a particular closure is
self-adjoint.  The minimal operators start on compactly supported smooth
functions; endpoint traces and adjoint domains must be established separately.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainSpec:
    name: str
    interval: str
    regularity: str
    boundary_condition: str
    closure_status: str


def minimal_domains() -> dict[str, DomainSpec]:
    core = "C_c^infinity(R)"
    return {
        "D_x": DomainSpec("D_x", "R", "smooth compact support", "none on the core", "not closed"),
        "L_phi": DomainSpec("L_phi", "R", "smooth compact support", "none on the core", "not closed"),
        "L_phi_D_x": DomainSpec("L_phi D_x", "R", "smooth compact support", "none on the core", "not closed"),
    }


def closure_questions() -> tuple[str, ...]:
    return (
        "identify the graph closure of each minimal operator",
        "compute the maximal adjoint domain",
        "classify endpoint traces at x -> +/- infinity",
        "compute deficiency spaces before choosing boundary conditions",
    )
