#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_certified_all.py — Blockweises Zertifizieren mit Auto-Fallback auf alte run_block-Signatur.
- Kompatibel mit alter run_block.run_block(..., scan_step=...) *ohne* rho/adapt_k/step_min/certifier
- Nutzt neue Parameter, wenn vorhanden (rho, adapt_k, step_min, certifier)
- Optionaler Auto-Rescan bei Mismatch
"""

import json, inspect, sys, os
from pathlib import Path

# Sicherstellen, dass wir wirklich das run_block.py aus *diesem* Ordner laden
sys.path.insert(0, os.path.dirname(__file__))

from count_argument import turing_count_block
import run_block as RB  # wir inspizieren die Signatur gleich

def _call_run_block(T1, T2, *, scan_step_max, eps, dps, rad, rho, adapt_k, step_min, certifier):
    """
    Ruft run_block.run_block auf und filtert kwargs anhand der echten Signatur.
    Mapped scan_step_max -> scan_step.
    """
    fn = RB.run_block
    sig = inspect.signature(fn)
    have = set(sig.parameters.keys())

    kwargs = {}
    # Mapping
    if "scan_step" in have:
        kwargs["scan_step"] = scan_step_max
    elif "scan_step_max" in have:
        kwargs["scan_step_max"] = scan_step_max  # falls jemand diese Variante gebaut hat
    # Standard-Args
    if "eps" in have: kwargs["eps"] = eps
    if "dps" in have: kwargs["dps"] = dps
    if "rad" in have: kwargs["rad"] = rad
    # Neue (falls vorhanden)
    if "rho" in have: kwargs["rho"] = rho
    if "adapt_k" in have: kwargs["adapt_k"] = adapt_k
    if "step_min" in have: kwargs["step_min"] = step_min
    if "certifier" in have: kwargs["certifier"] = certifier

    return fn(T1, T2, **kwargs)

def _one_block(T1, B, *, dps, eps, outdir, rho, adapt_k, scan_step_max, step_min, certifier, rad):
    zres = _call_run_block(
        T1, B,
        scan_step_max=scan_step_max, eps=eps, dps=dps, rad=rad,
        rho=rho, adapt_k=adapt_k, step_min=step_min, certifier=certifier
    )
    zeros = zres.get("certificates", [])
    count = turing_count_block(T1, B, dps=dps, nt=400, ns=64, pad=0.25)
    deltaN = count.get("deltaN_integer", None)
    report = {
        "schema": "zeta_rh_block/v1",
        "block": {"T1": T1, "T2": B},
        "zeros": zeros,
        "count": count,
        "consistency": {
            "n_zeros": len(zeros),
            "deltaN": deltaN,
            "match": (len(zeros) == deltaN) if (deltaN is not None) else False
        },
        "params": {
            "dps": dps, "eps": eps, "rad": rad,
            "rho": rho, "adapt_k": adapt_k,
            "scan_step_max": scan_step_max, "step_min": step_min,
            "block": B - T1, "certifier": certifier
        }
    }
    return report

def run_blocks_to_json(
    T1: float, T2: float, *,
    block: float = 16.0, dps: int = 80, eps: float = 1e-10, outdir: str = "zeta_cert_out",
    rho: float = 1.0, adapt_k: float = 6.0, scan_step_max: float = 0.02,
    step_min: float = 1e-3, certifier: str = "hybrid", rad: float = 1e-12,
    # Auto-Rescan-Optionen:
    rescan_on_mismatch: bool = True,
    rescan_dps_bump: int = 16,
    rescan_step_factor: float = 0.5,
    rescan_force_certifier: str = "arb"
):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    t = float(T1)
    while t < T2:
        B = min(T2, t + block)
        # 1) erster Versuch
        report = _one_block(
            t, B, dps=dps, eps=eps, outdir=out, rho=rho, adapt_k=adapt_k,
            scan_step_max=scan_step_max, step_min=step_min, certifier=certifier, rad=rad
        )
        # 2) Auto-Rescan bei Mismatch
        if rescan_on_mismatch and not report["consistency"]["match"]:
            report = _one_block(
                t, B,
                dps=dps + rescan_dps_bump, eps=eps, outdir=out, rho=rho, adapt_k=adapt_k,
                scan_step_max=scan_step_max * rescan_step_factor,
                step_min=step_min, certifier=rescan_force_certifier, rad=rad
            )
            report.setdefault("meta", {})["rescanned"] = True

        path = out / f"block_{int(t)}_{int(B)}.json"
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print("Wrote", path)
        t = B

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--T1", type=float, required=True)
    ap.add_argument("--T2", type=float, required=True)
    ap.add_argument("--block", type=float, default=16.0)
    ap.add_argument("--dps", type=int, default=80)
    ap.add_argument("--eps", type=float, default=1e-10)
    ap.add_argument("--outdir", type=str, default="zeta_cert_out")
    ap.add_argument("--rho", type=float, default=1.0)
    ap.add_argument("--adapt_k", type=float, default=6.0)
    ap.add_argument("--scan_step_max", type=float, default=0.02)
    ap.add_argument("--step_min", type=float, default=1e-3)
    ap.add_argument("--certifier", type=str, default="hybrid")
    ap.add_argument("--rad", type=float, default=1e-12)
    # Rescan-Flags
    ap.add_argument("--no-rescan", action="store_true")
    ap.add_argument("--rescan-dps-bump", type=int, default=16)
    ap.add_argument("--rescan-step-factor", type=float, default=0.5)
    ap.add_argument("--rescan-force-certifier", type=str, default="arb")
    a = ap.parse_args()

    run_blocks_to_json(
        a.T1, a.T2, block=a.block, dps=a.dps, eps=a.eps, outdir=a.outdir,
        rho=a.rho, adapt_k=a.adapt_k, scan_step_max=a.scan_step_max,
        step_min=a.step_min, certifier=a.certifier, rad=a.rad,
        rescan_on_mismatch=(not a.no_rescan),
        rescan_dps_bump=a.rescan_dps_bump,
        rescan_step_factor=a.rescan_step_factor,
        rescan_force_certifier=a.rescan_force_certifier
    )

