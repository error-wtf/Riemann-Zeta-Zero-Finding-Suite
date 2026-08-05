import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.log_operator import L_phi, null_vector, pair_equation
from src.inner_products.local_weight_no_go import local_weight_condition, pair_probe_status
from src.inner_products.prime_shift_kernel import kernel_audit, prime_shift_trace, prime_kernel_candidate
from src.audit.noncircularity import audit_definition_inputs


def test_log_operator_identities_and_null_vector():
    x = sp.symbols("x", real=True)
    phi = sp.cosh(x)
    u = null_vector(phi)
    assert sp.simplify(L_phi(u, phi, x)) == 0
    assert sp.simplify(pair_equation(sp.exp(-x**2), sp.symbols("alpha"), phi, x)) != 0


def test_local_weight_condition_is_explicit_not_pair_proof():
    x = sp.symbols("x", real=True)
    phi = sp.cosh(x)
    result = local_weight_condition(phi, 2 * phi, x)
    assert result["residual"] == 0
    assert result["pair_status"] == "undecided_without_inverse_domain"
    assert pair_probe_status(phi, x)["status"] == "diagnostic_only"


def test_prime_trace_and_kernel_status():
    assert np.isfinite(prime_shift_trace(17.0, prime_limit=30, repeats=4))
    A = np.diag([1.0, 2.0]).astype(complex)
    G = np.eye(2, dtype=complex)
    audit = kernel_audit(A, G)
    assert audit.status == "PATTERN_ONLY"
    assert audit.intertwining_residual == 0.0
    candidate = prime_kernel_candidate(prime_limit=11, repeats=2, modes=3)
    candidate_audit = kernel_audit(np.zeros_like(candidate), candidate)
    assert candidate_audit.min_eigenvalue > 0
    assert candidate_audit.status == "PATTERN_ONLY"


def test_non_circularity_fails_closed():
    assert audit_definition_inputs({"theta_profile": "published"}).passed
    assert not audit_definition_inputs({"gamma_n": [14.1]}).passed
