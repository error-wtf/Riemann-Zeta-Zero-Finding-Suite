import pytest

from src.hedenmalm.trace_theorem import require_weighted_l1_majorant, trace_theorem_status
from src.hedenmalm.xi_transform_identity import require_xi_normalization, xi_transform_status


def test_trace_certificate_fails_closed_without_majorant():
    with pytest.raises(RuntimeError):
        require_weighted_l1_majorant(None)
    assert trace_theorem_status()["trace_existence"] == "OPEN"


def test_xi_normalization_fails_closed_until_derived():
    with pytest.raises(RuntimeError):
        require_xi_normalization(None)
    assert xi_transform_status()["identity"] == "OPEN"


def test_finite_certified_majorant_is_accepted():
    assert require_weighted_l1_majorant(1.0)
