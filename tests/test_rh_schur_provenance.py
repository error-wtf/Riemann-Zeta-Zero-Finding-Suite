"""Independent exact regression for the reflected-left Weyl/Schur identity.

This checks finite symbolic algebra only. It does not certify RH, global
positivity, the Green-limit argument, or Lean compilation.
"""
import sympy as sp


def test_reflected_left_residual_and_schur_from_primitive_matrices():
    # Derive from A_-, J_- and the product rule, rather than importing the
    # implementation under test as an oracle.
    p, P, Pp, eta, beta, k, kp, q = sp.symbols(
        "p P Pp eta beta k kp q", real=True
    )
    alpha = eta + sp.I * beta
    A_minus = sp.Matrix([[-p, sp.I], [-sp.I * P, sp.I * alpha]])
    J_minus = q * sp.diag(-1, (1 + k) / P)
    # q' = 2(p-beta)q, P' = Pp and k' = kp.
    J_prime = q * sp.diag(
        -2 * (p - beta),
        2 * (p - beta) * (1 + k) / P + kp / P - (1 + k) * Pp / P**2,
    )
    H = J_prime + A_minus.conjugate().T * J_minus + J_minus * A_minus
    T = (2 * p * P - Pp) / P
    expected = q * sp.Matrix([
        [2 * beta, sp.I * k],
        [-sp.I * k, ((1 + k) * (T - 4 * beta) + kp) / P],
    ])
    assert (H - expected).applyfunc(sp.cancel) == sp.zeros(2)

    schur = H[1, 1] - H[1, 0] * H[0, 1] / H[0, 0]
    target = q / P * ((1 + k) * (T - 4 * beta) + kp - P * k**2 / (2 * beta))
    assert sp.cancel(schur - target) == 0

    # Negative control: 2*beta is the wrong coefficient for this A_-, J_-.
    wrong = q / P * ((1 + k) * (T - 2 * beta) + kp - P * k**2 / (2 * beta))
    assert sp.cancel(schur - wrong + 2 * beta * q * (1 + k) / P) == 0
    assert sp.cancel(schur - wrong) != 0


def test_plus_volterra_product_rule_sign():
    # E'=-i*a*E; Iplus'=-theta/E; uplus=-E*Iplus.
    # Pure product-rule check; existence of integrals is a separate theorem.
    a, E, Iplus, theta = sp.symbols("a E Iplus theta")
    uplus = -E * Iplus
    derivative = -((-sp.I * a * E) * Iplus + E * (-theta / E))
    assert sp.cancel(derivative + sp.I * a * uplus - theta) == 0
