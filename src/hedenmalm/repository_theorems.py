"""Canonical composition of the remaining repository proof obligations."""
from __future__ import annotations

from fractions import Fraction

from .endpoint_theorem import actual_volterra_endpoint_certificate
from .proof_ledger import (
    ProofEvidence,
    ProofStatus,
    _lower_ball,
    _load_json_certificate,
    load_global_production_evidence,
)
from .trace_theorem import trace_theorem_status


def repository_endpoint_theorem(beta, alpha_abs) -> ProofEvidence:
    """Compose the published profile certificate with the endpoint lemma.

    The result remains conditional until the repository promotes the endpoint
    theorem from its explicit source-profile hypothesis to an unconditional
    theorem object.
    """
    if beta <= 0 or beta >= Fraction(1, 2):
        raise ValueError("beta must lie in (0, 1/2)")
    if alpha_abs < 0:
        raise ValueError("alpha_abs must be nonnegative")
    production = load_global_production_evidence()
    if production.status is not ProofStatus.PROVED:
        return ProofEvidence("Repository endpoint theorem", ProofStatus.OPEN,
                             assumptions=("global production certificate",))
    far, _ = _load_json_certificate("artifacts/certificates/far_asymptotic_profile.json")
    m = Fraction(8) - Fraction(str(_lower_ball(far["B_DR"])))
    p0 = Fraction(str(_lower_ball(far["Phi_second_lower"])))
    certificate = actual_volterra_endpoint_certificate(
        m, p0, beta, alpha_abs, beta
    )
    trace = trace_theorem_status()
    return ProofEvidence(
        "Repository endpoint theorem", ProofStatus.CONDITIONAL,
        source_files=("src/hedenmalm/repository_theorems.py",
                      "src/hedenmalm/endpoint_theorem.py"),
        certificate_files=production.certificate_files,
        source_commits=production.source_commits,
        publication_commits=production.publication_commits,
        certificate_hashes=production.certificate_hashes,
        dependencies=("weighted source theorem", "global profile certificate",
                       certificate["status"]),
        assumptions=(trace["trace_existence"],
                     "endpoint certificate is conditional on source/profile hypotheses"),
    )


def repository_endpoint_theorem_schema() -> ProofEvidence:
    """Evidence for the universally quantified fixed-parameter theorem."""
    return ProofEvidence(
        "Repository endpoint theorem for every fixed alpha with 0<Im(alpha)<1/2",
        ProofStatus.CONDITIONAL,
        source_files=("src/hedenmalm/repository_theorems.py",
                      "src/hedenmalm/endpoint_theorem.py"),
        dependencies=("global profile certificate", "weighted source theorem",
                       "finite-support correction"),
        assumptions=("beta is arbitrary with 0<beta<1/2",
                     "alpha_abs is finite and fixed",
                     "Volterra integrals use the canonical source profile"),
    )


def repository_green_limit_theorem() -> ProofEvidence:
    """Compose oriented finite identities with the current endpoint evidence."""
    endpoint = repository_endpoint_theorem_schema()
    if endpoint.status is ProofStatus.PROVED:
        status = ProofStatus.PROVED
        assumptions = ()
    else:
        status = ProofStatus.OPEN
        assumptions = ("endpoint limits must be promoted to an unconditional theorem",
                       "finite oriented Green identities",)
    return ProofEvidence(
        "Repository global Green limit", status,
        source_files=("src/hedenmalm/green_identity_global.py",
                      "src/hedenmalm/repository_theorems.py"),
        dependencies=("oriented_halfline_balance", "repository endpoint theorem"),
        assumptions=assumptions,
    )


def repository_nondegeneracy_theorem() -> ProofEvidence:
    """Record the source/OE/nonzero-state implication with its assumptions."""
    production = load_global_production_evidence()
    status = (ProofStatus.CONDITIONAL
              if production.status is ProofStatus.PROVED else ProofStatus.OPEN)
    return ProofEvidence(
        "Repository right-state nondegeneracy", status,
        source_files=("src/hedenmalm/strict_nondegeneracy.py",
                      "src/hedenmalm/repository_theorems.py"),
        certificate_files=production.certificate_files,
        certificate_hashes=production.certificate_hashes,
        dependencies=("positive source", "right production positive for x>0"),
        assumptions=("existence of the improper production integral",
                     "continuity of the Volterra state"),
    )
