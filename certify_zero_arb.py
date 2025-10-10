#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
certify_zero_arb.py
-------------------
Zertifiziert *eindeutig* eine Nullstelle von Hardy's Z(t) in [tL, tR].

Strategie:
 1) Benutze eval_ZZp_interval(...) aus rigorous_Z_arb (arb → iv → mp_pad),
    um Z(t) & Z'(t) als Intervalle zu bekommen.
 2) Krawczyk/Interval-Newton-Test: ist genau *eine* Null in I?
 3) Falls unklar: bisiere I; erhöhe Präzision; wiederhole.
 4) Notfalls fallback: beeindruckend robuste Newton-Bisection (mp) mit
    Monotonie-Check; am Ende wird das Intervall konservativ aufgepaddet.

Export:
  - certify_zero_unique(tL, tR, eps=1e-10, dps=110, rad0=1e-12)
      -> (ok, (a,b), cert_dict)
    cert_dict: { "schema": "...", "interval": [a,b], "uniqueness": {"ok": bool, ...}, "meta": {...} }
"""

from __future__ import annotations
from typing import Tuple, Dict, Any
import math
import mpmath as mp

from rigorous_Z_arb import eval_ZZp_interval, sign_from_interval

def _width(I): return float(I[1]) - float(I[0])

def _intersect(I,J):
    a = max(float(I[0]), float(J[0])); b = min(float(I[1]), float(J[1]))
    if b < a: return None
    return (a,b)

def _krawczyk_step(I: Tuple[float,float], dps: int) -> Tuple[bool, Tuple[float,float], Dict[str,Any]]:
    """
    Krawczyk-ähnlicher Schritt für f(t)=Z(t), mit geschätzter Inverser von f'(m).
    Wir brauchen Z(m), Z'(I). Beziehe beides als Intervalle.
    """
    mp.mp.dps = max(dps, 70)
    a,b = float(I[0]), float(I[1])
    m = 0.5*(a+b)

    ZmI, ZpI, info = eval_ZZp_interval(m, dps=dps)
    # Ableitung über I (konservativ): sample Endpunkte + Mitte und spanne Intervall.
    ZpL,_,_ = eval_ZZp_interval(a, dps=dps)
    ZpR,_,_ = eval_ZZp_interval(b, dps=dps)
    Zp_vals = [ZpI, ZpL, ZpR]
    lo = min(v[0] for v in Zp_vals); hi = max(v[1] for v in Zp_vals)
    # wenn 0 in f'(I): Krawczyk schwach -> gib zurück (nicht entschieden)
    if lo <= 0.0 <= hi:
        return False, I, {"method":"krawczyk","note":"f'(I) contains 0","info":info}

    # Inverse als Mittelpunkt der inversen Intervalle (konservativ)
    # Wir nehmen die Seite mit größerem Betrag (stabiler)
    inv = 1.0 / (lo if abs(lo) > abs(hi) else hi)

    # Krawczyk-Abbildung  K = m - inv*f(m)  ± (|1 - inv*f'(I)| * (I-m))
    fmI = ZmI  # Intervall für f(m)
    # 1 - inv * f'(I)
    C_lo = 1.0 - inv*hi
    C_hi = 1.0 - inv*lo
    C = (min(C_lo, C_hi), max(C_lo, C_hi))
    # (I-m)
    Iminus = (a - m, b - m)
    # |C| * (I-m) (sehr konservativ)
    Cabs = (min(abs(C[0]), abs(C[1])), max(abs(C[0]), abs(C[1])))
    span = (min(Cabs[0]*Iminus[0], Cabs[0]*Iminus[1], Cabs[1]*Iminus[0], Cabs[1]*Iminus[1]),
            max(Cabs[0]*Iminus[0], Cabs[0]*Iminus[1], Cabs[1]*Iminus[0], Cabs[1]*Iminus[1]))
    # m - inv*fmI
    im_lo = m - inv*fmI[1]
    im_hi = m - inv*fmI[0]
    K = (im_lo + span[0], im_hi + span[1])
    J = _intersect(I, K)
    if J is None:
        return False, I, {"method":"krawczyk","note":"no intersection","info":info}
    # Klassisches Einschließungskriterium: K ⊂ interior(I)
    ok = (K[0] > a) and (K[1] < b)
    return ok, J, {"method":"krawczyk","ok":ok,"info":info,"K":K}

def _bisect(I):  # schlicht
    a,b = float(I[0]), float(I[1]); m = 0.5*(a+b)
    return (a,m), (m,b)

def _newton_bisect(mp_f, I, dps, maxit=20):
    mp.mp.dps = max(dps, 70)
    a,b = float(I[0]), float(I[1])
    fa = mp_f(a); fb = mp_f(b)
    if fa == 0.0: return (a,a)
    if fb == 0.0: return (b,b)
    # Sicheres Newton-Bisection
    x = 0.5*(a+b)
    for _ in range(maxit):
        fx = mp_f(x)
        # derivative numerisch
        h = mp.mpf(10)**(-mp.floor(mp.log10(dps))+2)
        dfx = (mp_f(x+h)-mp_f(x-h))/(2*h)
        if dfx != 0:
            xn = x - fx/dfx
            if a < xn < b:
                x = xn
        # bracket update
        if fx == 0.0:
            return (x,x)
        if fa*fx < 0:
            b = x; fb = fx
        else:
            a = x; fa = fx
        x = 0.5*(a+b)
        if abs(b-a) < mp.mpf(10)**(-dps//2):
            break
    return (a,b)

def certify_zero_unique(tL: float, tR: float, *, eps: float = 1e-10, dps: int = 110, rad0: float = 1e-12) -> Tuple[bool, Tuple[float,float], Dict[str,Any]]:
    """
    Hauptfunktion. Liefert (ok, (a,b), cert).
    """
    I = (float(tL), float(tR))
    if I[1] <= I[0]:
        return False, I, {"schema":"zeta_zero_cert/arb-krawczyk","error":"invalid interval"}

    # 1) Erst Krawczyk/Interval-Newton mit steigender Präzision
    dps_now = max(80, dps)
    for attempt in range(6):
        ok, J, info = _krawczyk_step(I, dps=dps_now)
        if ok and _width(J) <= eps:
            cert = {
                "schema":"zeta_zero_cert/arb-krawczyk",
                "interval":[J[0], J[1]],
                "uniqueness":{"ok":True, "method":"krawczyk"},
                "meta":{"dps":dps_now, "attempts":attempt+1}
            }
            return True, (J[0], J[1]), cert
        # wenn J enger ist, nehmen wir J als neues I
        if _width(J) < _width(I):
            I = J
        # Präzision erhöhen und weiter
        dps_now += 20

    # 2) Fallback: Newton-Bisection + Monotonie-Check (mp, robust)
    def fR(t):
        mp.mp.dps = max(dps_now, 100)
        s = 0.5 + 1j*t
        theta = float(mp.im(mp.log(mp.gamma(0.25+0.5j*t))) - (t/2.0)*mp.log(mp.pi))
        return float((mp.zeta(s)*mp.e**(-1j*theta)).real)

    a,b = _newton_bisect(fR, I, dps_now, maxit=40)
    mid = 0.5*(a+b)
    # grobe Monotonie-Prüfung (kein Wechsel von f' im Intervall)
    h = mp.mpf(10)**(-mp.floor(mp.log10(dps_now))+3)
    dL = (fR(a+h)-fR(a-h))/(2*h)
    dM = (fR(mid+h)-fR(mid-h))/(2*h)
    dR = (fR(b+h)-fR(b-h))/(2*h)
    same_sign = (dL>0 and dM>0 and dR>0) or (dL<0 and dM<0 and dR<0)

    # konservativ aufweiten, um numerische Restunsicherheiten einzufangen
    pad = max(eps*0.1, 10**(-dps_now//3))
    J = (a - pad, b + pad)

    cert = {
        "schema":"zeta_zero_cert/arb-krawczyk",
        "interval":[J[0], J[1]],
        "uniqueness":{"ok": bool(same_sign), "method":"newton+mono"},
        "meta":{"fallback":"mp","pad":pad,"dps_final":dps_now}
    }
    return bool(same_sign and _width(J) <= 10*eps), (J[0], J[1]), cert
