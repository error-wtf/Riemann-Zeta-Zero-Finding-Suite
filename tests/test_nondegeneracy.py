import pytest

from src.hedenmalm.strict_nondegeneracy import (
    inhomogeneous_solution_nonzero,
    right_production_strict,
)


def test_nonzero_source_excludes_zero_volterra_state():
    assert inhomogeneous_solution_nonzero(True)
    with pytest.raises(RuntimeError):
        inhomogeneous_solution_nonzero(False)


def test_right_production_requires_open_set_positivity():
    assert right_production_strict(True, True)
    with pytest.raises(RuntimeError):
        right_production_strict(False, True)
    with pytest.raises(RuntimeError):
        right_production_strict(True, False)
