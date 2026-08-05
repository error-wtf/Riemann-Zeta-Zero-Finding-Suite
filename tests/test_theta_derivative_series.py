import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.theta_derivative_series import phi_derivatives_from_series, s_phi_from_series
from src.hedenmalm.canonical_multiplier import S_phi


def test_direct_series_matches_independent_diagnostic():
    p1, p2, p3 = phi_derivatives_from_series(0.7, terms=80, dps=40)
    assert p2 > 0
    assert mp.almosteq(s_phi_from_series(0.7, terms=80, dps=40), S_phi(0.7, dps=40), rel_eps=mp.mpf("1e-20"))
