"""Non-degeneracy guard for the source eigenfunctions.

If ``L_phi u_alpha`` vanished, then ``u_alpha=C exp(-phi)=C Theta``. The
source first-order identity would force ``D^×Theta/Theta + alpha`` to be
constant. The published Gaussian asymptotic makes that logarithmic derivative
unbounded, so this is impossible for finite alpha and nonzero C.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NonDegeneracyStatus:
    status: str
    statement: str
    assumptions: tuple[str, ...]


def non_degeneracy_status() -> NonDegeneracyStatus:
    return NonDegeneracyStatus(
        "PROVED_UNDER_SOURCE_ASYMPTOTIC",
        "Xi(alpha)=0 and u_alpha nonzero imply L_phi00 u_alpha != 0",
        (
            "phi_00=-log(Theta_00(i t^2))",
            "Theta_00 has published Gaussian asymptotic",
            "alpha is finite",
            "u_alpha is the source boundary solution",
        ),
    )


def contradiction_if_null_image() -> dict[str, str]:
    return {
        "assumption": "L_phi00 u_alpha=0",
        "consequence": "u_alpha=C*Theta_00(i t^2)",
        "source_identity": "D^×u_alpha+alpha*u_alpha=i^(-1)*Theta_00(i t^2)",
        "asymptotic_obstruction": "D^×Theta/Theta+alpha is unbounded as t->infinity",
        "status": "CONTRADICTION_FOUND_UNDER_SOURCE_ASYMPTOTIC",
    }
