import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.inner_products.global_multiplier_no_go import global_multiplier_no_go, no_go_integral_identity


def test_global_multiplier_no_go_is_assumption_scoped():
    result = global_multiplier_no_go()
    assert result.status.startswith("CONTRADICTION")
    assert result.conclusion.startswith("Q=0")
    assert "de Branges" in result.escape_routes[-1]
    assert "q=0" in no_go_integral_identity()
