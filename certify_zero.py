import mpmath as mp
from rigorous_Z import eval_ZZp_interval, sign_from_interval

def _bisect_interval_zero(a, b, dps, max_steps=140, rad0=1e-12):
    for _ in range(max_steps):
        m = (a + b)/2.0
        Za,_,_ = eval_ZZp_interval(a, rad=rad0, dps=dps)
        Zm,_,_ = eval_ZZp_interval(m, rad=rad0, dps=dps)
        sa = sign_from_interval(Za)
        sm = sign_from_interval(Zm)
        if sa == 'unknown' or sm == 'unknown':
            b = m if (b - a) > 0 else b
            continue
        if sa != sm:
            b = m
        else:
            a = m
    return a, b

def certify_zero_unique(a, b, eps, dps, rad0=1e-12):
    a = float(a); b = float(b)
    Za, Zpa, _ = eval_ZZp_interval(a, rad=rad0, dps=dps)
    Zb, Zpb, _ = eval_ZZp_interval(b, rad=rad0, dps=dps)
    sa, sb = sign_from_interval(Za), sign_from_interval(Zb)
    if sa == 'unknown' or sb == 'unknown' or sa == sb:
        return False, (a,b), {"ok": False, "reason": "no robust sign change at endpoints"}

    A, B = a, b
    while (B - A) > eps:
        M = 0.5*(A + B)
        Zm, _, _ = eval_ZZp_interval(M, rad=rad0, dps=dps)
        sm = sign_from_interval(Zm)
        if sm == 'unknown':
            B = M
            continue
        if sm != sa:
            B = M
            Zb, sb = Zm, sm
        else:
            A = M
            Za, sa = Zm, sm

    grid = []
    k = 12
    max_gap = 0.0
    min_margin = float('inf')
    Lp_max = 0.0
    for i in range(k+1):
        x = float(A + (B - A)*i/k)
        _, Zp_iv, Lp = eval_ZZp_interval(x, rad=rad0, dps=dps)
        lo, hi = Zp_iv
        margin = min(abs(lo), abs(hi)) if (lo*hi) > 0 else 0.0
        grid.append({"x": x, "Zp": [lo,hi], "rad": rad0, "Lp": Lp})
        min_margin = min(min_margin, margin)
        Lp_max = max(Lp_max, Lp)
        if i>0:
            prevx = grid[-2]["x"]
            max_gap = max(max_gap, abs(x - prevx))

    uniqueness_ok = (min_margin > 0.0) and (Lp_max*max_gap/2.0 < min_margin)

    cert = {
        "schema": "zeta_zero_cert/v0.2",
        "params": {"dps": dps, "eps": eps},
        "bracket": [a,b],
        "interval": [A,B],
        "width": B - A,
        "sign": {
            "a": {"Z": [Za[0], Za[1]], "label": sign_from_interval(Za)},
            "b": {"Z": [Zb[0], Zb[1]], "label": sign_from_interval(Zb)}
        },
        "uniqueness": {
            "grid": grid,
            "max_gap": max_gap,
            "min_margin": min_margin,
            "test": uniqueness_ok
        },
        "method": "bisect+interval-diagnostic",
        "rigorous": False,
        "rigor_note": "Numerical padded intervals are not a proof certificate without validated outward rounding and complete Z/Z' remainder bounds.",
        "ok": bool(uniqueness_ok)
    }
    return bool(uniqueness_ok), (A,B), cert
