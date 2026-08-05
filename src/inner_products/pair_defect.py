"""Finite-basis pair-defect measurements (never an operator proof)."""

from __future__ import annotations

import numpy as np


def pair_defect(L: np.ndarray, LD: np.ndarray, G: np.ndarray) -> float:
    """Return ||(LD)^* G L - L^* G (LD)||_F."""
    L = np.asarray(L, dtype=complex)
    LD = np.asarray(LD, dtype=complex)
    G = np.asarray(G, dtype=complex)
    return float(np.linalg.norm(LD.conj().T @ G @ L - L.conj().T @ G @ LD, ord="fro"))


def defect_status(value: float, tolerance: float = 1e-10) -> str:
    return "ZERO_ON_FINITE_BASIS" if value <= tolerance else "NONZERO_FINITE_BASIS"
