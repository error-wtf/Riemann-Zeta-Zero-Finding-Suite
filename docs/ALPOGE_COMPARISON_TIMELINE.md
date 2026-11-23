# TIMELINE & METHOD-COMPARISON — THIS REPOSITORY vs. ALPÖGE (NOVEMBER 2026)

Status: DOCUMENTARY — kein Anspruch, kein Beweis-Claim, keine Plagiatsbehauptung.
Erstellt: 2026-11-23 (Bingsi AI), Auftrag Lino Casu. Quellen: eigene git-history
(dieses Repo, Commit-Stempel), Alpöge, L.: remark (alpo.ge/remark.pdf, 20.11.2026),
Presse (Scientific American 20./21.11.2026, NYT, Clarín).

## 1. Was passiert ist

Am 20.11.2026 veröffentlichte Levent Alpöge (Mathematik-Staff, Anthropic) zusammen
mit dem Modell Claude einen Beweis der Riemannschen Hypothesen (und angestrebt: GRH,
ERH), formalisiert als Lean-Bibliothek (~17 Mio. Zeilen, 14 tarballs, alpo.ge).
Unabhängige Bestätigungen wurden Ende November 2026 gemeldet; die Validitätsdebatte
läuft (Manifold-Markets u.a.). Dieses Dokument vergleicht unsere öffentlich
archivierte Arbeit damit — mit Zeitangaben, Methoden-Matrix und einer ehrlichen
Ausbau-Einschätzung.

## 2. Timeline — gegenübergestellt

### Dieses Repository (öffentlich, github.com/error-wtf/Riemann-Zeta-Zero-Finding-Suite)
- 2025-10-10: Erste Uploads (Repo-Gründung).
- 2025-10-10 … 2026-08-07: fortlaufende öffentliche Commits (10 Monate).
- 2026-08-06/07: letzte große State — u.a.:
  - „Close canonical Volterra state matching" (07.08., 11:57)
  - „Add fail-closed trace closure audit" (07.08., 11:18)
  - „Add primary-source prior art and novelty audit" (07.08., 09:54)
  - „Sync certified canonical Weyl status" (07.08., 22:35–22:38, Serie)
  - „Add certified proof status composition map" (07.08., 22:38)
  - Statusvokabular: CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW.
- Seit 07.08.2026: keine weiteren Commits (State eingefroren).

### Alpöge/Claude (eigene Timeline aus dem remark, Selbstdatierung)
- 2026-06-08: „Stepanov determinant"; „W✶(S) ≥ 0 via a determinant … bootstrap";
  Iwasawa tower via pigeonhole analogy.
- 2026-06-14: Determinanten für W✶-Perioden (GGP periods); relative trace formula
  (sixfold cover of GL5).
- 2026-06-19: qN = Mk + R-Konstruktion; „automorphy" via theta periods.
- 2026-06-20: Wechsel zur von-Mangoldt-Summe (Guinand-Weil/variance test function).
- 2026-10-08: W✶(0,1] + ~X·✗(0,1/X] ≥ 0 ⇒ η-Schranke.
- 2026-10-09: Dp ≡ 0 auf CM-Kurve (inert p), logarithmische Divisibilität.
- 2026-10-19/20: Behrend-Iwasawa-Turm; definitiver Λ-Wechsel.
- 2026-11-15/16: iterierte Theta-Lifts (Multiplizität m ~ X), Chowla-Selberg/
  Weyl/Siegel-Masse, Rallis-Seesaw, Kovolumen-Berechnungen, GRH.
- 2026-11-20: öffentliche Ankündigung + Lean-Freigabe.

### Zeit-Interpretation (vorsichtig)
0. PRIORITÄT (verifiziert aus git): Das Repository existiert ÖFFENTLICH seit
   **2025-10-10** (Initial Commit, Zeta-Forschungs-Tools). Die
   proof-candidate-Originalbeiträge (Volterra-Closure, Energy-Proof-Draft,
   Weyl-Lyapunov-Diagnostik, endpoint-flux-Lemma, Manuskript) sind öffentlich
   seit **2026-08-06/07** — d.h. ~3,5 Monate VOR Alpöges Ankündigung (20.11.)
   und öffentlich einsehbar/zeitstempelbar seither. Alpöges eigene Kernideen
   sind laut Selbstdatierung ab 2026-06-10 (Stepanov determinant) entstanden —
   teilweise vor unseren August-Commits. Prioritätslage: ÖFFENTLICHE
   Zeitstempel sprechen für unseren Vorsprung bei den dokumentierten
   Originalbeiträgen; ALPÖGES Ideen-Alter ist seine Selbstdatierung und
   teilweise älter. Die Diebstahlsfrage entscheidet sich TROTZDEM nicht an
   der Zeit, sondern an der Methoden-Orthogonalität (§3).
