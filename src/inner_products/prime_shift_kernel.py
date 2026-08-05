"""Non-circular prime-shift and positive-kernel pattern tools."""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


def _primes(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for n in range(2, int(limit**0.5) + 1):
        if sieve[n]:
            sieve[n * n : limit + 1 : n] = b"\x00" * (((limit - n * n) // n) + 1)
    return [n for n, is_prime in enumerate(sieve) if is_prime]


def prime_shift_trace(E: float, prime_limit: int = 100, repeats: int = 8) -> float:
    """Evaluate the finite prime-power trace using its recurrence directly."""
    total = 0.0
    for p in _primes(prime_limit):
        amplitude = math.log(p) / math.sqrt(p)
        phase = E * math.log(p)
        for _ in range(repeats):
            total += amplitude * math.cos(phase)
            amplitude /= math.sqrt(p)
            phase += E * math.log(p)
    return -total / math.pi


def shift_matrix(shift: float, modes: int = 8, period: float = 2 * math.pi) -> np.ndarray:
    """Fourier representation of ``T_shift f(x)=f(x+shift)`` on a test torus.

    The torus is a finite Galerkin *diagnostic*, not a claim about the true
    half-line domain.  The matrix is unitary, so its Hermitian part is a safe
    building block for kernel pattern searches.
    """
    if modes < 1 or period <= 0:
        raise ValueError("modes must be positive and period must be positive")
    frequencies = np.arange(-modes, modes + 1, dtype=float)
    return np.diag(np.exp(1j * frequencies * shift / period * 2 * math.pi))


def prime_kernel_candidate(prime_limit: int = 13, repeats: int = 2, modes: int = 4, epsilon: float = 1e-6) -> np.ndarray:
    """Build a positive baseline from prime shifts (pattern-finder only)."""
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    size = 2 * modes + 1
    G = epsilon * np.eye(size, dtype=complex)
    for p in _primes(prime_limit):
        for r in range(1, repeats + 1):
            shift = r * math.log(p)
            T = shift_matrix(shift, modes=modes)
            weight = math.log(p) / (p ** (r / 2))
            G += weight * (2 * np.eye(size) - T - T.conj().T)
    return (G + G.conj().T) / 2


@dataclass(frozen=True)
class KernelAudit:
    dimension: int
    hermitian: bool
    min_eigenvalue: float
    intertwining_residual: float
    status: str


def kernel_audit(A: np.ndarray, G: np.ndarray, epsilon: float = 1e-10) -> KernelAudit:
    """Check a finite candidate metric; this is not an operator proof."""
    A = np.asarray(A, dtype=complex)
    G = np.asarray(G, dtype=complex)
    eig = np.linalg.eigvalsh((G + G.conj().T) / 2)
    residual = np.linalg.norm(A.conj().T @ G - G @ A, ord="fro")
    hermitian = np.allclose(G, G.conj().T, rtol=1e-10, atol=1e-12)
    status = "PATTERN_ONLY" if hermitian and float(eig.min()) >= epsilon else "REJECT"
    return KernelAudit(G.shape[0], hermitian, float(eig.min()), float(residual), status)
