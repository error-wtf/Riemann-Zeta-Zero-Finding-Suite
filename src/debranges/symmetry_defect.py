"""Finite-grid symmetry-defect bookkeeping."""

from __future__ import annotations

import numpy as np


def symmetry_defect(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(left) - np.asarray(right), ord="fro"))
