import pytest

pytest.importorskip("flint")

from flint import arb
from src.certification.far_profile import (
    dominant_derivatives, dominant_T, far_positive_theta_term,
    far_positive_theta_lower_ball, dominant_global_positive_certificate,
    dominant_phi_prime_ratio_bounds,
)
from src.certification.far_remainder import global_remainder_bounds
from src.certification.far_remainder import full_phi_prime_far_bounds
from src.certification.far_remainder import certified_phi_prime_ratio_bound


def test_dominant_profile_is_positive_at_far_threshold():
    z = arb.pi() * (2 * arb(0.5)).exp()
    margins = dominant_derivatives(z)
    assert margins[1].lower() > 0
    assert (dominant_T(z) - 2).lower() > 0


def test_factorized_theta_has_strict_positive_lower_bound():
    theta = far_positive_theta_term(arb("0.5 +/- 0.0001"), terms=30, precision=128)
    assert theta.lower() > 0
    assert far_positive_theta_lower_ball(arb("0.5 +/- 0.0001"), 128).lower() > 0


def test_dominant_formulas_have_no_singular_denominator_on_far_range():
    z = arb(8)
    assert (2*z - 3).lower() > 0


def test_dominant_global_polynomial_certificate_is_exact():
    cert = dominant_global_positive_certificate()
    assert cert["all_shifted_coefficients_positive"]
    assert cert["status"] == "PROVED_EXACT_RATIONAL"
    assert dominant_phi_prime_ratio_bounds()["lower_coefficient"] == 1


def test_far_remainder_bounds_are_strictly_small():
    bounds = global_remainder_bounds(128)
    assert bounds["B_R"].upper() < 1
    assert bounds["L2_bound"].upper() < 1
    assert bounds["L3_bound"].upper() < 1
    full = full_phi_prime_far_bounds(128)
    assert full["lower_at_z8"].lower() > 0
    assert full["status"].startswith("PROVED")


def test_far_positive_theta_rejects_below_threshold():
    with pytest.raises(ValueError):
        far_positive_theta_lower_ball(arb("0.49"), 128)


def test_phi_prime_ratio_uses_only_lower_bound():
    cert = certified_phi_prime_ratio_bound(arb("0.5"), 128)
    assert cert["phi_prime_lower"].lower() > arb(7)
    assert cert["ratio_upper"].upper() < arb("1.067")


def test_phi_prime_ratio_rejects_nonpositive_beta():
    with pytest.raises(ValueError):
        certified_phi_prime_ratio_bound(arb(0), 128)
