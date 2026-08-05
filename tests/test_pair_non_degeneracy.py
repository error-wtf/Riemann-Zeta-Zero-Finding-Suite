import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.pair_non_degeneracy import non_degeneracy_status, contradiction_if_null_image
from src.hedenmalm.domain_theorem import domain_theorem_ledger


def test_non_degeneracy_status_is_assumption_labelled():
    assert non_degeneracy_status().status == "PROVED_UNDER_SOURCE_ASYMPTOTIC"
    assert contradiction_if_null_image()["status"].startswith("CONTRADICTION")


def test_positive_pair_and_rh_conclusion_remain_open():
    statuses = {item.name: item.status for item in domain_theorem_ledger()}
    assert statuses["POSITIVE_PAIR_FORM"] == "OPEN"
    assert statuses["RH_CONCLUSION"] == "OPEN"
