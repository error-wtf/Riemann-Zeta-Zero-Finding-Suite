#!/usr/bin/env python3
# batch_until_deadline.py — robust runner until a time budget is exhausted
import argparse, csv, glob, json, math, os, subprocess, sys, time
from datetime import timedelta, datetime
from pathlib import Path

# ---------- helpers ----------
def delta(t: float) -> float:
    """mittlerer Nullabstand ~ 2π / ln t"""
    return 1.0 if t <= math.e else (2*math.pi) / math.log(t)

def clamp(x, lo, hi): 
    return max(lo, min(hi, x))

def ensure_dir(p: str | Path):
    Path(p).mkdir(parents=True, exist_ok=True)

def write_block_zeros_csv(block_json: Path, zeros_csv: Path):
    """
    Lies den Block-Report (zeta_rh_block/v1). Erzeuge zeros.csv mit:
      idx, a, b, t_zero_est
    wobei a,b das zertifizierte Intervall und t_zero_est = (a+b)/2 ist.
    """
    with open(block_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    zeros = data.get("zeros", [])
    rows = []
    for i, z in enumerate(zeros, start=1):
        A, B = z.get("interval", [None, None])
        if A is None or B is None:
            continue
        a = float(A); b = float(B)
        rows.append({
            "idx": i,
            "a": f"{a:.18g}",
            "b": f"{b:.18g}",
            "t_zero_est": f"{(0.5*(a+b)):.18g}",
        })
    if not rows:
        return 0
    with open(zeros_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["idx","a","b","t_zero_est"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)

def append_csv(master: Path, src: Path, dedup_ndp: int = 12):
    # master neu anlegen?
    if not master.exists():
        ensure_dir(master.parent)
        with open(src, "r", encoding="utf-8") as fsrc, open(master, "w", encoding="utf-8") as fdst:
            fdst.write(fsrc.read())
        return

    # vorhandene + neue lesen
    with open(master, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        rows = list(rdr)
        fields = rdr.fieldnames or ["idx","a","b","t_zero_est"]

    with open(src, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        newrows = list(rdr)

    rows.extend(newrows)

    # Deduplizieren nach gerundetem t_zero_est
    seen = set()
    out = []
    for r in rows:
        try:
            k = round(float(r["t_zero_est"]), dedup_ndp)
        except Exception:
            continue
        if k in seen: 
            continue
        seen.add(k)
        out.append(r)

    # sortieren
    out.sort(key=lambda r: float(r["t_zero_est"]))

    with open(master, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

def call_run_certified(T1: float, T2: float, dps: int, outdir: Path, rho: float | None, pyexe: str) -> bool:
    """
    Versucht zuerst: import run_certified_all -> run_blocks_to_json(T1,T2,block=T2-T1,...)
    Fallback: subprocess run_certified_all.py --T1 ... --T2 ... (falls deine CLI das kennt).
    Gibt True zurück, wenn irgendwas erfolgreich lief und mindestens eine JSON-Datei im outdir liegt.
    """
    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))
    # 1) Import-Pfad
    try:
        import run_certified_all as rca  # noqa
        # block=Länge des Blocks, damit genau EIN Report entsteht
        rca.run_blocks_to_json(T1, T2, block=(T2-T1), dps=dps, eps=1e-10, outdir=str(outdir))
    except Exception as imp_err:
        # 2) CLI-Fallback
        cmd = [
            pyexe, str(script_dir / "run_certified_all.py"),
            "--T1", str(T1), "--T2", str(T2),
            "--dps", str(dps),
            "--outdir", str(outdir)
        ]
        if rho is not None:
            cmd.extend(["--rho", str(rho)])
        try:
            subprocess.check_call(cmd, cwd=str(script_dir))
        except subprocess.CalledProcessError as sub_err:
            print(f"[run_certified_all] ERROR (CLI) code={sub_err.returncode}")
            print(f"[run_certified_all] import error was: {imp_err}")
            return False
        except FileNotFoundError:
            print("[run_certified_all] not found. Make sure run_certified_all.py is in the same folder.")
            print(f"[run_certified_all] import error was: {imp_err}")
            return False

    # Erfolg, wenn im outdir mindestens ein Block-JSON entstanden ist
    jsons = list(Path(outdir).glob("*.json"))
    return len(jsons) > 0

# ---------- main loop ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tstart", type=float, default=10.0, help="Start t")
    ap.add_argument("--hours", type=float, default=12.0, help="Laufzeit (Stunden)")
    ap.add_argument("--outroot", default="big_run", help="Wurzel-Ausgabeordner")
    ap.add_argument("--dps", type=int, default=60)
    ap.add_argument("--rho", type=float, default=None, help="Optional: Schrittfaktor für ältere CLIs (falls vorhanden)")
    ap.add_argument("--min_block", type=float, default=5.0)
    ap.add_argument("--max_block", type=float, default=50.0)
    ap.add_argument("--mult", type=float, default=8.0, help="Blockbreite ≈ mult*Δ(t)")
    ap.add_argument("--python", default=sys.executable, help="Python-Interpreter")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir)  # wichtig für relative Imports/Dateien

    deadline = time.time() + args.hours*3600.0
    t = float(args.tstart)

    outroot = Path(args.outroot).resolve()
    ensure_dir(outroot)
    master_csv = outroot / "master_zeros.csv"

    block_idx = 0
    print(f"[batch] start t={t:.6f}, run for ~{args.hours}h (deadline {datetime.now() + timedelta(hours=args.hours)})")
    while time.time() < deadline:
        block_idx += 1
        # Blockbreite dynamisch und begrenzt
        W = clamp(args.mult * delta(max(t, 10.0)), args.min_block, args.max_block)
        T1, T2 = t, t + W

        outdir = outroot / f"block_{block_idx:05d}_{T1:.3f}_{T2:.3f}"
        ensure_dir(outdir)
        print(f"[block {block_idx}] [{T1:.3f}, {T2:.3f}]  W≈{W:.3f}  dps={args.dps}")

        ok = call_run_certified(T1, T2, dps=args.dps, outdir=outdir, rho=args.rho, pyexe=args.python)
        if not ok:
            print(f"[block {block_idx}] ERROR → verkleinere Block und weiter …")
            t = T1 + max(1.0, W/2.0)
            continue

        # JSONs -> zeros.csv erzeugen und in Master übernehmen
        created = 0
        for jpath in Path(outdir).glob("*.json"):
            zeros_csv = outdir / "zeros.csv"
            created += write_block_zeros_csv(jpath, zeros_csv)
        if created > 0 and (outdir / "zeros.csv").exists():
            append_csv(master_csv, outdir / "zeros.csv")
            try:
                n = sum(1 for _ in open(master_csv, "r", encoding="utf-8")) - 1
            except Exception:
                n = "?"
            print(f"[block {block_idx}] appended -> master has {n} zeros")
        else:
            print(f"[block {block_idx}] keine Zero-Zertifikate gefunden (prüfe Block-JSON in {outdir})")

        # weiter zum nächsten Block
        t = T2

    print(f"[done] Deadline erreicht. Letztes t ≈ {t:.6f}")
    if master_csv.exists():
        try:
            n = sum(1 for _ in open(master_csv, "r", encoding="utf-8")) - 1
        except Exception:
            n = "?"
        print(f"[done] master_zeros.csv enthält {n} Nullen: {master_csv}")

if __name__ == "__main__":
    main()
