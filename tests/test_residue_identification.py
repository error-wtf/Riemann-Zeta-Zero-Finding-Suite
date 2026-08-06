import sympy as sp

from src.hedenmalm.residue_identification import (
    matrix_residue_identification_status,
    right_residual_identity,
)


def test_right_residual_is_exactly_the_certified_diagonal_form():
    result = right_residual_identity()
    assert result["status"] == "PROVED_EXACT_SYMBOLIC"
    assert result["difference"] == sp.zeros(2)


def test_left_identification_remains_fail_closed_until_matrix_is_defined():
    status = matrix_residue_identification_status()
    assert status["right_residual_identity"] == "PROVED_EXACT_SYMBOLIC"
    assert status["left_residual_identity"].startswith("OPEN")
    assert status["global_lyapunov_production"].startswith("CONDITIONAL")
