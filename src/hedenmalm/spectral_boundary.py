"""Spectral boundary decomposition for the half-line Volterra solution.

For the even source profile theta, the full Fourier/Mellin condition controls
the cosine transform.  It does not by itself control the sine transform that
enters the one-sided trace w(0).  This module records that distinction
explicitly; it is diagnostic, not a proof of any trace inequality.
"""

from __future__ import annotations


def boundary_transform_decomposition() -> dict[str, str]:
    return {
        "full_transform": "Xi(alpha) proportional to 2*int_0^infty cos(alpha*x)*theta(x) dx",
        "one_sided_trace": "w(0) proportional to int_0^infty exp(i*alpha*x)*theta(x) dx",
        "decomposition": "one_sided = cosine_transform + i*sine_transform",
        "spectral_constraint": "Xi(alpha)=0 removes the cosine part only",
        "uncontrolled_component": "sine_transform",
        "trace_inequality": "OPEN",
        "status": "PROVED_DECOMPOSITION_OPEN_TRACE",
    }
