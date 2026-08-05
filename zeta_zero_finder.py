# zeta_zero_finder.py
# Enumerates zeros of zeta(1/2 + i t) up to T_max via Hardy Z(t).
# Features: hybrid Z(t), adaptive scan step, bracketing, bisection/secant, block processing,
#           dedup filter, CSV append, optional JSON "certificates" for each bracket.

import argparse, csv, json
from pathlib import Path
import mpmath as mp
import numpy as np

# ---------- Hardy Z(t): complete mpmath Siegel evaluation by default ----------
mp.mp.dps = 60  # default; can be overridden via --dps

_TWO_PI = mp.mpf('6.283185307179586476925286766559005768394338798750211641949')
_ln_cache = []

def _ensure_ln_cache(N_needed: int):
    global _ln_cache
    if not _ln_cache:
        _ln_cache = [mp.mpf('0.0')]
    curr = len(_ln_cache) - 1
    while curr < N_needed:
        _ln_cache.append(mp.log(curr + 1))
        curr += 1

def theta(t):
    t = mp.mpf(t)
    return mp.im(mp.log(mp.gamma(mp.mpf('0.25') + 0.5j*t))) - (t/2)*mp.log(mp.pi)

def Z_rs_main_sum(t):
    """Leading Riemann–Siegel sum only; never label its roots certified."""
    t  = mp.mpf(t)
    th = theta(t)
    N  = int(mp.floor(mp.sqrt(t / _TWO_PI)))
    if N < 1:
        return mp.mpf('0.0')
    _ensure_ln_cache(N)
    s = mp.mpf('0.0')
    invsqrt = mp.sqrt
    for n in range(1, N+1):
        s += (1 / invsqrt(n)) * mp.cos(th - t * _ln_cache[n])
    return 2*s

def Z_rs(t):
    """Complete available Riemann–Siegel evaluation supplied by mpmath."""
    return mp.siegelz(mp.mpf(t))

def Z_exact(t):
    t = mp.mpf(t)
    return mp.re(mp.exp(1j*theta(t)) * mp.zeta(0.5 + 1j*t))

def Z(t, switch=50.0, approximate=False):
    """Use exact zeta below the switch and complete Siegel Z above it.

    Set approximate=True only for exploratory leading-sum scans.
    """
    t = mp.mpf(t)
    if approximate and t > switch:
        return Z_rs_main_sum(t)
    return Z_exact(t) if t <= switch else Z_rs(t)

# ---------- Refinement ----------
def bisect_zero(a, b, steps=80):
    fa, fb = Z(a), Z(b)
    for _ in range(steps):
        m = (a + b) / 2
        fm = Z(m)
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2

def secant_zero(a, b, maxiter=40, tol=mp.mpf('1e-30')):
    x0, x1 = mp.mpf(a), mp.mpf(b)
    f0, f1 = Z(x0), Z(x1)
    for _ in range(maxiter):
        if f1 == f0:
            return (x0 + x1) / 2
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = Z(x2)
        if abs(f2) < tol:
            return x2
        x0, f0 = x1, f1
        x1, f1 = x2, f2
    return x1

# ---------- Chebyshev refinement ----------
def refine_zero_chebyshev(a, b, k=8, fallback=None):
    """
    Refine a zero estimate on the interval [a,b] using barycentric Chebyshev
    interpolation.  A polynomial of degree (k-1) is fit to k Chebyshev nodes
    within [a,b] and its roots are inspected.  The root closest to the
    fallback estimate (if provided) and inside [a,b] is returned.

    Args:
        a: left endpoint of the bracket.
        b: right endpoint of the bracket.
        k: number of Chebyshev nodes to sample (degree = k-1).
        fallback: optional fallback estimate (e.g. from bisection or secant).

    Returns:
        A float approximating the refined zero.  If no suitable root is found,
        the fallback (if provided) or the mid-point of [a,b] is returned.
    """
    try:
        # Generate Chebyshev nodes on [-1,1]
        js = np.arange(1, k+1)
        nodes = np.cos((2*js - 1) * np.pi / (2*k))
        # Map nodes to [a,b]
        points = 0.5*(a + b) + 0.5*(b - a) * nodes
        # Evaluate Hardy Z at those points
        vals = np.array([float(Z(p)) for p in points])
        # Fit polynomial of degree k-1
        coeffs = np.polyfit(points, vals, k-1)
        # Find roots of the polynomial
        roots = np.roots(coeffs)
        # Filter for real roots inside [a,b]
        real_roots = [r.real for r in roots if abs(r.imag) < 1e-6 and a <= r.real <= b]
        if not real_roots:
            # fall back
            return fallback if fallback is not None else 0.5*(a+b)
        # Choose the root closest to fallback or the mid-point
        target = fallback if fallback is not None else 0.5*(a+b)
        refined = min(real_roots, key=lambda r: abs(r - target))
        return float(refined)
    except Exception:
        return fallback if fallback is not None else 0.5*(a+b)

