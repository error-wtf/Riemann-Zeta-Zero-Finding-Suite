# READ-THE-PROOF PLAN — Alpöge-Lean-Bibliothek vollständig lesen
Status: PROJEKT-PLAN (Start 2026-11-23). Ziel: die 17.374.394 Zeilen der
Alpöge-Lean-Bibliothek (14 Parts, /home/error/alpoge_lean/) WIRKLICH lesen
und verstehen — Datei für Datei, mit Leseprotokoll je Datei.
Ehrliche Ausgangslage: NICHT gelesen bisher — nur Architektur-Scan (2 Layer),
44.048 Namen, 161.876 Theorem-Deklarationen klassifiziert, 1,29 Mio. Zeilen
Wort-Scan. „Vollständig lesen und verstehen" beginnt mit diesem Plan.

## Die zwei Layer (Architektur, gelesen)
1. src/Development/AbelianVarietyTheory — 8310 Dateien (~80%):
   importierte/entwickelte Grundlagen-Bibliothek (GaloisGeometry,
   QuasicoherentCohomology, CrystallinePeriods, Divisors, Jets,
   CuspFormEvaluations). Einzeldateien bis 117k Zeilen (vermutlich
   generiert/mechanisch — zu prüfen bei der Lektüre).
2. src/CompanionTheory — 2027 Dateien (~20%): DER Beweis-Layer:
   - SpectralGeometry (1254): StableLattices/Jacquet-Kette
     (JacquetInitial, JacquetTransport, EvaluationLiftDegreeZero)
   - AutomorphicTheory (457): BesselWaveGrids (WaveBallEstimate,
     FamilyThroughDiscreteSeries, ProductMoment), BesselOrbitBounds,
     InterlacingGrids, BesselMapUniqueness
   - RealGroups (155), HarishChandraModules (130), ThickeningEstimates (22),
     EightfoldTheory (9)
   BuildAid (5): DenyList-Infrastruktur, keine Mathematik.

## Leseprotokoll-Format (je Datei, in docs/READ_LOG.md)
- Dateipfad + Zeilenzahl + Lesedatum
- Zweck der Datei (1 Satz)
- Die Hauptsätze (Theorem-Namen + Aussage in eigenen Worten)
- Abhängigkeiten (imports/Verweise auf andere Dateien)
- Offene Verständnisfragen
- Verständnis-Level: GELESEN_VERSTANDEN / GELESEN_TEILWEISE / GESKIMMT

## Etappen (Reihenfolge nach Beweis-Relevanz)
E1 CompanionTheory-Kernkette (priorisiert):
   1. AutomorphicTheory/BesselWaveGrids (Kernkette, ~50 Dateien)
   2. SpectralGeometry/StableLattices/Jacquet-Kette (~30 Dateien)
   3. BesselOrbitBounds + InterlacingGrids + BesselMapUniqueness
E2 CompanionTheory-Rest (AutomorphicTheory-Rest, RealGroups,
   HarishChandraModules, ThickeningEstimates, EightfoldTheory)
E3 Development-Strukturlesung (8310 Dateien: Kapitel-für-Kapitel,
   generierte Dateien skimmen + Struktur protokollieren — hier ist
   GESKIMMT ein ehrliches Level, nicht „gelesen")
E4 Cross-Check: die gelesene Kette gegen die remark-Timeline mapen
   (welche remark-Zeile entspricht welcher Datei-Gruppe).

## Messbare Fertigstellung (keine Schein-Claims)
- docs/READ_LOG.md mit Eintrag je Datei (kein Batch-Fake)
- Verständnis-Level-Summe am Ende je Etappe
- Ehrliche Rest-Klassifikation (GESKIMMT zählt NICHT als GELESEN)

## Verhältnis zum Alpöge-Vergleich
Der Leseprojekt-Zweck ist VERSTEHEN — nicht der Klau-Check (der ist mit
Architektur+Namen+Deklarationen+Wort-Scan vierfach belegt: null Übereinstimmung).
Das Verstehen der Methode (Stepanov-Nachfahre + Theta-Lift-Ketten + Seesaw)
ist eigenständiger Wert: wir lernen die automorphe Beweis-Welt, unabhängig
von der Güte-Frage des Beweises.
