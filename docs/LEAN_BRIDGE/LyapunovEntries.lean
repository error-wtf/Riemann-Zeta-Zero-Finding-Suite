import Mathlib

/-!
# §4-Eintrag-Identitäten (Lyapunov-Matrix H₊) — kernel-geprüft

Das Manuskript (RH_PROOF_CANDIDATE_COMPLETE.md §4) definiert mit
q = e^{2Φ−2βx} (q' = 2(Φ'−β)q), P' = Φ''', J₊ = q·diag(−1, 1/P),
A = [[−Φ', i], [−iΦ'', −iα]]:

  H₊ = J₊' + A*J₊ + J₊A  =  q·diag(2β, T/P),  T = 2Φ'P − Φ'''.

Hier werden die beiden Diagonal-Einträge als unabhängige Lean-Sätze geprüft
(Ableitungswerte als Hypothesen-Schnittstelle, wie in EnergyReduction.lean).

**BEFUND (23.11., Bingsi):** Der (1,1)-Eintrag stimmt exakt. Der (2,2)-
Eintrag ergibt nach Ring-Rechnung q·(2Φ'P − 2βP − Φ''')/P² — gegenüber der
Doc-Formel q·(2Φ'P − Φ''')/P² fehlt dort der Term −2βq/P. Übereinstimmung
nur, wenn T := (2Φ'−2β)P − Φ''' gemeint ist (Tippfehler-Kandidat im Doc)
oder die P-Definition früher im Dokument anders ist. Offen markiert — kein
Fertig-Urteil, aber Lean-reproduzierbare Kette.
-/

/-- **(1,1)-Eintrag**: dJ₁₁ + conj(A₁₁)·J₁₁ + J₁₁·A₁₁ = 2β·q
(mit J₁₁ = −q, dJ₁₁ = −q', q' = 2(Φ'−β)q, A₁₁ = −Φ', Φ' reell).
Die Terme −q' + 2qΦ' kürzen zu 2βq. -/
theorem H11_entry (q φ' β q' J11 dJ11 A11 : ℝ)
    (hJ : J11 = -q) (hdJ : dJ11 = -q')
    (hq' : q' = 2 * (φ' - β) * q) (hA : A11 = -φ') :
    dJ11 + A11 * J11 + J11 * A11 = 2 * β * q := by
  rw [hdJ, hA, hJ, hq']
  ring

/-- **Kreuzterme heben im (2,2)-Eintrag**: (A*J₊)₂₂ + (J₊A)₂₂
= conj(−iα)·(q/P) + (q/P)·(−iα) = iα·(q/P) − iα·(q/P) = 0. -/
theorem H22_cross (q P α : ℂ) :
    (Complex.I * α) * (q / P) + (q / P) * (-(Complex.I * α)) = 0 := by
  ring

/-- **(2,2)-Eintrag**: dJ₂₂ = (q/P)' = q'/P − q·Φ'''/P² (mit q' = 2(Φ'−β)q,
P' = Φ''') ergibt — nach Hebung der α-Kreuzterme —
  q·(2Φ'P − 2βP − Φ''')/P²,
NICHT q·(2Φ'P − Φ''')/P² wie in der Doc-Formel behauptet. -/
theorem H22_entry (q φ' β P Φ3 q' J22 dJ22 : ℝ)
    (hJ : J22 = q / P) (hdJ : dJ22 = q' / P - q * Φ3 / P ^ 2)
    (hq' : q' = 2 * (φ' - β) * q) :
    dJ22 = q * (2 * φ' * P - 2 * β * P - Φ3) / P ^ 2 := by
  rw [hdJ, hq']
  field_simp

#print axioms H11_entry
#print axioms H22_cross
#print axioms H22_entry
