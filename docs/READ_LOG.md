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

### InterlacingGrids/CloudProd.lean (148 Zeilen, Kern) — 2026-11-23 — GELESEN_VERSTANDEN
Die CLOUD-KONTROLLE verstanden: (1) cloud_weight_prod: das harmonische
Gewicht ∏(2+c, 1+1/j) = (2+c)·(n+1) — LINEAR, nicht exponentiell.
(2) cloud_factor_le: die GAP-Struktur (lambda-Folge fällt mit Abstand g)
garantiert Distanz >= j·g für den j-ten Cloud-Punkt → Faktor <= 1+1/j
(das harmonische Gewicht). (3) prod_le_prod_range_of_rank: das generische
RANG/MATCHING-Argument (injektive Zuordnung je Cloud-Punkt zu einem Rang).
**VERSTÄNDNIS: die technische Substanz, die die Weil-Maschine vor der
b^k-Katastrophe rettet — die Null-Abstände (Gaps) machen die Cloud-Faktoren
harmonisch summierbar. Dasselbe Prinzip, das unsere count_argument.py-
Schranken trägt: Abstände machen Produkte kontrollierbar.**

### InterlacingGrids/CloudPair.lean (140 Zeilen, Kern) — 2026-11-23 — GELESEN_VERSTANDEN
DIE PAIR-ZUORDNUNG verstanden: φ s = if 0 < Y+λs then s else s+1 — die
SIGNATUR-ABHÄNGIGE Zuordnung (das Vorzeichen von Y+λs wählt den v-Partner;
das PairOK-Interlace-Pairing in Aktion). cloud_pair_factor: die
Faktorisierung a <= (Gewicht 1+(1+c)/d) × (Partner-Abstand |Y+1/2+v_i|)
— das Gewicht wird durch die Gaps harmonisch klein, der Partner-Abstand
trägt das Produkt; der ausgelassene Index e liefert den 3b-Faktor.
**DIE MASCHINE VOLLSTÄNDIG VERSTANDEN: CloudPair (Pairing) → CloudProd
(harmonische Gewichte, linear) → Bracket (Kopf fein + Schwanz grob) →
pst_mul_le (Weil-Oberschranke). Jede Stufe sitzt, jede Idee benannt.**
LESER-BILANZ E1 (BesselWaveGrids/InterlacingGrids): 10 Dateien gelesen
und verstanden — die komplette formalisierte Weil-Formel-Maschine.

### StableLattices/AdaptExistsStatement.lean (10 Zeilen) — 2026-11-23 — GELESEN_VERSTANDEN (WRAPPER)
ARCHITEKTUR-BEFUND: die Datei ist ein Wrapper — re-exportiert
GlobalTheory.T.AdaptedBasisExistsAlt aus BmuAdapt.adaptExists (der echte
Beweis liegt im GlobalTheory-Layer). Die first|exact|exact|Kette = robuste
Verifikation desselben Beweis-Terms über mehrere Tactic-Wege.
KARTEN-VERFEINERUNG: part01 hat nur 4 GlobalTheory-Dateien (LocalGlobalProofs/
GlobalTheory/: BernsteinZelevinskyFiniteness, ExistsExpUnitary, ImportsAlt,
ParabolicInductionFiniteLength). Der Haupt-GlobalTheory-Layer (BmuAdapt,
GroundTheory.BlockD etc.) verteilt sich auf spaetere Parts — die naechsten
Lese-Einheiten folgen dem Beweis-Layer, nicht der Companion-Fassade.
Die Adjoint-Valued-Matrix (GroundTheory.AdjointValued.MatrixAdapt …) =
in part01 gefunden (GroundTheory-Layer existiert teilweise hier).

### GlobalTheory.CompanionTheory.BmuAdapt (Z. 140535-140885, ~350 Z., Kern) — GELESEN_VERSTANDEN
Der ECHTE AdaptExists-Beweis (im GlobalTheory-Layer, nicht der Wrapper):
(1) herm-Infrastruktur: die hermitesche Bilinearform zu Matrix H mit allen
Linearitaets-Lemmata (add/sub/smul links+rechts, star_herm-Symmetrie,
herm_single = Matrix-Eintraege, mem_UH_of_herm).
(2) Verschiebe-Lemmata: refl_iso/exists_refl/exists_move — Vektoren mit
gleichen Form-Werten sind ineinander ueberfuehrbar (die Isotropie-Technik).
(3) Die KONSTRUKTION: s2 = 1/sqrt(2); col k r j = explizite Spaltenvektoren;
G0 k r = die Basis-Matrix (EXPLIZIT gebaut, Unitaritaet + Transformation
direkt bewiesen). Hauptsatz: fuer isotropes z: rho := sqrt(Tz/2) aus
herm Hpk z z = -Tz; u := rho*sqrt(2)*bvec(...) — die explizite
Normalisierung der Form auf -1.
**VERSTÄNDNIS: das ist die Lean-Form des SYLVESTER-Normalform-Verfahrens
(hermitesche Formen auf Standardform via explizite unitaere Basiswechsel,
Traegheits-Gesetz als Konstruktion). STRUKTURELL UNSER b4g-SYLVESTER-SCHRITT
aus der SSZ-Operator-Rekonstruktion — dieselbe lineare Algebra-Kernidee
(hermitesche Formen, Traegheit, unitaere Anpassung), zwei Realisierungen.**

