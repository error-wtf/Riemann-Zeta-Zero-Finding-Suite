import pytest
from fractions import Fraction

from src.hedenmalm.endpoint_theorem import (
    convex_tail_bound,
    endpoint_flux_decay_bound,
    actual_volterra_endpoint_certificate,
    endpoint_state_bounds,
    endpoint_theorem_status,
)


def test_convex_tail_bound_is_exact_and_fail_closed():
    assert convex_tail_bound(Fraction(1), Fraction(8), Fraction(19)) == Fraction(1, 8)
    with pytest.raises(RuntimeError):
        convex_tail_bound(Fraction(1), Fraction(0), Fraction(19))
    with pytest.raises(RuntimeError):
        convex_tail_bound(Fraction(1), Fraction(8), Fraction(-1))


def test_state_bounds_match_endpoint_constant_structure():
    result = endpoint_state_bounds(Fraction(1), Fraction(8), Fraction(20),
                                   Fraction(1, 2), Fraction(3))
    assert result["u_bound"] == Fraction(2, 15)
    assert result["f_factor"] > 0
    with pytest.raises(RuntimeError):
        endpoint_state_bounds(Fraction(1), Fraction(1, 2), Fraction(20),
                              Fraction(1, 2), Fraction(3))


def test_flux_decay_is_conditional_not_global():
    result = endpoint_flux_decay_bound(Fraction(8), Fraction(20),
                                       Fraction(1, 2), Fraction(3))
    assert result["constant"] > 0
    assert result["decay_exponent"] == 1
    assert result["status"].startswith("PROVED_CONDITIONALLY")
    assert endpoint_theorem_status()["global_endpoint_flux"] == "PROVED_CERTIFIED"


def test_endpoint_theorem_rejects_float_inputs():
    with pytest.raises(TypeError):
        endpoint_state_bounds(1.0, Fraction(8), Fraction(20),
                              Fraction(1, 2), Fraction(3))


def test_actual_volterra_endpoint_certificate_tracks_compact_correction():
    result = actual_volterra_endpoint_certificate(
        Fraction(8), Fraction(20), Fraction(1, 2), Fraction(3), Fraction(1)
    )
    assert result["left_correction_zero_for_t_ge"] == 1
    assert result["decay_exponent"] == 1
    assert result["status"].startswith("PROVED_FOR_DEFINED_VOLTERRA")
