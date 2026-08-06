"""Derived proof-status aggregation; no status is hard-coded as complete."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


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
    source_commits: tuple[str, ...] = ()
    publication_commits: tuple[str, ...] = ()
    certificate_hashes: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()


def _classify_status(value: str) -> ProofStatus:
    if value == "PROVED":
        return ProofStatus.PROVED
    if value.startswith("PROVED"):
        return ProofStatus.CONDITIONAL
    if value.startswith("FAILED"):
        return ProofStatus.FAILED
    return ProofStatus.OPEN


def _load_json_certificate(relative_path: str) -> tuple[dict, str]:
    root = Path(__file__).resolve().parents[2]
    path = root / relative_path
    try:
        raw = path.read_bytes()
        return json.loads(raw), hashlib.sha256(raw).hexdigest()
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"certificate cannot be loaded: {relative_path}") from exc


def _lower_ball(value: str) -> Decimal:
    try:
        text = value.strip().strip("[]")
        midpoint, radius = text.split("+/-")
        return Decimal(midpoint.strip()) - Decimal(radius.strip())
    except (AttributeError, InvalidOperation, ValueError) as exc:
        raise RuntimeError(f"invalid Arb ball: {value!r}") from exc


def load_global_production_evidence() -> ProofEvidence:
    compact_path = "artifacts/certificates/compact_profile_m500_M40.json"
    far_path = "artifacts/certificates/far_asymptotic_profile.json"
    compact, compact_hash = _load_json_certificate(compact_path)
    far, far_hash = _load_json_certificate(far_path)
    compact_ok = (
        compact.get("status") == "PROVED_OUTWARD_ROUNDED_ON_[0,1/2]"
        and compact.get("all_boxes_covered") is True
        and compact.get("number_of_boxes", 0) > 0
        and bool(compact.get("formula_version"))
    )
    far_ok = (
        far.get("status") == "PROVED_OUTWARD_ROUNDED_ON_[z>=8]"
        and _lower_ball(far["Phi_second_lower"]) > 0
        and _lower_ball(far["T_lower"]) > 2
        and bool(far.get("formula_version"))
    )
    status = ProofStatus.PROVED if compact_ok and far_ok else ProofStatus.OPEN
    return ProofEvidence(
        theorem="Global Lyapunov production", status=status,
        certificate_files=(compact_path, far_path),
        source_commits=tuple(filter(None, (
            compact.get("certificate_source_commit", compact.get("source_commit")),
            far.get("source_commit"),
        ))),
        publication_commits=tuple(filter(None, (
            compact.get("certificate_published_in"),
            far.get("certificate_published_in"),
        ))),
        certificate_hashes=(compact_hash, far_hash),
        dependencies=("compact profile certificate", "far remainder certificate"),
    )


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
        "production": load_global_production_evidence(),
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
    raise RuntimeError("deprecated: use assemble_repository_contradiction()")


def assemble_global_contradiction(*, xi: str, trace: str, endpoint: str,
                                  nondegeneracy: str, production: str,
                                  green_limit: str, origin_matching: str) -> dict[str, str]:
    raise RuntimeError("deprecated: use assemble_repository_contradiction()")
