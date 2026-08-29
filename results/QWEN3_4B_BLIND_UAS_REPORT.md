# Qwen3 4B Blind UAS Study — Result

## Frozen design

The model received no answer key. Flat prompts used three same-key text records with no type metadata. UAS prompts used a typed, stable address on the matching record plus a same-type irrelevant record. Exact code matching is automatic; malformed output is incorrect.

## Result

| Condition | Exact answers | Wrong-domain answers | Malformed |
| --- | ---: | ---: | ---: |
| Flat text bundle | 24/24 (100.0%) | 0 | 0 |
| Typed UAS bundle | 24/24 (100.0%) | 0 | 0 |

UAS minus flat accuracy: **+0.0%**.
Predeclared positive gate: **not passed**.
Frozen fixture SHA-256: `c1311dadbb9da40fc7b6d238b609c209fbf7b5bec63485eae4875cbb46a9ea71`.

## Interpretation

This is a local-model prompt-and-retrieval result, not a general reasoning claim. If the gate passes, it supports only the narrow claim that typed, address-linked evidence changed answer selection for Qwen3 4B on these frozen synthetic cases. If it does not pass, UAS is not confirmed as an improvement here. The raw model outputs are saved in the JSON result for audit.
