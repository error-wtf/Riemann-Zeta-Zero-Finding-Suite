"""Fail-closed global n=1 remainder majorants for z >= 8."""
from __future__ import annotations

from fractions import Fraction
from math import comb


def stirling2(n: int, k: int) -> int:
    if n == k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return k * stirling2(n - 1, k) + stirling2(n - 1, k - 1)


def C_constant(j: int, m: int) -> Fraction:
    total = Fraction(0)
    for k in range(j + 1):
        inner = Fraction(16, 13)
        for ell in range(1, k + 1):
            inner += Fraction(comb(k, ell) * 3 * (2**ell) * __import__('math').factorial(ell), 13 ** (ell + 1))
        total += (2**j) * stirling2(j, k) * (8 ** (k + m)) * inner
    return total


def ratio_bounds(precision: int = 256):
    from flint import arb, ctx
    old = ctx.prec
    try:
        ctx.prec = precision
        out = {}
        for j in range(4):
            p = 4 + 2*j
            rho = (arb(3)/2)**p * (-arb(40)).exp()
            if rho.lower() < 0 or rho.upper() >= 1:
                raise RuntimeError("far remainder ratio is not certified in [0,1)")
            out[p] = rho
        return out
    finally:
        ctx.prec = old


def global_remainder_bounds(precision: int = 256):
    from flint import arb, ctx
    old = ctx.prec
    try:
        ctx.prec = precision
        ratios = ratio_bounds(precision)
        bounds = {}
        for j in range(4):
            p = 4 + 2*j
            series = (arb(2)**p * (-arb(24)).exp()) / (1 - ratios[p])
            bounds[j] = arb(C_constant(j, 0).numerator) / C_constant(j, 0).denominator * series
        weighted = {}
        for j in range(1, 3):
            p = 4 + 2*j
            series = (arb(2)**p * (-arb(24)).exp()) / (1 - ratios[p])
            c = C_constant(j, 1)
            weighted[j] = arb(c.numerator) / c.denominator * series
        b0,b1,b2,b3 = (bounds[j] for j in range(4))
        l1 = b1
        l2 = b2 + b1*b1
        l3 = b3 + 3*b1*b2 + 2*b1**3
        return {"B_R": b0, "B_DR": b1, "B_D2R": b2, "B_D3R": b3,
                "weighted_B_DR": weighted[1], "weighted_B_D2R": weighted[2],
                "L1_bound": l1, "L2_bound": l2, "L3_bound": l3,
                "ratio_bounds": ratios}
    finally:
        ctx.prec = old
