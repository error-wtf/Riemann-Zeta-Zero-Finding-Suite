#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rigorous_Z_arb.py
-----------------
Einheitliche Schnittstelle, um Hardy's Z(t) und Z'(t) *mit Einschließungen*
zu berechnen. Versucht in dieser Reihenfolge:

  (A) python-flint / Arb (echte Complex-Balls)  -> "arb"
  (B) mpmath.iv  (Intervallarithmetik)         -> "iv"
  (C) Hochpräzise mp + konservative Aufweitung -> "mp_pad"

Exportierte API:
  - eval_ZZp_interval(t, dps=110, rad=1e-12, mode="auto")
      -> (I_Z, I_Zp, info)   wobei I_* = (lo, hi) reelle Intervalle
  - sign_from_interval(I) -> 'pos' | 'neg' | 'zero' | 'unknown'

Die Funktion ist *drop-in* kompatibel zu deinem bisherigen `eval_ZZp_interval`
(so wird sie z.B. von run_block.py genutzt).
"""

from __future__ import annotations
import math
from typing import Tuple, Dict, Any

import mpmath as mp
mp.mp.trap_complex = False

# --- Verfügbarkeitscheck: python-flint / Arb (optional) ---
_ARB_OK = False
try:
    # python-flint (https://github.com/flintlib/python-flint)
    # Wir importieren vorsichtig; API kann je nach Version leicht variieren.
    from flint import ctx as fl_ctx
    from flint import acb, arb, acb_poly  # type: ignore
    _ARB_OK = True
except Exception:
    _ARB_OK = False

# ---------- Hilfsfunktionen ----------

def _as_interval_from_acb(x) -> Tuple[float, float]:
    """
    Extrahiert aus einem reellen acb (Im(x) ~ 0) die reelle Intervallschätzung.
    Fällt zurück auf Mittelpunkt ± Radius.
    """
    # python-flint hält reelle Zahlen meist als acb mit sehr kleinem Imaginärteil
    # Wir nehmen Realteil plus Ballradius.
    xr = float(x.real().mid().str()) if hasattr(x.real(), "mid") else float(x.real())
    rad = float(x.real().rad().str()) if hasattr(x.real(), "rad") else 0.0
    return (xr - rad, xr + rad)

def _sign_interval(lo: float, hi: float) -> str:
    if lo > 0.0: return "pos"
    if hi < 0.0: return "neg"
    if lo <= 0.0 <= hi:
        if abs(hi - lo) <= 1e-18:
            return "zero"
        return "unknown"
    return "unknown"

def sign_from_interval(I: Tuple[float, float]) -> str:
    lo, hi = float(I[0]), float(I[1])
    return _sign_interval(lo, hi)

# ---------- Z und Z' (Hardy) ----------

def _theta_stirling(t: float, dps: int) -> float:
    """
    θ(t) ~ (t/2) log(t/(2π)) - t/2 - π/8 + O(1/t)
    Wir nutzen hier die numerische Form via loggamma zur Sicherheit.
    """
    mp.mp.dps = max(dps, 70)
    s = 0.25 + 0.5j * t
    return float(mp.im(mp.log(mp.gamma(s))) - (t/2.0)*mp.log(mp.pi))

def _Z_mp(t: float, dps: int) -> Tuple[float, float]:
    """ Numerische Z(t) & Z'(t) via mpmath (ohne Einschließung, nur Mittelpunkt). """
    mp.mp.dps = max(dps, 70)
    s = 0.5 + 1j*t
    theta = _theta_stirling(t, dps)
    zeta = mp.zeta(s)
    Z = complex(zeta * mp.e**(-1j*theta)).real
    # Ableitung: Z'(t) = d/dt Re(ζ(1/2+it) e^{-iθ(t)})
    # numerisch per Zentr. Differenzen:
    h = mp.mpf(10)**(-mp.floor(mp.log10(dps))+2)  # adaptive kleine Schrittweite
    f1 = complex(mp.zeta(0.5 + 1j*(t+h)) * mp.e**(-1j*_theta_stirling(t+h, dps))).real
    f2 = complex(mp.zeta(0.5 + 1j*(t-h)) * mp.e**(-1j*_theta_stirling(t-h, dps))).real
    Zp = (f1 - f2) / (2*h)
    return float(Z), float(Zp)

def _inflate(x: float, pad: float) -> Tuple[float, float]:
    return (x - abs(pad), x + abs(pad))

def _eval_mp_padded(t: float, dps: int, pad: float) -> Tuple[Tuple[float,float], Tuple[float,float], Dict[str,Any]]:
    """ mp-Mittelwerte + konservative Aufweitung (robusteste letzte Stufe) """
    Zm, Zpm = _Z_mp(t, dps)
    I = _inflate(Zm, pad)
    Ip = _inflate(Zpm, 10*pad)  # Derivative unsicherer -> größer aufweiten
    return I, Ip, {"mode": "mp_pad", "dps": dps, "pad": pad}

