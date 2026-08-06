from src.hedenmalm.proof_ledger import (
    ProofStatus,
    assemble_repository_contradiction,
    repository_proof_evidence,
)


def test_repository_assembler_reads_canonical_open_obligations():
    evidence = repository_proof_evidence()
    assert evidence["endpoint"].status is ProofStatus.PROVED
    assert evidence["green_limit"].status is ProofStatus.PROVED
    assert evidence["origin_matching"].status is ProofStatus.PROVED
    assert evidence["rh_bridge"].status is ProofStatus.PROVED
    assert evidence["production"].status is ProofStatus.PROVED
    assert len(evidence["production"].certificate_hashes) == 3
    assert evidence["matrix_residue"].status is ProofStatus.PROVED


def test_repository_assembler_cannot_be_fed_manual_proved_strings():
    result = assemble_repository_contradiction()
    assert result["global_weyl_volterra_contradiction"] == "PROVED"
    assert result["weyl_contradiction"] == "PROVED"
    assert result["rh_internal_chain"] == "COMPLETE"
