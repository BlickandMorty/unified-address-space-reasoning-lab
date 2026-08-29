# Blind Local-Model UAS Study Protocol

## Question

With the same local model and question, does an address-linked evidence packet
reduce wrong-domain answers compared with flat text evidence?

## Model and decoding

- Local-only model: `qwen3:4b` through Ollama.
- Deterministic decoding: temperature 0 and a JSON answer constrained to one code.
- No model-provider or network request is made by the runner.

## Corpus

There are 24 held-out synthetic questions: eight science observations, eight
safe local defensive-security observations, and eight AI-evaluation observations.
Every case uses a query-specific code such as `ALDER-03`. The answer key is
used for scoring but is never placed in a prompt.

Each case has a matching observation and two wrong-domain lookalikes sharing
the same key. Flat prompts contain the matching record and both lookalikes
without type metadata. UAS prompts contain the matching record with its typed
stable address plus one same-type irrelevant record. Both conditions use two
records, so the intervention is not only a shorter prompt.

## Outcomes

Primary: exact answer-code accuracy. Secondary: a wrong-domain answer is any
output matching one of the planted wrong-domain codes. Parse failures count as
incorrect and are never silently repaired.

## Interpretation gate

UAS is a positive local-model result only if it improves exact accuracy by at
least 15 percentage points and lowers wrong-domain answers. A tie or smaller
gain is reported as non-confirmation.

## Limits

This is an authored synthetic corpus. UAS makes type visible by design. It tests
whether this representation changes this model's answer selection here; it does
not prove general scientific reasoning or a production retrieval benefit.
