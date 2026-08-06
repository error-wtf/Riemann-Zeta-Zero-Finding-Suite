"""Derived proof-status aggregation; no status is hard-coded as complete."""
from __future__ import annotations


def global_weyl_volterra_status(*, xi: str, trace: str, endpoint: str, nondegeneracy: str,
                                production: str = "PROVED") -> dict[str, str]:
    obligations = {"xi": xi, "trace": trace, "endpoint": endpoint,
                   "nondegeneracy": nondegeneracy, "production": production}
    complete = all(value.startswith("PROVED") for value in obligations.values())
    return {
        **obligations,
        "global_weyl_volterra_contradiction": "PROVED" if complete else "OPEN",
        "rh_internal_chain": "COMPLETE" if complete else "INCOMPLETE",
        "rh_public_status": "CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW" if complete else "OPEN",
    }
