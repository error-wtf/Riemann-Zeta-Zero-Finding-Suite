"""Fail-closed audit for operator definitions.

Reference zero ordinates belong in comparison data, never in a candidate's
definition.  This small audit is deliberately conservative: suspicious input
names are rejected before a spectral candidate is evaluated.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


_FORBIDDEN = re.compile(r"(?:gamma|zeta[_-]?zero|zero[_-]?list|rho[_-]?n)", re.I)


@dataclass(frozen=True)
class AuditResult:
    passed: bool
    violations: tuple[str, ...]


def audit_definition_inputs(inputs: dict[str, object]) -> AuditResult:
    violations = tuple(sorted(k for k in inputs if _FORBIDDEN.search(k)))
    return AuditResult(not violations, violations)


def require_non_circular(inputs: dict[str, object]) -> None:
    result = audit_definition_inputs(inputs)
    if not result.passed:
        raise ValueError("Non-circularity audit failed: " + ", ".join(result.violations))
