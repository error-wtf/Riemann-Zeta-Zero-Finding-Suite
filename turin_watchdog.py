#!/usr/bin/env python3
# turing_watchdog.py — zwei Turing-Pässe (normal & --no-S) + To-Do-Liste für Rescan
import argparse, csv, json, subprocess, sys
from pathlib import Path

def run(cmd):
    print("[cmd]", " ".join(cmd)); sys.stdout.flush()
    return subprocess.call(cmd)

def load_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zeros-root", required=True)
    ap.add_argument("--T0", default="0.1")
    ap.add_argument("--T1", default="2000")
    ap.add_argument("--bins", default="80")
    ap.add_argument("--steps", default="20000")
    ap.add_argument("--out-json", default="turing_suspects.json")
    args = ap.parse_args()

    # Pass 1: normal
    csv1 = "turing_last.csv"
    cmd1 = [sys.executable, "turing_check.py", "--zeros-root", args.zeros_root,
            "--T0", args.T0, "--T1", args.T1, "--bins", args.bins, "--steps", args.steps, "--csv", csv1]
    run(cmd1)

    # Pass 2: no-S
    csv2 = "turing_last_noS.csv"
    cmd2 = [sys.executable, "turing_check.py", "--zeros-root", args.zeros_root,
            "--T0", args.T0, "--T1", args.T1, "--bins", args.bins, "--steps", args.steps, "--no-S", "--csv", csv2]
    run(cmd2)

    r1 = load_csv(csv1) if Path(csv1).exists() else []
    r2 = load_csv(csv2) if Path(csv2).exists() else []

    # Verdächtig: Bin mismatch in BEIDEN Pässen (nicht nur Unwrap)
    sus = []
    for a, b in zip(r1, r2):
        ok1 = (a.get("status","").upper() == "OK")
        ok2 = (b.get("status","").upper() == "OK")
        if (not ok1) and (not ok2):
            sus.append({
                "bin": a.get("bin"),
                "T_left": float(a.get("T_left", "nan")),
                "T_right": float(a.get("T_right", "nan")),
                "diff_normal": a.get("diff"),
                "diff_noS": b.get("diff")
            })

    Path(args.out_json).write_text(json.dumps({"suspects": sus}, indent=2), encoding="utf-8")
    print(f"[turing] suspects written to {args.out_json} (n={len(sus)})")

if __name__ == "__main__":
    main()