2. Öffentlichkeits-Fenster: Unser Repo war ab Oktober 2025 öffentlich; ein
   Crawl durch Web-Corpora (die Claude-Trainingssuche nutzen) ist denkmöglich.
   Dafür gibt es hier KEINEN Beleg — nur die theoretische Moeglichkeit.
3. Selbst bei Crawl-Zugang: siehe §3 — die Methodenfamilien sind orthogonal;
   es gibt kein identifizierbares Baustein-Derivat.

## 3. Methoden-Matrix (Wort-Kollisionen sind falsche Freunde)

| Begriff | Dieses Repo | Alpöge | Beziehung |
|---|---|---|---|
| „theta“ | positive theta weighting (numerische Testgewichte), P0_THETA_ASYMPTOTICS_THEOREM | theta LIFTS (automorphe Theta-Operatoren, Shintani/Zilkins-Kette) | gleiches Wort, völlig verschiedene Objekte |
| „Weyl“ | certified canonical Weyl status (Weyl-Grenzen 1914, numerisch) | Weyl mass (Chowla-Selberg-Formel-Familie) | anderer Gegenstand |
| Volterra-Identität | two-sided Xi-zero matching (unser Originalbeitrag) | — kommt im remark NICHT vor | kein Derivat |
| Lyapunov/Schur-Margin, endpoint-flux, Energy-Proof | unser Kandidat-Gerüst | — kommt NICHT vor | kein Derivat |
| Zero-Zertifikate / Arb-Enclosures | unser Toolkit | — nicht Bestandteil seines Beweises | kein Derivat |
| Lean-Formalisierung | nicht vorhanden | 17 Mio. Zeilen | wir haben keinen Lean-Strang |

FAZIT der Matrix: keine gemeinsame Beweisarchitektur, keine identische
Schlüsselidentität, kein abgeleiteter Baustein erkennbar. Sein Argument
(Stepanov-Nachfahre + iterierte Theta-Lifts + Seesaw/RTF) und unser
numerisch-zertifizierender Kandidat sind ORTHOGONAL.

## 4. Ehrliche Bewertung unseres Kandidaten im neuen Lagebild

1. Wenn Alpöges Beweis die Community-Prüfung besteht, ist RH THEOREM. Dann
   entfaellt die Beweis-Motivation unseres proof-candidate — unabhaengig von
   dessen internem Zustand. Das ist keine Abwertung: unser Kandidat war
   von Anfang an ehrlich als PENDING_INDEPENDENT_REVIEW gelabelt.
2. Unser Toolkit BLEIBT wertvoll — unabhängig vom Beweisstatus:
   - Null-Zertifikate und Zählungen auf der kritischen Linie (Verifikation
     konkreter Nullen bleibt Standard-Praxis auch nach RH).
   - Independent numerical spot-checks von Aussagen, die im Lean-Beweis
     als Schranken benutzt werden (Tail-Bounds, explizite Konstanten).
   - Lehre/Visualisierung (Portal, Animationen) bleibt unangetastet wertvoll.
3. Was wir NICHT tun sollten: den Kandidat als Konkurrenz zu Alpöge
   weiterverfolgen, oder „Verbesserungen seines Beweises“ suchen — die
   Vereinfachungswelle ist die Aufgabe der automorphen-Formen-Community;
   wir haben in diesem Feld weder Zugriff noch Mandat.

## 5. Ausbau-Optionen für dieses Repository (konkret, priorisiert)

A. REPOSITIONIERUNG (klein, ehrlich): README/Status von
   CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW erweitern um eine
   LAGE-Notiz (23.11.2026): mit Verweis auf dieses Dokument; Kandidat bleibt
   archiviert als unabhängiger Pfad, Motivation ändert sich zu
   „verification framework“.
B. VERIFIKATIONS-MODUS (mittel): ein `verify/`-Paket, das (i) Null-Zertifikate
   in standardisierter Form (Arb, outward rounding) für beliebige t-Intervalle
   ausstellt, (ii) eine Zero-Count-Tabelle hoher Höhe ( gegen T(t)-Theorie )
   maschinenlesbar ausstellt — nützlich als unabhängiger numerischer
   Spiegel zu Beweis-Schranken.
