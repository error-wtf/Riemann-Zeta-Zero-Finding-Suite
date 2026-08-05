import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.profile_identification import phi00, Phi_log, profile_identification_status, asymptotic_leading_terms


def test_source_profile_identification_and_inversion():
    assert profile_identification_status()["status"] == "PROVED_FROM_SOURCE"
    x = mp.mpf("0.7")
    assert mp.almosteq(Phi_log(x), Phi_log(-x), rel_eps=mp.mpf("1e-40"))
    assert mp.isfinite(phi00(1))


def test_source_asymptotic_is_recorded_without_overclaiming():
    result = asymptotic_leading_terms()
    assert "O(exp(-2x))" in result["x_to_plus_infinity"]
    assert result["status"] == "PROVED_FROM_SOURCE_ASYMPTOTIC"
