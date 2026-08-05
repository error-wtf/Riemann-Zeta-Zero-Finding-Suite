import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.spectral_boundary import boundary_transform_decomposition


def test_spectral_boundary_does_not_overclaim_trace_control():
    result = boundary_transform_decomposition()
    assert "cosine" in result["spectral_constraint"]
    assert result["uncontrolled_component"] == "sine_transform"
    assert result["trace_inequality"] == "OPEN"