# ---------- Dedup & step helpers ----------
def local_wavelength(t):
    """~ spacing scale ≈ 2π / log t (Riemann–Siegel)."""
    t_ref = max(mp.mpf(t), mp.mpf('3.0'))
    return float(2 * mp.pi / mp.log(t_ref))

def dedup_zeros(zs, factor=0.8):
    if not zs:
        return []
    zs = sorted(float(z) for z in zs)
    out = [zs[0]]
    for t in zs[1:]:
        if t - out[-1] >= factor * local_wavelength(t):
            out.append(t)
    return out

def adaptive_step(t, scale=1.0, min_step=0.002, max_step=0.08):
    """Δt ≍ scale * 2π / log t, clamped."""
    dt = scale * local_wavelength(t)
    return float(max(min_step, min(max_step, dt)))

# ---------- Scan & bracket ----------
def scan_brackets(T1, T2, fixed_step=None, adapt_scale=0.25, min_step=0.002):
    """
    Return a list of brackets ``[a, b]`` where the Hardy Z-function changes sign
    between ``a`` and ``b``.  The scanning mechanism supports both fixed and
    adaptive step sizes.  To minimize the risk of skipping zeros when the
    function oscillates rapidly, it employs a **repeated halving** strategy.

    Parameters
    ----------
    T1, T2 : float
        The start and end of the scanning interval (``T1 <= T2``).  Both
        endpoints are interpreted as real heights on the critical line.
    fixed_step : float or None
        If provided, a constant step length used throughout the scan.  When
        ``None``, the step size is chosen adaptively via
        ``adaptive_step(t, scale=adapt_scale)``.  Adaptive scanning is
        preferred at large heights since the zero spacing grows slowly.
    adapt_scale : float
        Scaling factor for the adaptive step when ``fixed_step`` is ``None``.
    min_step : float
        The lower bound for adaptive step sizes.  This value also determines
        when repeated halving terminates: once the halved step falls below
        ``1.5 * min_step`` the algorithm stops halving and accepts that no
        sign change occurs in the interval.

    Returns
    -------
    list of tuple(float, float)
        A list of tuples ``(a, b)`` where ``Z(a)`` and ``Z(b)`` have
        opposite signs, indicating a zero in ``(a, b)``.
    """
    brackets = []
    t = mp.mpf(T1)
    f = Z(t)
    # Continue scanning until we reach or surpass T2
    while t < T2:
        # Determine the nominal step length
        dt = fixed_step if fixed_step else adaptive_step(t, scale=adapt_scale)
        dt_cur = dt
        sign_found = False
        # Repeatedly probe midpoints by halving dt_cur until a sign change is
        # detected or the step becomes sufficiently small.  For fixed scanning
        # we do not halve at all.
        while True:
            t_candidate = mp.mpf(min(T2, t + dt_cur))
            g = Z(t_candidate)
            # If a sign change is detected between f and g, record the bracket
            if f * g < 0:
                brackets.append((float(t), float(t_candidate)))
                # Update state to the candidate point and mark as found
                t, f = t_candidate, g
                sign_found = True
                break
            # If no sign change and adaptive scanning is enabled, try halving
            if fixed_step is None and dt_cur > min_step * 1.5:
                dt_cur *= 0.5
                continue
            # No sign change and halving is exhausted; stop probing
            break
        # If no sign change was found, advance by the nominal step
        if not sign_found:
            t_next = mp.mpf(min(T2, t + dt))
            # Avoid infinite loops if dt rounds to zero
            if t_next == t:
                break
            f = Z(t_next)
            t = t_next
    return brackets

