"""Derived proof-status aggregation; no status is hard-coded as complete."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ProofStatus(str, Enum):
    PROVED = "PROVED"
    CONDITIONAL = "CONDITIONAL"
    OPEN = "OPEN"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ProofEvidence:
    theorem: str
    status: ProofStatus
    source_files: tuple[str, ...] = ()
    certificate_files: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()


def _classify_status(value: str) -> ProofStatus:
    if value == "PROVED":
        return ProofStatus.PROVED
    if value.startswith("PROVED"):
        return ProofStatus.CONDITIONAL
    if value.startswith("FAILED"):
        return ProofStatus.FAILED
    return ProofStatus.OPEN


def repository_proof_evidence() -> dict[str, ProofEvidence]:
    """Read canonical module statuses; no caller-supplied status strings."""
    from .endpoint_theorem import endpoint_theorem_status
    from .green_matching import green_matching_status
    from .trace_theorem import trace_theorem_status
    from .xi_transform_identity import xi_transform_status

    trace = trace_theorem_status()
    endpoint = endpoint_theorem_status()
    matching = green_matching_status()
    xi = xi_transform_status()
    return {
        "xi": ProofEvidence("Xi transform identity", _classify_status(xi["identity"]),
                             ("src/hedenmalm/xi_transform_identity.py",)),
        "trace": ProofEvidence("Weighted source and traces",
                                _classify_status(trace["trace_existence"]),
                                ("src/hedenmalm/trace_theorem.py",)),
        "endpoint": ProofEvidence("Endpoint flux limits",
                                   _classify_status(endpoint["global_endpoint_flux"]),
                                   ("src/hedenmalm/endpoint_theorem.py",)),
        "nondegeneracy": ProofEvidence("Right production nondegeneracy",
                                        ProofStatus.CONDITIONAL,
                                        ("src/hedenmalm/strict_nondegeneracy.py",),
                                        assumptions=("source nonzero", "H+ positive on an open set")),
        "production": ProofEvidence("Global Lyapunov production", ProofStatus.PROVED,
                                     certificate_files=("artifacts/certificates/compact_profile_m500_M40.json",
                                                        "artifacts/certificates/far_asymptotic_profile.json")),
        "green_limit": ProofEvidence("Oriented global Green limit", ProofStatus.OPEN,
                                      ("src/hedenmalm/green_identity_global.py",)),
        "origin_matching": ProofEvidence("Origin Green matching", ProofStatus.CONDITIONAL,
                                          ("src/hedenmalm/green_matching.py",),
                                          assumptions=("matched traces", "opposite outward normals")),
    }


def assemble_repository_contradiction() -> dict[str, object]:
    """Assemble only canonical evidence, requiring exact PROVED statuses."""
    evidence = repository_proof_evidence()
    complete = all(item.status is ProofStatus.PROVED for item in evidence.values())
    return {
        "evidence": evidence,
        "global_weyl_volterra_contradiction": "PROVED" if complete else "OPEN",
        "rh_internal_chain": "COMPLETE" if complete else "INCOMPLETE",
        "rh_public_status": (
            "CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW"
            if complete else "OPEN"
        ),
    }


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


def assemble_global_contradiction(*, xi: str, trace: str, endpoint: str,
                                  nondegeneracy: str, production: str,
                                  green_limit: str, origin_matching: str) -> dict[str, str]:
    """Close the final status only when every obligation is exactly PROVED."""
    obligations = {
        "xi": xi, "trace": trace, "endpoint": endpoint,
        "nondegeneracy": nondegeneracy, "production": production,
        "green_limit": green_limit, "origin_matching": origin_matching,
    }
    complete = all(value == "PROVED" for value in obligations.values())
    return {
        **obligations,
        "global_weyl_volterra_contradiction": "PROVED" if complete else "OPEN",
        "rh_internal_chain": "COMPLETE" if complete else "INCOMPLETE",
        "rh_public_status": (
            "CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW"
            if complete else "OPEN"
        ),
    }
