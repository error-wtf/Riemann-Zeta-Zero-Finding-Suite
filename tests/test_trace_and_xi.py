import pytest

from src.hedenmalm.trace_theorem import (
    certify_gaussian_weighted_integrability,
    certified_weighted_theta_l1_bound,
    require_weighted_l1_majorant,
    trace_theorem_status,
    weighted_theta_l1_bound_formula,
)
from src.hedenmalm.xi_transform_identity import canonical_xi_factor, require_xi_normalization, xi_transform_status


def test_trace_certificate_fails_closed_without_majorant():
    with pytest.raises(RuntimeError):
        require_weighted_l1_majorant(None)
    assert trace_theorem_status()["trace_existence"].startswith("PROVED_UNDER_SOURCE_PROFILE")


def test_xi_normalization_fails_closed_until_derived():
    assert require_xi_normalization(canonical_xi_factor()) == 1
    assert xi_transform_status()["identity"].startswith("PROVED")
    with pytest.raises(RuntimeError):
        require_xi_normalization(0)


def test_finite_certified_majorant_is_accepted():
    assert require_weighted_l1_majorant(1.0)


def test_gaussian_trace_condition_is_strictly_inside_strip():
    assert certify_gaussian_weighted_integrability(0.25, 1.0)
    with pytest.raises(RuntimeError):
        certify_gaussian_weighted_integrability(0.5, 1.0)
    with pytest.raises(RuntimeError):
        certify_gaussian_weighted_integrability(0.25, 0.0)


def test_weighted_theta_bound_formula_is_explicit():
    formula = weighted_theta_l1_bound_formula()
    assert formula["domain"] == "|beta| < 1/2"
    assert "16*exp(-3*pi)" in formula["source_bound"]


def test_trace_status_records_analytic_source_bound():
    status = trace_theorem_status()
    assert status["weighted_theta_integrability"].startswith("PROVED_ANALYTICALLY")
    assert status["volterra_absolute_convergence"].startswith("PROVED_ANALYTICALLY")


def test_certified_weighted_theta_bound_if_arb_available():
    flint = pytest.importorskip("flint")
    result = certified_weighted_theta_l1_bound(flint.arb("0.25"), 128)
    assert result["bound"].lower() > 0
    with pytest.raises(RuntimeError):
        certified_weighted_theta_l1_bound(flint.arb("0.5"), 128)
