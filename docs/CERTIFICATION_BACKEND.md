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
