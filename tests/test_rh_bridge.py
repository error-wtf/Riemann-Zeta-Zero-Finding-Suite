from src.hedenmalm.rh_bridge import parameter_map, rh_symmetry_bridge_status


def test_parameter_map_is_explicit():
    result = parameter_map(3, 1 / 4)
    assert result == {"real_s": 1 / 4, "imag_s": 3}


def test_symmetry_bridge_is_not_overclaimed():
    status = rh_symmetry_bridge_status()
    assert status["parameter_map"] == "PROVED_ALGEBRAIC"
    assert status["rh_bridge"] == "OPEN"
