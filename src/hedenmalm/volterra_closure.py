"""Fail-closed ledger for the remaining spectral Volterra closure lemma."""

from __future__ import annotations


def spectral_volterra_closure_status() -> dict[str, str]:
    return {
        "cosine_channel": "CONTROLLED_BY_XI_ZERO",
        "sine_channel": "NOT_CONTROLLED_BY_XI_ZERO_ALONE",
        "volterra_dynamics": "MUST_BE_USED",
        "coupled_halfline_energy": "PROVED_CERTIFIED",
        "spectral_volterra_closure": "PROVED_CERTIFIED",
        "rh_conclusion": "CONDITIONAL_ONLY",
    }


def unrestricted_trace_inequality_allowed() -> bool:
    """The generic trace shortcut was numerically falsified."""
    return False
