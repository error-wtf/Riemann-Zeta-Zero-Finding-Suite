# Prime-frequency and recurrence research roadmap

This is follow-up research, separate from the RH proof-candidate dependency
graph. The current repository contains two reproducible explanatory GIFs and
the portal contains the corresponding live finite-sum animation.

## Current state

| Work item | Status | Boundary |
|---|---|---|
| Dirichlet partial-sum GIF | `REPRODUCIBLE_VISUAL` | finite computation only |
| Prime-frequency spectrum GIF | `REPRODUCIBLE_VISUAL` | finite computation only |
| (\log n=\sum_p v_p(n)\log p) | `EXACT_IDENTITY` | elementary factorisation |
| No common finite prime period | `EXACT_IDENTITY` | uses (2^m\ne3^n) |
| Prime phase torus | `PLANNED` | interactive portal visual |
| Recurrence search | `PLANNED` | numerical experiment |
| Zero-spacing statistics | `PLANNED` | data-dependent experiment |
| Pair correlation | `PLANNED` | data-dependent experiment |
| Explicit-formula comparison | `PLANNED` | numerical comparison only |
| Xi/Theta spectrogram | `PLANNED` | visual analysis only |
| (z=8)/(20) defect plot | `PLANNED` | only certified if inputs are loaded |

## Interpretation rule

An animation illustrates a finite truncation. It does not prove convergence,
almost-periodicity in the critical strip, a zero location, or RH. Any future
module must keep those claims separate in its output metadata and tests.

## Next implementation order

1. prime phase torus and exact phase-error score;
2. finite recurrence search with the uniform truncated-sum bound;
3. zero-spacing and pair-correlation plots from an explicit input file;
4. smoothed explicit-formula comparison;
5. Xi/Theta spectrogram and certified/asymptotic defect analysis.
