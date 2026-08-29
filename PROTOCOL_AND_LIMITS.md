# Protocol and Limits

## Question

Can typed addresses prevent a retrieval system from selecting a wrong-domain
record when text is intentionally near-identical?

## Fixed comparison

Both methods use the same token-overlap ranking and the same 180 synthetic
records. The only intervention is that UAS retrieval restricts candidates to
the requested record type before ranking. Each query has one correct record and
one wrong-type record with the same key and topic text. The wrong-type record
is placed first to make the flat tie policy observable.

## Metrics

1. Exact target-address retrieval.
2. Cross-domain contamination: returned record type differs from requested
   record type.

## What could disprove the narrow claim

- UAS does not improve exact retrieval on this frozen corpus.
- UAS returns any wrong-type record.
- A rerun changes the corpus digest or stated counts.

## What this cannot establish

This setup is intentionally diagnostic, not naturalistic. The type field is
available to UAS by design, so a positive result means the policy works under
the specified ambiguity. It does not establish factual correctness, natural
language understanding, scientific reasoning, better model internals, or a
benefit on an independently authored corpus.

## Next real experiment

Build a blind, independently authored 3-stack corpus with conflicting
scientific measurements, safe local-security observations, and evaluator
records. Query a local model with either flat retrieval or address-linked
retrieval, hide the condition from graders, and score answer correctness,
citation validity, abstention, and wrong-domain contamination separately.
