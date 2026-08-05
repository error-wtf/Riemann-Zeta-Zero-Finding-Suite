"""Numerical positive Gram kernels from a source transform F."""

from __future__ import annotations

import numpy as np


def gram_kernel(F, z: complex, w: complex, grid: np.ndarray) -> complex:
    values = F(grid) if callable(F) else np.asarray(F, dtype=complex)
    return np.trapezoid(np.abs(values) ** 2 / ((grid - z) * (grid - np.conjugate(w))), grid)


def gram_matrix(F, parameters: list[complex], grid: np.ndarray) -> np.ndarray:
    return np.array([[gram_kernel(F, z, w, grid) for w in parameters] for z in parameters], dtype=complex)


def gram_status(G: np.ndarray, tolerance: float = 1e-9) -> dict[str, object]:
    H = (G + G.conj().T) / 2
    eigenvalues = np.linalg.eigvalsh(H)
    return {
        "hermitian": bool(np.allclose(G, G.conj().T, atol=tolerance)),
        "min_eigenvalue": float(eigenvalues.min()),
        "positive_on_grid": bool(eigenvalues.min() >= -tolerance),
        "status": "PATTERN_ONLY",
    }
