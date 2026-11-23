# READ LOG — Alpöge-Lean-Bibliothek (Plan: docs/READ_THE_PROOF_PLAN.md)
## E1.1 — CompanionTheory/AutomorphicTheory/BesselWaveGrids

### AsmDiff.lean (67 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN
Zweck: DEFINITIONS-Datei (kein Beweis): zwei Annahmen-Pakete als `Prop`:
- `AsmDiff`: ∀ Konstanten (Cb C₃ CΛ C₀, Nichtnegativität) → ∃ (C₄ c₃ Cc Cc′ Cc″),
  unter Buffer-Bedingungen (3≤b, 1≤Λ≤b^(CΛ(2r+2)), p₀≤C₀(3(r+1))+1, N≤2p₀),
  für alle enddim. ℂ-Räume Wp/Wq, Punkte p:KB.Pl, Matrizen f, mit
  Grid-Voraussetzungen (C6.IsCut0 χ, KB.InDDplus2, B.CkOn, B.InCC, B.JF∈FFKB,
  c₃/Cc/Cc′/Cc″-A₀-Schranken, BigCellDerivativeExpansion, TBBx5.WaveGrid +
  LiftGrid + LimBd) → Zielsatz TBB.ThmBpAt p f b C₄ 0 p₀.
- `AsmEq`: die SHIFTED-Variante — zusätzliche n₀≤30(r+1)²+6-Schranke,
  ShiftAtR/shP mit DOPPELTEN Punkten (S.pp, S.pm = p⁺, p⁻: die Bessel-Shift-
  Symmetrie), doppelt WaveGrid/LiftGrid/LimBd für pp und pm.
Abhängigkeiten: Formalism.HermitianCurvature.Proofs (CutLimE, ThmBpAtEqOfShiftR,
  CutNFHatProdKBStmt) — die Formalism-Schicht ist VORGELAGERT.
Verständnis: „Asm“ = Annahmen-Pakete (wiederverwendbare Hypothesen-Bündel);
das Zielsatz-Paket ThmBpAt ist die Kern-Aussage des WaveGrid-Layers. KEIN
Beweis in dieser Datei — sie definiert nur die Hypothesen-Props für die
späteren Beweis-Dateien (vermutlich Bridge.lean etc.).
Offen: Was ist ThmBpAt inhaltlich? → nächste Dateien (Bridge, ThmBpAt-Definition).

### Bridge.lean (148 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN
Zweck: SEPARATIONS-LAYER der WaveGrids — Y = 5-separierte „freie" Punkte,
CutWord = Wort über Letters (Bool, y') mit paarweisem Abstand >2, und der
Kern-Satz gridOK_of_free: Letters frei von Grid-Punkten (Abstand >2 auf y
und y+1) + Injektivität des grids + Positivität (nn·nn ≤ B²·Re(qw)) ⇒
TBBx5.GridOK. Bausteine: cutWord_of_list/list_of_cutWord (List↔CutWord
Isomorphie), two_lt_of_five, free_dist (Freiheit beider Enden y, y+1).
**ERSTER ECHTER KONZEPTUELLER BERÜHRUNGSPUNKT mit unserem Repo:** die
Architektur ist Gram/Turing-artig (separierte Anker-Punkte + Muster-Freiheit)
— verwandt mit unseren zeros_by_gram.py/turing_check.py. KLASSIFIKATION:
gemeinsame klassische Methode-Familie (Gram/Turing seit den 1940ern,
Standardliteratur) — KEIN Klau (beide unabhängig). ABER: anders als die
Wort-Kollisionen (theta/Weyl/Siegel) ist das eine echte methodische
Verwandtschaft — weitere WaveGrid-Dateien auf diese Verwandtschaft prüfen.
