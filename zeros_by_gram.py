# zeros_by_gram.py — robust Gram ladder
import mpmath as mp
from common import Z, theta
def gram_point(n: int, t_start: float = 14.0):
    target = n * mp.pi
    a = mp.mpf(max(7.0, t_start)); fa = theta(a) - target
    step = mp.mpf('0.2'); tries = 0
    while True:
        b = a + step; fb = theta(b) - target
        if fa*fb <= 0: break
        a, fa = b, fb; step *= 1.6; tries += 1
        if tries > 5000:
            t = a + 1.0
            for _ in range(50):
                th = theta(t) - target; dth = 0.5*mp.log(t/(2*mp.pi)); t -= th/dth
            return t
    for _ in range(120):
        m = (a+b)/2; fm = theta(m) - target
        if fa*fm <= 0: b, fb = m, fm
        else: a, fa = m, fm
    return (a+b)/2
def zeros_by_gram(n_from: int, n_to: int, t_seed: float = 14.0):
    zeros = []; g_prev = gram_point(n_from, t_seed); Z_prev = Z(g_prev)
    for n in range(n_from+1, n_to+1):
        g = gram_point(n, g_prev + 0.1); Zg = Z(g)
        if Z_prev == 0: zeros.append(g_prev)
        elif Zg == 0: zeros.append(g)
        elif Z_prev*Zg < 0:
            a,b = g_prev, g; fa,fb = Z_prev, Zg
            for _ in range(80):
                m = (a+b)/2; fm = Z(m)
                if fa*fm <= 0: b, fb = m, fm
                else: a, fa = m, fm
            zeros.append((a+b)/2)
        g_prev, Z_prev = g, Zg
    return zeros
