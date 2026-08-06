"""Ledger for the Xi/Fourier normalization obligation."""
from __future__ import annotations


def xi_transform_status() -> dict[str, str]:
    return {
        "integral": "I(alpha)=int_R exp(i*alpha*x)*theta(x) dx",
        "source_factor": "UNSPECIFIED_UNTIL_SOURCE_NORMALIZATION_IS_DERIVED",
        "identity": "OPEN",
        "nonzero_factor": "OPEN",
    }


def require_xi_normalization(factor):
    if factor is None or factor == 0:
        raise RuntimeError("Xi transform normalization is not certified")
    return factor
