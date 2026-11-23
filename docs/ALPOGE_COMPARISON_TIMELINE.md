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
1. Unsere letzte öffentliche State (07.08.2026) liegt VOR Alpöges Ankuendigung,
   aber ALLE seine Kernideen sind laut eigener Timeline Juni–November 2026
   datiert — d.h. Teile vor, Teile nach unserem Freeze.
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
