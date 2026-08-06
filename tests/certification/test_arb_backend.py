import pytest

pytest.importorskip("flint")

from src.certification.arb_backend import certified_exp_ball, definitely_positive


def test_outward_rounded_arb_smoke():
    value = certified_exp_ball("0.1 +/- 0.0001", precision=256)
    assert definitely_positive(value)
    assert value.lower() > 1
