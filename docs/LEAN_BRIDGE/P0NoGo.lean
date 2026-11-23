import Mathlib

/-!
# P0-No-Go-Kern (eigenes Repo, P0_GLOBAL_MULTIPLIER_NO_GO.md) in Lean

Der Kern des No-Go-Theorems aus `docs/P0_GLOBAL_MULTIPLIER_NO_GO.md`:
Wenn `q ≥ 0` (der Fourier-Multiplikator) stetig ist, das Energie-Integral
`∫ q·f² = 0` existiert und `f` (die Quell-Transformierte, z.B. Ξ) fast überall
nicht verschwindet, dann ist `q ≡ 0` — die globale Übersetzungs-invariante
Multiplikator-Route ist unter den stated assumptions ausgeschlossen.

Beweis-Skizze (eigene Rekonstruktion, 23.11.2026):
* `q·f² ≥ 0` + Integral null ⇒ `q·f² = 0` fast überall.
* `{y | q y ≠ 0} ⊆ {q·f² = 0} ∪ {f = 0}` (denn `q y ≠ 0 ∧ f y ≠ 0 ⇒ q·f² ≠ 0`),
  also `q = 0` fast überall (beide Mengen haben Maß null).
* `q` stetig: eine Stelle mit `q x > 0` erzwingt eine offene Kugel mit
  `q > q x / 2 > 0` — positives Lebesgue-Maß, Widerspruch zur a.e.-Nullheit.
-/

open MeasureTheory

/-- **P0-No-Go-Kern**: `q ≥ 0` stetig, `q·f²` integrierbar mit Integral 0,
und `f ≠ 0` fast überall ⇒ `q ≡ 0` (punktweise überall). -/
theorem no_go_core {q f : ℝ → ℝ} (hq : Continuous q) (hqn : ∀ x, 0 ≤ q x)
    (hf : Continuous f) (hfne : ∀ᵐ x : ℝ, f x ≠ 0)
    (hI : Integrable (fun x => q x * (f x) ^ 2) volume)
    (hzero : ∫ x : ℝ, q x * (f x) ^ 2 = 0) : q = 0 := by
  have hprod : ∀ y : ℝ, 0 ≤ q y * (f y) ^ 2 :=
    fun y => mul_nonneg (hqn y) (sq_nonneg _)
  have hgc : Continuous (fun y => q y * (f y) ^ 2) := hq.mul (hf.pow 2)
  -- Schritt 1: das Produkt ist fast überall null
  have hae' : ∀ᵐ y : ℝ, q y * (f y) ^ 2 = 0 :=
    (integral_eq_zero_iff_of_nonneg hprod hI).1 hzero
  -- Schritt 2: deshalb ist q fast überall null
  have hqae : ∀ᵐ y : ℝ, q y = 0 := by
    filter_upwards [hae', hfne] with y h1 h2
    exact (mul_eq_zero.1 h1).resolve_right (sq_eq_zero_iff.not.2 h2)
  -- Schritt 3: Stetigkeit + a.e.-Nullheit ⇒ punktweise null
  rw [ae_iff] at hqae
  funext x
  by_contra hx
  have hq0 : 0 < q x := lt_of_le_of_ne (hqn x) (Ne.symm hx)
  have hVopen : IsOpen (q ⁻¹' Set.Ioi (q x / 2)) := hq.isOpen_preimage _ isOpen_Ioi
  have hxV : x ∈ q ⁻¹' Set.Ioi (q x / 2) := by
    simp only [Set.mem_preimage, Set.mem_Ioi]
    linarith
  obtain ⟨B, hBpos, hBsub⟩ := Metric.isOpen_iff.1 hVopen x hxV
  have hxB : x ∈ Metric.ball x B := Metric.mem_ball_self hBpos
  have hposB : 0 < volume (Metric.ball x B) :=
    IsOpen.measure_pos volume Metric.isOpen_ball ⟨x, hxB⟩
  have hsub : (Metric.ball x B) ⊆ {y : ℝ | q y ≠ 0} := fun y hy => by
    have hBin := hBsub hy
    simp only [Set.mem_preimage, Set.mem_Ioi] at hBin
    exact ne_of_gt (by linarith)
  have hcontra : 0 < volume {y : ℝ | q y ≠ 0} :=
    lt_of_lt_of_le hposB (measure_mono hsub)
  rw [hqae] at hcontra
  exact lt_irrefl _ hcontra

#print axioms no_go_core
