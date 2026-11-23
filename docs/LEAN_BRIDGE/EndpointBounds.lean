import Mathlib

/-!
# Endpoint-Bounds (Doc §5) — kernel-geprüft

Die Doc-Kette (§5): Zertifikate geben m = 8 − B_DR > 1/2 und p₀ = inf P > 0;
dann |M₊(R)| ≤ C_{α,β}·e^{−2βR} mit

  C_{α,β} = 1/(m−β)² + (1/p₀)·(1 + m/(m−β) + |α|/(m−β))²  < ∞.

Hier kernel-geprüft: (a) C_{α,β} > 0 für m > β > 0, p₀ > 0; (b) die
exponentielle Dominanz — |M(R)| ≤ C·e^{−2βR} für R ≥ log(C/ε)/(2β) erzwingt
|M(R)| ≤ ε (das Verschwinden am Rande, das die Green-Limina braucht).
-/

/-- **C_{α,β} ist positiv**: für m > β > 0 und p₀ > 0 gilt
1/(m−β)² + (1/p₀)(1 + m/(m−β) + |α|/(m−β))² > 0 (beide Summanden > 0). -/
theorem endpoint_C_positive (m β α p₀ : ℝ) (hm : m > β) (hβ : β > 0) (hp₀ : p₀ > 0) :
    0 < 1 / (m - β) ^ 2 + 1 / p₀ * (1 + m / (m - β) + |α| / (m - β)) ^ 2 := by
  have h1 : (0:ℝ) < m - β := by linarith
  have h2 : (0:ℝ) < 1 / (m - β) ^ 2 :=
    div_pos one_pos (pow_pos (sub_pos.mpr hm) 2)
  have hpos : (0:ℝ) < 1 + m / (m - β) + |α| / (m - β) := by
    have hq : (0:ℝ) < m / (m - β) := div_pos (by linarith) h1
    have hq2 : (0:ℝ) ≤ |α| / (m - β) :=
      div_nonneg (abs_nonneg α) h1.le
    linarith
  have h3 : (0:ℝ) < 1 / p₀ * (1 + m / (m - β) + |α| / (m - β)) ^ 2 :=
    mul_pos (div_pos one_pos hp₀) (pow_pos hpos 2)
  linarith

/-- **Exponentielle Dominanz**: |M(R)| ≤ C·e^{−2βR} für
R ≥ log(C/ε)/(2β) erzwingt |M(R)| ≤ ε. -/
theorem exp_bound_small {M C R β ε : ℝ} (hC : 0 < C) (hβ : 0 < β) (hε : 0 < ε)
    (hR : Real.log (C / ε) / (2 * β) ≤ R)
    (hbound : |M| ≤ C * Real.exp (-(2 * β * R))) : |M| ≤ ε := by
  have hkey : Real.log (C / ε) ≤ 2 * β * R := by
    rw [div_le_iff₀ (by linarith : (0:ℝ) < 2 * β)] at hR
    exact hR.trans_eq (mul_comm R (2 * β))
  have h2 : C / ε ≤ Real.exp (2 * β * R) := by
    rw [← Real.exp_log (div_pos hC hε)]
    exact Real.exp_le_exp.mpr hkey
  have h3 : Real.exp (-(2 * β * R)) ≤ ε / C := by
    rw [Real.exp_neg, ← one_div]
    have hE : ε / C = 1 / (C / ε) := by field_simp
    rw [hE]
    exact (one_div_le_one_div (Real.exp_pos (2 * β * R)) (div_pos hC hε)).mpr h2
  calc |M| ≤ C * Real.exp (-(2 * β * R)) := hbound
    _ ≤ C * (ε / C) := mul_le_mul_of_nonneg_left h3 hC.le
    _ = ε := by field_simp

#print axioms endpoint_C_positive
#print axioms exp_bound_small
