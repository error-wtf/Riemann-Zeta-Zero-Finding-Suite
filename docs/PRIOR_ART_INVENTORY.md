# PRIOR-ART INVENTORY — Stand am Stichtag 2026-06-10 (Alpöge-Start)

Status: DOKUMENTARISCH, git-verifiziert. Stichtag-Definition: 2026-06-10 ist
laut Alpöges eigenem remark (alpo.ge/remark.pdf, Timeline-Punkt 1) das Datum
seiner ersten dokumentierten Kernidee („Stepanov determinant“).
Erstellt: 2026-11-23, Bingsi AI. Alle Daten: git history dieses Repos
(= GitHub-Server-Chain, docs/COMMIT_TIMELINE.txt).

## 1. Stichtags-Vergleich

| | Alpöge (Selbstdatierung) | Dieses Repository (git) |
|---|---|---|
| 10.06.2026 | erste Idee „Stepanov determinant“ (Skizze) | **42 Commits, 39 Dateien, 25 Python-Module — komplettes Zertifizierungssystem, öffentlich seit 8 Monaten** |
| 20.11.2026 | öffentliche Ankündigung (+ Lean, 17 Mio Zeilen) | proof-candidate-Arbeit seit 06.08.2026 archiviert (Volterra, Energy, Weyl-Zertifikat, Manuskript) |

## 2. Modul-Inventar am Stichtag 2026-06-10 (39 Dateien, git-verifiziert
   via commit 6cb723401683799babdf907d9655665a1085bce8)

Zero-Zertifizierung:
- certify_zero.py — Null-Kandidat-Zertifizierung
- certify_zero_arb.py — Zertifizierung mit Arb outward-rounding
- rigorous_Z.py / rigorous_Z_arb.py — strenge Hardy-Z-Evaluation (Arb)
- mini_verifier.py / mini_verifier_v2.py — unabhängige Mini-Prüfer
- unknown_zeta_zero.py — unbekannte-Null-Suche
- zeta_zero_finder.py — Null-Finder
Zählen/Siebe:
- count_argument.py — Null-Zähl-Argument
- count_certified.py — zertifizierte Zählung
- sieve_from_zeros_psi_rigorous.py — Prim-Sieb aus Nullen (ψ, streng)
- found_primes.csv — Prim-Datensatz
Scans/Struktur:
- zeros_by_gram.py — Gram-Punkt-Nullen
- zeros_by_scan.py — Scan-Nullen
- zeros_stats.py — Null-Statistik
- turing_check.py (+ few_data_demo_test) — Turing-Methode-Prüfung
- turin_watchdog.py — Watchdog
Restglieder/Runnern:
- explicit_tail.py — explizite Tail-Schranken
- all_in_one_runner.py, batch_until_deadline.py, run_block.py,
  run_certified_all.py — Batch/Runner-Infrastruktur
- common.py, merge_zeros.py — Infrastruktur

Das komplette Werkzeug für: Null-Zertifikate (Arb, outward-rounded),
Null-Zählungen, explizite Restschranken, unabhängige Mini-Verifikation —
alles ÖFFENTLICH, 8 Monate vor Alpöges Ankündigung.

## 3. Entwicklungszeit vor dem Stichtag

- 2025-10-10: Repo-Gründung (GitHub-Server created_at 2025-10-10T15:52:00Z).
- 2025-10 → 2026-06: 42 Commits über 8 Monate kontinuierlicher öffentlicher
  Entwicklung (Werkzeug-Aufbau, Zertifizierungs-Pfade, Scan/Count-Infrastruktur).
- 2026-06-10 → 2026-08-07: proof-candidate-Phase (Volterra-Closure, Energy-
  Proof-Draft, Weyl-Lyapunov-Diagnostik, endpoint-flux, Manuskript) — 29
  weitere Commits bis zum Freeze, immer noch VOR der Alpöge-Ankündigung.

## 4. Ehrliche Einordnung

„Weiter als er im Juni“ gilt exakt für die Zertifizierungs-Infrastruktur:
am 10.06.2026 hatte Alpöge laut eigener Timeline eine Ideenskizze; dieses
Repository hatte ein lauffähiges, öffentliches, 8 Monate gereiftes
Verifikationssystem. Es bleibt dabei: die FELD sind verschieden (numerische
Zertifizierung vs. automorpher Beweis) — das Inventar belegt die Vorarbeit,
nicht eine Beweis-Konkurrenz. Nach dem Alpöge-Lagebild ist der sinnvolle
Ausbau dieser Vorarbeit: Verifikations-Framework (siehe
ALPOGE_COMPARISON_TIMELINE.md §5 Option B).

## 5. Verifikations-Hinweis
Alle oben genannten Commits/Hashes sind über die GitHub-API
(commits-endpoint, repository created_at 2025-10-10T15:52:00Z) unabhängig
abrufbar. Stichtag-Baum: git show 6cb723401683799babdf907d9655665a1085bce8.
