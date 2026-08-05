import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.inner_products.local_pair_no_go import local_pair_conditions, source_profile_conclusion


def test_complete_local_pair_conditions_are_explicit():
    result = local_pair_conditions()
    assert result.status == "PROVED_FORMALLY_UNDER_LOCAL_WEIGHT_ANSATZ"
    assert "W'=0" in result.conditions


def test_source_profile_local_no_go_is_scoped():
    result = source_profile_conclusion()
    assert result["status"].startswith("CONTRADICTION")
    assert "nonlocal" in result["next"]
