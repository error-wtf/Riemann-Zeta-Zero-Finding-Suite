#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import math
import sys
from pathlib import Path

try:
    import mpmath as mp
except Exception:
    mp = None


# -------------------------------
# Hilfsfunktionen
# -------------------------------

def try_float(x):
    try:
        return float(x)
    except Exception:
        return None


def load_zero_list(zeros_root: str) -> list[float]:
    """
    Lädt Zero-Ordinaten aus zeros_root. Erwartet typischerweise:
      zeros_root/master_zeros.csv
    Ist tolerant gegenüber Spaltennamen: t, T, gamma, im, ordinate ...
    """
    root = Path(zeros_root)
    candidates = []
    # Bevorzugt master_zeros.csv
    if (root / "master_zeros.csv").exists():
        candidates.append(root / "master_zeros.csv")
    # Fallback: andere master_* Dateien
    for p in root.glob("master_*.csv"):
        if p not in candidates:
            candidates.append(p)
    # Noch ein Fallback: alles, was nach zeros aussieht
    if not candidates:
        for p in root.glob("*.csv"):
            candidates.append(p)

    zeros = []
    for csv_path in candidates:
        try:
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                rdr = csv.DictReader(f)
                # Heuristische Spaltenliste
                keys = [k.lower() for k in rdr.fieldnames or []]
                possible = [
                    "t", "T", "gamma", "im", "imag", "ordinate", "imag_part", "imagpart",
                    "y", "tau"
                ]
                # Mappe, finde erste passende Spalte
                pick = None
                for want in possible:
                    if want in keys:
                        pick = want
                        break
                # Sonderfall: exakte Namen nicht gefunden -> nimm erste numerische Spalte
                for row in rdr:
                    val = None
                    if pick is not None:
                        # hole über lower-keys
                        for k in row:
                            if k.lower() == pick:
                                val = try_float(row[k])
                                break
                    else:
                        # probiere alle Spalten der Reihe nach
                        for k in row:
                            val = try_float(row[k])
                            if val is not None:
                                break
                    if val is not None:
                        zeros.append(val)
        except Exception:
            # ignoriere defekte CSVs still
            continue

    zeros = sorted([z for z in zeros if z is not None and z >= 0.0])
    return zeros


def N_RvM_core(t: float) -> float:
    """Riemann–von Mangoldt ohne S(T)."""
    if t <= 0:
        return 0.0
    return (t/(2*math.pi)) * math.log(t/(2*math.pi)) - (t/(2*math.pi)) + 7.0/8.0


def S_of_T(t: float, mp_dps: int, last_s=None):
    """
    Grobe, aber konsistente Approximation von S(T) = (1/pi) * Arg zeta(1/2 + i t)
    mit kontinuierlichem Branch-Tracking.
    """
    if mp is None:
        raise RuntimeError("mpmath nicht verfügbar; installiere mpmath oder nutze --no-S.")

    if t <= 0:
        # Konventionell S(0)=0
        return 0.0, 0.0

    # Präzision
    mp.mp.dps = max(30, int(mp_dps))

    s = mp.mpf("0.5") + 1j * mp.mpf(t)
    z = mp.zeta(s)
    raw = mp.arg(z) / mp.pi  # in Einheiten von 1/π

    if last_s is None:
        return float(raw), float(raw)

    # Branch-Anpassung: wähle k ∈ 2Z (Vielfache von 2), so dass |raw + k - last_s| minimal
    # (weil Arg in Einheiten 1/π gemessen wird, ist 2 eine volle 2π-Umwicklung)
    delta = raw - last_s
    # k ≈ -round(delta/2)*2
    k = int(round(-delta/2.0)) * 2
    adj = raw + k
    return float(adj), float(raw)


def N_RvM_with_S(t: float, s_val: float) -> float:
    """N_RvM(t) inklusive S(T)-Term."""
    return N_RvM_core(t) + s_val


def format_float(x: float, nd=3) -> str:
    return f"{x:.{nd}f}"


