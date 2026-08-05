"""Fail-closed weak factorisation interface for a nonlocal form."""

from __future__ import annotations


def weak_factorization_status(*, kernel_removed: bool, range_closed: bool) -> dict[str, object]:
    """Describe the conditions needed before defining G from Q and L."""
    admissible = kernel_removed and range_closed
    return {
        "kernel_removed": kernel_removed,
        "range_closed": range_closed,
        "factorization_allowed": admissible,
        "status": "OPEN" if not admissible else "PATTERN_ONLY",
    }


def require_weak_factorization(*, kernel_removed: bool, range_closed: bool) -> None:
    if not kernel_removed or not range_closed:
        raise ValueError("weak factorization requires a removed kernel and proved closed range")
