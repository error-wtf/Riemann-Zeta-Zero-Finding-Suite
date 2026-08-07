from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_license_split_and_authorship_files_exist():
    for name in (
        "LICENSE.md", "LICENSE-CODE", "LICENSE-DOCUMENTATION", "AUTHORS.md",
        "NOTICE.md", "CITATION.cff",
    ):
        assert (ROOT / name).is_file()


def test_human_rights_holders_and_ai_credit_are_unambiguous():
    authors = (ROOT / "AUTHORS.md").read_text()
    notice = (ROOT / "NOTICE.md").read_text()
    assert "Carmen Wrede" in authors and "Lino Casu" in authors
    assert "Bingsi AI" in authors and "AI research collaborator" in authors
    assert "legal copyright holder" in authors
    assert "Bingsi AI" in notice


def test_code_license_has_no_general_use_grant():
    code = (ROOT / "LICENSE-CODE").read_text()
    assert "ALL RIGHTS RESERVED" in code
    assert "No permission is granted" in code
    assert "prior written permission" in code


def test_documentation_license_contains_unmodified_acsl_core():
    text = (ROOT / "LICENSE-DOCUMENTATION").read_text()
    official = (ROOT / "ANTI-CAPITALIST SOFTWARE LICENSE (v 1.4)").read_text()
    assert "ANTI-CAPITALIST SOFTWARE LICENSE (v 1.4)" in text
    assert "The User is one of the following" in text
    assert "law enforcement or military" in text
    assert "All rights not expressly granted" in text
    assert "Copyright © 2026 Carmen Wrede and Lino Casu" in official


def test_public_scientific_status_is_not_rh_proved():
    notice = (ROOT / "NOTICE.md").read_text()
    assert "CANDIDATE_PROOF_PENDING_TRACE_CLOSURE_AND_INDEPENDENT_REVIEW" in notice
    assert "RH = PROVED" not in notice
