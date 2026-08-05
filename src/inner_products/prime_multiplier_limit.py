"""Regularised prime-shift multiplier diagnostics."""

from __future__ import annotations

import math

from .prime_shift_kernel import _primes


def regularized_coefficients(prime_limit: int, repeats: int, sigma: float) -> list[tuple[int, int, float]]:
    if sigma <= 0:
        raise ValueError("sigma must be positive for the regularized diagnostic")
    result = []
    for p in _primes(prime_limit):
        for r in range(1, repeats + 1):
            result.append((p, r, math.log(p) / (p ** (r * (0.5 + sigma)))))
    return result


def multiplier_limit_status(*, sigma: float, prime_limit: int, repeats: int) -> dict[str, object]:
    if sigma <= 0:
        return {
            "status": "REGULARIZED_ONLY",
            "reason": "the unregularized prime sum is not declared convergent",
            "sigma": sigma,
        }
    coeffs = regularized_coefficients(prime_limit, repeats, sigma)
    return {
        "status": "REGULARIZED_ONLY",
        "sigma": sigma,
        "finite_terms": len(coeffs),
        "absolute_finite_cutoff": sum(abs(c) for _, _, c in coeffs),
        "infinite_limit": "OPEN",
    }
