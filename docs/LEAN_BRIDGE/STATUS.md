# Lean-Bridge — verifizierte Lean-Module des Repositories

**Datum:** 2026-11-23
**Status:** VERIFIED (kernel-geprüft, Einzellauf + lake-Target)
**Toolchain:** leanprover/lean4 v4.35.0-rc4 + mathlib master (Projekt: /home/error/math-verify)
**Autor:** Bingsi AI (Auftrag Lino Casu)

## Was das ist

Der Start der Option C aus `ALPOGE_COMPARISON_TIMELINE.md` (Lean-Bücke): die
Kern-Identitäten und No-Go-Sätze des Kandidaten werden als eigenständige,
kernel-verifizierte Lean-Module formalisiert — unabhängig von Alpöges
Bibliothek, kompakter Stil (Kapselung statt Varianten-Fabrik).

## Die drei Module (alle exit 0, Axiome = [propext, Classical.choice, Quot.sound],
kein sorryAx, kein eigenes axiom, kein native_decide)

| Modul | Inhalt | Zeilen | Verifikation |
|---|---|---|---|
| `RhReduction.lean` | RH-Reduktion: ζ ≠ 0 auf Re(s) > 1/2 ⇒ jede Null auf der kritischen Linie oder trivial. Eigene `CritOrTrivial`-Definition + gekapselter Vorfaktor (`prefactor_one_sub_ne_zero`) mit ehrlicher Nichttrivialitäts-Hypothese (cos-Fall s = −2k, k ≥ 1). | 91 | `lake env lean` exit 0; `lake build Mathverify.RhReduction` success (9039 jobs) |
| `P0NoGo.lean` | Der Kern von `P0_GLOBAL_MULTIPLIER_NO_GO.md` als Maßtheorie-Satz: q ≥ 0 stetig, ∫ q·f² = 0, f ≠ 0 fast überall ⇒ q ≡ 0. Beweis in 3 Schritten (Integral→a.e.; Maß-Vererbung {q≠0} ⊆ {g=0} ∪ {f=0}; Stetigkeit + `IsOpen.measure_pos`-Widerspruch). | 60 | `lake env lean` exit 0; `lake build Mathverify.P0NoGo` success |
| `VolterraCore.lean` | §2 des Manuskripts: `volterra_difference_identity` (u₋(x) − u₊(x) = e^{−iαx}·∫e^{iαy}θ(y)dy) + `volterra_states_equal_at_zero` (Trace-Ledger Schritt 5: bei Ξ(α) = 0 sind beide Zustände gleich). Beweis via `setIntegral_union` + `Iic_disjoint_Ioi` + `ring`. | 60 | `lake env lean` exit 0; `lake build Mathverify.VolterraCore` success |
| `EnergyReduction.lean` | Lemma 2 der Energie-Seite (algebraischer Kern): mit `a·Φ'' = h·e^{2Φ}` und der Produkt-Ableitungs-Expansion ist `R_a = e^{2Φ}·h'` (die 2Φ'-Terme heben sich exakt) + `weighted_split` (Summen-Spaltung bei S_Φ ≥ 0). | 41 | `lake env lean` exit 0; `lake build Mathverify.EnergyReduction` success |

## Verifikations-Kommandos (reproduzierbar)

```bash
export PATH="$HOME/.elan/bin:$PATH"
cd /home/error/math-verify
lake env lean Mathverify/RhReduction.lean    # exit 0, Axiom-Info am Dateiende
lake env lean Mathverify/P0NoGo.lean         # exit 0
lake env lean Mathverify/VolterraCore.lean   # exit 0
lake build Mathverify.RhReduction Mathverify.P0NoGo Mathverify.VolterraCore
```

Jedes Modul endet mit `#print axioms` aller Hauptsätze — die Axiom-Listen sind
damit Teil der Datei (Zertifikatszeilen), nicht des Berichts.

## Eleganz-Vergleich mit der Alpöge-Bibliothek

Alpöge/Claude lösen dieselbe Reduktion (RH ⇔ ζ ≠ 0 auf Re > 1/2) in
`RhOfRight.lean` mit 62 Zeilen, wobei die triviale Nullstellen-Seite als
Separates Statement-Argument (`htriv`) durchgereicht wird. Unsere Version:
(a) `CritOrTrivial` integriert die negative-ganzzahlige Seite — der
Re(s) < 1/2-Fall startet mit einem `by_cases`, das diesen Fall sofort erfüllt,
das separate `hnat`-Zwischenlemma entfällt; (b) der Vorfaktor ist gekapselt
mit expliziter Nichttrivialitäts-Hypothese (der cos-Faktor ist bei s = −2k
wirklich null — wir machen die Beweislast sichtbar statt sie zu verstecken);
(c) Axiom-Zertifikate gehören zur Datei.

Struktur-Befund aus der Alpöge-Lesung (siehe `ALPOGE_LEAN_READSTATE.md`):
die Bibliothek ist stark assembly-artig (167 Lemmata-Verzeichnisse, davon 94
Cauchy-Binet-Varianten) — unser Kapselungs-Stil ist nachweislich möglich und
senkt die Verdrahtungslast.

## Fehlerhistorie (ehrlich, Teil der Abnahme)

- RhReduction: 3 Korrekturrounden. Runde 1: eigener `hnat`-Ansatz mathematisch
  falsch (ζ(−ungerade) ≠ 0 — negative ganze Zahlen sind ein Erfüllungsfall,
  kein Widerspruchsfall); Runde 2: Funktionalgleichung muss bei `1 − s`
  instanziiert werden (Mathlib-Normalform `riemannZeta (1 - (1 - s))`); Runde 3:
  toNat-ℂ-Cast via `omega` + `exact_mod_cast`.
- P0NoGo: 2 Runden. Runde 1: Punktargument `f x ≠ 0` reicht nicht — der
  Beweis läuft über Maß-Vererbung ({q≠0} ⊆ {g=0} ∪ {f=0}, beide Maß null);
  `sq_ne_zero` heißt heute `sq_eq_zero_iff`, Kontraposition `.not.2`;
  `Metric.isOpen_iff` liefert 2-Tupel (B + B > 0); `measure_mono` mit 1 Arg;
  Widerspruch über `hcontra`-Kette (ℂ/ENNReal: kein linarith).
- VolterraCore: 3 Runden. ℂ-Coercion-Falle (`fun y` ohne Annotation bindet ℂ
  durch die `Complex.I * α * y`-Kette); `setIntegral_add_compl` gehört zur
  VectorMeasure-∫ᵛ-API (falsche Schicht) → `setIntegral_union` +
  `Iic_disjoint_Ioi le_rfl` + `← setIntegral_univ` als Notations-Brücke;
  `sub_eq_zero` statt `linarith` (ℂ hat keine Ordnung).

## FINDING 23.11. — §4-(2,2)-Eintrag (kernel-geprüft, aufgelöst)

`LyapunovEntries.lean` verifiziert: **(H₊)₂₂ = q·(2Φ′P − 2βP − Φ‴)/P²**.
Das Doc (RH_PROOF_CANDIDATE_COMPLETE §4) behauptet q·(2Φ′P − Φ‴)/P² = q·T/P
(mit T = (2Φ′Φ″ − Φ‴)/Φ″, P = Φ″ aus §1 — Definitionen geprüft, ändern nichts).

**Differenz: −2βq/P.** Die (1,1)-Einträge stimmen exakt (2βq ✓), die
α-Kreuzterme heben exakt (0 ✓). Der Fehler: q′ = 2(Φ′−β)q wurde im (1,1)-
Eintrag korrekt verarbeitet (−q′ + 2qΦ′ = 2βq), im (2,2)-Eintrag der Doc-
Formel aber der −2βq/P-Anteil von (q/P)′ verschluckt.

**KONSEQUENZ — AUFGELÖST (23.11., zweiter Check):** Die Python-Seite
(`src/hedenmalm/weyl_lyapunov.py`, 37 Z. komplett gelesen) benutzt eine
ANDERE J (a·diag(−Φ″, 1) — ohne q und ohne 1/P, Hedenmalm-Diagnostik-Linie)
und berechnet H nur generisch-symbolisch (`lyapunov_residual`); ihr eigener
Status: `positive_J_or_H: CONDITIONAL_ON_RESIDUE_IDENTIFICATION`,
`rh_conclusion: CONDITIONAL_ONLY`. **Es gibt KEIN Python-Zertifikat, das die
Doc-§4-H₊-Formel benutzt** — der Fehler war prosaisch und stand
ungeprüft neben der offenen Positivitäts-Frage. **Urteil: Doc-§4-(2,2)-Formel
= Rechenfehler im Prosa-Text (−2βP-Term verschluckt), KEIN Zertifikats-Impact;
Doc-Korrektur nötig; die korrekte (strengere) Positivitäts-Bedingung ist
kernel-geprüft in LyapunovEntries.lean.** Statusvokabel: FAILED→CORRECTED
(für die Doc-Formel), Lean-Satz VERIFIED.

**ZERTIFIKATS-FRAGE für H₋/G_β — AUFGELÖST (23.11., dritter Check):** Die
Python-Positivitäts-Zertifikate BENUTZEN die Doc-G_β mit T−4β
(`residue_identification.py:83,89`, `scaled_left_correction.py:26`). Aber:
G_korr = G_doc + 2β(1+k) > G_doc (kernel-geprüft in `GbetaMonotone.lean`,
Sätze `G_korr_identity` + `G_korr_positive`, exit 0, Target success). Die
zertifizierte Positivität der KLEINEREN Funktion impliziert die der korrekten
— **Zertifikate bleiben gültig (konservativ-valide)**; zu korrigieren ist nur
die Notation (Doc + Python-Kommentare auf T−2β).

## Nächste Schritte (Lean-Ziel 4)

Energie-Lemma 1/2 aus `ENERGY_PROOF_DRAFT.md` (§3): `R_{a_h} = e^{2Φ}·h'`
unter `a_h = h·e^{2Φ}/Φ''` — **ERLEDIGT** (siehe `EnergyReduction.lean`,
kern-verifiziert mit Ableitungswerten als Hypothesen-Schnittstelle).
Weiter: §4-Matrixidentitäten (H₊ = J₊' + A*J₊ + J₊A₊ = q·diag(2β, T/P))
als 2×2-Matrix-ring-Sätze mit deklarierten Ableitungs-Gleichungen.
→ **ERLEDIGT** (LyapunovEntries.lean) + FINDING oben.
