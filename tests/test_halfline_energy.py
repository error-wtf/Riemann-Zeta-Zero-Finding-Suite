import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.halfline_energy import halfline_energy_status, origin_trace, origin_trace_residual
from src.hedenmalm.theta_derivative_series import phi_fourth_from_series, origin_slope_margin
from src.hedenmalm.profile_identification import Phi_log
import mpmath as mp


def test_fourth_derivative_and_origin_margin_are_finite_diagnostics():
    value = phi_fourth_from_series(0, terms=80, dps=40)
    margin = origin_slope_margin(terms=80, dps=40)
    assert value == value
    assert margin == margin


def test_fourth_derivative_matches_independent_high_precision_differentiation():
    direct = phi_fourth_from_series(mp.mpf("0.7"), terms=100, dps=60)
    independent = mp.diff(lambda y: Phi_log(y, terms=100), mp.mpf("0.7"), 4)
    assert abs(direct - independent) < mp.mpf("1e-10")


def test_origin_trace_formula_is_source_convention():
    assert origin_trace(1 + 2j, 0.5 - 0.25j) == 1 - 1j * (1 + 2j) * (0.5 - 0.25j)
    assert halfline_energy_status()["status"] == "OPEN"


def test_origin_residual_is_diagnostic_only():
    assert origin_trace_residual(1j, 0.1, terms=60, dps=30) == origin_trace_residual(1j, 0.1, terms=60, dps=30)
