"""Analytic no-go ledger for a global positive Fourier multiplier Q."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalMultiplierNoGo:
    status: str
    conclusion: str
    assumptions: tuple[str, ...]
    escape_routes: tuple[str, ...]


def global_multiplier_no_go() -> GlobalMultiplierNoGo:
    return GlobalMultiplierNoGo(
        "CONTRADICTION_FOUND_UNDER_GLOBAL_MULTIPLIER_ASSUMPTIONS",
        "Q=0 almost everywhere if Q=L^* G L, [D,Q]=0 and theta is in the form domain",
        (
            "D is the usual self-adjoint -i d/dx on L2(R)",
            "Q is a nonnegative closed form/operator",
            "Q strongly commutes with D and is q(D), q>=0",
            "L theta=0 and theta is in the form domain",
            "Fourier(theta)=Xi and Xi is nonzero almost everywhere on R",
        ),
        (
            "restrict to a non-global analytic model space",
            "drop strong D-invariance or retain boundary commutator terms",
            "use a non-multiplicative/operator-valued structure",
            "use a de Branges or related reproducing-kernel space",
        ),
    )


def no_go_integral_identity() -> str:
    return "0=<L theta,G L theta>=int q(xi)|Xi(xi)|^2 dxi => q=0 a.e."
