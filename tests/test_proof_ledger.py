from src.hedenmalm.proof_ledger import global_weyl_volterra_status


def test_open_endpoint_blocks_global_chain():
    status = global_weyl_volterra_status(
        xi="PROVED", trace="PROVED", endpoint="OPEN", nondegeneracy="PROVED"
    )
    assert status["global_weyl_volterra_contradiction"] == "OPEN"
    assert status["rh_internal_chain"] == "INCOMPLETE"
    assert status["rh_public_status"] == "OPEN"


def test_complete_internal_chain_never_claims_public_rh_proof():
    status = global_weyl_volterra_status(
        xi="PROVED", trace="PROVED", endpoint="PROVED", nondegeneracy="PROVED"
    )
    assert status["global_weyl_volterra_contradiction"] == "PROVED"
    assert status["rh_public_status"].startswith("CANDIDATE")
