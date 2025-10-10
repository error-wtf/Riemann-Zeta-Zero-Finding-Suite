# rigorous_Z.py - complex-safe theta and analytic Z' ; interval-like enclosures for Z and Z'
import mpmath as mp

# Optional fast real-valued Z/theta from your project (used only for real Z, not for derivatives)
try:
    from common import Z as Z_common, theta as theta_common
except Exception:
    Z_common = None
    theta_common = None

SAFETY = 32.0
MIN_H = mp.mpf('1e-12')

# ---------------- theta and its derivative (complex-safe) ----------------
def _theta(z):
    """
    Riemann-Siegel theta for real/complex z:
      theta(z) = Im(log Gamma(1/4 + i z/2)) - (z/2) log(pi)
    """
    if isinstance(z, (int, float)):
        z = mp.mpf(z)
    return mp.im(mp.log(mp.gamma(mp.mpf('0.25') + 0.5j*z))) - (z/2)*mp.log(mp.pi)

def _theta_prime(t):
    """
    theta'(t) = 0.5*Re(psi(1/4 + i t/2)) - 0.5*log(pi),  for real t
    """
    t = mp.mpf(t)
    w = mp.mpf('0.25') + 0.5j*t
    return 0.5*mp.re(mp.digamma(w)) - 0.5*mp.log(mp.pi)

# ---------------- analytic F(z) and Z, Z' ----------------
def _F(z):
    """
    F(z) = exp(i*theta(z)) * zeta(1/2 + i z). For real z, Re(F(z)) = Z(z).
    """
    if isinstance(z, mp.mpc):
        th = _theta(z)
    else:
        th = theta_common(z) if theta_common is not None else _theta(z)
    return mp.exp(1j*th) * mp.zeta(mp.mpf('0.5') + 1j*z)

def Z_eval_real(t):
    """
    Real-valued Hardy Z on the critical line.
    Prefer project's fast Z if available (real t only), else Re(F(t)).
    """
    if Z_common is not None:
        return mp.mpf(Z_common(t))
    return mp.re(_F(mp.mpf(t)))

def _zeta_and_derivative(s):
    """
    Return (zeta(s), zeta'(s)) using mpmath.diff for the analytic derivative.
    """
    z = mp.zeta(s)
    zp = mp.diff(mp.zeta, s)
    return z, zp

def Z_prime_real(t, dps):
    """
    Z'(t) = Re{ i e^{i theta(t)} [ theta'(t) * zeta(1/2+i t) + zeta'(1/2+i t) ] }.
    """
    old = mp.mp.dps
    mp.mp.dps = max(old, dps + 10)
    try:
        t = mp.mpf(t)
        th = theta_common(t) if theta_common is not None else _theta(t)
        s = mp.mpf('0.5') + 1j*t
        z, zp = _zeta_and_derivative(s)
        return mp.re(1j * mp.exp(1j*th) * (_theta_prime(t)*z + zp))
    finally:
        mp.mp.dps = old

def Z_second_real_numeric(t, dps):
    """
    Numeric second derivative Z''(t) via symmetric difference on Z' (real t only).
    Used to build a conservative Lipschitz bound for Z'.
    """
    h = mp.mpf(10) ** (-max(7, dps//4))
    if h < MIN_H:
        h = MIN_H
    old = mp.mp.dps
    mp.mp.dps = max(old, dps + 20)
    try:
        zp_p = Z_prime_real(t + h, dps + 8)
        zp_m = Z_prime_real(t - h, dps + 8)
        return (zp_p - zp_m) / (2*h)
    finally:
        mp.mp.dps = old

# ---------------- interval helpers ----------------
def _machine_eps():
    return mp.power(10, -mp.mp.dps)

def sign_from_interval(iv):
    lo, hi = iv
    if hi < 0: return 'neg'
    if lo > 0: return 'pos'
    if abs(lo) < 1e-30 and abs(hi) < 1e-30: return 'zero'
    if lo <= 0 <= hi: return 'unknown'
    return 'unknown'

def eval_ZZp_interval(t, rad, dps):
    """
    Conservative (padded) enclosures for Z(t) and Z'(t) over [t-rad, t+rad],
    plus a Lipschitz bound Lp >= sup_{[t-rad,t+rad]} |Z''(x)|.
    Note: this uses numeric pads; for fully rigorous bounds plug in Arb outward rounding.
    """
    t = mp.mpf(t); rad = mp.mpf(rad)
    old = mp.mp.dps
    mp.mp.dps = max(dps, 60)
    try:
        # center values
        Z0   = Z_eval_real(t)
        Zp0  = Z_prime_real(t, dps)
        Zpp0 = Z_second_real_numeric(t, dps)

        eps  = _machine_eps()
        # Taylor/rounding pads
        pad_Z  = SAFETY*10*eps + abs(Zp0)*rad + 0.5*abs(Zpp0)*rad*rad
        pad_Zp = SAFETY*100*eps + abs(Zpp0)*rad

        Z_iv   = (float(Z0 - pad_Z),  float(Z0 + pad_Z))
        Zp_iv  = (float(Zp0 - pad_Zp), float(Zp0 + pad_Zp))
        Lp = float(abs(Zpp0) * (1.0 + float(SAFETY)*0.1))

        return Z_iv, Zp_iv, Lp
    finally:
        mp.mp.dps = old