### Bmu-Definitions-Layer (Hpk/Tz/wI/bvec/inWb, Z. 12546080+) — GELESEN_VERSTANDEN
Die Kern-FORM der Bessel-Map-Geometrie komplett gelesen: Hpk = Blockstruktur
(r Anti-Diagonalen-Bloecke [[0,1],[1,0]] oben, gespiegelt hermitesch;
Mittelblock (k+1)x(k+1) mit +1-Diagonale, EIN −1 bei i=r+k) →
Sylvester-Traegheit (r+k, r+1). Tz = −(herm Hpk z z).re (negatives
Form-Funktional); rho = sqrt(Tz/2) normalisiert auf Formwert −1 (die
Hyperbel-Struktur). bvec = Pi.single-Basis; wI = Mittelblock-Index;
inWb = mittlerer Traeger-Unterraum.
**VERSTÄNDNIS: Hpk ist die kanonische Signatur-Form — dasselbe Objekt,
das unser b4g-Sylvester-Schritt behandelt (Traegheits-Gleichheit). Seine
Konstruktion ist explizit blockweise, unsere Traegheits-Argumentation
algebraisch — dieselbe Sylvester-Welt, jetzt auf Definitions-Ebene
verstanden. Die Bessel-Map-Lehre: die Form Hpk + die adapted basis G0
= die komplette Normalform-Maschinerie der Geometrie.**

### HpkFacts/NSubgroup/EllAdd/PsiChar/HeadOrbit/CharBlock/DetZj (Prop-Strukturen) — GELESEN_VERSTANDEN
Die bewiesenen Form-Eigenschaften: HpkFacts = (hermitesch, INVOLUTORISCH
(Hpk^2 = 1 — selbstinvers!), eI/esI-Orthonormalpaare, SYLVESTER-Kongruenz:
exists P mit P^H * Jm(eps) * P = Hpk, Traegheit (k+r, ...) als Kongruenz-
Existenz). NSubgroup = die Form-erhaltende Gruppe (g^H H g = H);
EllAdd = ell additiv auf der Gruppe (Charakter-Funktional); PsiChar = psi
multiplikativ, ||psi|| = 1 (unitaere Charaktere); HeadOrbit = LDU-Zerlegung
l*hMat*u MIT EINDEUTIGKEIT (Iwasawa!); CharBlock/CornerInv = Block-Algebra
der unipotenten Ränder; DetZj = Determinanten-Faktorisierung.
**VERSTÄNDNIS: die lokale Gruppen-Theorie der Bessel-Map = Form
(involutorisch!) + isotrope Gruppe + unitaere Charaktere + eindeutige
Iwasawa-Zerlegung. Die Sylvester-Kongruenz (HpkFacts-4) ist EXAKT unser
b4g-Thema (Traegheits-Gleichheit) — seine Formalisierung: Kongruenz-
Existenz mit explizitem eps-Vektor. Die involutorische Struktur (Hpk^2=1)
ist der elegante Kern: die Form ist ihr eigenes Inverses.**

### Formalism.REAL.Jm (Z. 6632602) — GELESEN_VERSTANDEN
Jm N p = diagonal fun a => sgn(p, a) — die SIGNATUR-DIAGONALE (±1 auf der
Diagonalen, p zaehlt die negativen Positionen). Schliesst die Sylvester-
Kette der Geometrie-Saeule: Hpk (involutorische Blockform, Hpk^2=1)
≅_kongruent Jm(eps) (Signatur-Diagonale, Traegheit (k+r, r+1)) via P.
Das Traegheits-Gesetz als explizite Kongruenz auf die kanonische
Diagonalform — die Standardform-Definition ist trivial (diagonal + sgn),
die Substanz liegt in der Kongruenz-Existenz (HpkFacts-4).
**SAEULE 2 (Sylvester-Geometrie) JETZT VOLLSTAENDIG: Hpk → G0 → Jm.**

