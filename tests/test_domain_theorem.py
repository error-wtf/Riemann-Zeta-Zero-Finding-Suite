import sys
from pathlib import Path

import sympy as sp
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.domain_theorem import domain_theorem_ledger, nullspace_solution, require_proved


def test_nullspace_solution_is_exact():
    x = sp.symbols("x", real=True)
    assert nullspace_solution(x**2) == sp.exp(-x**2)
    assert next(s for s in domain_theorem_ledger() if s.name == "NULLSPACE").status == "PROVED_UNDER_ASSUMPTIONS"


def test_closed_range_remains_open_and_fails_closed():
    closed = next(s for s in domain_theorem_ledger() if s.name == "CLOSED_RANGE")
    assert closed.status == "OPEN"
    with pytest.raises(ValueError):
        require_proved(closed)
