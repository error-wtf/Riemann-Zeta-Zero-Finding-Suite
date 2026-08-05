"""Positive-inner-product and prime-shift diagnostics."""

from .local_weight_no_go import local_weight_condition, pair_probe_status
from .prime_shift_kernel import prime_shift_trace, kernel_audit
from .local_pair_no_go import local_pair_conditions, source_profile_conclusion
from .prime_multiplier_limit import multiplier_limit_status
from .quadratic_form import quadratic_form_status
from .nullspace_compatibility import compatibility_status
from .pair_defect import pair_defect, defect_status
from .global_multiplier_no_go import global_multiplier_no_go, no_go_integral_identity

__all__ = ["local_weight_condition", "pair_probe_status", "prime_shift_trace", "kernel_audit", "local_pair_conditions", "source_profile_conclusion", "multiplier_limit_status", "quadratic_form_status", "compatibility_status", "pair_defect", "defect_status", "global_multiplier_no_go", "no_go_integral_identity"]
