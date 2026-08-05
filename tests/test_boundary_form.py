import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.boundary_form import dilation_green_form, weighted_L_green_form, pair_status
from src.hedenmalm.operator_domains import minimal_domains


def test_dilation_green_form_vanishes_on_compact_support_proxy():
    x = sp.symbols("x", real=True)
    u = x * (1 - x)
    v = x**2 * (1 - x)
    # Both test functions vanish at the finite proxy endpoints.
    assert sp.simplify(dilation_green_form(u, v, x, 0, 1)) == 0


def test_weighted_L_boundary_and_volume_condition_are_visible():
    x = sp.symbols("x", real=True)
    phi = x**2
    W = 2 * phi
    result = weighted_L_green_form(x * (1 - x), x**2 * (1 - x), phi, W, x, 0, 1)
    assert sp.simplify(result["boundary"]) == 0
    assert sp.simplify(result["volume_residual"]) == 0


def test_domain_status_does_not_claim_self_adjointness():
    assert minimal_domains()["D_x"].closure_status == "not closed"
    assert pair_status()["self_adjointness"] == "unproven"
