import json, sys
ALLOWED_SIGN = {"pos","neg","zero","unknown"}

def _as_float(x):
    if isinstance(x, (int,float)): return float(x)
    if isinstance(x, str): return float(x)
    raise TypeError(f"not a number: {x!r}")

def verify_zero_cert(cert):
    if cert.get("schema") != "zeta_zero_cert/v0.2":
        raise ValueError("schema mismatch for zero cert")
    a,b = cert.get("bracket",[None,None])
    A,B = cert.get("interval",[None,None])
    a = _as_float(a); b = _as_float(b); A = _as_float(A); B = _as_float(B)
    width = _as_float(cert.get("width"))
    if abs((B-A) - width) > 1e-18:
        raise ValueError("width mismatch")
    if not (a-1e-12 <= A <= B <= b+1e-12):
        raise ValueError("interval not nested in bracket")
    sA = cert["sign"]["a"]["label"]; sB = cert["sign"]["b"]["label"]
    if sA not in ALLOWED_SIGN or sB not in ALLOWED_SIGN:
        raise ValueError("invalid sign label")
    if sA == sB:
        raise ValueError("endpoint signs must differ")
    uq = cert.get("uniqueness",{})
    if not uq: raise ValueError("missing uniqueness")
    grid = uq.get("grid",[])
    if not grid: raise ValueError("empty uniqueness grid")
    max_gap = _as_float(uq.get("max_gap"))
    min_margin = _as_float(uq.get("min_margin"))
    if min_margin <= 0: raise ValueError("min_margin must be > 0")
    for node in grid:
        lo,hi = node["Zp"]
        lo = _as_float(lo); hi=_as_float(hi)
        if lo <= 0 <= hi: raise ValueError("Z' interval crosses 0")
    if not bool(uq.get("test")):
        raise ValueError("uniqueness test flagged false")
    return True

def verify_turing(cert):
    if cert.get("schema") != "zeta_turing_cert/v0.1":
        raise ValueError("schema mismatch for turing cert")
    dA,dB = cert.get("deltaN_interval",[None,None])
    k = int(cert.get("deltaN_integer"))
    dA = _as_float(dA); dB=_as_float(dB)
    if not (dA <= k <= dB): raise ValueError("integer not inside interval")
    margin = _as_float(cert.get("rounding_margin"))
    if not cert.get("ok_integer"): raise ValueError("ok_integer is false")
    if margin <= 0.0: raise ValueError("rounding margin must be positive")
    return True

def verify_block(report):
    if report.get("schema") != "zeta_rh_block/v1":
        raise ValueError("schema mismatch for block report")
    zeros = report.get("zeros",[])
    for c in zeros: verify_zero_cert(c)
    count = report.get("count",{})
    verify_turing(count)
    N = int(report["consistency"]["n_zeros"])
    k = int(report["consistency"]["deltaN"])
    if N != k or not report["consistency"].get("match"):
        raise ValueError("count/zeros mismatch")
    return True

def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("usage: python mini_verifier_v2.py <json> [<json> ...]", file=sys.stderr)
        return 2
    for path in argv:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sch = data.get("schema")
        if sch == "zeta_rh_block/v1":
            verify_block(data); print(f"OK block: {path}")
        elif sch == "zeta_zero_cert/v0.2":
            verify_zero_cert(data); print(f"OK zero:  {path}")
        elif sch == "zeta_turing_cert/v0.1":
            verify_turing(data); print(f"OK turing:{path}")
        else:
            raise ValueError(f"unknown schema: {sch}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
