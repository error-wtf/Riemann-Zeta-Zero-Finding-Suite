# ERRATUM zu RH_PROOF_CANDIDATE_COMPLETE.md, §4 — (2,2)-Eintrag von H₊

**Datum:** 2026-11-23 · **Status:** CONFIRMED_BY_KERNEL_CHECK · **Freeze:**
`rh-candidate-v1` bleibt unverändert; dieses Erratum ist die korrekte
Begleitnotiz (keine Umbenennung, kein Umbau des Frozen-Documents).

## Befund

Das Doc behauptet (§4, mit q = e^{2Φ−2βx}, q′ = 2(Φ′−β)q, P = Φ″, P′ = Φ‴,
J₊ = q·diag(−1, 1/P)):

    H₊ = J₊′ + A*J₊ + J₊A = q·diag(2β, T/P),  T = (2Φ′Φ″ − Φ‴)/Φ″
    ⇒ zweiter Diagonaleintrag: q·(2Φ′P − Φ‴)/P².

Die kernel-geprüfte Ring-Rechnung (`docs/LEAN_BRIDGE/LyapunovEntries.lean`,
Satz `H22_entry`, exit 0, Axiome [propext, Classical.choice, Quot.sound])
liefert dagegen:

    (H₊)₂₂ = q·(2Φ′P − 2βP − Φ‴)/P²  =  q·((2Φ′ − 2β)P − Φ‴)/P².

**Differenz: −2βq/P.** Der Term entsteht aus q′ = 2(Φ′−β)q im Produkt
(q/P)′ = q′/P − qP′/P²; er wurde im Doc-(2,2)-Eintrag verschluckt, während
derselbe q′ im (1,1)-Eintrag korrekt verarbeitet wird (−q′ + 2qΦ′ = 2βq ✓,
Satz `H11_entry`). Die α-Kreuzterme heben exakt zu 0 (Satz `H22_cross`).

## Provenienz-Check (kein Zertifikats-Impact)

Die Python-Seite `src/hedenmalm/weyl_lyapunov.py` benutzt eine andere,
diagnostische J (a·diag(−Φ″, 1), ohne q und ohne 1/P), berechnet H nur
generisch-symbolisch und weist die H-Positivität explizit als offen aus
(`positive_J_or_H: CONDITIONAL_ON_RESIDUE_IDENTIFICATION`,
`rh_conclusion: CONDITIONAL_ONLY`). **Kein Python-Zertifikat benutzt die
Doc-§4-H₊-Formel** — der Fehler war prosaisch und ohne Zertifikats-Berührung.

## Konsequenz (für die künftige Positivitäts-Nutzung)

Die korrekte zweite Diagonale ist um −2βq/P < 0 verschoben — jede künftige
H₊-Positivitäts-Bedingung (Green-Identität) ist gegenüber der Doc-Version
STRENGER. Korrigierte Lesart:

    H₊ = q·diag(2β, ((2Φ′ − 2β)P − Φ‴)/P²).

In der T-Notation des Docs (T = (2Φ′P − Φ‴)/P) heißt das konsistent:
**T_korr := T − 2β**, sodass H₊ = q·diag(2β, T_korr/P). Die Korrektur
gehört in die nächste Doc-Auflage (nach Freeze-Richtlinie: getrennte
Folgaversion), nicht in den Frozen-Snapshot.

## Statusvokabel

- Doc-§4-Formel (2,2-Eintrag): **FAILED → CORRECTED** (durch dieses Erratum).
- Lean-Sätze `H11_entry`, `H22_cross`, `H22_entry`: **VERIFIED**.
- H₊-Positivität als Ganzes: weiterhin **OPEN** (wie vom Doc selbst
  deklariert); die korrigierte Bedingung ist die zu benutzende.
