"""Null-free Mellin/Fourier resolvent family interface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ResolventFamily:
    numerator_name: str
    variable: str
    poles_allowed_as_inputs: bool
    status: str


def resolvent_family(numerator: Callable[[float], complex] | None = None) -> ResolventFamily:
    """Describe F(xi)/(xi-z) without taking a zero list as input."""
    return ResolventFamily("source Mellin transform F", "xi", False, "PATTERN_ONLY")


def resolvent_value(F: Callable[[float], complex], xi: float, z: complex) -> complex:
    if xi == z:
        raise ValueError("resolvent evaluation at its parameter is undefined")
    return F(xi) / (xi - z)
