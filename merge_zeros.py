#!/usr/bin/env python3
# merge_zeros.py — robustes Dedupe + Merge aus vielen Blockverzeichnissen
import argparse, csv, json
from pathlib import Path

def gather_blocks(roots):
    for root in roots:
        r = Path(root)
        if not r.exists(): continue
        for j in sorted(r.rglob("*.json")):
            yield j

def extract_rows(jpath, ndp=12):
    data = json.loads(jpath.read_text(encoding="utf-8"))
    zeros = data.get("zeros", [])
    rows = []
    for z in zeros:
        iv = z.get("interval", [None, None])
        if not iv or len(iv) != 2: continue
        a, b = float(iv[0]), float(iv[1])
        t = 0.5*(a+b)
        rows.append({"t_zero_est": f"{t:.18g}", "a": f"{a:.18g}", "b": f"{b:.18g}"})
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", action="append", required=True, help="add a root folder (use multiple --roots)")
    ap.add_argument("--out-root", default="merged_runs")
    ap.add_argument("--block-size", type=int, default=2000)
    ap.add_argument("--ndp", type=int, default=12, help="rounding digits for dedupe")
    args = ap.parse_args()

    out = Path(args.out_root); out.mkdir(parents=True, exist_ok=True)
    all_rows = []
    for j in gather_blocks(args.roots):
        all_rows.extend(extract_rows(j, ndp=args.ndp))

    # Dedupe nach gerundetem t
    seen = set(); clean = []
    for r in all_rows:
        k = round(float(r["t_zero_est"]), args.ndp)
        if k in seen: continue
        seen.add(k); clean.append(r)
    clean.sort(key=lambda r: float(r["t_zero_est"]))

    # Schreibe master + optionale Teilblöcke
    master = out / "master_zeros.csv"
    with master.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["t_zero_est", "a", "b"])
        w.writeheader(); w.writerows(clean)
    print(f"[merge] wrote {master}  (n={len(clean)})")

    if args.block_size > 0:
        for i in range(0, len(clean), args.block_size):
            chunk = clean[i:i+args.block_size]
            p = out / f"master_{i+1:06d}_{i+len(chunk):06d}.csv"
            with p.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["t_zero_est", "a", "b"])
                w.writeheader(); w.writerows(chunk)
            print(f"[merge] wrote {p}")

if __name__ == "__main__":
    main()
