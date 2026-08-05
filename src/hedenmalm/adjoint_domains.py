"""Formal maximal domains for first-order expressions on the line."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdjointDomainSpec:
    operator: str
    minimal_domain: str
    maximal_formal_domain: str
    endpoint_condition: str
    status: str


def formal_adjoint_domains() -> dict[str, AdjointDomainSpec]:
    """Return the weak-derivative domains before endpoint classification."""
    return {
        "D_x": AdjointDomainSpec(
            "-i d/dx", "C_c^infinity(R)",
            "f in L2, f locally AC, f' in L2", "trace limits require proof", "PROVED_UNDER_ASSUMPTIONS",
        ),
        "L_phi": AdjointDomainSpec(
            "-i(d/dx+Phi')", "C_c^infinity(R)",
            "f in L2, f locally AC, f'+Phi'f in L2", "trace limits require proof", "PROVED_UNDER_ASSUMPTIONS",
        ),
    }
