import pytest

from src.hedenmalm.proof_ledger import global_weyl_volterra_status


def test_open_endpoint_blocks_global_chain():
    with pytest.raises(RuntimeError):
        global_weyl_volterra_status(
            xi="PROVED", trace="PROVED", endpoint="OPEN", nondegeneracy="PROVED"
        )


def test_complete_internal_chain_never_claims_public_rh_proof():
    with pytest.raises(RuntimeError):
        global_weyl_volterra_status(
            xi="PROVED", trace="PROVED", endpoint="PROVED", nondegeneracy="PROVED"
        )
