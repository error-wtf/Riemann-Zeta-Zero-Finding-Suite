"""Strictness ledger for the positive production integrals."""
from __future__ import annotations


def inhomogeneous_solution_nonzero(source_nonzero: bool) -> bool:
    """The ODE u'+i alpha u=theta excludes u identically zero if theta is not."""
    if not source_nonzero:
        raise RuntimeError("nonzero-source hypothesis is required")
    return True


def right_production_strict(source_nonzero: bool,
                            production_positive_on_open_set: bool) -> bool:
    """Strict positivity once the improper production integral exists."""
    if not source_nonzero:
        raise RuntimeError("nonzero-source hypothesis is required")
    if not production_positive_on_open_set:
        raise RuntimeError("positive production on an open set is required")
    return True


def strict_energy_status(*, source_nonzero: bool, production_positive_on_open_set: bool) -> dict[str, str]:
    if not source_nonzero or not production_positive_on_open_set:
        return {"volterra_solution_nonzero": "OPEN", "strict_energy": "OPEN"}
    return {
        "volterra_solution_nonzero": "PROVED_ALGEBRAIC_UNDER_INHOMOGENEOUS_SOURCE",
        "strict_energy": "CONDITIONAL_ON_TRACE_AND_INTEGRABILITY",
    }
