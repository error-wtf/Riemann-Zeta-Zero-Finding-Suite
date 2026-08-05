import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.theta_profile_exact import vartheta00_it2, vartheta00_bounds, theta_asymptotic_status


def test_theta_profile_positive_and_inversion_symmetric():
    t = mp.mpf("1.7")
    assert vartheta00_it2(t) > 0
    assert mp.almosteq(vartheta00_it2(t), vartheta00_it2(1 / t), rel_eps=mp.mpf("1e-40"))


def test_theta_bounds_enclose_profile():
    t = mp.mpf("1.3")
    lower, upper = vartheta00_bounds(t)
    value = vartheta00_it2(t)
    assert lower <= value <= upper
    assert theta_asymptotic_status()["phi_identification"] == "OPEN"
