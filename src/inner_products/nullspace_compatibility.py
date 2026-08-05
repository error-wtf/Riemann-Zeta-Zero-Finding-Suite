"""Necessary compatibility checks for descending a Q-form through L."""

from __future__ import annotations


def compatibility_status(*, q_kernel_zero: bool, quotient_declared: bool) -> dict[str, object]:
    return {
        "q_annihilates_L_kernel": q_kernel_zero,
        "quotient_declared": quotient_declared,
        "status": "PROVED_UNDER_ASSUMPTIONS" if q_kernel_zero or quotient_declared else "OPEN",
        "necessary_condition": "Q ker(L)=0 or an explicit quotient/projection must be supplied",
    }
