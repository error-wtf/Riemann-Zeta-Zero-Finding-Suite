from src.hedenmalm.green_identity_global import (
    finite_boundary_balance,
    finite_matrix_green_identity_status,
)


def test_finite_green_identity_balance():
    assert finite_boundary_balance(2.0, 7.0, 5.0) == 0.0


def test_infinite_limit_remains_open():
    status = finite_matrix_green_identity_status()
    assert status["finite_interval_green_identity"] == "PROVED_ALGEBRAIC"
    assert status["infinite_limit"] == "OPEN"
