"""Rational-coefficient Gaussian tail majorants for Theta derivatives."""
from __future__ import annotations
from fractions import Fraction


def q_coefficients(a: Fraction, order: int) -> tuple[Fraction, ...]:
    coeff = [Fraction(1)]
    for _ in range(order):
        out = [Fraction(0)] * (len(coeff) + 1)
        for j, c in enumerate(coeff):
            out[j] += (a + 2*j) * c
            out[j+1] -= 2*c
        coeff = out
    return tuple(coeff)


def validate_ratio(rho):
    if rho.lower() < 0 or rho.upper() >= 1:
        raise ValueError("tail ratio is not certified in [0,1)")


def gaussian_tail_bound(n0, lam, power, rho):
    validate_ratio(rho)
    return (n0**power * (-lam * n0**2).exp()) / (1-rho)


def tail_bound(x_ball, order, terms=30, precision=256):
    try:
        from flint import arb, ctx
    except ImportError as exc:
        raise RuntimeError("install requirements-certify.txt") from exc
    ctx.prec = precision
    x = arb(x_ball); y = (2*x).exp(); ym = y.lower(); yp = y.upper(); pi=arb.pi()
    lam = pi * ym; n0=arb(terms+1); total=arb(0)
    for a,p,pref in ((Fraction(9,2),4,2*pi**2*(arb(9)*x.upper()/2).exp()),
                     (Fraction(5,2),2,3*pi*(arb(5)*x.upper()/2).exp())):
        for j,q in enumerate(q_coefficients(a,order)):
            if not q: continue
            power=p+2*j
            rho=((n0+1)/n0)**power * (-lam*(2*n0+1)).exp()
            total += (arb(abs(q.numerator))/abs(q.denominator)) * pref * (pi*yp)**j * gaussian_tail_bound(n0,lam,power,rho)
    return total