# ---------- Block runner ----------
def process_block(T1, T2, args, csv_writer=None, cert_list=None):
    brackets = scan_brackets(T1, T2, fixed_step=args.fixed_step, adapt_scale=args.adapt_scale)
    results = []
    for (a, b) in brackets:
        # refine: use bisect and optionally secant and Chebyshev
        z_bi = bisect_zero(a, b, steps=args.bisect_steps)
        z_sec = secant_zero(a, b) if not args.no_sec else z_bi
        z_ref = z_sec
        if getattr(args, "cheb", False):
            z_ref = refine_zero_chebyshev(a, b, k=getattr(args, "cheb_k", 8), fallback=z_sec)
        # optional certificate (proof trace = just the bracket endpoints + method summary)
        cert = None
        if cert_list is not None:
            method_label = []
            if args.no_sec:
                method_label.append("bisect")
            else:
                method_label.append("secant")
            if getattr(args, "cheb", False):
                method_label.append("cheb")
            cert = {
                "bracket": [a, b],
                "refined": float(z_ref),
                "method": "+".join(method_label),
                "bisect_steps": args.bisect_steps,
                "dps": args.dps,
                "cheb_k": getattr(args, "cheb_k", None) if getattr(args, "cheb", False) else None
            }
            cert_list.append(cert)
        if csv_writer:
            csv_writer.writerow([f"{float(z_ref):.12f}", f"{a:.12f}", f"{b:.12f}", args.dps, args.bisect_steps])
        results.append(float(z_ref))
    return results

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser(description="Enumerate zeros of zeta(1/2+it) up to T_max (blockwise).")
    ap.add_argument("--tmin", type=float, default=10.0, help="start height (>= ~10 recommended)")
    ap.add_argument("--tmax", type=float, required=True, help="end height")
    ap.add_argument("--block", type=float, default=20.0, help="block size in t")
    ap.add_argument("--out", type=str, default="zeros.csv", help="CSV output file (append if exists)")
    ap.add_argument("--dps", type=int, default=60, help="mpmath precision")
    ap.add_argument("--bisect-steps", type=int, default=80, help="bisection refinement steps")
    ap.add_argument("--no-sec", action="store_true", help="disable secant refinement (use only bisection)")
    ap.add_argument("--dedup", action="store_true", help="deduplicate zeros by local wavelength")
    ap.add_argument("--fixed-step", type=float, default=None, help="override adaptive step with a fixed Δt")
    ap.add_argument("--adapt-scale", type=float, default=0.25, help="scale for adaptive step (Δt ≈ scale*2π/log t)")
    ap.add_argument("--json", action="store_true", help="write JSON 'certificates' alongside CSV per block")
    ap.add_argument("--cheb", action="store_true", help="enable Chebyshev refinement for zeros")
    ap.add_argument("--cheb-k", type=int, default=8, help="number of Chebyshev nodes for refinement")
    args = ap.parse_args()

    mp.mp.dps = args.dps

    out_path = Path(args.out)
    write_header = not out_path.exists()
    out_file = out_path.open("a", newline="", encoding="utf-8")
    csv_writer = csv.writer(out_file)
    if write_header:
        csv_writer.writerow(["t_zero", "bracket_a", "bracket_b", "dps", "bisect_steps"])

    T = float(max(1.0, args.tmin))
    T_end = float(args.tmax)
    all_zeros = []

    while T < T_end:
        B_end = min(T_end, T + args.block)
        print(f"[Block] {T:.3f} .. {B_end:.3f} @ dps={args.dps}")
        certs = [] if args.json else None
        zs = process_block(T, B_end, args, csv_writer=csv_writer, cert_list=certs)
        out_file.flush()
        if args.dedup:
            zs = dedup_zeros(zs)
        all_zeros.extend(zs)
        if args.json:
            jname = f"{out_path.with_suffix('')}_block_{int(T)}_{int(B_end)}.json"
            Path(jname).write_text(json.dumps({
                "T1": T, "T2": B_end, "dps": args.dps, "zeros": zs, "certificates": certs
            }, indent=2), encoding="utf-8")
        T = B_end

    out_file.close()

    # Print brief summary
    print(f"Total zeros found (raw): {len(all_zeros)}")
    if args.dedup:
        deduped = dedup_zeros(all_zeros)
        print(f"Total zeros after dedup: {len(deduped)}")
        # write a companion CSV with deduped list
        dpath = out_path.with_name(out_path.stem + "_dedup.csv")
        with dpath.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["t_zero"])
            for z in deduped:
                w.writerow([f"{z:.12f}"])
        print(f"Deduped CSV written -> {dpath.resolve()}")

if __name__ == "__main__":
    main()
