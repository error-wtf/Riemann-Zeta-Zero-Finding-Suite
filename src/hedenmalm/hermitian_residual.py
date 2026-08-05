"""Component form of the Hermitian Weyl-Lyapunov residual."""

from __future__ import annotations

import sympy as sp


def residual_components(r, s, c, d, phi_prime, phi_second, xi, beta, x):
    """Return the real components of J'+A*J+JA for J=[[r,c+id],[c-id,s]]."""
    r11 = sp.diff(r, x) - 2 * phi_prime * r + 2 * phi_second * d
    r22 = sp.diff(s, x) + 2 * d + 2 * beta * s
    real12 = sp.diff(c, x) + (beta - phi_prime) * c + xi * d
    imag12 = sp.diff(d, x) + (beta - phi_prime) * d - xi * c + phi_second * s + r
    return tuple(map(sp.simplify, (r11, r22, real12, imag12)))


def right_halfline_diagonal_residual(phi, phi_prime, phi_second, phi_third, beta, x):
    """Residual entries for a=exp(2*Phi-2*beta*x)/Phi'' (diagnostic)."""
    S = (2 * phi_prime * phi_second - phi_third) / phi_second**2
    factor = sp.exp(2 * phi - 2 * beta * x)
    return (sp.simplify(2 * beta * factor), sp.simplify(S * factor))
