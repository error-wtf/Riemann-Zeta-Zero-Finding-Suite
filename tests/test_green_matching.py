from src.hedenmalm.green_matching import (
    reflected_trace_flux_equal,
    green_matching_status,
)


def test_reflected_origin_flux_matches_when_k_zero():
    assert reflected_trace_flux_equal(3, 7)


def test_green_matching_keeps_trace_and_endpoint_obligations_separate():
    status = green_matching_status()
    assert status["trace_matching"].startswith("PROVED")
    assert status["origin_flux_cancellation"].startswith("PROVED")
    assert status["trace_existence"] == "OPEN"
    assert status["endpoint_flux"] == "OPEN"
