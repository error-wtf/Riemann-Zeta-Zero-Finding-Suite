#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
explicit_tail.py
----------------
Konservative, parametrisierbare Fehlerabschätzung (Tail-Bound) für die
trunkierte Explizitformel (ψ), wenn man die Nullstellensumme bei |γ|>T kappt.

Grundidee (klassische Titchmarsh/Littlewood-Heuristik):
  |R_T(x)| = | sum_{|γ|>T} 2 Re( x^{ρ} / ρ ) |  ≲  2 * x^{1/2} * C * (log(x*T))^2 / T
für geeignete Konstante C > 0. Glättungs-Kerne (Fejér/Parzen) wirken als Faktor ≤ 1.

Dieses Modul liefert eine *konservative* Implementierung mit frei wählbarem
Sicherheitsfaktor C_tail (Default 50.0). Für formale Rigorosität kann C_tail
später via Literaturkonstanten/striktere Bounds nachgezogen werden.

Funktionen:
- kernel_weight(u, kind)
- tail_bound_psi(x, T, kernel="fejer", C_tail=50.0)
- tail_bound_delta_psi(X, H, T, kernel="fejer", C_tail=50.0)
"""

import math
from typing import Literal

KernelKind = Literal["none","fejer","parzen"]

def kernel_weight(u: float, kind: KernelKind = "fejer") -> float:
    u = abs(u)
    if kind == "none" or u <= 0.0:
        return 1.0
    if kind == "fejer":
        return max(0.0, 1.0 - u)
    if kind == "parzen":
        return max(0.0, (1.0 - u) ** 2)
    return max(0.0, 1.0 - u)

def _kernel_tail_factor(kind: KernelKind) -> float:
    # Worst-case „Gewichtsverlust“ im Tail (sehr konservativ).
    # Fejér/Parzen bringen Reduktion ~O(1/T), hier als fixer Faktor ≤ 1 modelliert.
    if kind == "fejer":
        return 0.75
    if kind == "parzen":
        return 0.6
    return 1.0  # none

def _safe_log2(xT: float) -> float:
    v = max(3.0, xT)
    L = math.log(v)
    return max(1.0, L*L)

def tail_bound_psi(x: float, T: float, kernel: KernelKind = "fejer", C_tail: float = 50.0) -> float:
    """
    Obergrenze für |R_T(x)| bei trunkierter ψ-Explizitformel.
    Formel (konservativ):
        |R_T(x)| ≤ 2 * x^{1/2} * (C_tail * _kernel_tail_factor(kernel)) * log(x*T)^2 / max(1, T)
    """
    if x <= 1.0:
        return 0.0
    if T <= 0.0:
        return float("inf")
    fac = _kernel_tail_factor(kernel)
    return 2.0 * (x ** 0.5) * (C_tail * fac) * _safe_log2(x*T) / max(1.0, T)

def tail_bound_delta_psi(X: float, H: float, T: float, kernel: KernelKind = "fejer", C_tail: float = 50.0) -> float:
    """
    Obergrenze für | R_T(X+H) - R_T(X) |. Dreiecksungleichung über Einzelbounds.
    """
    if H <= 0:
        return 0.0
    return tail_bound_psi(X + H, T, kernel, C_tail) + tail_bound_psi(X, T, kernel, C_tail)
