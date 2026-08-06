# Optional Arb certification backend

The diagnostic suite uses `mpmath`. Outward-rounded certification uses
`python-flint==0.9.0` in a separate environment:

```bash
python3 -m venv .venv-cert
.venv-cert/bin/python -m pip install -r requirements-certify.txt
.venv-cert/bin/python -m pytest -q tests/certification
```

The smoke test verifies Arb ball containment and directed lower/upper bounds.
The Theta interval path attaches its absolute Gaussian tail majorant as the
symmetric error ball ``[-B, B]``; it never treats a magnitude bound as a
signed remainder.  It also fails closed if the Theta denominator enclosure
contains zero and restores the caller's FLINT precision.

This does **not** certify the infinite Theta series globally: explicit
derivative tail bounds are implemented, but adaptive interval subdivision and
profile-bound certificates are still required before any energy status may
become a theorem.

## Compact profile certificate

The fail-closed driver
`scripts/certify_compact_profile.py` certifies the logarithmic interval
`[0,1/2]`.  It requires strict `Theta.lower() > 0`, uses `F'` rather than
`F/x` on the origin box, and checks `P > 0`, `40-P > 0`, and `F=T-500*x > 0`
on every remaining box.  Unresolved boxes or resource limits produce a
nonzero exit status and `INCONCLUSIVE`.

Reproduction in the pinned environment:

```bash
.venv-cert/bin/python scripts/certify_compact_profile.py \
  --precision 256 --terms 30 --origin-cut 1/256 \
  --max-depth 30 --max-boxes 100000 \
  --output artifacts/certificates/compact_profile_m500_M40.json
```

The current certificate covers 2276 exact rational boxes (maximum depth 15)
and reports `PROVED_OUTWARD_ROUNDED_ON_[0,1/2]`.  This proves only the compact
profile bounds; it does not prove the far tail, endpoint flux conditions,
Weyl--Volterra positivity, or RH.
