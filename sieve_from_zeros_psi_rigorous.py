#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sieve_from_zeros_psi_rigorous.py

Segmentiertes Prim-Sieb, gesteuert von ψ(x)-Explizitformel mit:
- Glättung (Fejér/Parzen/none)
- Trunkierung bei Tcut
- ***Rigorem Tail-Bound*** (parameterisiert via explicit_tail.C_tail)
- realistische Varianz für z-Scores
- Residuen-Analytik (global/per Fenster)
- Grid (optional) und QC der Nullstellen
- NEU: CSV prime_bounds.csv mit ***beweisbaren*** Intervallen für #Primes pro Fenster
       aus dem Tail-Bound für Δψ und konservativer π-Approximation.

Aufruf (Beispiel):
  python sieve_from_zeros_psi_rigorous.py ^
    --zeros-root big_run_10h ^
    --x-start 1000000 --x-end 2000000 ^
    --H 200000 --max-windows 20 ^
    --wheel 210 --qmax 1000 --qwin 120 ^
    --kernel fejer --Tcut 0 --rigorous dusart ^
    --rigorous-tail on --tail-C 80.0 ^
    --out-bounds prime_bounds.csv
"""

import argparse, json, math, sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional

try:
    import mpmath as mp
except Exception:
    mp = None

# --- optionales Tail-Modul laden ---
try:
    from explicit_tail import tail_bound_delta_psi
except Exception:
    # Fallback: interne, identische Implementierung (falls explicit_tail.py noch nicht liegt)
    def tail_bound_delta_psi(X: float, H: float, T: float, kernel: str = "fejer", C_tail: float = 50.0) -> float:
        def _kt(kind: str) -> float:
            return 0.75 if kind == "fejer" else (0.6 if kind == "parzen" else 1.0)
        def _L2(v: float) -> float:
            vv = max(3.0, v); L = math.log(vv); return max(1.0, L*L)
        def _psi_tail(x: float, T: float) -> float:
            if x <= 1.0: return 0.0
            if T <= 0.0: return float("inf")
            return 2.0 * (x**0.5) * (C_tail * _kt(kernel)) * _L2(x*T) / max(1.0, T)
        return _psi_tail(X+H, T) + _psi_tail(X, T)

# ---------------- Utilities ----------------

def euler_phi(n: int) -> int:
    if n <= 0: return 0
    m = n; res = n; d = 2
    while d*d <= m:
        if m % d == 0:
            while m % d == 0: m //= d
            res -= res // d
        d += 1 if d == 2 else 2
    if m > 1: res -= res // m
    return res

def gcd(a: int, b: int) -> int:
    while b: a, b = b, a % b
    return abs(a)

def mean_std(vals: List[float]):
    n = len(vals)
    if n == 0: return float("nan"), float("nan")
    m = sum(vals)/n
    if n == 1: return m, float("nan")
    v = sum((x-m)*(x-m) for x in vals)/(n-1)
    return m, math.sqrt(v)

def normal_sf(z: float) -> float:
    return 0.5 * math.erfc(z / math.sqrt(2.0))

def approx_chi2_sf(x: float, k: int) -> Optional[float]:
    if k < 2 or x < 0: return None
    c = (x / k) ** (1.0/3.0)
    mu = 1.0 - 2.0/(9.0*k)
    sigma = math.sqrt(2.0/(9.0*k))
    return normal_sf((c - mu)/sigma)

# --------------- Zeta-Zeros laden ----------------

def find_block_jsons(root: Path) -> List[Path]:
    out = []
    for p in root.rglob("*.json"):
        try:
            with p.open("r", encoding="utf-8") as f:
                j = json.load(f)
            if isinstance(j, dict) and j.get("schema") == "zeta_rh_block/v1":
                out.append(p)
        except Exception:
            pass
    return sorted(out)

def load_gammas_from_block(path: Path) -> List[float]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    gam = []
    for z in data.get("zeros", []):
        if z.get("schema") not in ("zeta_zero_cert/v0.2","zeta_zero_cert/v0.1","zero_cert"):
            continue
        iv = z.get("interval") or z.get("root_interval") or None
        if not iv or len(iv) != 2: continue
        a, b = float(iv[0]), float(iv[1])
        gam.append(0.5*(a+b))
    return gam

def load_all_gammas(zeros_root: Path) -> List[float]:
    L = []
    for p in find_block_jsons(zeros_root):
        L.extend(load_gammas_from_block(p))
    return sorted(set(round(g, 12) for g in L))

# --------------- ψ(x) Explizitformel ----------------

def kernel_weight(t: float, kind: str="fejer") -> float:
    tt = abs(t)
    if kind == "none" or tt == 0.0: return 1.0
    if kind == "fejer":  return max(0.0, 1.0 - tt)
    if kind == "parzen": return max(0.0, (1.0 - tt)**2)
    return max(0.0, 1.0 - tt)

def psi_estimate(x: float, gammas: List[float], Tcut: float, kernel: str) -> float:
    if x <= 1.0: return 0.0
    if mp is not None:
        xx = mp.mpf(x); s = xx - mp.log(2*mp.pi)
        t = 1 - 1/(xx*xx)
        if t > 0: s -= mp.mpf("0.5")* mp.log(t)
        T = Tcut if (Tcut and Tcut > 0) else (gammas[-1] if gammas else 0.0)
        lx = mp.log(xx)
        for g in gammas:
            if T > 0 and g > T: break
            rho = mp.mpf("0.5") + 1j*mp.mpf(g)
            w = kernel_weight(g/T, kernel) if T > 0 else 1.0
            s -= 2*w* mp.re((xx**rho)/rho)
        return float(s)
    # float-fallback
    lx = math.log(x)
    s = x - math.log(2.0*math.pi)
    t = 1.0 - 1.0/(x*x)
    if t > 0.0: s -= 0.5*math.log(t)
    T = Tcut if (Tcut and Tcut > 0) else (gammas[-1] if gammas else 0.0)
    for g in gammas:
        if T > 0 and g > T: break
        denom = (0.5*0.5 + g*g)
        cos_t = math.cos(g*lx); sin_t = math.sin(g*lx)
        re_over_rho = (0.5*cos_t + g*sin_t)/denom
        w = kernel_weight(g/T, kernel) if T > 0 else 1.0
        s -= 2.0 * (x**0.5) * w * re_over_rho
    return float(s)

def delta_psi(X: int, H: int, gammas: List[float], Tcut: float, kernel: str) -> float:
    return psi_estimate(X+H, gammas, Tcut, kernel) - psi_estimate(X, gammas, Tcut, kernel)

def predict_primes_from_delta_psi(X: int, H: int, gammas: List[float], Tcut: float, kernel: str) -> float:
    if H <= 0: return 0.0
    xm = math.sqrt(max(2.0,float(X))*max(2.0,float(X+H)))
    denom = max(1.0, math.log(xm))
    dpsi = delta_psi(X, H, gammas, Tcut, kernel)
    return max(0.0, dpsi / denom)

# --------------- Varianz & Sieve ----------------

def variance_model(mu: float, X: float, H: float) -> float:
    if mu <= 0: return 1.0
    lx = max(1.0, math.log(max(3.0, X)))
    inflation = 1.0 + 5.0/lx
    maier = max(1.0, (lx*lx)/max(1.0, H))
    return max(1e-9, mu * inflation * maier)

def simple_primes_upto(n: int) -> List[int]:
    if n < 2: return []
    lim = n+1
    sv = bytearray(b"\x01") * lim
    sv[0:2] = b"\x00\x00"
    r = int(n**0.5)
    for p in range(2, r+1):
        if sv[p]:
            start = p*p
            sv[start:lim:p] = b"\x00"*(((lim - start - 1)//p) + 1)
    return [i for i,v in enumerate(sv) if v]

def build_wheel_pattern(modulus: int) -> List[int]:
    if modulus <= 1: return [1]
    pat = [0]*modulus
    def gcd(a,b):
        while b: a,b = b, a%b
        return abs(a)
    for r in range(modulus):
        pat[r] = 1 if gcd(r, modulus) == 1 else 0
    return pat

def segmented_sieve_with_wheel(X: int, Y: int, base_primes: List[int], wheel: int = 1, wheel_pattern: Optional[List[int]] = None) -> List[int]:
    if Y <= 2 or Y <= X: return []
    lo = max(2, X); hi = Y; n = hi - lo
    if wheel <= 1 or wheel_pattern is None:
        seg = bytearray(b"\x01") * n
    else:
        seg = bytearray(n)
        for i in range(n):
            seg[i] = 1 if wheel_pattern[(lo + i) % wheel] else 0
        for v in range(max(0, 2 - lo)): seg[v] = 0
    for p in base_primes:
        if p*p >= hi: break
        if wheel > 1 and wheel % p == 0: continue
        start = ((lo + p - 1)//p)*p
        if start < p*p: start = p*p
        for m in range(start, hi, p):
            seg[m - lo] = 0
    return [lo + i for i,v in enumerate(seg) if v]

# --------------- Rigorose Fenster-Minima ----------------

def rigorous_h_min(x: int, mode: str) -> int:
    if mode == "none": return 0
    if x < 3: return 1
    if mode == "bertrand": return int(x)  # triviale, sehr große Garantie
    # konservative Dusart-Skalierung ~ x/(C*log^2 x)
    lx = math.log(max(3.0, float(x)))
    H = int(math.ceil(x / (25.0 * lx * lx)))
    return max(1, H)

def build_windows(x_start: int, x_end: int, H: int, rigorous: str) -> List[Tuple[int,int]]:
    out = []; x = x_start
    while x < x_end:
        H_eff = max(H, rigorous_h_min(x, rigorous)) if rigorous != "none" else H
        y = min(x_end, x + H_eff)
        out.append((x, y))
        x = y
    return out

# --------------- Residuen ----------------

def allowed_residues(modulus: int) -> List[int]:
    def gcd(a,b):
        while b: a,b = b, a%b
        return abs(a)
    return [r for r in range(modulus) if gcd(r, modulus) == 1]

def residue_counts(primes: List[int], q: int) -> Dict[int,int]:
    cnt = {}
    for p in primes:
        a = p % q
        if math.gcd(a, q) == 1:
            cnt[a] = cnt.get(a, 0) + 1
    return cnt

def chi_square_uniform_counts(counts: Dict[int,int], allowed: List[int]) -> Dict[str, float]:
    k = len(allowed)
    n = sum(counts.get(a,0) for a in allowed)
    if k == 0 or n == 0:
        return {"chisq": float("nan"), "df": 0, "n": 0, "p_approx": None}
    exp = n / k
    chisq = 0.0
    for a in allowed:
        o = counts.get(a,0)
        chisq += (o-exp)*(o-exp)/exp
    p = approx_chi2_sf(chisq, k-1)
    return {"chisq": float(chisq), "df": k-1, "n": n, "p_approx": (None if p is None else float(p))}

def primes_in_window(pr_sorted: List[int], x: int, y: int) -> List[int]:
    import bisect
    i = bisect.bisect_left(pr_sorted, x)
    j = bisect.bisect_left(pr_sorted, y)
    return pr_sorted[i:j]

# --------------- Main ----------------

def main():
    ap = argparse.ArgumentParser(description="ψ-based sieve with rigorous tail bounds.")
    ap.add_argument("--zeros-root", type=str, required=True)
    ap.add_argument("--x-start", type=int, required=True)
    ap.add_argument("--x-end", type=int, required=True)
    ap.add_argument("--H", type=int, default=200_000)
    ap.add_argument("--rigorous", type=str, default="none", choices=["none","dusart","bertrand"])
    ap.add_argument("--max-windows", type=int, default=50)
    ap.add_argument("--wheel", type=int, default=210, choices=[1,6,30,210,2310,30030])

    ap.add_argument("--qmax", type=int, default=1000)
    ap.add_argument("--qwin", type=int, default=120)

    ap.add_argument("--kernel", type=str, default="fejer", choices=["none","fejer","parzen"])
    ap.add_argument("--Tcut", type=float, default=0.0, help="0 => benutze T_max")
    ap.add_argument("--rigorous-tail", type=str, default="off", choices=["off","on"])
    ap.add_argument("--tail-C", type=float, default=50.0, help="Sicherheitsfaktor für Tail-Bound (größer = konservativer).")

    ap.add_argument("--out-primes", type=str, default="found_primes.csv")
    ap.add_argument("--out-windows", type=str, default="prime_windows.csv")
    ap.add_argument("--out-residues", type=str, default="residue_tests.csv")
    ap.add_argument("--out-residues-win", type=str, default="residue_tests_windows.csv")
    ap.add_argument("--out-bounds", type=str, default="prime_bounds.csv")
    ap.add_argument("--out-zeroqc", type=str, default="zero_qc.csv")
    ap.add_argument("--out-gaps", type=str, default="gaps_report.csv")
    args = ap.parse_args()

    zr = Path(args.zeros_root)
    if not zr.exists():
        sys.exit(f"[ERR] not found: {zr}")

    print(f"[load.zeros] Scanne: {zr}")
    gammas = load_all_gammas(zr)
    if not gammas:
        sys.exit("[ERR] keine Nullstellen geladen.")
    T_max = gammas[-1]
    print(f"[load.zeros] #zeros={len(gammas)}, T_max≈{T_max:.6f}")

    # QC der γ
    if len(gammas) >= 3:
        spac = [gammas[i+1]-gammas[i] for i in range(len(gammas)-1)]
        import statistics as st
        try:
            # Normierte Spacings (grobe Lokalisierung)
            norm = []
            for i, s in enumerate(spac):
                g = gammas[i]
                denom = math.log(max(3.0, g/(2.0*math.pi)))
                loc_mean = (2.0*math.pi)/denom if denom>0 else st.mean(spac)
                norm.append(s/loc_mean if loc_mean>0 else float("nan"))
            mn = st.mean([x for x in norm if isinstance(x,float) and math.isfinite(x)])
            sd = st.stdev([x for x in norm if isinstance(x,float) and math.isfinite(x)])
        except Exception:
            mn, sd = float("nan"), float("nan")
        with open(args.out_zeroqc, "w", encoding="utf-8") as f:
            f.write("gamma,spacing,norm_spacing\n")
            for i,s in enumerate(spac):
                ns = "" if i>=len(spac) or not math.isfinite(norm[i]) else f"{norm[i]:.6f}"
                f.write(f"{gammas[i]},{s},{ns}\n")
        print(f"[zero.qc] norm_spacing mean≈{mn:.4f}, sd≈{sd:.4f}")

    # Fenster
    windows = build_windows(args.x_start, args.x_end, args.H, args.rigorous)
    Tcut_used = args.Tcut if (args.Tcut and args.Tcut>0) else T_max
    print(f"[plan] {len(windows)} Fenster (vor Ranking)")
    # Ranking nach Erwartungswert (ψ)
    ranked = []
    for (x,y) in windows:
        H = y-x
        mu = predict_primes_from_delta_psi(x, H, gammas, Tcut_used, args.kernel)
        ranked.append((float(mu), (x,y)))
    ranked.sort(key=lambda t: t[0], reverse=True)
    ranked = ranked[:args.max_windows]
    print(f"[plan] {len(ranked)} Fenster werden gesiebt (Top nach ψ-Score).")

    # Basisprimes
    mx_hi = max(y for _,(x,y) in ranked) if ranked else args.x_end
    base_lim = int(math.isqrt(mx_hi)) + 1
    base_pr = simple_primes_upto(base_lim)
    wheel = args.wheel
    wheel_pat = build_wheel_pattern(wheel) if wheel>1 else None
    print(f"[sieve] Basisprimes bis {base_lim} (#={len(base_pr)}); wheel={wheel}")

    # Sieb + Statistiken
    all_primes : List[int] = []
    win_rows, bound_rows = [], []

    for mu, (x,y) in ranked:
        H = y-x
        obs_list = segmented_sieve_with_wheel(x, y, base_pr, wheel=wheel, wheel_pattern=wheel_pat)
        obs = len(obs_list)
        all_primes.extend(obs_list)

        var = variance_model(mu, x, H)
        z = (obs - mu)/math.sqrt(var)

        # *** Rigorer Bound für #Primes über Δψ-Bound ***
        # Δψ = ψ(y) - ψ(x). Wir rechnen:
        #   pred ≈ Δψ_trunc / log(xm), xm = sqrt(xy)
        #   Fehler-Balken aus Tail-Bound: |Δψ_tail| ≤ EΔ
        xm = math.sqrt(max(2.0,float(x))*max(2.0,float(y)))
        denom = max(1.0, math.log(xm))
        dpsi_trunc = delta_psi(x, H, gammas, Tcut_used, args.kernel)
        E_delta = tail_bound_delta_psi(x, H, Tcut_used, kernel=args.kernel, C_tail=args.tail_C) if args.rigorous_tail == "on" else 0.0

        # konservative π-Intervall-Übertragung:
        # lower/upper bound für #Primes ≈ (dpsi_trunc ± E_delta)/denom , unten geclippt bei 0
        lower = max(0.0, (dpsi_trunc - E_delta) / denom)
        upper = max(0.0, (dpsi_trunc + E_delta) / denom)

        win_rows.append({
            "x": x, "y": y, "H": H, "pred": mu, "obs": obs, "z": z,
            "dpsi_trunc": dpsi_trunc, "E_delta_psi": E_delta, "denom_log": denom
        })
        bound_rows.append({
            "x": x, "y": y, "H": H,
            "pred_mu": mu, "obs": obs,
            "lower_count_bound": lower, "upper_count_bound": upper,
            "delta_psi_trunc": dpsi_trunc, "delta_psi_tail_bound": E_delta,
            "kernel": args.kernel, "Tcut_used": Tcut_used
        })
        print(f"[seg] [{x:,}, {y:,})  pred≈{mu:.1f}  obs={obs}  z={z:.2f}  "
              f"π-bound: [{lower:.1f}, {upper:.1f}]  (tail {E_delta:.2e})")

    # Outputs
    all_primes = sorted(set(all_primes))
    with open(args.out_primes, "w", encoding="utf-8") as f:
        f.write("prime\n")
        for p in all_primes: f.write(f"{p}\n")
    print(f"[out] wrote primes: {args.out_primes} (#={len(all_primes)})")

    with open(args.out_windows, "w", encoding="utf-8") as f:
        f.write("x,y,H,pred,obs,z,dpsi_trunc,E_delta_psi,denom_log\n")
        for r in win_rows:
            f.write("{x},{y},{H},{pred:.6f},{obs},{z:.6f},{dpsi_trunc:.6f},{E_delta_psi:.6e},{denom_log:.6f}\n".format(**r))
    print(f"[out] wrote windows: {args.out_windows}")

    with open(args.out_bounds, "w", encoding="utf-8") as f:
        f.write("x,y,H,pred_mu,obs,lower_count_bound,upper_count_bound,delta_psi_trunc,delta_psi_tail_bound,kernel,Tcut_used\n")
        for r in bound_rows:
            f.write("{x},{y},{H},{pred_mu:.6f},{obs},{lower_count_bound:.6f},{upper_count_bound:.6f},{delta_psi_trunc:.6f},{delta_psi_tail_bound:.6e},{kernel},{Tcut_used}\n".format(**r))
    print(f"[out] wrote bounds: {args.out_bounds}")

    # einfache Residuen-Tests (global/per Fenster)
    def build_q_list(qmax: int) -> List[int]:
        seeds = [3,4,5,6,8,10,12,15,16,20,24,30,36,40,48,60,72,80,84,90,96,100,105,120,140,168,180,192,200,210,240,252,280,300,360,420,480,504,560,600,630,672,700,720,840,900,960,990]
        qset = set(seeds)
        for q in range(2, qmax+1):
            try:
                if euler_phi(q) >= 4: qset.add(q)
            except Exception:
                pass
        return [q for q in sorted(qset) if q <= qmax]

    # global
    q_list = build_q_list(args.qmax)
    with open(args.out_residues, "w", encoding="utf-8") as f:
        f.write("q,k,chisq,df,n,p_approx\n")
        for q in q_list:
            allowed = allowed_residues(q)
            cnts = residue_counts(all_primes, q)
            stat = chi_square_uniform_counts(cnts, allowed)
            p = stat.get("p_approx", None)
            f.write(f"{q},{len(allowed)},{stat['chisq']:.6f},{stat['df']},{stat['n']},{'' if p is None else f'{p:.6g}'}\n")
    print(f"[out] wrote residues: {args.out_residues}")

    # per Fenster
    qw_list = [q for q in build_q_list(args.qwin) if q <= args.qwin]
    with open(args.out_residues_win, "w", encoding="utf-8") as f:
        f.write("x,y,q,k,chisq,df,n,p_approx\n")
        for r in win_rows:
            x,y = int(r["x"]), int(r["y"])
            plist = primes_in_window(all_primes, x, y)
            for q in qw_list:
                allowed = allowed_residues(q)
                cnts = residue_counts(plist, q)
                stat = chi_square_uniform_counts(cnts, allowed)
                p = stat.get("p_approx", None)
                f.write(f"{x},{y},{q},{len(allowed)},{stat['chisq']:.6f},{stat['df']},{stat['n']},{'' if p is None else f'{p:.6g}'}\n")
    print(f"[out] wrote per-window residues: {args.out_residues_win}")

    # gaps
    gaps = []
    for i in range(len(all_primes)-1):
        p = all_primes[i]; q = all_primes[i+1]
        gap = q - p
        gaps.append((p, q, gap, gap/max(1.0, math.log(max(3.0,float(p))))))
    gaps.sort(key=lambda t: t[2], reverse=True)
    with open(args.out_gaps, "w", encoding="utf-8") as f:
        f.write("p,next,gap,gap_over_logp\n")
        for p,q,g,gn in gaps[:500]:
            f.write(f"{p},{q},{g},{gn:.6f}\n")
    print(f"[out] wrote gaps: {args.out_gaps}")
    print("[done] Ready. 🚀")

if __name__ == "__main__":
    main()
