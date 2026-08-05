"""Formal local-weight no-go calculation for the complete pair.

On the compactly supported core, let ``M=d/dx+p`` with ``p=Phi'`` and
``L=-i M, D=-i d/dx``. For ``w=exp(W)>0`` in the weighted L2 pairing, the
pair identity reduces to ``d_w^* Q + Q d = 0`` with ``Q=M_w^* M``. Comparing
the independent differential coefficients yields ``W'=0`` and then constant
``p``. Thus a nonconstant source profile admits no local scalar weight within
this ansatz. This is not a statement about nonlocal kernels or other domains.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalPairNoGo:
    status: str
    conditions: tuple[str, ...]
    scope: str


def local_pair_conditions() -> LocalPairNoGo:
    return LocalPairNoGo(
        "PROVED_FORMALLY_UNDER_LOCAL_WEIGHT_ANSATZ",
        ("W'=0", "(W'-2 Phi')'=0", "(Phi' W' - (Phi')^2 - Phi'')'=0"),
        "compactly supported core, real locally smooth Phi, positive scalar w=e^W, standard weighted L2",
    )


def source_profile_conclusion() -> dict[str, str]:
    return {
        "premise": "Phi'(x) is nonconstant for the source phi_00 asymptotic",
        "result": "no positive scalar local weight satisfies the complete pair identity in the stated ansatz",
        "status": "CONTRADICTION_FOUND_UNDER_LOCAL_WEIGHT_ANSATZ",
        "next": "nonlocal kernel or a different Hilbert/domain structure is required",
    }
