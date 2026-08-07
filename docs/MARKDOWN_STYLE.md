# Markdown and formula style

The repository uses one rendering convention for mathematical documentation:

- Use `$$ ... $$` for display equations.
- Use `\( ... \)` for inline equations.
- Keep one mathematical claim per display block and put punctuation after the
  closing delimiter when the sentence continues.
- Use fenced code blocks only for commands, file names, JSON, or literal
  source text; do not use them as a substitute for displayed mathematics.
- Introduce symbols before using them and keep the parameter names `\eta`,
  `\beta`, and `\xi` distinct from the completed function `\xi(s)` and the
  transform `\Xi(\alpha)`.
- State the quantifier and proof status next to a computational or certified
  claim. A passing test is evidence of implementation consistency, not a
  replacement for an analytic lemma.

The canonical dependency-aware status for the current proof candidate is

```text
CANDIDATE_PROOF_COMPLETE_PENDING_INDEPENDENT_REVIEW
```

Any document that describes Xi-zero origin matching or the final contradiction
must cite the full two-sided Volterra difference identity and retain the
independent-review boundary.