### Jacquet-Saeule: Twisted-Conjugacy-Basis (Z. 70085-70350) — GELESEN_VERSTANDEN
Die Fundament-Technik: twR = theta-Twist-Aequivalenz (y = g^-1 * x * theta g
— twisted conjugacy, die Standard-Technik der Jacquet-Modul-Rechnung);
cls = Twisted-Klassen als Quotient (twR_equiv = Aequivalenz bewiesen);
thE = die Involution (thE thE = id); nrm_tw/locEl_tw = Norm-Vertauschung
unter dem Twist; param_main = der Parametrisierungs-Hauptsatz unter 6
Voraussetzungen (SkewEx, Struct, QuadField, LocDict, ClsNorm, ClsOnto).
**VERSTÄNDNIS: die orbitale Struktur der Jacquet-Saeule beginnt mit der
klassischen Twisted-Conjugacy — die Klassen-Quotienten parametrisieren
die Jacquet-Moduln. Die 6-Bedingungs-Struktur von param_main ist ein
modulares Beweis-Architektur-Muster (jede Bedingung eine eigene Datei-
Gruppe). Naechste Einheit: die 6 Bedingungen einzeln (SkewEx zuerst).**

### SkewEx + ClsNorm (param_main-Bedingungen 1 und 5) — GELESEN_VERSTANDEN
SkewEx (15 Z., komplett): in jedem CM-Koerper E existiert s != 0 mit
conj(s) = -s und s^2 im maximalen reellen Teilkörper. BEWEIS verstanden:
z mit conj(z) != z (aus conj != id, der CM-Eigenschaft); s := z - conj(z)
(der klassische anti-fixierte Trick); conj(s) = -s via Linearitaet+
Involution; s^2 fixiert → reeller Teilkörper. Die kanonische Konstruktion
rein-imaginaerer Elemente, sauber in Lean.
ClsNorm: die Vertreter-Normierung pt*thetaGL(pt) = delta*thetaGL(delta)
unter IsFrame — die Multiplikator-Gleichung des Twists (Bedingung 5/6).
**param_main-Fortschritt: 2 von 6 Bedingungen verstanden (SkewEx = CM-
Feld-Basis, ClsNorm = Vertreter-Normierung). Die verbleibenden: Struct,
QuadField, LocDict, ClsOnto.**

### Struct + QuadField (param_main-Bedingungen 2 und 3) — GELESEN_VERSTANDEN
Struct: fuer delta mit (delta*thE delta)-charpoly in Ell (elliptische
Charakteristik) existiert die Zerlegung in total-reelle Zahlkoerper K_i
(card iota = nfac(charpoly) = Faktorisierungszahl, Rang-Summe = n) plus
die E-Algebra-Struktur rho mit Frame-Bedingung — die Zerlegung des
twisted Endomorphismus in total-reelle Komponenten.
QuadField: die Hasse-Norm-Charakterisierung — global UND lokal:
x in Norms K L <=> x = a^2 - d*b^2 (die Norm-Form von L = K(sqrt d),
die PELL-Struktur). Die Kette: s anti-fixiert (SkewEx) → d = s^2 reell
→ L = K(sqrt d) → Normen = a^2 - d*b^2 — die kanonische CM→quadratisch-
Pipeline.
**param_main-Stand: 4 von 6 Bedingungen verstanden (SkewEx, Struct,
QuadField, ClsNorm). Verbleiben: LocDict, ClsOnto. Die Architektur ist
jetzt als Ganzes sichtbar: CM-Basis → Zerlegung → Norm-Charakterisierung
→ lokales Woerterbuch → Vertreter → Surjektivität = die parametrische
Zerlegung der Twisted-Klassen-Theorie.**

### LocDict + ClsOnto (param_main-Bedingungen 4 und 6) — GELESEN_VERSTANDEN — PARAM_MAIN KOMPLETT (6/6)
ClsOnto: die Klassen-TRANSITIVITAET — fuer jedes y mit derselben
separablen elliptischen Charakteristik: y = g^-1 * pt(delta,t) * theta(g)
— die Charakteristik ist die VOLLSTAENDIGE Klassen-Invariante.
LocDict: das lokale Woerterbuch — lokale Existenz <=> lokale
Norm-Zerlegung x = t*(a^2-d*b^2) in den Kompletionen (das HASSE-PRINZIP,
verteilt ueber alle Plaetze).
**PARAM_MAIN KOMPLETT (6/6): SkewEx (CM-Basis) → Struct (total-reelle
Zerlegung) → QuadField (Pell/Hasse a^2-d*b^2) → LocDict (Hasse-Prinzip
lokal<->global) → ClsNorm (Vertreter) → ClsOnto (Transitivitaet).
Die Jacquet-Klassen sind durch (Charakteristik, Norm-Werte) PARAMETRIERT.
Logische Spiegel zu unserem Feld: Charakteristik = vollstaendige
Invariante <=> unsere EW-Knoten als Instabilitaets-Klassifikation;
Hasse lokal<->global <=> unsere lokale Arb-Enclosures → globale
Null-Claims.**
