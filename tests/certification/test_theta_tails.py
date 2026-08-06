import pytest
pytest.importorskip("flint")
from src.certification.theta_tail_bounds import q_coefficients, tail_bound
from fractions import Fraction

def test_q_coefficients_are_rational_and_tail_finite():
    assert all(isinstance(x, Fraction) for x in q_coefficients(Fraction(9,2),4))
    assert tail_bound("0.1 +/- 0.001", 4, terms=20, precision=128).upper() >= 0


def test_tail_bound_does_not_increase_with_truncation():
    b20 = tail_bound("0.1 +/- 0.001", 4, terms=20, precision=128).upper()
    b25 = tail_bound("0.1 +/- 0.001", 4, terms=25, precision=128).upper()
    assert b25 <= b20


def test_ratio_validation_rejects_non_geometric_tail():
    from flint import arb
    from src.certification.theta_tail_bounds import validate_ratio

    with pytest.raises(ValueError):
        validate_ratio(arb("1.0"))
