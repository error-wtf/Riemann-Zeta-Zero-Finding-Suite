import Mathlib

/-!
# G_β-Korrektur-Folgerung (kernel-geprüft, 7. Modul)

Doc/Python benutzen in den Positivitäts-Zertifikaten die G_β mit T−4β
(`residue_identification.py:83,89`, `scaled_left_correction.py:26`).
Kernel-geprüft ist T−2β richtig (Hm22_entry). Die korrekte G ist

    G_korr = G_doc + 2β(1+k),

also für β > 0, k > −1 STRENG GRÖSSER als die zertifizierte Funktion —
zertifizierte Positivität von G_doc impliziert die von G_korr (monotone
Absicherung: die Zertifikate bleiben gültig und sind konservativ).
-/

/-- Die Identität: korrekte G_β = Doc-G_β + 2β(1+k). -/
theorem G_korr_identity (T β P kk kk' : ℝ) :
    (1 + kk) * (T - 2 * β) + kk' - P * kk ^ 2 / (2 * β)
      = (1 + kk) * (T - 4 * β) + kk' - P * kk ^ 2 / (2 * β) + 2 * β * (1 + kk) := by
  ring

/-- **Monotone Absicherung**: ist die Doc-G_β (T−4β-Form, kleiner) positiv
zertifiziert, so ist die korrekte G_β (T−2β-Form) ebenfalls positiv. -/
theorem G_korr_positive {T β P kk kk' : ℝ} (hβ : 0 < β) (hkk : -1 < kk)
    (hpos : 0 < (1 + kk) * (T - 4 * β) + kk' - P * kk ^ 2 / (2 * β)) :
    0 < (1 + kk) * (T - 2 * β) + kk' - P * kk ^ 2 / (2 * β) := by
  have h1 : (1 + kk) * (T - 2 * β) + kk' - P * kk ^ 2 / (2 * β)
      = (1 + kk) * (T - 4 * β) + kk' - P * kk ^ 2 / (2 * β) + 2 * β * (1 + kk) := by
    ring
  have h2 : 0 < 2 * β * (1 + kk) := by
    have hp : (0:ℝ) < 2 * β := by linarith
    have hk : (0:ℝ) < 1 + kk := by linarith
    positivity
  linarith

#print axioms G_korr_identity
#print axioms G_korr_positive
