import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.energy_experiment import scan_energy_coefficients


def test_energy_scan_is_reproducible_and_not_a_proof():
    result = scan_energy_coefficients(points=9, radius=1.0, dps=30)
    assert result["phi2_positive_on_grid"]
    assert result["s_positive_on_right_grid"]
    assert result["status"] == "NUMERICALLY_SUPPORTED_ONLY"
