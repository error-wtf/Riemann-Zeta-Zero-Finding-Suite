"""Fast integrity checks for the numerical claims made by the suite.

These checks deliberately distinguish a numerically accurate evaluation from a
formal proof certificate.  They are safe to run in CI and do not scan a large
height interval.
"""

import mpmath as mp

import common
from rigorous_Z_arb import eval_ZZp_interval
from certify_zero import certify_zero_unique


def test_complete_siegel_path_matches_exact_zeta():
    mp.mp.dps = 60
    for t in (60, 100, 250):
        assert abs(common.Z(t) - common.Z_exact(t)) < mp.mpf("1e-45")
        assert abs(common.Z_rs(t) - common.Z_exact(t)) < mp.mpf("1e-45")


def test_main_sum_is_explicitly_not_the_complete_path():
    # At this height the leading sum is intentionally only an approximation.
    assert abs(common.Z_rs_main_sum(100) - common.Z_exact(100)) > mp.mpf("1e-4")


def test_diagnostic_metadata_never_claims_formal_rigor():
    _, _, info = eval_ZZp_interval(30.0, dps=60)
    assert info.get("rigorous") is not True
    ok, _, cert = certify_zero_unique(14.13, 14.14, eps=1e-8, dps=60)
    assert isinstance(ok, bool)
    assert cert.get("rigorous") is False
    assert "rigor_note" in cert


if __name__ == "__main__":
    test_complete_siegel_path_matches_exact_zeta()
    test_main_sum_is_explicitly_not_the_complete_path()
    test_diagnostic_metadata_never_claims_formal_rigor()
    print("OK: complete Z path, approximation boundary and certificate semantics verified")
