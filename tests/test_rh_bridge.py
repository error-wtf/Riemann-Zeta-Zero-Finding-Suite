from fractions import Fraction
from src.hedenmalm.rh_bridge import parameter_map, rh_symmetry_bridge_status


def test_parameter_map_is_explicit():
    result = parameter_map(3, 1 / 4)
    assert result == {"real_s": Fraction(1, 4), "imag_s": 3}


def test_symmetry_bridge_is_explicit_and_separate_from_public_review():
    status = rh_symmetry_bridge_status()
    assert status["parameter_map"] == "PROVED_ALGEBRAIC"
    assert status["xi_evenness"].startswith("PROVED")
    assert status["right_halfplane_exclusion_by_xi_symmetry"].startswith("PROVED")
    assert status["rh_bridge"] == "PROVED"
