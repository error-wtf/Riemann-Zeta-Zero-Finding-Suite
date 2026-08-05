import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.energy_proof_guards import contradiction_status
from src.hedenmalm.theta_derivative_diagnostics import diagnostic_status, phi_derivatives


def test_energy_contradiction_guard_fails_closed():
    result = contradiction_status(multiplier_positive=True, residual_nonpositive=True, boundary_terms_zero=False, nondegenerate=True)
    assert result["status"] == "OPEN"
    assert "boundary terms vanish" in result["missing"]


def test_theta_derivative_layer_is_not_a_proof():
    values = phi_derivatives(0.4, dps=30)
    assert len(values) == 3
    assert diagnostic_status()["P2_COERCIVE_MULTIPLIER"] == "OPEN"
