from src.hedenmalm.proof_ledger import assemble_global_contradiction


def test_assembly_stays_open_for_conditional_endpoint_status():
    result = assemble_global_contradiction(
        xi="PROVED", trace="PROVED", endpoint="PROVED_CONDITIONALLY",
        nondegeneracy="PROVED", production="PROVED",
        green_limit="PROVED", origin_matching="PROVED",
    )
    assert result["global_weyl_volterra_contradiction"] == "OPEN"
    assert result["rh_internal_chain"] == "INCOMPLETE"


def test_assembly_closes_only_with_exact_proved_inputs():
    result = assemble_global_contradiction(
        xi="PROVED", trace="PROVED", endpoint="PROVED",
        nondegeneracy="PROVED", production="PROVED",
        green_limit="PROVED", origin_matching="PROVED",
    )
    assert result["global_weyl_volterra_contradiction"] == "PROVED"
    assert result["rh_public_status"].startswith("CANDIDATE_PROOF_COMPLETE")
