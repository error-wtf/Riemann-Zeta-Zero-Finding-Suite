"""Status records for positive Fourier-multiplier quadratic forms."""

from __future__ import annotations


def quadratic_form_status(*, epsilon: float, multiplier_nonnegative: bool, domain_declared: bool) -> dict[str, object]:
    strict = epsilon > 0 and multiplier_nonnegative
    return {
        "multiplier_nonnegative": multiplier_nonnegative,
        "strict_floor": strict,
        "domain_declared": domain_declared,
        "status": "OPEN" if not domain_declared else ("CLOSED_POSITIVE_CANDIDATE" if strict else "SEMIDEFINITE_CANDIDATE"),
        "proof_scope": "finite/regularized diagnostic until an infinite-domain closure is proved",
    }
