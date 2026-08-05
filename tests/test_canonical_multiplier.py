import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.canonical_multiplier import canonical_h, canonical_multiplier_status, S_phi
from src.hedenmalm.volterra_coercivity import volterra_coercivity_status


def test_canonical_multiplier_reduction_is_statused():
    assert canonical_h(0.5, 0.2) > 0
    assert canonical_multiplier_status()["status"] == "OPEN"
    assert isinstance(S_phi(0.4, dps=30), type(S_phi(0.4, dps=30)))


def test_volterra_coercivity_fails_closed():
    result = volterra_coercivity_status(phi2_positive=True, s_positive_right=True, half_axis_control=False, boundary_terms=False)
    assert result["status"] == "OPEN"
    assert "negative half-axis controlled" in result["missing"]
