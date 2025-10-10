# common.py — hybrid Hardy Z(t) small-t exact, large-t RS main sum
import mpmath as mp
mp.mp.dps = max(mp.mp.dps, 60)
_TWO_PI = mp.mpf('6.283185307179586476925286766559005768394338798750211641949')
_ln_cache = []
def _ensure_ln_cache(N_needed: int):
    global _ln_cache
    if not _ln_cache: _ln_cache = [mp.mpf('0.0')]
    curr = len(_ln_cache)-1
    while curr < N_needed:
        _ln_cache.append(mp.log(curr+1)); curr += 1
def theta(t):
    t = mp.mpf(t)
    return mp.im(mp.log(mp.gamma(mp.mpf('0.25')+0.5j*t))) - (t/2)*mp.log(mp.pi)
def Z_rs(t):
    t = mp.mpf(t); th = theta(t)
    N = int(mp.floor(mp.sqrt(t/_TWO_PI)))
    if N < 1: return mp.mpf('0.0')
    _ensure_ln_cache(N)
    s = mp.mpf('0.0')
    for n in range(1, N+1):
        s += (1/mp.sqrt(n))*mp.cos(th - t*_ln_cache[n])
    return 2*s
def Z_exact(t):
    t = mp.mpf(t)
    return mp.re(mp.exp(1j*theta(t)) * mp.zeta(0.5 + 1j*t))
def Z(t):
    t = mp.mpf(t)
    return Z_exact(t) if t <= 50 else Z_rs(t)
