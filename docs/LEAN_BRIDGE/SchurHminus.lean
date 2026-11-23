import Mathlib

/-!
# Schur(H₋) = (q/P)·G_korr — kernel-geprüft (Satz-Schluss aus den Einträgen)

Aus den kernel-verifizierten Einträgen: (H₋)₁₁ = 2βq; H₁₂·H₂₁ = (iqk)(−iqk)
= q²k² (reell-positiv — der i-Faktor kippt das Vorzeichen NICHT, geprüft in
GbetaMonotone-Folge via schur_structure-Rechnung); (H₋)₂₂ =
q((T−2β)(1+k)+k′)/P (Hm22_entry). Damit

  Schur(H₋) = (H₋)₂₂ − H₁₂H₂₁/(H₋)₁₁
            = q·((T−2β)(1+k) + k′ − P·k²/(2β))/P
            = (q/P)·G_korr,   G_korr = (T−2β)(1+k) + k′ − P·k²/(2β).

Die Doc-Struktur (Schur = (q/P)·G_β mit MINUS P·k²/(2β)) stimmt in der
Vorzeichen-Struktur; nur der T-Koeffizient ist T−2β (nicht T−4β).
-/

/-- **Schur(H₋) komplett**: mit (H₋)₁₁ = 2βq, dem kernel-geprüften
Produkt H₁₂H₂₁ = q²k² (reell-positiv) und (H₋)₂₂ = q((T−2β)(1+k)+k′)/P ist
das Schur-Komplement (q/P)·G_korr mit der KORRIGIERTEN G_korr
(T−2β statt Doc-T−4β). -/
theorem schur_Hminus {q β P T kk kk' H11 H12 H21 H22 : ℝ}
    (hβ : 0 < β) (hP : 0 < P) (hq : q ≠ 0)
    (h11 : H11 = 2 * β * q)
    (hprod : H12 * H21 = q * q * kk * kk)
    (h22 : H22 = q * ((T - 2 * β) * (1 + kk) + kk') / P) :
    H22 - H12 * H21 / H11
      = q * ((T - 2 * β) * (1 + kk) + kk' - P * kk ^ 2 / (2 * β)) / P := by
  rw [h11, hprod, h22]
  field_simp

#print axioms schur_Hminus
