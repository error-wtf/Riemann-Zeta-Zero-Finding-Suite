import pytest

from src.hedenmalm.strict_nondegeneracy import (
    inhomogeneous_solution_nonzero,
    strict_energy_status,
)


def test_inhomogeneous_source_excludes_zero_solution():
    assert inhomogeneous_solution_nonzero(True)
    with pytest.raises(RuntimeError):
        inhomogeneous_solution_nonzero(False)


def test_strict_energy_keeps_integrability_condition_visible():
    status = strict_energy_status(source_nonzero=True, production_positive_on_open_set=True)
    assert status["volterra_solution_nonzero"].startswith("PROVED")
    assert status["strict_energy"].startswith("CONDITIONAL")
