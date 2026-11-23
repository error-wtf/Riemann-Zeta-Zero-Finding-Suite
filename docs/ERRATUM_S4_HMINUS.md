# ERRATUM zu RH_PROOF_CANDIDATE_COMPLETE.md, §4 — (2,2)-Eintrag von H₋

**Datum:** 2026-11-23 · **Status:** CONFIRMED_BY_KERNEL_CHECK · **Freeze:**
`rh-candidate-v1` bleibt unverändert (Begleitnotiz, wie ERRATUM_S4_H22.md).

## Befund

Das Doc behauptet (§4, J₋ = q·diag(−1, (1+k)/P)):

    H₋ = q·[[2β, ik], [−ik, ((1+k)(T−4β) + k′)/P]].

Die kernel-geprüfte Rechnung (`docs/LEAN_BRIDGE/LyapunovEntriesHminus.lean`,
Satz `Hm22_entry`, exit 0, Axiome [propext, Classical.choice, Quot.sound])
liefert:

    (H₋)₂₂ = ((1+k)(T − 2β) + k′)/P.

**Diskrepanz: das Doc zählt die β-Korrektur doppelt (T−4β statt T−2β).**
Dies ist das Spiegelbild des H₊-Findings (ERRATUM_S4_H22.md): dort fehlte
die Korrektur (T statt T−2β), hier ist sie doppelt. Gemeinsame Ursache in
beiden Fällen: q′ = 2(Φ′−β)q — die (1,1)-Einträge (Satz `H11_entry`) und
die α-Kreuzterme (Satz `H22_cross`, Hebung zu 0) sind korrekt.

## Struktur, die bleibt

Die Schur-Form des Docs ist strukturrichtig: H₁₂H₂₁ = (iqk)(−iqk) = q²k²
reell-positiv (Satz `schur_structure`), also Schur(H₋) = (q/P)·G_β mit der
**korrigierten** G_β:

    G_β = (1+k)(T − 2β) + k′ − P·k²/(2β).

Die Positivitäts-Zertifikate des Docs (0 < P < 40, T > 500x auf [0,1/2];
P > 0, T > 2 für x ≥ 1/2; Sturm-Korrekturen) müssen gegen die korrigierte
G_β neu ausgewertet werden: der Term (1+k)·2β macht die Bedingung STRENGER
als die Doc-Version. Die Frage, ob die Zertifikate die Doc-G_β oder die
korrigierte G_β rechnen, ist die offene Prüf-Aufgabe (wie beim H₊-Finding).

## Statusvokabel

- Doc-§4-Formel H₋-(2,2): **FAILED → CORRECTED** (durch dieses Erratum).
- Lean-Sätze `Hm22_entry`, `schur_structure`: **VERIFIED**.
- H₋-Positivität als Ganzes: weiterhin **OPEN** mit strengerer Bedingung.
- Beide §4-Findings zusammen deuten auf eine systematische β-Quellen-
  Verwechslung im Doc-Prosa-Teil (q′ ohne β in H₊, β doppelt in H₋) —
  die korrigierte Auflage sollte beide Einträge aus der Lean-Kette
  regenerieren statt neu handrechnen.
