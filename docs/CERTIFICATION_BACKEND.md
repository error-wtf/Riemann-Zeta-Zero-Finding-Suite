# Optional Arb certification backend

The diagnostic suite uses `mpmath`. Outward-rounded certification uses
`python-flint==0.9.0` in a separate environment:

```bash
python3 -m venv .venv-cert
.venv-cert/bin/python -m pip install -r requirements-certify.txt
.venv-cert/bin/python -m pytest -q tests/certification
```

The smoke test verifies Arb ball containment and directed lower/upper bounds.
This does **not** certify the infinite Theta series: explicit derivative tail
bounds and adaptive interval subdivision are still required before any energy
status may become a theorem.
