#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import time
from pathlib import Path


def run(cmd: list[str], tag: str) -> int:
    print(f"[cmd] {' '.join(cmd)}", flush=True)
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        print(f"[{tag}] exit code {proc.returncode}", flush=True)
    return proc.returncode


def main():
    p = argparse.ArgumentParser(description="Merge + Turing-Check watcher")

    # Entweder wir mergen regelmäßig, oder wir zeigen direkt auf ein fertiges zeros-root
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--merge-roots",
        nargs="+",
        help="Ordner mit Roh-Blocks (z.B. runs\\big_run_48h_final_ultrafine ...)",
    )
    g.add_argument(
        "--zeros-root",
        help="Direktmodus: überspringe Merge und nimm diesen Root für turing_check.py",
    )

    p.add_argument(
        "--out-merged",
        default="runs\\merged_runs",
        help="Zielordner für merge_zeros.py (Default: runs\\merged_runs)",
    )
    p.add_argument(
        "--minutes",
        type=int,
        default=60,
        help="Schlafzeit zwischen Zyklen (min). min=60 wird erzwungen",
    )

    # Turing-Parameter
    p.add_argument("--T0", type=float, default=0.1)
    p.add_argument("--T1", type=float, default=2000.0)
    p.add_argument("--bins", type=int, default=80)
    p.add_argument("--steps", type=int, default=20000)

    # Neue, weiterzureichende Flags
    p.add_argument(
        "--edge-soft",
        type=float,
        default=0.0,
        help="Weiche Kanten pro Bin (Anteil der Binbreite) für N_RvM und Datencount",
    )
    p.add_argument(
        "--csv",
        default=None,
        help="CSV-Pfad für turing_check.py (optional; ohne Pfad wird keine CSV geschrieben)",
    )
    p.add_argument(
        "--noS",
        action="store_true",
        help="Turing ohne S(T); wird als --no-S an turing_check.py weitergereicht",
    )
    p.add_argument(
        "--mp-dps",
        type=int,
        default=80,
        help="mpmath Präzision (digits) für S(T), falls aktiviert",
    )
    p.add_argument(
        "--once",
        action="store_true",
        help="Nur einen Zyklus ausführen und beenden",
    )

    args = p.parse_args()

    py = sys.executable or "python"
    out_merged = Path(args.out_merged)

    while True:
        # 1) Merge (wenn gewünscht)
        if args.merge_roots:
            print("[watch] merge…", flush=True)
            out_merged.parent.mkdir(parents=True, exist_ok=True)
            merge_cmd = [
                py,
                "merge_zeros.py",
                "--out-root",
                str(out_merged),
                "--block-size",
                "2000",
                "--roots",
                *args.merge_roots,
            ]
            rc = run(merge_cmd, "merge")
            if rc != 0:
                # Fehler werden geloggt; wir versuchen im nächsten Zyklus erneut
                pass
            zeros_root = str(out_merged)
        else:
            zeros_root = args.zeros_root

        # 2) Turing
        print("[watch] turing…", flush=True)
        turing_cmd = [
            py,
            "turing_check.py",
            "--zeros-root",
            zeros_root,
            "--T0",
            str(args.T0),
            "--T1",
            str(args.T1),
            "--bins",
            str(args.bins),
            "--steps",
            str(args.steps),
            "--mp-dps",
            str(args.mp_dps),
        ]
        if args.noS:
            turing_cmd.append("--no-S")
        if args.edge_soft and args.edge_soft > 0:
            turing_cmd += ["--edge-soft", str(args.edge_soft)]
        if args.csv:
            turing_cmd += ["--csv", args.csv]

        run(turing_cmd, "turing")

        if args.once:
            break

        sleep_s = max(60, 60 * int(args.minutes))
        print(f"[watch] sleep {args.minutes} min", flush=True)
        try:
            time.sleep(sleep_s)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