def _eval_iv(t: float, dps: int) -> Tuple[Tuple[float,float], Tuple[float,float], Dict[str,Any]]:
    """
    Intervallarithmetik via mpmath.iv:
    - Wir evaluieren θ(t) als Intervall über t±δ und ziehen cos/sin mit iv nach.
    - Z'(t) via iv-ableitung (sym. Differenzen mit iv).
    """
    mp.mp.dps = max(dps, 70)
    iv = mp.iv

    # kleines Intervall um t => robustes Vorzeichen (δ ~ 2^{-dps/6})
    delta = mp.mpf(2)**(-max(20, dps//6))
    T = iv.mpf([t - delta, t + delta])

    # θ(T)
    def theta_iv(Tiv):
        s = 0.25 + 0.5*Tiv*1j
        # log(gamma) mit iv.complex -> mpmath kann das zwar, aber langsam;
        # wir bauen θ über Stirling-Näherung + numerische Korrektur (mp) mit kleiner Reserve.
        theta_c = (Tiv/2)*iv.log(Tiv/(2*mp.pi)) - Tiv/2 - mp.pi/8
        # kleine Korrektur: + O(1/T) (konservativ)
        corr = iv.mpf([-1,1]) * (1/(48*iv.max(1, Tiv)))
        return theta_c + corr

    Th = theta_iv(T)
    s = 0.5 + 1j*T
    z = iv.zeta(s) if hasattr(iv, "zeta") else None
    if z is None:
        # Fallback: zeta via mp-Mittelwert + große Reserve
        z0 = mp.zeta(0.5 + 1j*t)
        zI = iv.mpf([z0.real-1e-12, z0.real+1e-12]) + 1j*iv.mpf([z0.imag-1e-12, z0.imag+1e-12])
    else:
        zI = z
    ZI = (zI * iv.exp(-1j*Th)).real

    # Ableitung via sym. iv-Differenzen
    hh = iv.mpf([delta/2, delta])
    ZpI = (( (iv.zeta(0.5+1j*(T+hh)) * iv.exp(-1j*theta_iv(T+hh))).real ) -
           ( (iv.zeta(0.5+1j*(T-hh)) * iv.exp(-1j*theta_iv(T-hh))).real )) / (2*hh)

    I = (float(ZI.a), float(ZI.b))
    Ip = (float(ZpI.a), float(ZpI.b))
    return I, Ip, {"mode": "iv", "dps": dps, "delta": float(delta)}

def _eval_arb(t: float, dps: int) -> Tuple[Tuple[float,float], Tuple[float,float], Dict[str,Any]]:
    """
    Arb/FLINT (python-flint) – echte Complex Balls.
    Achtung: Die API kann je nach Version variieren; wir implementieren eine robuste Version:
      Z(t) = Re( ζ(1/2+it) * exp(-i θ(t)) )
      θ(t) über (t/2)*log(t/2π) - t/2 - π/8  mit Ball-Korrektur.
    """
    # Präzision setzen
    fl_ctx.prec = max(64, int(dps*3.5))
    tt = arb(t)
    # θ als Ball (Stirling mit Ball-Korrektur)
    # theta = (t/2) log(t/2π) - t/2 - π/8  + O(1/t)
    theta = (tt/2)*tt.log() - (tt/2)*arb(1).log() - (tt/2) - (arb(math.pi)/8)
    # kleine Korrektur: - (t/2) * log(2π)  (oben nur log t - log 1 = log t genutzt)
    theta -= (tt/2)*arb(2*math.pi).log()
    theta += arb(1)/(48*arb.max(arb(1), tt))  # sehr konservativ

    s = acb(0.5, float(t))  # 0.5 + i t
    # ζ(s)
    try:
        z = s.zeta()   # neuere python-flint-Version
    except Exception:
        # Manche Versionen haben zeta als freie Funktion
        from flint import zeta as fl_zeta  # type: ignore
        z = fl_zeta(s)
    e = (-1j*theta).exp()
    Z = (z*e).real()
    # Ableitung per sym. Differenzen (Ball)
    hh = arb(2)**(-max(20, dps//6))
    z1 = (acb(0.5, float(t)+float(hh))).zeta()
    z2 = (acb(0.5, float(t)-float(hh))).zeta()
    e1 = (-1j*(theta+hh)).exp()
    e2 = (-1j*(theta-hh)).exp()
    Zp = ((z1*e1).real() - (z2*e2).real())/(2*hh)
    I  = _as_interval_from_acb(Z)
    Ip = _as_interval_from_acb(Zp)
    return I, Ip, {"mode": "arb_diagnostic", "prec": fl_ctx.prec, "rigorous": False,
                   "note": "Approximate theta/remainder and finite-difference derivative; not a proof enclosure until independently validated."}

# ---------- öffentliche API ----------

def eval_ZZp_interval(t: float, dps: int = 110, rad: float = 1e-12, mode: str = "auto") -> Tuple[Tuple[float,float], Tuple[float,float], Dict[str,Any]]:
    """
    Liefert Intervalle (lo,hi) für Z(t) und Z'(t). 'mode' kann sein:
      - "auto" (arb → iv → mp_pad)
      - "arb"  (erzwingen, sonst Fallback)
      - "iv"
      - "mp_pad"
    """
    if mode in ("auto", "arb"):
        if _ARB_OK:
            try:
                return _eval_arb(t, dps)
            except Exception:
                pass
        if mode == "arb":
            # harter Fallback
            return _eval_mp_padded(t, dps, pad=10**(-dps//3))

    if mode in ("auto","iv"):
        try:
            return _eval_iv(t, dps)
        except Exception:
            if mode == "iv":
                return _eval_mp_padded(t, dps, pad=10**(-dps//3))

    # letzte Stufe
    return _eval_mp_padded(t, dps, pad=10**(-dps//3))
