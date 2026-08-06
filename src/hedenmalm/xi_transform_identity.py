"""Ledger for the Xi/Fourier normalization obligation."""
from __future__ import annotations


def xi_transform_status() -> dict[str, str]:
    return {
        "integral": "I(alpha)=int_R exp(i*alpha*x)*theta(x) dx",
        "source_factor": "1 after x=log(t), dt/t=dx",
        "identity": "PROVED_FROM_SOURCE_MELLIN_FORMULA",
        "nonzero_factor": "PROVED (factor 1)",
        "source_equation": "Xi(alpha)=int_0^infty Theta00(i*t^2)*t^(i*alpha) dt/t",
    }


def require_xi_normalization(factor):
    if factor is None or factor == 0:
        raise RuntimeError("Xi transform normalization is not certified")
    return factor


def canonical_xi_factor() -> int:
    """The source Mellin formula becomes a plain Fourier integral in x=log t."""
    return 1
