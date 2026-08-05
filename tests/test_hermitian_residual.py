import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.hermitian_residual import residual_components


def test_hermitian_residual_component_formula():
    x = sp.symbols("x", real=True)
    r, s, c, d = (sp.Function(name)(x) for name in "rscd")
    p, p2, xi, beta = sp.symbols("p p2 xi beta", real=True)
    out = residual_components(r, s, c, d, p, p2, xi, beta, x)
    assert out[0] == sp.diff(r, x) - 2*p*r + 2*p2*d
    assert out[1] == sp.diff(s, x) + 2*d + 2*beta*s
    assert out[2] == sp.diff(c, x) + (beta-p)*c + xi*d
    assert out[3] == sp.diff(d, x) + (beta-p)*d - xi*c + p2*s + r
