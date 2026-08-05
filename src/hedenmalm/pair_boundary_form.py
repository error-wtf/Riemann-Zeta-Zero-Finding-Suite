"""Status-aware boundary-form interface for the operator pair."""

from __future__ import annotations


def pair_boundary_status() -> dict[str, str]:
    return {
        "expression": "<L_phi D_x u,L_phi v>-<L_phi u,L_phi D_x v>",
        "volume_term": "requires full symbolic expansion with declared weight",
        "boundary_term": "requires traces of u, D_x u, L_phi u",
        "inverse_domain": "required before defining -L_phi D_x L_phi^{-1}",
        "status": "OPEN",
    }
