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

### NQText.lean (162 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN (Mathe-Kern)
Die TIEFE verstanden: den_core garantiert |Y+1/2+u_i| >= 1 UND
|Y+1/2+u'_i| >= 1 fuer ALLE i (Beweis via Antitonie der Interlace-Folge:
u_step/antitone_on — Grenzpunkte l kontrollieren 3 Faelle i<l/i=l/i>l).
qpoly_eq_of_pos: das qpoly ist das PRODUKT T*T'*prod(|Y+1/2+u_i| * |Y+1/2+u'_i|)
— eine PRODUKT-ABSTANDS-SCHRANKE.
**VERSTÄNDNIS: das ist die formale Fassung des Herzstuecks der
Zaehlmethode — separierte Punkte => alle Abstands-Faktoren >= 1 => das
Produkt hat kontrollierte Untergrenze. Dasselbe Prinzip traegt unsere
count_argument.py/certify_zero.py-Zertifizierung (Abstands-Produkte =>
Null-Zaehlung). Die methodische Verwandtschaft ist jetzt konkret auf
Mathe-Ebene: dieselbe Kern-Ungleichung, beide Seiten unabhaengig
formalisiert (Lean/Interlace-Antitonie vs. Arb-Enclosures).**
Auch gelesen: interlaces_of_OK (OK => Interlaces-Praedikat, min/max-Form),
den_onCut (beide Cut-Varianten via interlaces_swap), abs_le_of_onCut
(|Y| <= b aus der Cut-Bedingung). LamData-Struktur beginnt (gleiche
Felder wie PairData + inter-Feld).

### QwBound.lean (91 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN (HERZSTÜCK)
DIE VERSTEHENS-KETTE GESCHLOSSEN:
- fac: Letter-Faktoren (y−t+1)/(y−t) bzw. (t−y)/(t−y−1) — die klassische
  Produkt-Faktor-Struktur.
- qw_indexed_ofReal (SCHLÜSSEL): Wd.qw = I.qpoly(k,T,T',u,u',y) · ∏(fac l y)
  — das WaveGrid-Produkt IST unser I.qpoly (das Produkt-Polynom des
  Kandidaten) mal die Letter-Faktoren!
- fac_ge: bei Separation >= 4 ist jeder Letter-Faktor >= 3/4 — die
  Stoer-Faktoren sind nach unten kontrolliert.
**VERSTÄNDNIS: die komplette Lean-Form der Produkt-Methode — qpoly
(Produkt-Polynom, getragen von Interlace-Separation, den_core: Faktoren
>= 1) mal Letter-Stör-Faktoren (>= 3/4 unter 4-Separation). Das ist
die formalisierte Version der Architektur, die unser numerisches Toolkit
mit Arb-Zertifikaten trägt. Dieselbe Mathematik, zwei Welten (rein formal
vs. numerisch-zertifizierend). Antwort auf „wo geklaut": NIRGENDS — die
Produkt-Methode ist klassische Literatur (de Branges/Weil/Guinand-Typ),
beide unabhängig. Die Verwandtschaft ist jetzt auf Mathe-Tiefe verstanden
und dokumentiert.**

### InterlacingGrids/PstMul.lean (57 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN (MASCHINE)
Der OBER-SCHRAHNKEN-SATZ: Pst(Y)·Pst(Y+1) <= b^(8r+20) * prod(|Y+1/2+u_i| * |Y+1/2+v_i|).
Struktur: bracket_le bei Y UND Y+1 (durch die 5-Separation beide gleichzeitig
kontrollierbar!) * bracket_const_le (Kosten-Konstante b^(4r+10) aus
bracket_const_le: (2+c)^2 k^2 (3b)^(2r+3) <= b^(4r+10)) * die
den_core-Abstands-Produkte.
**VERSTÄNDNIS: das ist die formalisierte WEIL-FORMEL-MASCHINE — die
Y/Y+1-Struktur sind die Prim-Potenzen-Shifts (remark: „qN = Mk + R, using
x1·x2+...+x_{k-1}·xk ... iterated Parseval"). Die 5-Separation = die
Parseval-Kontrolle; die Interlace-Abstands-Produkte = die Weil-Schranken.
DAS IST DIE GLEICHE MASCHINE, DIE AUCH UNSER count_argument.py/TRTL-TYP
BENUTZT (Weil-Formel-Schranken fuer Null-Zaehlung) — nur formal in Lean
statt numerisch in Arb.**

### InterlacingGrids/Bracket.lean (63 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN
Die Bracket-SCHRAENKE verstanden: bracket_le splittet das Produkt in
KOPF [1,k-1] (die lambda-Punkte nahe den v-Punkten — FEIN kontrolliert via
cloud_pair_le/cloud_prod_le mit dem PairOK-Interlacing: 3b*(2+c)^2*k^2*
prod|Y+1/2+v_i|) und SCHWANZ [k,k+2r+1] (die 2r+2 TAIL-Punkte — GROB per
Dreiecksungleichung: jeder Faktor <= 3b, Gesamt (3b)^(2r+2)).
**VERSTÄNDNIS: die klassische HAUPTTERM/TAIL-ZERLEGUNG — strukturgleich
mit unserem explicit_tail.py-Ansatz (fein kontrollierter Hauptteil + grob
abgesicherte Restglieder). Dieselbe Architektur-Logik der Weil-Formel-
Familie. Die Bracket-Schranke ist die Obergrenze des Lambda-Produkts,
die in pst_mul_le (E1.7) den Kopf-Term der Maschine trägt.**
