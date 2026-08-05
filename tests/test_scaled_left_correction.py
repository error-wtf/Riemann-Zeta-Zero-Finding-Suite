import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.scaled_left_correction import schur_residual, scaled_correction_status


def test_scaled_correction_is_positive_on_small_diagnostic_grid():
    for beta in (0.1, 0.25, 0.5):
        values = [schur_residual(beta * j / 10, beta, terms=30, dps=20) for j in range(11)]
        assert min(values) > 0
    assert scaled_correction_status()["status"] == "OPEN"
