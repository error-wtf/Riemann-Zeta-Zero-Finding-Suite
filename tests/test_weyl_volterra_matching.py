import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.weyl_volterra_matching import matching_identity, unconditional_weyl_ready


def test_two_endpoint_matching_is_explicit_but_positivity_open():
    result = matching_identity()
    assert "full Fourier transform" in result["difference"]
    assert result["spectral_matching"].startswith("Xi(alpha)=0")
    assert result["weyl_flux_positivity"] == "OPEN"
    assert unconditional_weyl_ready() is False
