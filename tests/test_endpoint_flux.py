import pytest

from src.hedenmalm.endpoint_flux import (
    convex_tail_bound_at_endpoint,
    endpoint_flux_status,
    require_convex_tail,
    volterra_left_bound,
    volterra_right_bound,
    state_second_component_bound,
    endpoint_flux_bound,
)


def test_convex_tail_bound_requires_positive_derivative():
    assert convex_tail_bound_at_endpoint(2.0, 4.0) == 0.5
    with pytest.raises(RuntimeError):
        convex_tail_bound_at_endpoint(2.0, 0.0)


def test_convex_tail_hypotheses_fail_closed():
    assert require_convex_tail(1.0, 0.0)
    with pytest.raises(RuntimeError):
        require_convex_tail(-1.0, 0.0)
    with pytest.raises(RuntimeError):
        require_convex_tail(1.0, -1.0)


def test_endpoint_status_remains_open():
    assert endpoint_flux_status()["global_endpoint_flux"] == "OPEN"


def test_volterra_denominators_fail_closed():
    assert volterra_right_bound(2.0, 3.0, 0.5) == 2.0 / 3.5
    assert volterra_left_bound(2.0, 3.0, 0.5) == 2.0 / 2.5
    with pytest.raises(RuntimeError):
        volterra_left_bound(2.0, 0.25, 0.5)


def test_state_and_flux_bounds_are_conditional_and_positive():
    f = state_second_component_bound(2.0, 0.5, 3.0, 1.0)
    assert f == 4.0
    assert endpoint_flux_bound(2.0, 0.5, f, 2.0, 0.1, 0.2, 4.0) > 0
    with pytest.raises(RuntimeError):
        endpoint_flux_bound(2.0, 0.5, f, 0.0, 0.1, 0.2)
