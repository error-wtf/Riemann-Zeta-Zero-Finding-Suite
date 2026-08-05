import sys
from pathlib import Path

import sympy as sp
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.theta_asymptotics import null_vector_integrability, even_profile_check
from src.hedenmalm.adjoint_domains import formal_adjoint_domains
from src.hedenmalm.closures import graph_closure_specs
from src.hedenmalm.inverse_domain import inverse_domain_status, require_inverse_domain
from src.hedenmalm.pair_boundary_form import pair_boundary_status


def test_asymptotic_null_vector_diagnostic():
    x = sp.symbols("x", real=True)
    result = null_vector_integrability(x**2, x)
    assert result["status"] == "PROVED_FORMALLY"
    assert even_profile_check(x**2, x) == sp.true


def test_domain_and_closure_statuses_are_explicit():
    assert formal_adjoint_domains()["L_phi"].status == "PROVED_UNDER_ASSUMPTIONS"
    assert graph_closure_specs()["L_phi"].status == "PROVED_UNDER_ASSUMPTIONS"
    assert inverse_domain_status().status == "OPEN"
    assert pair_boundary_status()["status"] == "OPEN"


def test_inverse_guard_fails_closed():
    with pytest.raises(ValueError):
        require_inverse_domain(kernel_removed=False, range_closed=False)
    with pytest.raises(ValueError):
        require_inverse_domain(kernel_removed=True, range_closed=False)
