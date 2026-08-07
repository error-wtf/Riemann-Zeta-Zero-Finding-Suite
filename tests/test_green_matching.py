from src.hedenmalm.green_matching import (
    reflected_trace_flux_equal,
    green_matching_status,
    symbolic_origin_matching,
)
from src.hedenmalm.weyl_volterra_matching import (
    matching_identity,
    state_matching_from_xi_zero,
)


def test_reflected_origin_flux_matches_when_k_zero():
    assert reflected_trace_flux_equal(3, 7)


def test_green_matching_keeps_trace_and_endpoint_obligations_separate():
    status = green_matching_status()
    assert status["trace_matching"].startswith("PROVED")
    assert status["origin_flux_cancellation"].startswith("PROVED")
    assert status["trace_existence"].startswith("PROVED_UNDER_SOURCE_PROFILE")
    assert status["endpoint_flux"] == "PROVED_CERTIFIED"


def test_actual_symbolic_matrix_conjugation_has_k_factor():
    result = symbolic_origin_matching()
    assert str(result["factorized"]) == 'a*k'
    assert str(result["vanishes_iff"]) == "Eq(k, 0)"


def test_nonzero_origin_correction_breaks_matching():
    result = symbolic_origin_matching()
    assert result["matrix"][1, 1] != 0


def test_full_two_sided_volterra_identity_closes_state_matching():
    status = matching_identity()
    assert status["state_matching"] == "PROVED_FROM_FULL_TWO_SIDED_XI_IDENTITY"
    assert status["reflected_origin_matching"] == "PROVED_UNDER_P0_REFLECTION_CONVENTION"
    assert state_matching_from_xi_zero()["status"] == "PROVED"


def test_one_sided_trace_diagnostic_is_not_used_by_matching_route():
    status = state_matching_from_xi_zero()
    assert "ONE_SIDED" not in " ".join(status.values())
