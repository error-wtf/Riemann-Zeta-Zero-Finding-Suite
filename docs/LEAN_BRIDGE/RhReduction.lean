import Mathlib

/-!
# RH-Reduktion in kompakter Form (eigene Version, 23.11.2026)

Reduktion: Nichtverschwinden von ζ auf Re(s) > 1/2 impliziert: jede Null von ζ
liegt auf der kritischen Linie Re(s) = 1/2 oder ist eine negative ganze Zahl
(die geraden davon sind die trivialen Nullstellen).

Struktur:
* Re(s) > 1/2: direkt durch die Hypothese.
* s = -n: sofort `CritOrTrivial` (negative ganze Zahl).
* Sonst Re(s) < 1/2: Funktionalgleichung bei `1 - s`:
  ζ(1-(1-s)) = 2·(2π)^{-(1-s)}·Γ(1-s)·cos(π(1-s)/2)·ζ(1-s);
  mit ζ(s) = 0 folgt ζ(1-s) = 0 trotz Re(1-s) > 1/2 — Widerspruch.
  Der Vorfaktor verschwindet nie: Γ-Positivität; der cos-Fall s = -2k, k ≥ 1,
  kollidiert mit Re(s) < 1/2; s = 0 und s = 1 sind ausgeschlossen.
-/

/-- Auf der kritischen Linie oder negative ganze Zahl. -/
def CritOrTrivial (s : ℂ) : Prop := s.re = 1 / 2 ∨ ∃ n : ℕ, s = -(n : ℂ)

/-- Der Vorfaktor der Funktionalgleichung bei `1 - s` ist nie null. -/
theorem prefactor_one_sub_ne_zero {s : ℂ} (hlt : s.re < 1 / 2) (hs0 : s ≠ 0)
    (hneg : ∀ n : ℕ, s ≠ -(n : ℂ)) :
    (2 : ℂ) * (2 * (Real.pi : ℂ)) ^ (-(1 - s)) * Complex.Gamma (1 - s)
      * Complex.cos ((Real.pi : ℂ) * (1 - s) / 2) ≠ 0 := by
  have hpi : (Real.pi : ℂ) ≠ 0 := by exact_mod_cast Real.pi_ne_zero
  have h2pi : (2 : ℂ) * (2 * (Real.pi : ℂ)) ^ (-(1 - s)) ≠ 0 :=
    mul_ne_zero two_ne_zero
      (Complex.cpow_ne_zero_iff.2 (Or.inl (mul_ne_zero two_ne_zero hpi)))
  have hG : Complex.Gamma (1 - s) ≠ 0 :=
    Complex.Gamma_ne_zero_of_re_pos (by rw [Complex.sub_re, Complex.one_re]; linarith)
  have hcos : Complex.cos ((Real.pi : ℂ) * (1 - s) / 2) ≠ 0 := by
    rw [Ne, Complex.cos_eq_zero_iff]
    rintro ⟨k, hk⟩
    have h3 : ((1 - s) - (2 * (k : ℂ) + 1)) * (Real.pi : ℂ) = 0 := by
      linear_combination 2 * hk
    rcases mul_eq_zero.1 h3 with h | h
    · have hsk : s = -2 * (k : ℂ) := by linear_combination -h
      have hre : s.re = -2 * (k : ℝ) := by simp [hsk, Complex.mul_re]
      rcases lt_trichotomy k 0 with hk0 | hk0 | hk0
      · have hk1 : (k : ℝ) ≤ -1 := by exact_mod_cast (show k ≤ -1 by omega)
        rw [hre] at hlt
        linarith
      · exact hs0 (by simp [hsk, hk0])
      · exact hneg (2 * k.toNat) (by
          have e0 : k.toNat = k := Int.toNat_of_nonneg (by omega : (0 : ℤ) ≤ k)
          have e1 : ((2 * k.toNat : ℕ) : ℤ) = 2 * k := by omega
          have e2 : ((2 * k.toNat : ℕ) : ℂ) = ((2 * k : ℤ) : ℂ) := by exact_mod_cast e1
          rw [hsk, e2]
          push_cast
          ring)
    · exact hpi h
  exact mul_ne_zero (mul_ne_zero h2pi hG) hcos

/-- **Haupttheorem**: ζ ≠ 0 auf `Re(s) > 1/2` (ohne den Pol `s = 1`) ⇒ jede
Null von ζ liegt auf der kritischen Linie oder ist eine negative ganze Zahl. -/
theorem rh_from_right_nonvanishing
    (h : ∀ s : ℂ, 1 / 2 < s.re → s ≠ 1 → riemannZeta s ≠ 0)
    (s : ℂ) (hs : riemannZeta s = 0) (hs1 : s ≠ 1) : CritOrTrivial s := by
  rcases lt_trichotomy s.re (1 / 2) with hlt | heq | hgt
  · rcases em (∃ n : ℕ, s = -(n : ℂ)) with hex | hnex
    · exact Or.inr hex
    · exfalso
      have hs0 : s ≠ 0 := by
        rintro rfl
        rw [riemannZeta_zero] at hs
        norm_num at hs
      have hnat : ∀ n : ℕ, (1 - s) ≠ -(n : ℂ) := by
        intro n hc
        have hr := congrArg Complex.re hc
        rw [Complex.sub_re, Complex.one_re, Complex.neg_re, Complex.natCast_re] at hr
        have hge : (0 : ℝ) ≤ n := n.cast_nonneg
        linarith
      have h1s1 : (1 - s) ≠ 1 := by
        intro hc
        exact hs0 (by linear_combination -hc)
      have key := riemannZeta_one_sub (s := 1 - s) hnat h1s1
      rw [show (1 : ℂ) - (1 - s) = s from by ring, hs] at key
      have ht : 1 / 2 < (1 - s).re := by
        rw [Complex.sub_re, Complex.one_re]; linarith
      exact absurd key.symm
        (mul_ne_zero (prefactor_one_sub_ne_zero hlt hs0
          (fun n hc => hnex ⟨n, hc⟩))
          (h (1 - s) ht h1s1))
  · exact Or.inl heq
  · exact absurd hs (h s hgt hs1)

#print axioms prefactor_one_sub_ne_zero
#print axioms rh_from_right_nonvanishing
