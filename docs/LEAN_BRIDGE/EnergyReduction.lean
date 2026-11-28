import Mathlib

/-!
# Energie-Reduktion (Lemma 2-Kern aus ENERGY_PROOF_DRAFT.md) in Lean

Die algebraische Kaskade der Energie-Seite unseres Kandidaten:
Mit `a_h = h·e^{2Φ}/Φ''` gilt `a_h·Φ'' = h·e^{2Φ}` (Produktterm `H`), und die
Produkt-Ableitung expandiert zu `(a_h·Φ'')' = e^{2Φ}·h' + 2·Φ'·H`. In der
Residuum-Definition `R_a = (a·Φ'')' − 2·a·Φ'·Φ''` heben sich die beiden
`2·Φ'·H`-Terme exakt, und es bleibt

  `R_{a_h} = e^{2Φ}·h'`.

Die Ableitungswerte `(a_h·Φ'')'` und die Kettenregel-Expansion sind hier
Hypothesen (`dAP`, Kettensatz = Mathlib-Standard; die analytische Substanz der
Grenzen bleibt wie im Draft bei den Zertifikaten).
-/

/-- **Energie-Reduktion (Lemma 2, algebraischer Kern)**: mit `a·Φ'' = H`
(`H = h·e^{2Φ}`) und der Produkt-Ableitungs-Expansion
`(a·Φ'')' = e^{2Φ}·h' + 2·Φ'·H` ist das Residuum `R_a = e^{2Φ}·h'`. -/
theorem energy_reduction {A P dAP H E h' φ' : ℝ}
    (hprod : A * P = H)
    (hdAP : dAP = E * h' + 2 * φ' * H) :
    dAP - 2 * A * P * φ' = E * h' := by
  calc
    dAP - 2 * A * P * φ' = (E * h' + 2 * φ' * H) - 2 * A * P * φ' := by rw [hdAP]
    _ = E * h' + 2 * φ' * H - 2 * H * φ' := by linear_combination -(2 * φ') * hprod
    _ = E * h' := by ring

/-- **Triviale Fortsetzung** (Lemma 2, zweiter Teil): die transformierte
Gewichts-Identität `S_Φ·|w'|² + 2β·|w|² = 0` bei `S_Φ ≥ 0` spaltet in
beide Terme = 0 (positiver Summand + nichtnegativer Summand + Summe null). -/
theorem weighted_split {SΦ w' w : ℝ} (hS : 0 ≤ SΦ)
    (hcoef : SΦ * w' ^ 2 + 2 * w ^ 2 = 0) : SΦ * w' ^ 2 = 0 ∧ 2 * w ^ 2 = 0 := by
  have h1 : 0 ≤ SΦ * w' ^ 2 := by positivity
  have h2 : 0 ≤ 2 * w ^ 2 := by positivity
  refine ⟨?_, ?_⟩ <;> linarith

#print axioms energy_reduction
#print axioms weighted_split
