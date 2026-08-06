#!/usr/bin/env python3
"""Persist the complete finite viewport geometry used by the zeta visual."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path("artifacts/periodicity/zeta_term_map.json"))
    p.add_argument("--terms", type=int, default=36)
    p.add_argument("--sigma-count", type=int, default=18)
    p.add_argument("--t-count", type=int, default=21)
    p.add_argument("--points", type=int, default=720)
    args = p.parse_args()
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    sigmas = [-1.25 + 2.25 * i / (args.sigma_count - 1) for i in range(args.sigma_count)]
    ts = [-4.0 + 8.0 * i / (args.t_count - 1) for i in range(args.t_count)]
    phase = [-math.pi + 2 * math.pi * i / (args.points - 1) for i in range(args.points)]
    rings = []
    rays = []
    for n in primes:
        for sigma in sigmas:
            r = n ** (-sigma)
            rings.append({"n": n, "sigma": sigma, "points": [[r * math.cos(a), r * math.sin(a)] for a in phase]})
        for t in ts:
            a = -t * math.log(n)
            rays.append({"n": n, "t": t, "angle": a})
    payload = {"definition": "n**(-s)=exp(-s*log(n))", "terms": primes, "sigma_grid": sigmas, "t_grid": ts, "rings": rings, "rays": rays, "viewport": {"re": [-7.2, 7.2], "im": [-3.8, 3.8], "points_per_ring": args.points}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
