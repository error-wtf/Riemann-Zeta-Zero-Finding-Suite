import json
from pathlib import Path


def test_correction_sturm_artifact_is_exact_and_positive():
    path = Path(__file__).parents[1] / "artifacts/certificates/correction_sturm_q_m500_M40.json"
    data = json.loads(path.read_text())
    assert data["status"] == "PROVED_EXACT_RATIONAL"
    assert data["q_minus"]["root_count"] == 0
    assert data["q_plus"]["root_count"] == 0
    assert data["q_minus"]["positive_if_no_roots"]
    assert data["q_plus"]["positive_if_no_roots"]
