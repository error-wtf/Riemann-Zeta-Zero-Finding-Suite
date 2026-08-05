"""Guards for the formal inverse of ``L_Phi``."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InverseDomainCheck:
    kernel_dimension: str
    range_closed: str
    inverse_domain: str
    status: str


def inverse_domain_status() -> InverseDomainCheck:
    return InverseDomainCheck(
        kernel_dimension="unknown until Phi and its Hilbert domain are fixed",
        range_closed="not established",
        inverse_domain="not defined globally",
        status="OPEN",
    )


def require_inverse_domain(*, kernel_removed: bool, range_closed: bool) -> None:
    """Fail closed before constructing ``L_Phi^{-1}``."""
    if not kernel_removed:
        raise ValueError("L_Phi inverse is undefined while its kernel is present")
    if not range_closed:
        raise ValueError("L_Phi inverse requires a proved closed range")
