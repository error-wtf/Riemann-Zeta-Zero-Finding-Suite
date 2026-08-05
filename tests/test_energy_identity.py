import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.boundary_solution import boundary_solution_formula
from src.hedenmalm.energy_identity import multiplier_residual, weighted_energy_identity, energy_ledger


def test_boundary_solution_avoids_inverse():
    result = boundary_solution_formula()
    assert result["inverse_used"] == "False"
    assert "Xi(alpha)" in result["spectral_boundary"]


def test_energy_residual_is_exactly_symbolic():
    x = sp.symbols("x", real=True)
    a = 1 + x**2
    Phi = x**4
    expected = sp.diff(a * sp.diff(Phi, x, 2), x) - 2 * a * sp.diff(Phi, x) * sp.diff(Phi, x, 2)
    assert sp.simplify(multiplier_residual(a, Phi, x) - expected) == 0
    assert weighted_energy_identity(a, Phi, x).status.startswith("PROVED_FORMALLY")


def test_energy_sign_and_coercivity_remain_open():
    ledger = energy_ledger()
    assert ledger["P0_ENERGY_IDENTITY"].startswith("PROVED")
    assert ledger["P2_COERCIVE_MULTIPLIER"] == "OPEN"
