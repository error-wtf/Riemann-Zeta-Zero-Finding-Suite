import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.polynomial_certificate import conservative_polynomial_certificate, conservative_polynomials


def test_conservative_q_polynomials_are_exactly_positive():
    qm, qp = conservative_polynomials()
    assert qm.degree() == 6 and qp.degree() == 6
    result = conservative_polynomial_certificate()
    assert result["q_minus"]["root_count"] == 0
    assert result["q_plus"]["root_count"] == 0
    assert result["q_minus"]["positive_if_no_roots"]
    assert result["q_plus"]["positive_if_no_roots"]
    assert result["status"] == "PROVED_EXACT_RATIONAL"
