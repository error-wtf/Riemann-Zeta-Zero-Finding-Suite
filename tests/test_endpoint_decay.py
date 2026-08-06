import pytest

from src.hedenmalm.endpoint_decay import endpoint_decay_status, flux_decay_constant


def test_decay_constant_is_finite_when_hypotheses_hold():
    assert flux_decay_constant(10.0, 20.0, 5.0, 0.5, 3.0) > 0


def test_decay_rejects_zero_beta_and_bad_denominators():
    with pytest.raises(RuntimeError):
        flux_decay_constant(10.0, 20.0, 5.0, 0.0, 3.0)
    with pytest.raises(RuntimeError):
        flux_decay_constant(0.25, 20.0, 5.0, 0.5, 3.0)


def test_endpoint_decay_status_remains_conditional():
    assert endpoint_decay_status()["global_endpoint_flux"] == "OPEN"
