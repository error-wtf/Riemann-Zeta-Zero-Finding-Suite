# RH formal-proof and provenance audit — 2026-11-23

**Scope:** Riemann–Zeta–Zero-Finding-Suite only. No Segmented Spacetime
claims, code or proof-status counts enter this audit.

**Scientific status:** a mathematical RH **candidate**, not an accepted RH
proof and not a Lean-certified proof. A successful symbolic test only proves
the stated finite algebraic identity; a green CI job is not an RH certificate.

## 1. Exact Weyl/Schur sign gate

The canonical candidate defines

```text
alpha = eta + i beta
A_minus = [[-p, i], [-i P, i alpha]]
J_minus = q diag(-1, (1+k)/P)
p = Phi', P = Phi'', Pp = Phi''', q' = 2(p-beta)q, k' = kp
T = (2 p P - Pp)/P.
```

Taking the **Hermitian adjoint** (not a plain transpose), the full residual
`H_minus = J_minus' + A_minus^* J_minus + J_minus A_minus` is

```text
H_minus = q [[2 beta,             i k],
             [-i k, ((1+k)(T-4 beta)+kp)/P]].
```

For `beta != 0`, `P != 0`, the Schur complement (of the 11-entry) is

```text
Schur(H_minus) = q/P * [(1+k)(T-4 beta)+kp - P*k^2/(2 beta)].
```

The coefficient **4 beta** is fixed by two contributions: `-2 beta`
from `q'` and `-2 beta` from the sum of the diagonal entries
`(i alpha)^* + (i alpha)`.

The user-supplied `SchurHminus.lean` file (received 2026-11-23; not
present in the repository's current `main`) instead postulates

```text
H22 = q*((T-2 beta)*(1+k)+kp)/P.
```

That is a *different premise*. Relative to the actual residual,

```text
H22(actual) - H22(2-beta) = -2 beta*q*(1+k)/P.
```

Thus proving a Schur-complement identity **conditional on that premise**
cannot certify the candidate's actual operator. This is an **identified
source-to-formalization discrepancy**, not an established error in the
canonical Python/Markdown `4 beta` formula.

Reproduction:

```bash
python -m pytest -q tests/test_rh_schur_provenance.py tests/test_residue_identification.py
```

The new regression independently reconstructs `H_minus` instead of
calling `left_residual_identity()` as an oracle. A negative control rejects
the `2 beta` substitution.

## 2. Uploaded Lean material: admission status

These files were provided for review but **are not part of the repository
tree on main** as of this audit. They have **not** passed a reproducible,
repo-pinned Lean/Mathlib build in this audit.

| Source | Specific issue / evidence needed | Eligible for RH closure? |
| --- | --- | --- |
| `SchurHminus.lean` | `T-2 beta` premise disagrees with the canonical `T-4 beta` left residual | **No** until corrected and derived from the canonical matrices |
| `E067RH_Volterra.lean` | V1/V2 depend on derivative hypotheses; V2's `(hexp.mul hI).neg` has to be matched to the **negated** `uPlus` function, not the unnegated product | **No** until type-check/build and integration assumptions closed |
| `VolterraCore.lean` | Difference identity assumes integrability of the actual weighted source; zero consequence assumes the **full** transform integral is zero | Conditional lemma only |
| `RhReduction.lean` | `rh_from_right_nonvanishing` assumes nonvanishing of zeta throughout `Re(s)>1/2` (except the pole); the premise must itself be proved | Conditional reduction only |
| `CheckApex.lean` | Imports `Main`; no corresponding Lean project or `Main` module on current repo main. Need exact source of exported `riemannHypothesis` and full dependency closure | **Not verified** |
| `CheckFormB.lean`, `CheckLandau.lean`, `CheckReduction.lean`, `ImportInventory.lean` | Imports and local toolchain from another project; ensure source modules exist and expose every substantive premise | **Not verified** |

The supplied `lean-toolchain` names Lean `v4.33.1`. This alone does
not pin Mathlib or demonstrate that the files build. Only a complete
`lakefile` + lockfile + clean `lake build`, with theorem statements
and `#print axioms`, can establish a reproducible formal checkpoint.
Even then, a proof of `P -> RH` does not prove RH until `P` is proved.

## 3. Proof-dependency gates (separate evidence levels)

1. **Definitions / provenance:** derive the source `theta`, exact
   `Xi(alpha)` normalization and the `s=1/2+i alpha` bridge from
   `xi(s)`; match every constant to primary definitions.
2. **Analytic Volterra domain:** prove integrability of the *actual*
   kernel for all relevant complex `alpha`, differentiation under the
   integral and both boundary conditions.
3. **Algebraic evolution:** prove that the Volterra states solve the
   first-order system; link the exact reflected system and true
   Hermitian residual. This audit addresses **only** the finite Schur
   algebra in this gate.
4. **Global positivity:** check that the compact, far-field and Sturm
   certificates certify the exact `4 beta` Schur expression on the
   complete parameter domain. Certificate hashes alone do not prove
   a theorem unless checkers and hypotheses are validated.
5. **Green/endpoint bridge:** prove regularity, reflected trace matching,
   orientation signs and the actual improper limits of both fluxes.
6. **RH closure:** derive nonvanishing for the required open half-strip
   without inserting equivalent nonvanishing as an assumption; finish
   with the completed-zeta symmetry and nontrivial-zero localization.

A conditional Lean theorem may be catalogued as **FORMALLY_PROVED_CONDITIONAL**,
but not as **RH_PROVED**. A symbolic or numerical script receives only
**SYMBOLIC_CHECK** or **NUMERICAL_CHECK**, respectively.

## 4. Integration policy

Before adding uploaded Lean files as certificates, put a *separate*
Lean package under `formal/`, pin Lean and Mathlib versions, provide a
clean build and guard each proposed physical/analytic instantiation
against the exact theorem source. Never infer a whole-RH result from
`#print axioms` alone: the statement, hypotheses and transitive
dependencies also require review.

No part of this audit changes the canonical proof manuscript or upgrades
its status. An independent mathematical review remains necessary.
