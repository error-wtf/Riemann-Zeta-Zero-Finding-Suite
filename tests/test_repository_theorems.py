from fractions import Fraction
import pytest

from src.hedenmalm.proof_ledger import ProofStatus
from src.hedenmalm.repository_theorems import (
    repository_endpoint_theorem,
    repository_green_limit_theorem,
    repository_nondegeneracy_theorem,
)


def test_repository_endpoint_composes_real_certificate_inputs():
    evidence = repository_endpoint_theorem(Fraction(1, 4), Fraction(3))
    assert evidence.status is ProofStatus.PROVED
    assert evidence.certificate_hashes
    assert "global profile certificate" in evidence.assumptions or evidence.dependencies
    with pytest.raises(ValueError):
        repository_endpoint_theorem(Fraction(1, 2), Fraction(3))


def test_repository_green_limit_follows_from_endpoint_decay_and_finite_identity():
    evidence = repository_green_limit_theorem()
    assert evidence.status is ProofStatus.PROVED


def test_repository_nondegeneracy_follows_from_source_and_positive_production():
    evidence = repository_nondegeneracy_theorem()
    assert evidence.status is ProofStatus.PROVED
    assert "theta is strictly positive" in evidence.assumptions[0]
