import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.rigorous_energy_bounds import backend_status, certification_plan, proof_readiness


def test_certification_is_fail_closed_without_arb():
    plan = certification_plan(compact_radius=2.0, compact_cells=32)
    assert len(plan) == 3
    assert proof_readiness()["status"] == "OPEN"
    if backend_status()["status"] == "none":
        assert all(item.status == "OPEN" for item in plan)
