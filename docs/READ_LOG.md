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

### CfgTie.lean (183 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN
Zweck: Beweise über die Sz.Cfg-Konfiguration (aus Formalism.HermitianCurvature.
StatementSz): cfgPar baut M.Par-Pakete; cfg_v_step (arithmetische Folge mit
Schritt 4·Del); cfg_v_mem (Monotonie-Intervall [v_last, v1]); cfg_b_pos
(Induktion: alle b >= 1 via hgap); cfg_inter (KERN: lam+1/2 <= u(s) UND
u(s+1) <= lam−1/2 — die INTERLACING-Bedingung mit Mindestabstand 1/2).
**VERGLEICH VERTEIFT: cfg_inter ist die formale Interlacing-Struktur, die
exakt der Gram-Punkt-Logik unseres Feldes entspricht (Nullen vs. Testpunkte
verschränken sich mit Mindest-Abstand) — dieselbe klassische Architektur,
nicht nur Wort-Kollision. Seine WaveGrids und unsere Gram/Turing-Zertifikate
sind derselben Methode-Familie zuzurechnen (Guinand-Weil-Tradition).
KEIN Klau (Standardliteratur, beide unabhängig), aber echte strukturelle
Verwandtschaft — der erste nicht-triviale methodische Berührungspunkt.

### NqMovedExample.lean (55+ Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN
Die MATHEMATIK verstanden (nicht nur Struktur): PairData = das Paket
(c>0, g≥1+c, b-Schranken, |λs|≤b, GAP: λ(s+1)+g ≤ λ(s) = monotone
λ-Folge mit Mindestabstand g, |u_l|≤b, pair: Interlacing-Partner auf −Y
existiert). LamData.toPair: die λ-Sequenz erzeugt PairData.
KERN-SATZ pairOK_of_moved: wenn u die Interlacing-Bedingung erfüllt
(cfg_inter-Form: λ(s)+1/2 ≤ u(s) ∧ u(s+1) ≤ λ(s)−1/2) und v nur an
EINER Stelle l von u abweicht (x zwischen u_l und v_l), dann
interlacingt auch v — mit EXPLIZITEM Partner (e = l−1 bzw. e = l je
Verschiebungsrichtung). Beweis: Fallunterscheidung + hv-Substitution +
linarith — die Robustheit ist algebraisch direkt.
**VERSTÄNDNIS: das ist die diskrete STÖRUNGS-ROBUSTHEIT des Interlacings
— ein einzelner verschobener Punkt zerstört die Verschränkung nicht. Das
ist die formale Gram-Punkt-Verschiebungs-Robustheit, die auch unsere
Zertifizierung bei Turing-Checks implizit nutzt. Seine Bibliothek
formalisiert exakt die Robustheits-Eigenschaft unserer Methode-Familie.**
Verbindung zum cfg_inter (E1.3): die Bedingung ist dieselbe — der Satz
ist ihre Stabilitäts-Garantie.