# -------------------------------
# Hauptlogik
# -------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Turing-Check gegen Riemann–von Mangoldt mit optionalem S(T)."
    )
    ap.add_argument("--zeros-root", required=True, help="Wurzelordner mit master_zeros.csv")
    ap.add_argument("--T0", required=True, type=float)
    ap.add_argument("--T1", required=True, type=float)
    ap.add_argument("--bins", type=int, default=10, help="Anzahl Bins")
    ap.add_argument("--steps", type=int, default=20000, help="(Reserve) Granularität; v.a. für S(T)")
    ap.add_argument("--tol", type=float, default=0.5, help="Toleranzschwelle für MISMATCH-Hinweis")
    ap.add_argument("--no-S", dest="noS", action="store_true", help="S(T) nicht berücksichtigen")
    ap.add_argument("--edge-soft", type=float, default=0.0,
                    help="Weiche Kanten pro Bin (Anteil der Binbreite) – vermeidet Grenzartefakte")
    ap.add_argument("--mp-dps", type=int, default=80, help="mpmath digits für S(T)")
    ap.add_argument("--csv", default=None, help="Optionaler CSV-Report")

    args = ap.parse_args()

    zeros = load_zero_list(args.zeros_root)
    if not zeros:
        print("[merge] WARN: keine zeros gefunden – prüfe Pfad/CSV.", flush=True)

    T_max = zeros[-1] if zeros else 0.0
    if args.T1 > T_max and T_max > 0:
        print(f"[warn] T1={args.T1:.6f} exceeds T_max≈{T_max:.6f} from data. Clamping to T_max.", flush=True)
        T1 = T_max
    else:
        T1 = args.T1

    T0 = max(0.0, args.T0)
    if T1 <= T0:
        print("[turing] ERROR: T1 <= T0 nach Clamping.", flush=True)
        sys.exit(1)

    # Bin-Grenzen
    Nbin = max(1, args.bins)
    width = (T1 - T0) / Nbin
    eps = max(0.0, min(0.49, args.edge_soft)) * width  # max 49% – rein defensiv

    # Precompute S(T) auf allen relevanten Grenzen, falls nötig
    # Wir brauchen S an T0+eps, T1-eps und an allen inneren Grenzen.
    useS = not args.noS
    boundaries = [T0 + i * width for i in range(Nbin + 1)]
    if useS and mp is None:
        print("[turing] WARN: mpmath fehlt -> erzwinge --no-S", flush=True)
        useS = False

    S_at = {}  # T -> S(T) (kontinuierliche Branch)
    if useS:
        last_S = None
        last_raw = None
        for i, t in enumerate(boundaries):
            # Für weiche Kanten nutzen wir später t_in = t + eps, t_out = t - eps
            # Hier speichern wir S an beiden Seiten, indem wir direkt am "echten" Punkt evaluieren.
            s_val, s_raw = S_of_T(t, mp_dps=args.mp_dps, last_s=last_S if i > 0 else None)
            S_at[t] = s_val
            last_S = s_val
            last_raw = s_raw

    # Data-Count vorbereiten
    # Wir zählen zeros in [L+eps, R-eps) – linksgeschlossen, rechtsoffen – um Grenzartefakte zu vermeiden.
    # (Gesamtsumme vergleichen wir separat ohne eps.)
    zi = 0
    nZ = len(zeros)

    def count_data(L, R):
        nonlocal zi
        # bewege Startindex vor
        while zi < nZ and zeros[zi] < L:
            zi += 1
        cnt = 0
        j = zi
        while j < nZ:
            z = zeros[j]
            if z < R:
                cnt += 1
                j += 1
            else:
                break
        return cnt

    # CSV?
    csv_path = args.csv
    csv_writer = None
    csv_file = None
    if csv_path:
        csv_file = open(csv_path, "w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ["bin_idx", "L", "R", "data_count", "RvM_bin", "diff", "status"]
        )

    # Auswertung pro Bin
    data_total = 0
    rvm_total = 0.0
    status_any_mismatch = False

    print(f"[turing] Interval [{T0:.6f}, {T1:.6f}] bins={Nbin} steps={args.steps} edge_soft={args.edge_soft}", flush=True)

    for b in range(Nbin):
        L = T0 + b * width
        R = L + width

        Ls = L + eps
        Rs = R - eps
        if Rs < Ls:
            # bei sehr großen edge-soft: fall-back auf harte Grenzen
            Ls, Rs = L, R

        # Data
        data_cnt = count_data(Ls, Rs)
        data_total += data_cnt

        # RvM
        if useS:
            SL = S_at.get(L, 0.0)
            SR = S_at.get(R, 0.0)
            NR = N_RvM_with_S(Rs, SR)
            NL = N_RvM_with_S(Ls, SL)
        else:
            NR = N_RvM_core(Rs)
            NL = N_RvM_core(Ls)

        rvm_bin = NR - NL
        rvm_total += rvm_bin

        diff = data_cnt - rvm_bin
        ok = abs(diff) <= args.tol
        status = "OK" if ok else "MISMATCH"
        if not ok:
            status_any_mismatch = True

        print(
            f"[turing.bin {b+1}/{Nbin}] "
            f"[{format_float(L,3)},{format_float(R,3)}] "
            f"data={data_cnt}  RvM≈{format_float(rvm_bin,3)}  diff≈{format_float(diff,3)}  -> {status}",
            flush=True,
        )

        if csv_writer:
            csv_writer.writerow([b + 1, L, R, data_cnt, rvm_bin, diff, status])

    # Gesamtsummen auf dem EXAKTEN Intervall (ohne edge-soft) vergleichen
    # Data total exakt:
    data_sum_exact = sum(1 for z in zeros if (z >= T0 and z < T1))
    if useS:
        S0 = S_at.get(T0, 0.0)
        S1 = S_at.get(T1, 0.0)
        rvm_sum_exact = N_RvM_with_S(T1, S1) - N_RvM_with_S(T0, S0)
    else:
        rvm_sum_exact = N_RvM_core(T1) - N_RvM_core(T0)

    diff_total = data_sum_exact - rvm_sum_exact
    status_total = "OK" if abs(diff_total) <= args.tol else "MISMATCH"

    print(
        f"[turing.total] [{T0:.6f},{T1:.6f}] "
        f"data_total={data_sum_exact}  RvM_total={format_float(rvm_sum_exact,3)}  "
        f"diff≈{format_float(diff_total,3)}  -> {status_total}",
        flush=True,
    )

    if csv_writer:
        # Leerzeile + Totals
        csv_writer.writerow([])
        csv_writer.writerow(
            ["TOTAL", T0, T1, data_sum_exact, rvm_sum_exact, diff_total, status_total]
        )
        csv_file.close()
        print(f"[out] wrote CSV: {csv_path}", flush=True)

    # Exit-Code optional: 0 auch bei MISMATCH (reiner Report). Wer strikt sein will, hier ändern.
    sys.exit(0)


if __name__ == "__main__":
    main()
