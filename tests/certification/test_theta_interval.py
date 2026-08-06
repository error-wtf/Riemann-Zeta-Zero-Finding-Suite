import pytest

pytest.importorskip("flint")

from src.certification.theta_interval import finite_phi_derivative_balls, finite_profile_status


def test_finite_theta_interval_derivatives_are_balls():
    p1, p2, p3 = finite_phi_derivative_balls("0.1 +/- 0.001", terms=20, precision=128)
    assert p2.lower() > 0
    assert finite_profile_status()["status"] == "FINITE_TRUNCATION_ONLY"
