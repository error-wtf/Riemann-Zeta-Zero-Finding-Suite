import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.volterra_closure import spectral_volterra_closure_status, unrestricted_trace_inequality_allowed


def test_spectral_volterra_closure_is_explicitly_open():
    status = spectral_volterra_closure_status()
    assert status["cosine_channel"] == "CONTROLLED_BY_XI_ZERO"
    assert status["sine_channel"] == "NOT_CONTROLLED_BY_XI_ZERO_ALONE"
    assert status["spectral_volterra_closure"] == "OPEN"
    assert unrestricted_trace_inequality_allowed() is False
