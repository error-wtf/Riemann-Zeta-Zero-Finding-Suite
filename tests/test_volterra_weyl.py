from src.hedenmalm.volterra_weyl import (
    left_solution_integrand,
    right_solution_integrand,
    volterra_ode_residual,
    volterra_weyl_status,
)


def test_endpoint_integrands_have_opposite_signs():
    theta = lambda y: 2.0
    left = left_solution_integrand(0.2 + 0.1j, 0.3, -0.4, theta)
    right = right_solution_integrand(0.2 + 0.1j, 0.3, -0.4, theta)
    assert abs(left + right) < 1e-12


def test_ode_residual_is_zero_for_formal_derivative():
    alpha = 0.4 + 0.2j
    u = 1.2 - 0.3j
    theta = 0.7 + 0.1j
    derivative = theta - 1j * alpha * u
    assert abs(volterra_ode_residual(alpha, 0.0, u, theta, derivative)) < 1e-15


def test_open_functional_analytic_status_is_not_upgraded():
    status = volterra_weyl_status()
    assert status["ode"] == "PROVED_ALGEBRAIC"
    assert status["trace_existence"] == "OPEN"
    assert status["xi_transform_identity"] == "OPEN"
