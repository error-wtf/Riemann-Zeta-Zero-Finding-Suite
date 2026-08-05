"""Log-coordinate diagnostics for the published Hedenmalm-type operator pair."""

from .log_operator import (
    log_coordinate_map,
    dilation_operator,
    L_phi,
    null_vector,
    pair_equation,
    operator_spec,
)
from .operator_domains import minimal_domains
from .boundary_form import dilation_green_form, weighted_L_green_form, pair_status
from .theta_asymptotics import null_vector_integrability, even_profile_check
from .adjoint_domains import formal_adjoint_domains
from .closures import graph_closure_specs
from .inverse_domain import inverse_domain_status, require_inverse_domain
from .pair_boundary_form import pair_boundary_status
from .domain_theorem import domain_theorem_ledger, nullspace_theorem, nullspace_solution
from .profile_identification import phi00, Phi_log, profile_identification_status
from .pair_non_degeneracy import non_degeneracy_status, contradiction_if_null_image
from .boundary_solution import boundary_solution_formula
from .energy_identity import multiplier_residual, weighted_energy_identity, energy_ledger
from .theta_derivative_diagnostics import phi_derivatives, residual_value, diagnostic_status
from .energy_proof_guards import contradiction_status
from .canonical_multiplier import canonical_h, canonical_multiplier, S_phi, canonical_multiplier_status
from .volterra_coercivity import volterra_coercivity_status
from .rigorous_energy_bounds import backend_status, certification_plan, proof_readiness
from .theta_derivative_series import theta_derivative_series, phi_derivatives_from_series, phi_fourth_from_series, origin_slope_margin, s_phi_from_series
from .halfline_energy import origin_trace, origin_trace_residual, halfline_energy_status
from .proof_draft import energy_proof_ledger, unconditional_ready
from .spectral_boundary import boundary_transform_decomposition
from .volterra_closure import spectral_volterra_closure_status, unrestricted_trace_inequality_allowed
from .weyl_volterra_matching import matching_identity, unconditional_weyl_ready
from .weyl_lyapunov import system_matrix, diagonal_flux_matrix, lyapunov_residual, weyl_lyapunov_status
from .hermitian_residual import residual_components, right_halfline_diagonal_residual
from .scaled_left_correction import bump_profile, schur_residual, scaled_correction_status

__all__ = ["log_coordinate_map", "dilation_operator", "L_phi", "null_vector", "pair_equation", "operator_spec", "minimal_domains", "dilation_green_form", "weighted_L_green_form", "pair_status", "null_vector_integrability", "even_profile_check", "formal_adjoint_domains", "graph_closure_specs", "inverse_domain_status", "require_inverse_domain", "pair_boundary_status", "domain_theorem_ledger", "nullspace_theorem", "nullspace_solution", "phi00", "Phi_log", "profile_identification_status", "non_degeneracy_status", "contradiction_if_null_image", "boundary_solution_formula", "multiplier_residual", "weighted_energy_identity", "energy_ledger", "phi_derivatives", "residual_value", "diagnostic_status", "contradiction_status", "canonical_h", "canonical_multiplier", "S_phi", "canonical_multiplier_status", "volterra_coercivity_status", "backend_status", "certification_plan", "proof_readiness", "theta_derivative_series", "phi_derivatives_from_series", "phi_fourth_from_series", "origin_slope_margin", "s_phi_from_series", "origin_trace", "origin_trace_residual", "halfline_energy_status", "energy_proof_ledger", "unconditional_ready", "boundary_transform_decomposition", "spectral_volterra_closure_status", "unrestricted_trace_inequality_allowed", "matching_identity", "unconditional_weyl_ready", "system_matrix", "diagonal_flux_matrix", "lyapunov_residual", "weyl_lyapunov_status", "residual_components", "right_halfline_diagonal_residual", "bump_profile", "schur_residual", "scaled_correction_status"]
