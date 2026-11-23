import Mathlib

/-!
# H₋-(2,2)-Eintrag (reflektierte Seite) — kernel-geprüft

Doc §4 (J₋ = q·diag(−1, (1+k)/P), A₋ = [[−Φ′, i], [−iΦ″, iα]]): behauptet
(H₋)₂₂ = ((1+k)(T−4β) + k′)/P mit T = (2Φ′P − Φ‴)/P = 2Φ′ − Φ‴/P.

Die kernel-geprüfte Rechnung (dieses Modul) liefert
  (H₋)₂₂ = ((1+k)(T−2β) + k′)/P
— das Doc zählt die β-Korrektur DOPPELT (T−4β statt T−2β). Strukturgleich
zum H₊-Finding (T statt T−2β dort): dort fehlte die β-Korrektur, hier ist
sie doppelt. Beide Male ist die Quelle q′ = 2(Φ′−β)q.
-/

/-- **(H₋)₂₂-Eintrag**: mit J₋₂₂ = q(1+k)/P, dessen Ableitung
(J₋₂₂)′ = q′(1+k)/P + q·k′/P − q(1+k)Φ‴/P² (q′ = 2(Φ′−β)q, P′ = Φ‴) und den
sich exakt hebenden α-Kreuztermen (iα·J₂₂ + J₂₂·(−iα) = 0, vgl. H22_cross)
gilt — in T-Notation (T = 2Φ′ − Φ‴/P):
  (H₋)₂₂ = ((1+k)(T − 2β) + k′)/P. -/
theorem Hm22_entry (q φ' β P Φ3 T kk kk' q' dJ22 : ℝ)
    (hT : T = 2 * φ' - Φ3 / P)
    (hdJ : dJ22 = q' * (1 + kk) / P + q * kk' / P - q * (1 + kk) * Φ3 / P ^ 2)
    (hq' : q' = 2 * (φ' - β) * q) :
    dJ22 = q * ((T - 2 * β) * (1 + kk) + kk') / P := by
  rw [hdJ, hq', hT]
  ring

/-- **Schur-Korrektheit der Struktur**: das Produkt H₁₂H₂₁ = (iqk₀)(−iqk₀)
= q²k₀² — reell und positiv; die Schur-Form H₂₂ − H₁₂H₂₁/H₁₁ ist also
strukturrichtig (nur der T-Koeffizient folgt als T−2β, nicht T−4β). -/
theorem schur_structure (q kk0 : ℂ) :
    (Complex.I * q * kk0) * (-(Complex.I * q * kk0)) = q * kk0 * (q * kk0) := by
  calc (Complex.I * q * kk0) * (-(Complex.I * q * kk0))
      = -(Complex.I * Complex.I) * (q * kk0) * (q * kk0) := by ring
    _ = q * kk0 * (q * kk0) := by rw [Complex.I_mul_I]; ring

#print axioms Hm22_entry
#print axioms schur_structure
