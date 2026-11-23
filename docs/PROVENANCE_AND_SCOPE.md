# Provenance and Scope — binding rules (2026-11-23, Lino)

**Verbindliche Anweisung: RH zuerst. SSZ separat. Wissenschaftliche
Provenienz strikt einhalten.**

## Scope-Trennung (BINDEND)

1. **Dieses Repository ist das RH-Projekt** (Riemann-/Volterra-Beweiskette,
   Lean-Bridge, Zertifikate). Die SSZ-/E-067-Arbeit ist ein **separates,
   eingefrorenes Projekt** (`/home/error/physics/SSZ_*`) und bleibt
   unverändert.
2. **Kein Transfer zwischen den Projekten:** keine SSZ-Lemmata als
   RH-Beweise zählen, keine RH-Ergebnisse in SSZ, keine gemeinsamen
   Dateien, Beweisregister, Verzeichnisse oder Statusberichte.
3. **Keine projektfremden Voraussetzungen oder Ergebnisse ungeprüft
   übernehmen.** Jede Eingabe in eine RH-Herleitung wird im RH-Kontext
   selbst belegt oder explicit als Hypothese markiert.

## Beweisdisziplin (BINDEND)

- **Keine Fits.** Interpolation/Polynom-Fits als Ersatz oder Baustein einer
  Herleitung sind unzulässig (FAIL CLOSED: fehlende Herleitung ⇒ Resultat
  bleibt offen).
- **Keine Zirkelschlüsse.** "Unabhängig" heißt: unabhängiger
  Herleitungspfad, nicht unabhängiger Code-Klon.
- **Keine unbegründeten Axiome.** Lean-Module dürfen nur die mathlib-
  Grundaxiome (`propext`, `Classical.choice`, `Quot.sound`) benutzen;
  jedes Modul trägt seine `#print axioms`-Zertifikatszeilen.
- **Keine unbelegten Vollbeweis-Behauptungen.** Statusvokabel strikt:
  VERIFIED / CONSISTENT / OPEN / FAILED / BLOCKED — ein Claim gilt nur mit
  reproduzierbarem Befehl + echter Ausgabe (Pfad + Zeile).

## Beweisregister (RH-Projekt)

- **Lean-Module (kernel-geprüft):** `docs/LEAN_BRIDGE/` — RhReduction,
  P0NoGo, VolterraCore, EnergyReduction, LyapunovEntries (alle exit 0,
  Grundaxiome, kein sorryAx; Fehlerhistorie in STATUS.md).
- **Offenes Finding:** §4-(2,2)-Eintrag — Doc-Formel q(2Φ′P−Φ‴)/P² vs.
  kernel-geprüfte Rechnung q(2Φ′P−2βP−Φ‴)/P² (Differenz −2βq/P);
  Zertifikate-vs-Doc-Check ausstehend.
- **Alpöge-Lesung (Referenz, kein Beweisanteil):**
  `docs/ALPOGE_LEAN_READSTATE.md` — rein dokumentarisch, orthogonale
  Methoden, kein Transfer.

## Status (23.11.)

RH-Kette: 5 kernel-verifizierte Module + 1 offenes Finding (§4-H₂₂) +
laufende Gesamtverifikation der Alpöge-Referenzbibliothek (Full-Build).
Kein Vollbeweis-Claim. Nächster Schritt: Zertifikate-vs-Doc-Check.
