"""Finite-precision diagnostic for the scaled left-half-line correction."""

from __future__ import annotations

import mpmath as mp

from .theta_derivative_series import phi_derivatives_from_series


def bump_profile(t: float, beta: float, amplitude: float = 10.0, width: float = 1.0) -> tuple[mp.mpf, mp.mpf]:
    if beta <= 0 or width <= 0:
        raise ValueError("beta and width must be positive")
    tau = mp.mpf(t) / beta
    if tau < 0 or tau > width:
        return mp.mpf("0"), mp.mpf("0")
    return (beta**2 * amplitude * tau * (1 - tau / width) ** 2,
            beta * amplitude * (1 - tau / width) * (1 - 3 * tau / width))


def schur_residual(t: float, beta: float, *, amplitude: float = 10.0, width: float = 1.0, terms: int = 80, dps: int = 40) -> mp.mpf:
    with mp.workdps(dps):
        p1, p2, p3 = phi_derivatives_from_series(t, terms, dps)
        S = (2 * p1 * p2 - p3) / p2**2
        T = S * p2
        k, kp = bump_profile(t, beta, amplitude, width)
        return (1 + k) * (T - 4 * beta) + kp - p2 * k**2 / (2 * beta)


def scaled_correction_status() -> dict[str, str]:
    return {
        "ansatz": "k_beta=beta^2*A*(t/beta)*(1-t/(beta*L))^2 on 0<=t<=beta*L",
        "sampled_schur_residual": "NUMERICALLY_SUPPORTED_ONLY",
        "global_interval_certificate": "OPEN",
        "left_endpoint_and_matching": "OPEN",
        "status": "OPEN",
    }
