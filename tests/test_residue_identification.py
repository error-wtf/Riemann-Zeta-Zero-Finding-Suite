import sympy as sp

from src.hedenmalm.residue_identification import (
    left_residual_identity,
    matrix_residue_identification_status,
    right_residual_identity,
)


def test_right_residual_is_exactly_the_certified_diagonal_form():
    result = right_residual_identity()
    assert result["status"] == "PROVED_EXACT_SYMBOLIC"
    assert result["difference"] == sp.zeros(2)


def test_left_identification_and_schur_match_are_exact():
    status = matrix_residue_identification_status()
    assert status["right_residual_identity"] == "PROVED_EXACT_SYMBOLIC"
    assert status["left_residual_identity"] == "PROVED_EXACT_SYMBOLIC"
    assert status["left_schur_identification"] == "PROVED_EXACT_SYMBOLIC"
    assert status["global_lyapunov_production"] == "PROVED_EXACT_SYMBOLIC"


def test_left_identity_contains_the_correction_derivative_and_four_beta_term():
    result = left_residual_identity()
    assert result["difference"] == sp.zeros(2)
    assert result["schur_difference"] == 0
    assert result["matrix"][0, 1] != 0
    assert result["matrix"][1, 0] != 0
