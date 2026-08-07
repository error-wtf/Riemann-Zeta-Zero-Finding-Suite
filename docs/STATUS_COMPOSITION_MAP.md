# Status composition map

The repository deliberately exposes both local lemma diagnostics and a
canonical theorem-composition layer. They answer different questions and
must not be read as contradictory global verdicts.

| Layer | Example | Meaning |
| --- | --- | --- |
| Local theorem status | `endpoint_flux_status()["global_endpoint_flux"] == "PROVED_CERTIFIED"` | The helper is proved for the canonical profile, parameter range and exact certificate inputs tested in its contract. |
| Matching module | `matching_identity()["coupled_halfline_energy"] == "PROVED_CERTIFIED"` | The reflected energy step is certified by the named exact certificates and regularity checks. |
| Canonical composition | `repository_theorems.repository_endpoint_theorem_schema()` | Composes source, profile, certificate and quantifier obligations and reports `PROVED` on the declared theorem domain. |
| Final public claim | RH status | Remains `CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW`; internal composition is not community acceptance. |

The intended reading is:

```text
PROVED_CERTIFIED in the certified canonical domain
  + explicit theorem/certificate dependencies
  + canonical composition gate
  = PROVED on the declared theorem domain
```

`PROVED_CERTIFIED` records that the canonical profile, parameter range,
regularity checks and exact certificates have been tested and composed. The
profile and parameter range are the theorem's declared domain, not unresolved
"hypotheses" left open by the implementation. It is not the same as an
external community acceptance claim. The composition layer is the place where
the full dependency graph is assembled. The
`composition_note` and `status_scope` fields make this distinction
machine-readable.

The historical one-sided trace diagnostic remains `OPEN` and is not a
dependency of the canonical two-sided Volterra state-matching route.
