#!/usr/bin/env python3
"""Fail-closed outward-rounded certificate on the logarithmic interval [0,1/2]."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.certification.theta_interval import profile_margin_balls


def arb_interval(left: Fraction, right: Fraction):
    from flint import arb
    mid = (left + right) / 2
    rad = (right - left) / 2
    # All subdivision endpoints are dyadic; render them exactly as decimals
    # rather than passing an imprecise binary float to Arb.
    def decimal_fraction(value: Fraction) -> str:
        with localcontext() as context:
            context.prec = 300
            return format(Decimal(value.numerator) / Decimal(value.denominator), "f")
    return arb(f"{decimal_fraction(mid)} +/- {decimal_fraction(rad)}")


def bound_string(value) -> str:
    return str(value)


def positive(value) -> bool:
    return value.lower() > 0


def negative(value) -> bool:
    return value.upper() < 0


def certify(args):
    try:
        from flint import ctx, __version__ as flint_version
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("compact certification requires python-flint") from exc

    origin = Fraction(args.origin_cut)
    left0, right0 = Fraction(0), origin
    target_left, target_right = Fraction(0), Fraction(1, 2)
    boxes = []
    pending = [(left0, right0, 0, True), (origin, target_right, 0, False)]
    inconclusive = False
    contradiction = False
    max_depth_used = 0
    min_theta = None
    min_p = None
    max_p = None
    min_40mp = None
    min_fp = None
    min_f = None
    old_precision = ctx.prec

    def update_min(current, value):
        return value if current is None or value < current else current

    def inspect(left, right, depth, is_origin):
        nonlocal inconclusive, contradiction, max_depth_used
        nonlocal min_theta, min_p, max_p, min_40mp, min_fp, min_f
        max_depth_used = max(max_depth_used, depth)
        try:
            margins = profile_margin_balls(arb_interval(left, right), args.terms, args.precision)
        except RuntimeError:
            return None
        theta, p, mp, f, fp = (margins[k] for k in ("theta", "P", "40_minus_P", "F", "F_prime"))
        if theta.upper() < 0 or p.upper() < 0 or mp.upper() < 0 or (fp if is_origin else f).upper() < 0:
            contradiction = True
            return {"contradiction": True}
        ok = positive(theta) and positive(p) and positive(mp) and positive(fp if is_origin else f)
        if not ok:
            return None
        min_theta = update_min(min_theta, theta.lower())
        min_p = update_min(min_p, p.lower())
        max_p = p.upper() if max_p is None or p.upper() > max_p else max_p
        min_40mp = update_min(min_40mp, mp.lower())
        if is_origin:
            min_fp = update_min(min_fp, fp.lower())
        else:
            min_f = update_min(min_f, f.lower())
        return {
            "left": str(left), "right": str(right), "depth": depth,
            "origin": is_origin, "theta_lower": bound_string(theta.lower()),
            "P_lower": bound_string(p.lower()), "P_upper": bound_string(p.upper()),
            "F_lower": bound_string(fp.lower() if is_origin else f.lower()),
            "F_prime_lower": bound_string(fp.lower()), "precision": args.precision,
            "terms": args.terms,
        }

    while pending:
        left, right, depth, is_origin = pending.pop(0)
        result = inspect(left, right, depth, is_origin)
        if result is not None and not result.get("contradiction"):
            boxes.append(result)
            continue
        if contradiction:
            break
        if depth >= args.max_depth or len(pending) + len(boxes) >= args.max_boxes:
            inconclusive = True
            break
        mid = (left + right) / 2
        pending.insert(0, (mid, right, depth + 1, is_origin))
        pending.insert(0, (left, mid, depth + 1, is_origin))

    # Validate exact adjacency independently of the numeric enclosures.
    ordered = sorted(boxes, key=lambda b: Fraction(b["left"]))
    covered = bool(ordered) and Fraction(ordered[0]["left"]) == target_left
    for previous, current in zip(ordered, ordered[1:]):
        covered = covered and Fraction(previous["right"]) == Fraction(current["left"])
    covered = covered and bool(ordered) and Fraction(ordered[-1]["right"]) == target_right
    if pending:
        covered = False
    if not covered and not contradiction:
        inconclusive = True
    status = "CONTRADICTION_FOUND" if contradiction else ("INCONCLUSIVE" if inconclusive else "PROVED_OUTWARD_ROUNDED_ON_[0,1/2]")
    artifact = {
        "status": status,
        "repository_commit": subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "python_flint_version": str(getattr(__import__("flint"), "__version__", "unknown")),
        "flint_version": str(flint_version), "precision_bits": args.precision,
        "theta_terms": args.terms, "tail_method": "geometric_gaussian_majorant_symmetric_ball",
        "certified_interval": "[0,1/2]", "origin_cut": str(origin),
        "number_of_boxes": len(boxes), "maximum_depth_used": max_depth_used,
        "minimum_theta_lower": bound_string(min_theta) if min_theta is not None else None,
        "minimum_P_lower": bound_string(min_p) if min_p is not None else None,
        "maximum_P_upper": bound_string(max_p) if max_p is not None else None,
        "minimum_40_minus_P_lower": bound_string(min_40mp) if min_40mp is not None else None,
        "minimum_F_prime_origin_lower": bound_string(min_fp) if min_fp is not None else None,
        "minimum_F_rest_lower": bound_string(min_f) if min_f is not None else None,
        "all_boxes_covered": covered, "formula_version": "compact-profile-v1",
        "boxes": ordered,
    }
    ctx.prec = old_precision
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: artifact[k] for k in ("status", "number_of_boxes", "maximum_depth_used", "all_boxes_covered")}, indent=2))
    return 0 if status == "PROVED_OUTWARD_ROUNDED_ON_[0,1/2]" else 2


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--precision", type=int, default=256)
    p.add_argument("--terms", type=int, default=30)
    p.add_argument("--origin-cut", default="1/256")
    p.add_argument("--max-depth", type=int, default=30)
    p.add_argument("--max-boxes", type=int, default=100000)
    p.add_argument("--output", default="artifacts/certificates/compact_profile_m500_M40.json")
    args = p.parse_args()
    raise SystemExit(certify(args))


if __name__ == "__main__":
    main()
