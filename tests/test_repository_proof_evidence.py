from src.hedenmalm.proof_ledger import (
    ProofStatus,
    assemble_repository_contradiction,
    repository_proof_evidence,
)


def test_repository_assembler_reads_canonical_open_obligations():
    evidence = repository_proof_evidence()
    assert evidence["endpoint"].status is ProofStatus.CONDITIONAL
    assert evidence["green_limit"].status is ProofStatus.OPEN
    assert evidence["origin_matching"].status is ProofStatus.CONDITIONAL
    assert evidence["rh_bridge"].status is ProofStatus.OPEN
    assert evidence["production"].status is ProofStatus.CONDITIONAL
    assert len(evidence["production"].certificate_hashes) == 3
    assert evidence["matrix_residue"].status is ProofStatus.CONDITIONAL


def test_repository_assembler_cannot_be_fed_manual_proved_strings():
    result = assemble_repository_contradiction()
    assert result["global_weyl_volterra_contradiction"] == "OPEN"
    assert result["weyl_contradiction"] == "OPEN"
    assert result["rh_internal_chain"] == "INCOMPLETE"
