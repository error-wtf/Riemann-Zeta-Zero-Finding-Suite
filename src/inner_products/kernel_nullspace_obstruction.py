"""Obstruction check for a strictly positive Q and a nontrivial L-kernel."""

from __future__ import annotations


def nullspace_obstruction_status(*, q_annihilates_kernel: bool, strict_q: bool) -> dict[str, object]:
    return {
        "q_annihilates_kernel": q_annihilates_kernel,
        "strict_q": strict_q,
        "obstruction": strict_q and not q_annihilates_kernel,
        "status": "CONTRADICTION_FOUND" if strict_q and not q_annihilates_kernel else "OPEN",
        "scope": "necessary condition for a form descending through L; not a full kernel theorem",
    }
