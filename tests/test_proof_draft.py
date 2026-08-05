import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.hedenmalm.energy_identity import multiplier_residual
from src.hedenmalm.proof_draft import energy_proof_ledger, unconditional_ready


def test_canonical_multiplier_reduction_is_symbolically_exact():
    x = sp.symbols("x", real=True)
    h = sp.Function("h")(x)
    Phi = sp.Function("Phi")(x)
    a = h * sp.exp(2 * Phi) / sp.diff(Phi, x, 2)
    expected = sp.exp(2 * Phi) * sp.diff(h, x)
    assert sp.simplify(multiplier_residual(a, Phi, x) - expected) == 0


def test_conditional_draft_remains_fail_closed():
    ledger = energy_proof_ledger()
    assert ledger["LEMMA_1_WEIGHTED_IDENTITY"].startswith("PROVED")
    assert ledger["LEMMA_2_CANONICAL_REDUCTION"] == "PROVED_ALGEBRAICALLY"
    assert ledger["LEMMA_3_GLOBAL_COEFFICIENT_BOUNDS"] == "OPEN"
    assert ledger["LEMMA_4_ENDPOINT_AND_TRACE_CONTROL"] == "OPEN"
    assert ledger["LEMMA_5_VOLTERRA_COERCIVITY"] == "OPEN"
    assert ledger["RH_CONCLUSION"] == "CONDITIONAL_ONLY"
    assert unconditional_ready() is False
