from fractions import Fraction

from src.hedenmalm.proof_ledger import ProofStatus
from src.hedenmalm.repository_theorems import (
    repository_endpoint_theorem,
    repository_green_limit_theorem,
    repository_nondegeneracy_theorem,
)


def test_repository_endpoint_composes_real_certificate_inputs():
    evidence = repository_endpoint_theorem(Fraction(1, 2), Fraction(3))
    assert evidence.status is ProofStatus.CONDITIONAL
    assert evidence.certificate_hashes
    assert "global profile certificate" in evidence.assumptions or evidence.dependencies


def test_repository_green_limit_stays_open_until_endpoint_is_unconditional():
    evidence = repository_green_limit_theorem()
    assert evidence.status is ProofStatus.OPEN


def test_repository_nondegeneracy_is_not_falsely_unconditional():
    evidence = repository_nondegeneracy_theorem()
    assert evidence.status is ProofStatus.CONDITIONAL
    assert "improper production integral" in evidence.assumptions[0]
