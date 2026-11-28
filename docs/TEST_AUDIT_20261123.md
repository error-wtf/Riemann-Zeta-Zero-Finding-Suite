# Test-Audit 2026-11-23 (vollständiger Lauf, HEAD `98749a8`+)

## Python-Suite (pytest tests/, 3.4 s)

**116 Tests: 109 passed · 5 skipped · 1 FAILED**

Der eine FAILED (`test_theta_derivative_series.py::test_direct_series_
matches_independent_diagnostic`) ist **vorbestehend** (Datei seit Commit
`5860c83` "non-circular spectral operator laboratory" unverändert; von der
Lean-Bridge-Session nicht berührt). Präzise Klassifizierung aus der
Traceback:

    s_phi_from_series(0.7, terms=80, dps=40) = 0.76561887465633505
    S_phi(0.7)                               = 0.76561887465633414
    rel. Differenz ≈ 1.2e-16, Test verlangt 1e-20.

Beide Pfade stimmen bis ~15 Stellen überein; die 80-Term-Reihe erreicht bei
x = 0.7 die 1e-20-Schärfe nicht (Konvergenz-Marge, kein Widerspruch der
Pfade). **Nicht still repariert** (kein Fit, kein Test-Schärfen ohne
Ursachenkenntnis): offen als NUMERIC_CONVERGENCE_MARGIN. Options für die
Folge-Auflage: terms skalieren, x-abhängige Termzahl, oder Schärfe an
erreichte Präzision koppeln — Entscheidung mit Herleitung, nicht per Patch.

## Lean-Seite (6/6 grün)

Alle Module exit 0, kein sorryAx, Grundaxiome only (Einzellauf + lake-
Targets): RhReduction, P0NoGo, VolterraCore, EnergyReduction,
LyapunovEntries, LyapunovEntriesHminus.

## Alpöge-Referenz-Build

Läuft (8773/12913, 0 Fehler-Zeilen im Log; Clean-Re-Verifikation bei Ende
geplant wegen Log-Kontamination durch den toten Erstversuch-Job).

## Vorher → Nachher (Repo-Zustand, belegt über git-Historie)

| Aspekt | Vorher (bis 2026-11-22) | Nachher (23.11., Session) |
|---|---|---|
| Kernresultate | Prosa-Docs (§2–§4) ungeprüft | 6 kernel-verifizierte Lean-Module |
| §4-Matrizen | Handrechnung, unkontrolliert | **2 Fehler kernel-bewiesen** (H₊ fehlt −2βP; H₋ β doppelt), 2 Errata |
| Alpöge-Referenz | „nicht durchsucht" (§6) | 14/14 Tarballs verifiziert, ~5.372 Z. Kernkette gelesen, Zirkularität kreisfrei |
| Testbasis | Suite existierte, 1 Test rot ungeklärt | 116 Tests vermessen, FAILED präzise klassifiziert + offen dokumentiert |
| Provenienz | implizit | BINDEND verankert (Memory + PROVENANCE_AND_SCOPE.md) |
| Eleganz | — | Kernel-Zertifikate statt Verdrahtungs-Fabrik: eigene Module 40–92 Z. vs. Alpöge 94:1-Varianten |

Commits dieser Session: 16, alle additiv (kein Freeze angetastet).
