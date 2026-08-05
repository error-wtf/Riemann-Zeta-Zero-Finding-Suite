"""Fail-closed certification plan for the energy inequalities.

The module separates a proof plan (interval partition + validated backend)
from ordinary high-precision sampling. It never labels mpmath samples as a
global proof.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BoundStatus:
    name: str
    status: str
    backend: str
    reason: str


def backend_status() -> dict[str, str]:
    try:
        import flint  # type: ignore
    except ImportError:
        return {"backend": "none", "status": "OPEN", "reason": "python-flint/Arb is not installed"}
    return {"backend": "python-flint/Arb", "status": "AVAILABLE", "reason": "validated ball arithmetic can be requested"}


def certification_plan(*, compact_radius: float = 4.0, compact_cells: int = 512) -> tuple[BoundStatus, ...]:
    if compact_radius <= 0 or compact_cells < 2:
        raise ValueError("compact_radius must be positive and compact_cells >= 2")
    backend = backend_status()
    status = "OPEN" if backend["status"] != "AVAILABLE" else "READY_FOR_VALIDATED_RUN"
    return (
        BoundStatus("PHI2_GLOBAL_BOUND", status, backend["backend"], "prove Phi''>0 on compact core and asymptotic tails"),
        BoundStatus("S_PHI_RIGHT_BOUND", status, backend["backend"], "prove 2 Phi' Phi''-Phi'''>0 on x>0"),
        BoundStatus("VOLTERRA_BOUNDARY_CONTROL", status, backend["backend"], "prove weighted integrability and vanishing Green terms"),
    )


def proof_readiness() -> dict[str, object]:
    statuses = certification_plan()
    return {
        "all_formal_bounds_ready": all(s.status == "READY_FOR_VALIDATED_RUN" for s in statuses),
        "statuses": tuple((s.name, s.status) for s in statuses),
        "status": "OPEN",
    }
