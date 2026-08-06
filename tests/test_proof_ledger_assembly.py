import pytest

from src.hedenmalm.proof_ledger import assemble_global_contradiction


def test_assembly_stays_open_for_conditional_endpoint_status():
    with pytest.raises(RuntimeError):
        assemble_global_contradiction(
            xi="PROVED", trace="PROVED", endpoint="PROVED_CONDITIONALLY",
            nondegeneracy="PROVED", production="PROVED",
            green_limit="PROVED", origin_matching="PROVED",
        )


def test_assembly_closes_only_with_exact_proved_inputs():
    with pytest.raises(RuntimeError):
        assemble_global_contradiction(
            xi="PROVED", trace="PROVED", endpoint="PROVED",
            nondegeneracy="PROVED", production="PROVED",
            green_limit="PROVED", origin_matching="PROVED",
        )
