"""Status guard for the final Volterra-Hardy coercivity lemma."""

from __future__ import annotations


def volterra_coercivity_status(*, phi2_positive: bool, s_positive_right: bool, half_axis_control: bool, boundary_terms: bool) -> dict[str, object]:
    ready = phi2_positive and s_positive_right and half_axis_control and boundary_terms
    return {
        "status": "PROVED_UNDER_ASSUMPTIONS" if ready else "OPEN",
        "missing": tuple(name for name, ok in (
            ("Phi''>0 globally", phi2_positive),
            ("S_Phi>0 on x>0", s_positive_right),
            ("negative half-axis controlled", half_axis_control),
            ("canonical multiplier boundary terms vanish", boundary_terms),
        ) if not ok),
    }
