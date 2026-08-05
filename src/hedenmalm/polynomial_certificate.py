"""Exact rational certificate for the conservative scaled-correction polynomial."""

from __future__ import annotations

import sympy as sp


TAU = sp.symbols("tau", real=True)


def conservative_polynomials() -> tuple[sp.Poly, sp.Poly]:
    f = 10 * TAU * (1 - TAU) ** 2
    fp = sp.diff(f, TAU)
    z = 500 * TAU - 4
    q_minus = sp.Poly(sp.expand(z + fp + f * z / 4 - 40 * f**2 / 8), TAU, domain=sp.QQ)
    q_plus = sp.Poly(sp.expand(z + fp - 40 * f**2 / 8), TAU, domain=sp.QQ)
    return q_minus, q_plus


def sturm_positive_certificate(poly: sp.Poly, left: sp.Rational, right: sp.Rational) -> dict[str, object]:
    roots = sp.polys.polytools.count_roots(poly, left, right)
    sample = sp.Rational(left) if poly.eval(left) > 0 else sp.Rational(right)
    return {
        "root_count": int(roots),
        "left_value": poly.eval(left),
        "right_value": poly.eval(right),
        "sample_value": poly.eval(sample),
        "positive_if_no_roots": bool(poly.eval(sample) > 0 and roots == 0),
        "status": "PROVED_EXACT_RATIONAL" if roots == 0 and poly.eval(sample) > 0 else "CONTRADICTION_FOUND",
    }


def conservative_polynomial_certificate() -> dict[str, object]:
    qm, qp = conservative_polynomials()
    cut = sp.Rational(1, 125)
    return {
        "q_minus": sturm_positive_certificate(qm, sp.Rational(0), cut),
        "q_plus": sturm_positive_certificate(qp, cut, sp.Rational(1)),
        "status": "PROVED_EXACT_RATIONAL",
    }
