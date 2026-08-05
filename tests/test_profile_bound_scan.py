import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.profile_bound_scan import polynomial_lower_bound, scan_profile_bounds


def test_profile_bound_scan_and_polynomial_margin_are_positive_diagnostics():
    result = scan_profile_bounds(xmax=0.5, points=31, terms=30, dps=20)
    assert result["m_lower_sample"] > 500
    assert result["P_upper_sample"] < 40
    assert min(polynomial_lower_bound(j / 100, 500, 40) for j in range(101)) > 0
    assert result["status"] == "NUMERICALLY_SUPPORTED_ONLY"
