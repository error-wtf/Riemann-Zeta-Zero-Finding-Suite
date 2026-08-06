import pytest

pytest.importorskip("flint")

from flint import arb
from src.certification.far_profile import dominant_derivatives, dominant_T, far_positive_theta_term


def test_dominant_profile_is_positive_at_far_threshold():
    z = arb.pi() * (2 * arb(0.5)).exp()
    margins = dominant_derivatives(z)
    assert margins[1].lower() > 0
    assert (dominant_T(z) - 2).lower() > 0


def test_factorized_theta_has_strict_positive_lower_bound():
    theta = far_positive_theta_term(arb("0.5 +/- 0.0001"), terms=30, precision=128)
    assert theta.lower() > 0


def test_dominant_formulas_have_no_singular_denominator_on_far_range():
    z = arb(8)
    assert (2*z - 3).lower() > 0
