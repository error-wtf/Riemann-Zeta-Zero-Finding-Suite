#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
turing_check.py  (robust)
-------------------------
- Lädt Zeta-Nullen aus zeros-root (schema zeta_rh_block/v1).
- Ermittelt T_max aus den geladenen Gammas.
- Prüft Nulldichte in [T0, T1] via Riemann–von–Mangoldt:
    N(T) = (T/2π) log(T/2π) - T/2π + 7/8 + S(T) + O(1/T)
  mit S(T) = (1/π) arg ζ(1/2 + iT) (kontinuierlich „unwrapped“).
- Warnt und *clamped* standardmäßig, wenn T1 > T_max (abschaltbar).
- Optional: binweise Auswertung und CSV-Report.

Beispiele:
  # Automatisch clampen, dichteres Raster:
  python turing_check.py --zeros-root merged_runs --T0 0 --T1 2000 --steps 1200

  # Ohne Clamp (nur zu Demo-Zwecken):
  python turing_check.py --zeros-root merged_runs --T0 0 --T1 2000 --steps 1200 --no-clamp

  # Binweise prüfen und CSV schreiben:
  python turing_check.py --zeros-root merged_runs --T0 0 --T1 1350 --bins 10 --csv turing_report.csv
"""

import argparse, json, math, sys
from pathlib import Path
from typing import List, Tuple

try:
    import mpmath as mp
except Exception:
    mp = None

def _load_blocks(root: Path) -> List[Path]:
    out = []
    for p in root.rglob("*.json"):
        try:
            with p.open("r", encoding="utf-8") as f:
                j = json.load(f)
            if isinstance(j, dict) and j.get("schema") == "zeta_rh_block/v1":
                out.append(p)
        except Exception:
            pass
    return sorted(out)

def load_gammas(root: Path) -> List[float]:
    L = []
    for p in _load_blocks(root):
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for z in data.get("zeros", []):
            iv = z.get("interval") or z.get("root_interval")
            if not iv or len(iv) != 2: continue
            a, b = float(iv[0]), float(iv[1])
            L.append(0.5*(a+b))
    return sorted(L)

def N_main_term(T: float) -> float:
    if T <= 0: return 0.0
    x = T/(2*math.pi)
    return x*math.log(max(x,1.0)) - x + 0.875

def S_of_T_continuous(Ts: List[float]) -> List[float]:
    """Kontinuierliches Arg ζ auf der 1/2-Linie via Unwrap entlang aufsteigender Ts."""
    if mp is None:
        return [0.0 for _ in Ts]
    mp.mp.dps = max(50, int(20 + 0.02*(Ts[-1]-Ts[0])))
    vals = []
    prev = None
    for t in Ts:
        z = mp.mpf("0.5") + 1j*mp.mpf(t)
        a = float(mp.arg(mp.zeta(z)))
        if prev is None:
            prev = a
        else:
            da = a - prev
            # 2π-Unwrap
            while da > math.pi:  da -= 2*math.pi
            while da < -math.pi: da += 2*math.pi
            prev = prev + da
        vals.append(prev / math.pi)  # S(T) = arg / π
    return vals

def N_rvm_interval(T0: float, T1: float, steps: int, use_S: bool=True) -> float:
    if T1 <= T0: return 0.0
    if not use_S or mp is None:
        # Grob: nur Hauptterm
        return N_main_term(T1) - N_main_term(T0)
    # adaptives Raster: dichter, wenn Intervall groß
    steps = max(steps, int(10 + 0.5*(T1 - T0)))
    Ts = [T0 + (T1 - T0)*k/steps for k in range(steps+1)]
    Svals = S_of_T_continuous(Ts)
    return (N_main_term(T1) + Svals[-1]) - (N_main_term(T0) + Svals[0])

def count_data_interval(gammas: List[float], T0: float, T1: float) -> int:
    import bisect
    i0 = bisect.bisect_left(gammas, T0)
    i1 = bisect.bisect_right(gammas, T1)
    return max(0, i1 - i0)

def main():
    ap = argparse.ArgumentParser(description="Turing-like zero count check (robust).")
    ap.add_argument("--zeros-root", type=str, required=True)
    ap.add_argument("--T0", type=float, required=True)
    ap.add_argument("--T1", type=float, required=True)
    ap.add_argument("--steps", type=int, default=1200, help="Grundraster für S(T)-Unwrap.")
    ap.add_argument("--no-clamp", action="store_true", help="Nicht auf T_max kappen, selbst wenn T1 > T_max ist.")
    ap.add_argument("--bins", type=int, default=0, help="Wenn >0: [T0,T1] in so viele Bins teilen und pro Bin prüfen.")
    ap.add_argument("--csv", type=str, default="", help="Optional: CSV-Report schreiben.")
    ap.add_argument("--no-S", action="store_true", help="S(T) ignorieren (nur Hauptterm).")
    args = ap.parse_args()

    root = Path(args.zeros_root)
    if not root.exists():
        sys.exit(f"[ERR] not found: {root}")

    gam = load_gammas(root)
    if not gam:
        sys.exit("[ERR] no zeros loaded.")
    T_max = gam[-1]

    T0, T1 = float(args.T0), float(args.T1)
    if T1 <= T0:
        sys.exit("[ERR] need T1 > T0")

    # Warnen / clampen, wenn T1 > T_max
    if T1 > T_max:
        msg = f"[warn] T1={T1:.6f} exceeds T_max≈{T_max:.6f} from data. You don't have zeros up to T1."
        if args.no_clamp:
            print(msg + " Proceeding without clamp (expect MISMATCH).")
        else:
            print(msg + " Clamping to T_max-ε.")
            eps = 1e-6
            T1 = T_max - eps

    # Einzel-Intervall oder binweise
    rows: List[Tuple[float,float,int,float,float]] = []
    if args.bins and args.bins > 0:
        k = args.bins
        for i in range(k):
            a = T0 + (T1 - T0)*i/k
            b = T0 + (T1 - T0)*(i+1)/k
            n_data = count_data_interval(gam, a, b)
            n_rvm  = N_rvm_interval(a, b, args.steps, use_S = (not args.no_S))
            diff   = n_data - n_rvm
            rows.append((a, b, n_data, n_rvm, diff))
            ok = abs(diff) <= 1.0  # tolerantes Fenster
            print(f"[turing.bin {i+1}/{k}] [{a:.3f},{b:.3f}] data={n_data}  RvM≈{n_rvm:.3f}  diff≈{diff:.3f}  -> {'OK' if ok else 'MISMATCH'}")
    else:
        n_data = count_data_interval(gam, T0, T1)
        n_rvm  = N_rvm_interval(T0, T1, args.steps, use_S = (not args.no_S))
        diff   = n_data - n_rvm
        ok     = abs(diff) <= 1.0
        print(f"[turing] Interval [{T0:.6f}, {T1:.6f}]: data_count={n_data}, RvM≈{n_rvm:.3f}, diff≈{diff:.3f}  -> {'OK' if ok else 'MISMATCH'}")
        rows.append((T0, T1, n_data, n_rvm, diff))

    if args.csv:
        with open(args.csv, "w", encoding="utf-8") as f:
            f.write("T0,T1,data_count,RvM_est,diff\n")
            for a,b,nd,nr,df in rows:
                f.write(f"{a:.6f},{b:.6f},{nd},{nr:.6f},{df:.6f}\n")
        print(f"[out] wrote CSV: {args.csv}")

if __name__ == "__main__":
    main()
