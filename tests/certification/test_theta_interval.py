import pytest

pytest.importorskip("flint")

from src.certification.theta_interval import (
    finite_phi_derivative_balls,
    finite_profile_status,
    theta_derivative_ball,
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
