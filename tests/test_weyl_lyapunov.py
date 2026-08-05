import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.weyl_lyapunov import diagonal_flux_matrix, lyapunov_residual, system_matrix, weyl_lyapunov_status


def test_two_component_system_matrix_is_exact():
    x = sp.symbols("x", real=True)
    p, p2, alpha = sp.Function("p")(x), sp.Function("p2")(x), sp.symbols("alpha")
    A = system_matrix(p, p2, alpha)
    assert A[0, 0] == -p
    assert A[0, 1] == sp.I
    assert A[1, 0] == -sp.I * p2
    assert A[1, 1] == -sp.I * alpha


def test_flux_residual_is_exposed_without_positive_claim():
    x = sp.symbols("x", real=True)
    a, p2, alpha = sp.Function("a")(x), sp.Function("p2")(x), sp.symbols("alpha")
    A = system_matrix(sp.Function("p")(x), p2, alpha)
    J = diagonal_flux_matrix(a, p2)
    residual = lyapunov_residual(J, A, x)
    assert residual.shape == (2, 2)
    assert weyl_lyapunov_status()["positive_J_or_H"] == "OPEN"
