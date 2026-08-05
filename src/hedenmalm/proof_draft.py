"""Machine-readable ledger for the conditional energy-proof draft.

The ledger is intentionally fail-closed: formal algebra is separated from
the global analytic lemmas still required for an unconditional conclusion.
"""

from __future__ import annotations


def energy_proof_ledger() -> dict[str, str]:
    return {
        "LEMMA_1_WEIGHTED_IDENTITY": "PROVED_FORMALLY_UNDER_BOUNDARY_ASSUMPTIONS",
        "LEMMA_2_CANONICAL_REDUCTION": "PROVED_ALGEBRAICALLY",
        "LEMMA_3_GLOBAL_COEFFICIENT_BOUNDS": "OPEN",
        "LEMMA_4_ENDPOINT_AND_TRACE_CONTROL": "OPEN",
        "LEMMA_5_VOLTERRA_COERCIVITY": "OPEN",
        "NONDEGENERACY": "PROVED_UNDER_SOURCE_ASSUMPTIONS",
        "RH_CONCLUSION": "CONDITIONAL_ONLY",
    }


def unconditional_ready() -> bool:
    """Never silently promote the conditional draft to a theorem."""
    return False
