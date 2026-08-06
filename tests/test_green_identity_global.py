from src.hedenmalm.green_identity_global import (
    finite_boundary_balance,
    finite_matrix_green_identity_status,
    oriented_halfline_balance,
)


def test_finite_green_identity_balance():
    assert finite_boundary_balance(2.0, 7.0, 5.0) == 0.0


def test_infinite_limit_remains_open():
    status = finite_matrix_green_identity_status()
    assert status["finite_interval_green_identity"] == "PROVED_ALGEBRAIC"
    assert status["infinite_limit"] == "OPEN"


def test_oriented_halfline_signs_are_explicit():
    result = oriented_halfline_balance(5, 0, -7, 0, 5, 7)
    assert result["left_residual"] == 0
    assert result["right_residual"] == 0
    assert result["outward_origin_sum"] == 12
    assert result["production_sum"] == 12
    assert result["endpoint_free_balance"] == 0


def test_nonzero_endpoint_is_not_silently_dropped():
    result = oriented_halfline_balance(5, 2, -7, -3, 3, 4)
    assert result["endpoint_sum"] == 5
    assert result["endpoint_free_balance"] == 5
