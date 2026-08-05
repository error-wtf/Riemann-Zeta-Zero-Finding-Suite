import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.inner_products.exact_pair_reduction import pair_reduction
from src.inner_products.commuting_multiplier import prime_shift_multiplier, multiplier_status
from src.inner_products.weak_factorization import weak_factorization_status, require_weak_factorization
from src.inner_products.kernel_nullspace_obstruction import nullspace_obstruction_status
from src.hedenmalm.mellin_fourier_model import resolvent_family
from src.debranges.positive_gram_kernel import gram_matrix, gram_status


def test_pair_reduction_and_positive_multiplier():
    assert pair_reduction().commuting_condition == "D Q = Q D"
    assert prime_shift_multiplier(1.2, [(2, 1)], [0.5], epsilon=0.1) >= 0.1
    assert multiplier_status([0.5], epsilon=0.1)["strictly_positive"]


def test_factorization_and_kernel_obstruction_fail_closed():
    assert weak_factorization_status(kernel_removed=False, range_closed=False)["status"] == "OPEN"
    with pytest.raises(ValueError):
        require_weak_factorization(kernel_removed=False, range_closed=True)
    assert nullspace_obstruction_status(q_annihilates_kernel=False, strict_q=True)["obstruction"]


def test_null_free_resolvent_and_positive_gram_are_diagnostics():
    assert resolvent_family()["status"] if isinstance(resolvent_family(), dict) else resolvent_family().status == "PATTERN_ONLY"
    grid = np.linspace(-5, 5, 401)
    F = lambda x: np.exp(-x * x)
    G = gram_matrix(F, [1j, 2j], grid)
    assert gram_status(G)["positive_on_grid"]
