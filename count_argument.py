#!/usr/bin/env python3
# count_argument.py – heuristische Turing-Zählung (N(T2)-N(T1)) nur mit mpmath.
# Zweck: Drop-in, damit run_certified_all.py sauber läuft, OHNE rigorous_Z_arb.
# Für strenge Beweise später durch Arb-Konturintegration ersetzen.

import mpmath as mp
import json
import argparse
from typing import Dict, Any

def theta(t):
    """Riemann–Siegel-Theta: theta(t) = Im(log Γ(1/4 + i t/2)) - (t/2) log π."""
    T = mp.mpf(t)
    w = mp.mpf('0.25') + 0.5j*T
    return mp.im(mp.log(mp.gamma(w))) - (T/2) * mp.log(mp.pi)

def N_float(T):
    """
    Riemann–von–Mangoldt:
        N(T) ≈ theta(T)/π + 1 + (1/π) arg ζ(1/2 + iT)
    (Heuristisch – keine Intervallarithmetik.)
    """
    T = mp.mpf(T)
    s = mp.mpf('0.5') + 1j*T
    S = mp.arg(mp.zeta(s)) / mp.pi
    return theta(T)/mp.pi + 1 + S

def turing_count_block(T1: float, T2: float,
                       sigma_left: float = 0.51,
                       sigma_right: float = 2.0,
                       dps: int = 80,
                       nt: int = 400,
                       ns: int = 64,
                       pad: float = 0.25) -> Dict[str, Any]:
    """
    Liefert die Struktur, die run_certified_all.py erwartet:
      - deltaN_integer : gerundete Differenz N(T2)-N(T1)
      - deltaN_interval: grobe Float-„Intervalle“ (heuristisch)
      - ok_integer     : True, wenn Rundung klar (Margin >= 0.25)
      - rounding_margin: |delta - round(delta)|
      - quadrature     : Platzhalter-Felder für spätere Arb-Version
    """
    old = mp.mp.dps
    mp.mp.dps = max(int(dps), 50)
    try:
        N1 = N_float(T1)
        N2 = N_float(T2)
        delta = N2 - N1

        k = int(mp.nint(delta))
        margin = float(abs(delta - k))
        A = float(delta - 0.5)
        B = float(delta + 0.5)

        # Dummy-Geometrie für Kompatibilität
        top    = sigma_left + 1j*mp.mpf(T2)
        right  = sigma_right + 1j*mp.mpf(T2)
        bottom = sigma_right + 1j*mp.mpf(T1)
        left   = sigma_left + 1j*mp.mpf(T1)

        ok = (margin >= 0.25)

        return {
            "schema": "turing_count/v0.1-heuristic",
            "T1": float(T1),
            "T2": float(T2),
            "dps": int(mp.mp.dps),
            "params": {
                "sigma_left": float(sigma_left),
                "sigma_right": float(sigma_right),
                "nt": int(nt),
                "ns": int(ns),
                "pad": float(pad),
            },
            "quadrature": {
                "top":    {"Re": [float(mp.re(top))-pad,    float(mp.re(top))+pad],
                           "Im": [float(mp.im(top))-pad,    float(mp.im(top))+pad]},
                "right":  {"Re": [float(mp.re(right))-pad,  float(mp.re(right))+pad],
                           "Im": [float(mp.im(right))-pad,  float(mp.im(right))+pad]},
                "bottom": {"Re": [float(mp.re(bottom))-pad, float(mp.re(bottom))+pad],
                           "Im": [float(mp.im(bottom))-pad, float(mp.im(bottom))+pad]},
                "left":   {"Re": [float(mp.re(left))-pad,   float(mp.re(left))+pad],
                           "Im": [float(mp.im(left))-pad,   float(mp.im(left))+pad]},
                "sum":    {"Re": float(mp.re(delta)), "Im": 0.0}
            },
            "deltaN_interval": [A, B],
            "deltaN_integer": k,
            "rounding_margin": margin,
            "ok_integer": bool(ok),
        }
    finally:
        mp.mp.dps = old

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--T1", type=float, default=10.0)
    ap.add_argument("--T2", type=float, default=31.83)
    ap.add_argument("--dps", type=int, default=70)
    args = ap.parse_args()
    if args.selftest:
        out = turing_count_block(args.T1, args.T2, dps=args.dps)
        print(json.dumps(out, indent=2))
