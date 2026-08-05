import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.inner_products.prime_multiplier_limit import multiplier_limit_status
from src.inner_products.quadratic_form import quadratic_form_status
from src.inner_products.nullspace_compatibility import compatibility_status
from src.inner_products.pair_defect import pair_defect, defect_status


def test_prime_limit_is_regularized_only():
    result = multiplier_limit_status(sigma=0.2, prime_limit=30, repeats=3)
    assert result["status"] == "REGULARIZED_ONLY"
    assert result["infinite_limit"] == "OPEN"


def test_quadratic_form_and_nullspace_statuses_are_explicit():
    assert quadratic_form_status(epsilon=1e-6, multiplier_nonnegative=True, domain_declared=False)["status"] == "OPEN"
    assert compatibility_status(q_kernel_zero=False, quotient_declared=False)["status"] == "OPEN"


def test_pair_defect_measurement():
    I = np.eye(2)
    assert pair_defect(I, I, I) == 0.0
    assert defect_status(0.0) == "ZERO_ON_FINITE_BASIS"
