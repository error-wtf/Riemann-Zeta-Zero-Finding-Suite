import pytest

pytest.importorskip("flint")

from src.certification.theta_interval import (
    finite_phi_derivative_balls,
    finite_profile_status,
    theta_derivative_ball,
    profile_derivative_balls,
    profile_margin_balls,
)


def test_finite_theta_interval_derivatives_are_balls():
    p1, p2, p3 = finite_phi_derivative_balls("0.1 +/- 0.001", terms=20, precision=128)
    assert p2.lower() > 0
    assert finite_profile_status()["status"] == "TAIL_INCLUDED_NOT_PROFILE_CERTIFIED"


def test_absolute_tail_is_attached_symmetrically():
    from flint import arb

    # A magnitude bound B must include both possible signs of the unknown tail.
    enclosure = arb(0) + arb(0, arb("0.01"))
    assert enclosure.lower() <= arb("-0.01")
    assert enclosure.upper() >= arb("0.01")


def test_theta_ball_restores_precision():
    from flint import ctx

    old = ctx.prec
    theta_derivative_ball("0.1", order=0, terms=20, precision=128)
    assert ctx.prec == old


def test_zero_theta_denominator_fails_closed(monkeypatch):
    import src.certification.theta_interval as module
    from flint import arb

    monkeypatch.setattr(module, "theta_derivative_ball", lambda *args, **kwargs: arb(0))
    with pytest.raises(RuntimeError, match="contains zero"):
        module.finite_phi_derivative_balls("0.1")


def test_profile_derivatives_include_phi_four_and_margins():
    values = profile_derivative_balls("0.1 +/- 0.0001", terms=20, precision=128)
    assert len(values) == 5
    margins = profile_margin_balls("0.1 +/- 0.0001", terms=20, precision=128)
    assert margins["theta"].lower() > 0


def test_negative_theta_ball_is_rejected(monkeypatch):
    import src.certification.theta_interval as module
    from flint import arb

    monkeypatch.setattr(module, "theta_derivative_ball", lambda *args, **kwargs: arb("-1"))
    with pytest.raises(RuntimeError, match="Strict positivity"):
        module.profile_derivative_balls("0.1")
