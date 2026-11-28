import Mathlib

/-!
# Volterra-Differenzidentität (Kern des eigenen RH-Kandidaten, §2) in Lean

Unser Manuskript (docs/RH_PROOF_CANDIDATE_COMPLETE.md, §2) definiert die beiden
Volterra-Zustände

  u₋(x) =  e^{−iαx} · ∫_{(−∞,x]} e^{iαy} θ(y) dy
  u₊(x) = −e^{−iαx} · ∫_{[x,∞)} e^{iαy} θ(y) dy

und gewinnt aus der Differenz

  u₋(x) − u₊(x) = e^{−iαx} · Ξ(α)                    (Differenzidentität)

die zentrale Konsequenz: bei Ξ(α) = 0 sind beide Zustände als Funktionen gleich
(`volterra_states_equal_at_zero` unten — die Erfüllung des §6-Arguments).
Die Integrierbarkeit des vollen Integranden ist die analytische Substanz
(analytischer Gaussian-Majorant, |Im α| < 1/2) und geht als Hypothese ein.
-/

open MeasureTheory Complex

noncomputable section

/-- Der linke Volterra-Zustand. -/
def volterraUminus (θ : ℝ → ℂ) (α : ℂ) (x : ℝ) : ℂ :=
  Complex.exp (-Complex.I * α * x) * ∫ (y : ℝ) in Set.Iic x, Complex.exp (Complex.I * α * y) * θ y

/-- Der rechte Volterra-Zustand. -/
def volterraUplus (θ : ℝ → ℂ) (α : ℂ) (x : ℝ) : ℂ :=
  -Complex.exp (-Complex.I * α * x) * ∫ (y : ℝ) in Set.Ioi x, Complex.exp (Complex.I * α * y) * θ y

/-- **Volterra-Differenzidentität**: `u₋(x) − u₊(x) = e^{−iαx} · ∫ e^{iαy}θ(y)dy`
(das volle Integral = Ξ(α) unter der Quell-Normierung). -/
theorem volterra_difference_identity {θ : ℝ → ℂ} {α : ℂ}
    (hI : Integrable (fun (y : ℝ) => Complex.exp (Complex.I * α * y) * θ y) volume) (x : ℝ) :
    volterraUminus θ α x - volterraUplus θ α x
      = Complex.exp (-Complex.I * α * x)
        * ∫ y : ℝ, Complex.exp (Complex.I * α * y) * θ y := by
  have hIic : MeasurableSet (Set.Iic x) := measurableSet_Iic
  have hcompl : (Set.Iic x)ᶜ = Set.Ioi x := Set.compl_Iic
  have hsplit := setIntegral_union (Set.Iic_disjoint_Ioi (le_rfl : x ≤ x)) measurableSet_Ioi
    hI.integrableOn hI.integrableOn
  rw [Set.Iic_union_Ioi] at hsplit
  rw [← setIntegral_univ, volterraUminus, volterraUplus, hsplit]
  ring

/-- **Ξ-Null-Folgerung** (§6, Schritt 5 des Trace-Ledgers): bei `Ξ(α) = 0` sind die
beiden Volterra-Zustände als Funktionen gleich. -/
theorem volterra_states_equal_at_zero {θ : ℝ → ℂ} {α : ℂ}
    (hI : Integrable (fun (y : ℝ) => Complex.exp (Complex.I * α * y) * θ y) volume)
    (hzero : ∫ y : ℝ, Complex.exp (Complex.I * α * y) * θ y = 0) (x : ℝ) :
    volterraUminus θ α x = volterraUplus θ α x := by
  have h := volterra_difference_identity hI x
  rw [hzero, mul_zero] at h
  exact sub_eq_zero.mp h

#print axioms volterra_difference_identity
#print axioms volterra_states_equal_at_zero
