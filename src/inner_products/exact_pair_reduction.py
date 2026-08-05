"""Formal reduction of the pair identity to a commuting positive Q."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PairReduction:
    equation: str
    commuting_condition: str
    positivity_condition: str
    scope: str


def pair_reduction() -> PairReduction:
    return PairReduction(
        "Q = L^* G L",
        "D Q = Q D",
        "Q >= 0 and <Lu,G Lv>=<u,Qv>",
        "formal identity on a common core; adjoint domains and boundary limits remain required",
    )
