"""Graph-norm closure records for the minimal differential expressions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GraphClosureSpec:
    operator: str
    graph_norm: str
    candidate_domain: str
    status: str


def graph_closure_specs() -> dict[str, GraphClosureSpec]:
    return {
        "D_x": GraphClosureSpec("D_x", "||f||_2 + ||f'||_2", "H^1(R)", "PROVED_UNDER_ASSUMPTIONS"),
        "L_phi": GraphClosureSpec(
            "L_phi", "||f||_2 + ||f'+Phi'f||_2",
            "f in L2, f locally AC, f'+Phi'f in L2", "PROVED_UNDER_ASSUMPTIONS",
        ),
    }
