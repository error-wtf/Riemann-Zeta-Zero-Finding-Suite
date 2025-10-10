#!/usr/bin/env python3
"""
unknown_zeta_zero.py
--------------------
Findet GENAU EINE neue Nullstelle von zeta(1/2 + i t) direkt oberhalb der
bisher größten in einer CSV (Standard: zeros.csv). Es wird vorwärts gescannt,
bis der ERSTE Vorzeichenwechsel von Hardys Z(t) auftaucht; nur dieses Intervall
wird per Bisektion verfeinert und an die CSV angehängt.

Voraussetzung: zeta_zero_finder.py liegt im selben Ordner (liefert Z() und bisect_zero()).

Beispiele:
  python unknown_zeta_zero.py
  python unknown_zeta_zero.py --csv zeros.csv --dps 60 --bisect-steps 120
  python unknown_zeta_zero.py --start-margin 0.6 --step-factor 0.20 --json

CSV-Format (wie in zeta_zero_finder.py):
  t_zero, bracket_a, bracket_b, dps, bisect_steps

Optionales JSON-Zertifikat:
  unknown_zero_cert.json mit Klammer- und Refinement-Infos.
"""
import argparse, csv, math, sys, json
from pathlib import Path

# ---- Z() und bisect_zero() aus deinem Finder laden ----
try:
    from zeta_zero_finder import Z, bisect_zero
except Exception as e:
    print("ERROR: Import aus zeta_zero_finder.py fehlgeschlagen.")
    print("Lege unknown_zeta_zero.py und zeta_zero_finder.py in denselben Ordner.")
    print("ImportError:", e)
    sys.exit(1)

try:
    import mpmath as mp
except Exception as e:
    print("ERROR: mpmath wird benötigt.")
    sys.exit(1)

def read_max_zero(csv_path: Path) -> float:
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} nicht gefunden. Bitte zuerst eine Start-CSV erzeugen.")
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        vals = []
        for row in rd:
            # bevorzugt Spalte "t_zero", sonst erste Spalte
            try:
                vals.append(float(row.get("t_zero")))
            except Exception:
                try:
                    vals.append(float(next(iter(row.values()))))
                except Exception:
                    pass
    if not vals:
        raise RuntimeError(f"{csv_path} enthält keine gültigen t_zero-Werte.")
    return max(vals)

def ensure_header(csv_path: Path):
    """Falls Datei leer ist, Standard-Header schreiben."""
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["t_zero","bracket_a","bracket_b","dps","bisect_steps"])

def next_zero(csv_path: Path,
              dps: int = 60,
              bisect_steps: int = 120,
              start_margin: float = 0.60,
              step_factor: float = 0.20,
              max_scan_steps: int = 5000,
              write_json: bool = False):
    """Suche nur die nächste Nullstelle > max(t_zero in csv_path) und hänge sie an."""
    mp.mp.dps = dps

    tmax = read_max_zero(csv_path)

    # Lokale Abstandsskala Δt ≈ 2π / log t
    Dt = 2*math.pi / math.log(max(tmax, 3.0))
    start = tmax + start_margin * Dt
    step  = step_factor * Dt

    a = mp.mpf(start)
    fa = Z(a)
    b = a
    found = False

    trace = [{"a": float(a), "Za": float(fa)}]

    for _ in range(max_scan_steps):
        b = a + step
        fb = Z(b)
        trace.append({"b": float(b), "Zb": float(fb)})
        if fa * fb < 0:
            found = True
            break
        a, fa = b, fb

    if not found:
        raise RuntimeError(
            f"Kein Vorzeichenwechsel nach {max_scan_steps} Schritten.\n"
            f"Erhöhe --step-factor oder --max-scan-steps."
        )

    # Nur dieses Intervall verfeinern (robust: Bisektion)
    z = float(bisect_zero(float(a), float(b), steps=bisect_steps))

    # An CSV anhängen
    ensure_header(csv_path)
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([f"{z:.12f}", f"{float(a):.12f}", f"{float(b):.12f}", dps, bisect_steps])

    # Optional: kleines „Zertifikat“
    if write_json:
        cert = {
            "csv": str(csv_path),
            "tmax_prev": tmax,
            "local_spacing_est": Dt,
            "start": float(start),
            "step": float(step),
            "bracket": [float(a), float(b)],
            "bisect_steps": bisect_steps,
            "dps": dps,
            "zero_estimate": z,
            "scan_trace_len": len(trace),
        }
        Path("unknown_zero_cert.json").write_text(json.dumps(cert, indent=2), encoding="utf-8")

    return z, (float(a), float(b)), Dt

def main():
    ap = argparse.ArgumentParser(description="Finde genau eine neue Zeta-Nullstelle oberhalb der aktuell größten (aus zeros.csv).")
    ap.add_argument("--csv", type=str, default="zeros.csv", help="Pfad zur CSV (Default: zeros.csv)")
    ap.add_argument("--dps", type=int, default=60, help="mpmath-Präzision")
    ap.add_argument("--bisect-steps", type=int, default=120, help="Bisektionsschritte")
    ap.add_argument("--start-margin", type=float, default=0.60, help="Start = t_max + start_margin * Δt")
    ap.add_argument("--step-factor", type=float, default=0.20, help="Scan-Schritt = step_factor * Δt")
    ap.add_argument("--max-scan-steps", type=int, default=5000, help="Sicherheitslimit für Vorwärtsscan")
    ap.add_argument("--json", action="store_true", help="Zertifikat unknown_zero_cert.json schreiben")
    args = ap.parse_args()

    csv_path = Path(args.csv)

    try:
        z, br, Dt = next_zero(csv_path,
                              dps=args.dps,
                              bisect_steps=args.bisect_steps,
                              start_margin=args.start_margin,
                              step_factor=args.step_factor,
                              max_scan_steps=args.max_scan_steps,
                              write_json=args.json)
        print(f"[OK] nächste Null bei t ≈ {z:.12f}  (Bracket=({br[0]:.12f},{br[1]:.12f}), Δt≈{Dt:.4f})")
        print(f"    angehängt an {csv_path}")
        if args.json:
            print("    Zertifikat: unknown_zero_cert.json")
    except Exception as e:
        print("[ERROR]", e)
        sys.exit(2)

if __name__ == "__main__":
    main()