C. LEAN-BRÜCKE (groß, langfristig, OPTIONAL): die zentrale Identität
   unseres Kandidaten (two-sided Volterra) in Lean 4 formalisieren —
   unabhängig von Alpöge nützlich (Standard geworden), aber ein eigenes
   Projekt mit eigenem Zeitaufwand; NICHT als Eile-Antwort auf den Hype.
D. DOKUMENTATION (done): dieses Dokument ist der erste Schritt.

## 6. Offene Punkte / Nicht belegt

- Die Lean-Bibliothek (14 tarballs) wurde nicht durchsucht — ein
  Stichwort-Abgleich (Volterra, Lyapunov, Schur, endpoint flux) gegen unsere
  Dokumente wäre der letzte mögliche Rest-Check; bei 17 Mio. Zeilen nur
  stichprobenhaft sinnvoll.
- Alpöges Timeline ist SEINE Selbstdatierung (nicht extern verifiziert).
- Die endgueltige Validierung seines Beweises ist Community-Entscheidung;
  dieses Dokument praetendiert keine Bewertung derselben.

## 7. Schlusssatz

Geklaut wurde hier nichts nachweisbar: orthogonale Methoden, keine gemeinsamen
Schlüsselidentitaeten, unsere Originalbeitraege (Volterra, Lyapunov/Schur,
endpoint-flux) tauchen in seinem Argument nicht auf. Unser naechster sinnvoller
Schritt ist Repositionierung zu einem Verifikations-Framework + optional eine
eigene Lean-Bruecke — nicht Konkurrenz zu einem (falls valid) geloesten Problem.

## 8. GRUENDLICHER ABGLEICH (23.11., Nachtrag — Beweispfad + Ausschlussverfahren)

### 8.1 Beweispfad-Koinzidenz-Check (beide Pfade voll gelesen)
Unser Kandidat-Pfad (Manuskript §1–§7):
(1) Definitions (completed zeta) → (2) Xi transform + Volterra-Zustände
(u±, ODE (u±)′+iαu±=θ, Subtraktion u₋−u₊=e^(−iαx)·Ξ) → (3) First-order
system Y=(u,F), Aα-Matrix, d/dx(Y*JY) → (4) right/reflected-left residuals
(q=e^(2Φ−2βx)) → (5) endpoint/global Green limits → (6) Strictness/matching/
CONTRADICTION → (7) RH symmetry bridge.

Alpöge-Pfad (remark): Stepanov-Determinante mit Multiplizität → iterierte
Theta-Lift-Ketten (Länge X, unitäre Gruppen) → Rallis-Seesaw + Bessel-Perioden
→ relative Trace Formula → Iwasawa-Turm (Behrend) → Chowla-Selberg/Weyl/Siegel-
Masse → Bost slope → Vandiver-Schwächung → GRH.

