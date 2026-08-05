"""P0 domain-theorem ledger for ``L_Phi``.

The general ODE statement is exact under its stated local-absolute-continuity
assumptions.  Theta-specific asymptotics and closed-range estimates remain
open until the source-faithful profile is supplied.
"""

from __future__ import annotations

from dataclasses import dataclass
import sympy as sp


@dataclass(frozen=True)
class TheoremStatus:
    name: str
    status: str
    statement: str
    assumptions: tuple[str, ...]
    dependency: str


def nullspace_theorem() -> TheoremStatus:
    return TheoremStatus(
        "NULLSPACE",
        "PROVED_UNDER_ASSUMPTIONS",
        "L_Phi u=0 implies u=C exp(-Phi) locally",
        ("Phi is locally absolutely continuous", "u is locally absolutely continuous"),
        "domain membership of exp(-Phi) is profile-dependent",
    )


def nullspace_solution(Phi: sp.Expr) -> sp.Expr:
    """Return the exact formal solution of the first-order null equation."""
    return sp.exp(-Phi)


def domain_theorem_ledger() -> tuple[TheoremStatus, ...]:
    return (
        TheoremStatus(
            "PROFILE_IDENTITY", "PROVED_FROM_SOURCE",
            "phi_00(t)=-log(Theta_00(i t^2)), Phi(x)=phi_00(exp(x))",
            ("published source normalization",), "profile_identification.py",
        ),
        nullspace_theorem(),
        TheoremStatus(
            "THETA_ASYMPTOTICS", "PROVED_FROM_SOURCE",
            "source profile phi_00=-log(Theta_00(i t^2)) has stated endpoint asymptotic",
            ("source normalization and published Theta series",), "profile_identification.py",
        ),
        TheoremStatus(
            "ADJOINT_DOMAIN", "PROVED_UNDER_ASSUMPTIONS",
            "maximal weak-derivative domain for the formal first-order expression",
            ("real locally integrable Phi'", "L2 reference measure", "endpoint Green limits are controlled"),
            "adjoint_domains.py",
        ),
        TheoremStatus(
            "CLOSED_RANGE", "OPEN",
            "ran(L_Phi) is closed on the selected Hilbert domain",
            ("a coercive estimate or equivalent Fredholm argument",), "inverse_domain.py",
        ),
        TheoremStatus(
            "POSITIVE_PAIR_FORM", "OPEN",
            "a positive source-independent form makes (L D,L) symmetric",
            ("positive definite Hilbert form", "all source eigenfunctions admissible"),
            "inner_products and pair_boundary_form",
        ),
        TheoremStatus(
            "LOCAL_WEIGHT_PAIR", "PROVED_UNDER_ASSUMPTIONS",
            "the complete pair has no positive scalar local weight for nonconstant Phi'",
            ("compactly supported core", "real smooth Phi", "w=exp(W)>0", "standard weighted L2"),
            "inner_products/local_pair_no_go.py",
        ),
        TheoremStatus(
            "NONDEGENERACY", "PROVED_UNDER_SOURCE_ASYMPTOTIC",
            "Xi(alpha)=0 and u_alpha nonzero imply L_phi00 u_alpha != 0",
            ("published Theta asymptotic", "source boundary solution"),
            "pair_non_degeneracy.py",
        ),
        TheoremStatus(
            "RH_CONCLUSION", "OPEN",
            "positive pair symmetry would force alpha=conjugate(alpha)",
            ("POSITIVE_PAIR_FORM", "NONDEGENERACY"), "not yet applicable",
        ),
        TheoremStatus(
            "PRIME_MULTIPLIER_LIMIT", "REGULARIZED_ONLY",
            "prime-shift multiplier has a finite regularized cutoff; infinite limit is open",
            ("sigma>0 regularization",), "prime_multiplier_limit.py",
        ),
        TheoremStatus(
            "GLOBAL_MULTIPLIER_NO_GO", "CONTRADICTION_FOUND_UNDER_ASSUMPTIONS",
            "global positive q(D) with Q=L^*GL and the Theta null vector forces Q=0",
            ("strong D-commutation", "Theta in form domain", "Xi nonzero almost everywhere"),
            "global_multiplier_no_go.py",
        ),
        TheoremStatus(
            "NULLSPACE_COMPATIBILITY", "OPEN",
            "Q must annihilate ker(L) or an explicit quotient must be declared",
            ("kernel of L", "positive Q"), "nullspace_compatibility.py",
        ),
        TheoremStatus(
            "PAIR_DEFECT", "PATTERN_ONLY",
            "finite-basis defect can be measured but not promoted to an operator theorem",
            ("finite matrices",), "pair_defect.py",
        ),
        TheoremStatus(
            "P0_ENERGY_IDENTITY", "PROVED_FORMALLY_UNDER_BOUNDARY_ASSUMPTIONS",
            "weighted energy identity with multiplier residual R_a",
            ("pair equation", "real smooth a", "convergent integrals", "vanishing boundary terms"),
            "energy_identity.py",
        ),
        TheoremStatus(
            "P2_COERCIVE_MULTIPLIER", "OPEN",
            "positive a_b makes the energy residual nonpositive for Im(alpha)>0",
            ("Theta derivative sign bounds",), "energy_identity.py",
        ),
        TheoremStatus(
            "P1_SIGN_STRUCTURE", "NUMERICALLY_SUPPORTED_ONLY",
            "sampled Phi derivative signs and multiplier residuals",
            ("finite precision samples",), "theta_derivative_diagnostics.py",
        ),
        TheoremStatus(
            "P3_BOUNDARY_VANISHING", "OPEN",
            "all Green terms vanish for the actual complex-alpha boundary solution",
            ("weighted endpoint estimates",), "energy_proof_guards.py",
        ),
        TheoremStatus(
            "P2_CANONICAL_MULTIPLIER", "OPEN",
            "h_b reduction yields a positive multiplier with controlled endpoints",
            ("Phi''>0 globally", "S_Phi sign bounds", "negative-half-axis control"),
            "canonical_multiplier.py",
        ),
        TheoremStatus(
            "RIGOROUS_ENERGY_BOUNDS", "OPEN",
            "validated interval bounds for Phi'', S_Phi and Volterra boundary terms",
            ("outward-rounded interval backend",), "rigorous_energy_bounds.py",
        ),
    )


def require_proved(status: TheoremStatus) -> None:
    if status.status not in {"PROVED_FORMALLY", "PROVED_UNDER_ASSUMPTIONS"}:
        raise ValueError(f"{status.name} is not proved: {status.status}")