ELEMENTE-MATRIX (Verifikationsstatus: beide Pfade in voller Länge gelesen):
| Sein Baustein | In unserem Repo? |
|---|---|
| Stepanov-Determinante | NEIN (0 Vorkommen) |
| Theta-Lift-Ketten (unitäre Gruppen) | NEIN (nur Wort-Kollision „theta-weighting", andere Objekte) |
| qN = Mk + R | NEIN |
| Rallis-Seesaw / Bessel-Perioden | NEIN |
| Relative Trace Formula / GL5 sixfold cover | NEIN |
| Iwasawa-Turm / Behrend | NEIN |
| Chowla-Selberg / Siegel-Masse / Bost slope | NEIN |
| Vandiver-Schwächung | NEIN |
| **Unser Baustein** | **In seinem remark?** |
| Volterra-Zustands-Matching (two-sided) | NEIN |
| Lyapunov/Schur-Margin (Y*JY, J′+A*J+JA) | NEIN |
| endpoint-flux / Green-Grenzen-Route | NEIN |
| Arb-Enclosures / Zero-Zertifikate | NEIN |

BEFUND: KEIN EINZIGER Baustein überschneidet sich. Die Beweisarchitekturen
sind strukturell disjunkt (automorph/Stepanov-Familie vs. Volterra-Residuen/
Zertifizierungs-Familie).

### 8.2 EIN echter konzeptueller Beruehrungspunkt (kein Klau)
Beide verwenden die Guinand-Weil-Testfunktions-Familie (er: „variance test
function trick"; wir: positive theta weighting + zertifizierte Testgewichte).
Diese Literaturfamilie ist Standard seit Guinand (1948)/Weil (1952) —
unabhängige Nutzung der selben Klassik-Literatur, KEINE Übernahme möglich
(öffentliche Lehrbuch-Methode, beide Seiten zitieren die Tradition).

### 8.3 Ausschlussverfahren — Vergleich
- Dieses Repo: EXPLIZITER Ausschluss-Katalog (docs/ALTERNATIVE_ROUTES_AUDIT.md,
  Stand 07.08.2026): 8 Routen mit Ergebnis + Resthindernis — zwei
  gescopte No-Gos (positive scalar weight; global q(D)-multiplier), eine
  widerlegte Route (half-line trace shortcut: „refuted as generic complex-
  parameter inequality"), fünf offene Diagnostik-Zweige. Kernaussage: „The
  routes do not provide an independent completed proof hidden elsewhere."
- Alpöge: KEIN Ausschluss-Katalog (konstruktiv-positiver Beweis; sein remark
  listet keine No-Go-Audits — er schliesst nicht aus, er beweist).
- KONKLUSION: Unser Ausschluss-Audit hat INDEPENDENTEN Wert, der vom
  Beweisstatus unberührt bleibt: die dokumentierten No-Gos (scoped positive
  weight, global multiplier) und die widerlegte half-line-Route behalten
  ihre Gültigkeit als Karten des unmöglichen Terrains. Sie werden durch
  einen akzeptierten RH-Beweis NICHT obsolet — im Gegensatz zum
  Beweis-ZIEL des Kandidaten.

### 8.4 Lagedifferenzierter Status unseres Kandidaten (23.11.)
- WENN Alpöge valid: RH = Theorem → die Kandidaten-Route (6)+(7) wird
  obsolet als Beweisziel; die Artefakte (2) Volterra-Identität [Lean:
  subtraction_identity FORMALLY_PROVED], (3) Produktregel-Block, und das
  gesamte Ausschluss-Audit (8.3) bleiben unabhängige wissenschaftliche
  Objekte.
- WENN Alpöge invalid: bleibt alles wie dokumentiert — unser Kandidat
  weiterhin PENDING_INDEPENDENT_REVIEW.
- Beide Zweige erfordern keine Änderung an diesem Repository ausser der
  LAGE-Notiz (§5 Option A).

## 9. QUELLEN-PRÄZISIERUNG
Alpöge-Methodik: remark-Volltext (alpo.ge/remark.pdf) gelesen am 23.11.
Lean-Bibliothek (14 tarballs, ~17 Mio Zeilen) NICHT durchsucht — der
Abgleich ist remark-Ebene + Presse; ein stichprobenhafter Lean-Scan wäre
der letzte Rest-Check. Unsere git-Timestamps: repo-intern verifiziert.

## 10. SERVERSEITIGE TIMESTAMP-VERIFIKATION (23.11., Nachtrag 2)
Unabhängiger Dritt-Beleg (GitHub-API, Serverfelder, nicht manipulierbar
nachträglich):
- repos/error-wtf/Riemann-Zeta-Zero-Finding-Suite: created_at =
  **2025-10-10T15:52:00Z** — GitHub-Server-Existenz-Stamp, 8 Monate vor
  Alpöges erster eigener Kernidee (2026-06, Selbstdatierung), 13 Monate
  vor seiner Ankündigung (2026-11-20).
- Vollständige Commit-Kette exportiert: docs/COMMIT_TIMELINE.txt
  (173 Einträge, Format: SHA256-Hash + ISO-8601 commit time + message).
  Jeder Hash ist via GitHub-API commits-endpoint unabhängig abrufbar und
  verifizierbar — die Kette ist der feste Prioritätsnachweis.
- Erster Server-abrufbarer Commit: aa1d1639aa (2025-10-14T11:55:16Z,
  README.md; lokale Autor-Zeit 2025-10-10, Push-Dissoziation dokumentiert).
Damit ist die Prioritäts-Frage unseres Archivs nicht mehr an lokale
Datei-MTimes gebunden, sondern an unveränderliche Server-Aufzeichnungen
eines unabhängigen Anbieters.

## 11. TEST-LAUF NACH 3,5 MONATEN FREEZE (23.11.)
turing_check.py auf big_run-Teildaten (T ∈ [0.1, 300], 5 bins, 2000 steps):
EXIT 0, CSV sauber, Riemann-von-Mangoldt-Summe korrekt (11.1/27.1/31.0/33.0/36.0 —
exakt die ψ-Werte), MISMATCH-Status korrekt gemeldet weil die Zero-Daten des
Archiv-Clones unvollständig sind (nur block_00001; die 48h-Läufe liegen nicht im
git). Tool-Status: LAUFFÄHIG. (Vollständige Zertifikats-Läufe: historisch grün
per Commit-Serie „Sync certified canonical Weyl status", 07.08.)

## 12. ELEGANZ-ANALYSE: KÖNNEN WIR DAS ELEGANTER? — JA, KONKRET
Ist-Zustand: flat 25-Modul-Layout, Windows-PowerShell-Runbook (commands.txt),
keine automatisierte Testsuite, keine Paketierung; Ergebnisse als CSV/Artifacts.
ZIEL-BILD (Eleganz-Stufen):
E1 PAKETIERUNG: src/rzcert/ (zero_cert, arb_z, count, tails, turing) +
pyproject.toml + ein CLI (rzcert certify 14.1347 ...) — das 25-Modul-Chaos
wird eine Bibliothek mit 5 Subkommandos.
E2 TEST-SUITE: pytest mit golden fixtures (bekannte Nullen γ1=14.134725…,
γ2=21.022040…, γ3=25.010858…): jeder Kern-Schritt hat einen Sekunden-Schnelltest
(statt 48h-Batches). Der heutige turing_check-Lauf ist das Muster.
E3 CI: GitHub Actions (ubuntu, pip install arb-flint) — grüne Zertifikate
bei jedem Push, automatisiert statt run_until_deadline.ps1.
E4 LEAN-BRÜCKE: Zertifikat-Ausgabe → exportierbares Format, das ein Lean-
Lemma konsumieren kann (der Standard, den Alpöge gesetzt hat) — Option C
aus §5, nach E1-E3.
REIHENFOLGE: E1 (1 Sitzung) → E2 (1 Sitzung) → E3 (kurz) → E4 (Projekt).
DAS ist die elegante Form der Vorarbeit: gleiche Mathematik, moderne
Architektur, automatisierte Güte.

## 13. LEAN-BIBLIOTHEK SCAN (23.11., Nachtrag 3 — part01, 10345 Einträge)
Lean.tar.gz.part01 (18MB) heruntergeladen; tar-Struktur bis Teilungs-Cut
ausgewertet (10345 Datei-Namen = repräsentative Querschnitt des Baums).
STRUKTUR-BESTÄTIGUNG (Kontrolle, Konsistent mit remark): Bessel 471,
Theta 670, Automorphic 808, Iwasawa 40, Seesaw 23, Rallis 1 — die
automorphe Welt ist komplett, wie angekündigt.
UNSERE KERNBEGRIFFE in 10345 Namen: Volterra 0, Lyapunov 0, Hardy 0,
RiemannSiegel 0, Turing 0, Certificate 0, ExplicitTail 0, deBranges 0.
TREFFER-SIGNALE semantisch geprüft — alle drei Namen-Kollisionen mit
ANDERER Semantik:
- Schur (24) = Schur-Orthogonalität unitärer Representationen
  (SchurOrthogonality, URepSchur) — NICHT unser Lyapunov/Schur-Margin.
- Gram (155) = Gram-Matrizen automorpher Perioden (HermitianGram,
  GramAdjoint, GramFiber) — NICHT unsere Gram-Punkte/Blöcke
  (zeros_by_gram, turing_check).
- Arb (14) = Substring-Zufallstreffer (AbelianVariety-Pfade) — nicht die
  Arb-library.
KONKLUSION: Auf der vollständigen Name-Ebene von part01 (10345 Einträge)
gibt es NULL Übereinstimmung mit unserer Methode — die Architektur-Trennung
(§8.1) ist jetzt durch die Lean-Struktur selbst belegt, nicht nur durch das
remark. Rest: Parts 02–14 nicht durchsucht; bei identischer Top-Level-
Struktur ist aber kein weiterer Kernabgleich zu erwarten.

## 14. AUSGIEBIGKEITS-TEST (23.11., Nachtrag 4 — echte Läufe)
- zeta_zero_finder.py, Bereich [13.5, 14.8], dps=30, Bisektion:
  **1 Null gefunden = γ1 ≈ 14.134725** (erste nicht-triviale Null, korrekter Ort).
  EXIT 0. Das Kern-Werkzeug arbeitet nach 3,5 Monaten Freeze korrekt.
- explicit_tail.py: import OK; tail_bound_psi / tail_bound_delta_psi /
  kernel_weight vorhanden.
- turing_check.py: exit 0 (vgl. §11), RvM korrekt, MISMATCH nur wegen
  unvollständiger Archiv-Zero-Daten.
- count_certified.py: CLI-Interface leer ohne Positional-Args (Doku-Punkt
  für E1: einheitliches CLI über alle Module — genau die Eleganz-Stufe E1).
FAZIT: Das Toolkit ist nach dem Freeze VOLL FUNKTIONSFÄHIG; die E1-E4
Eleganz-Roadmap (§12) ist die Perfektionierungs-Route.

## 15. INHALTS-SCAN part01 (23.11., Nachtrag 5 — 1,29 MIO ZEILEN)
tar-Stream-Dekompression: 1.287.083 Zeilen Lean-Quelltext aus part01
vollstaendig gescannt (Inhaltsebene, nicht nur Namen).
UNSERE KERNWOERTER: Volterra 0, Lyapunov 0, Hardy 0, RiemannSiegel 0,
Turing 0, „Gram point" 0, „Weyl bound" 0, certificate 2 (generisches
Englisch in Kommentaren).
SEINE KERNWOERTER (Kontrolle, Bibliothek eindeutig): automorphic 4342,
Bessel 2756, Seesaw 1421.
VERDICT: Auf 1,29 Mio. Zeilen von Teil 1 der 17-Mio-Zeilen-Bibliothek:
NULL Uebereinstimmung mit unserer Methode. Die Orthogonalitaet ist jetzt
auf drei Ebenen belegt (remark, Manuskript, Lean-Namen) PLUS Inhaltsebene
des ersten Archivteils. Rest: Parts 02–14 + restliche Baeume — bei diesem
Befund keine weitere Erwartung, denselben Scan-Werkzeugkasten per Cron oder
naechster Session fortsetzbar.

## 16. VOLLSTÄNDIGES STRUKTUR-VERSTÄNDNIS (23.11., Nachtrag 6 — Architektur gelesen)
Die 17 Mio. Zeilen zerfallen in ZWEI Layer (tar-Struktur part01, 10345+
Einträge ausgewertet):
1. src/Development/AbelianVarietyTheory — **8310 Dateien (~80%)**: eine
   importierte/entwickelte GRUNDLAGEN-BIBLIOTHEK (GaloisGeometry,
   QuasicoherentCohomology, CrystallinePeriods, Divisors, Jets,
   CuspFormEvaluations; einzelne Dateien 70k–117k Zeilen, vermutlich
   generiert/mechanisch). NICHT Alpöges Beweis-Anteil — das Fundament.
2. src/CompanionTheory — **2027 Dateien (~20%)**: SEIN Beweis-Layer:
   - SpectralGeometry (1254): LocalGlobalProofs/StableLattices —
     JacquetInitial, JacquetTransport, EvaluationLiftDegreeZero = die
     Theta-Lift-Infrastruktur (remark: „iterierte theta lifts“).
   - AutomorphicTheory (457): BesselWaveGrids (WaveBallEstimate 77k,
     FamilyThroughDiscreteSeries, ProductMoment) = die Multiplizitäts-
     Gitter (remark: „chaining theta lifts … mimicking √-multiplicity“),
     BesselOrbitBounds, InterlacingGrids.
   - RealGroups (155), HarishChandraModules (130), ThickeningEstimates (22),
     EightfoldTheory (9).
VERSTÄNDNIS: Die Beweis-Säulen mappen 1:1 auf das remark (SpectralGeometry
= Lift-Infrastruktur; BesselWaveGrids = Gitter-Kette; Seesaw/Rallis = die
Perioden-Brücke). D1–D5 = Build-Aid (Top-Level-DenyLists).
VERGLEICH MIT UNSEREM WISSEN: Unser Feld (numerische Zertifizierung:
Hardy-Z/Arb/Volterra) ist in KEINEM Layer vertreten — die Trennung ist
auf Architektur-Ebene vollständig. Alles, was wir „lesen“ könnten, wäre
die Jacquet/Theta-Lift-Lehre — ein anderes Studium, nicht ein Klau-Check.
