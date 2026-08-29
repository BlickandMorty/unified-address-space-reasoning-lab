# Independent-Corpus UAS Study — preregistration

## Status

**Scaffold only; no result exists yet.** This document is committed before an
external corpus is accepted and before a new model is run. It exists to prevent
the retrieval implementation, the case design, and the grader from quietly
sharing the same assumptions.

## Question

When a local model answers questions using independently authored public
evidence from the three stacks, does typed, address-linked retrieval reduce
wrong-domain citations or improve the predeclared composite score relative to
flat retrieval with the same source records?

The study will compare representations, not source quantity. Flat and UAS
conditions must receive the same evidence text, record count, and token budget;
only the address/type representation and the type-aware candidate selection
may differ.

## Required corpus contract

The future corpus must pass `verify_external_corpus_contract.py`.

- At least 36 held-out cases: 12 science, 12 safe defensive-security, and 12
  AI-evaluation records.
- Every source record must be a public third-party item with URL, publisher,
  access date, verbatim-source SHA-256, license/terms note, and a short,
  attribution-preserving excerpt.
- The case author declares a role ID different from the retrieval implementer.
  The grader declares a role ID different from both and receives shuffled,
  condition-blind answer packets.
- Each task has an answer key and a required source record, but the runner may
  not serialize either field into a model prompt.
- Queries must be written without revealing a record type label. The requested
  type is supplied to the UAS retriever as a separately logged policy field.
- Each question must include a plausible same-topic cross-domain distractor.
  No broad claim is permitted if the result only comes from deleting a needed
  discriminator from the flat representation.

## Fixed methods

The retrieval primitive is frozen by the SHA-256 in the accepted corpus
manifest. The implementation starts from `uas.py`; any change to its ranking,
candidate eligibility, text normalization, or address construction requires a
new preregistration and a new corpus manifest.

Both conditions use deterministic local inference with a recorded model
revision, template, decoding settings, context limit, and seed. The model sees
only the selected evidence packet and the question. It never sees the answer
key, source-record ID, expected address, condition name, or grader labels.

## Outcomes and gates

Primary outcome: exact answer correctness, graded blind to condition.

Secondary outcomes:

1. citation/address validity;
2. wrong-domain citation or answer contamination;
3. correct abstention where the authored source set lacks enough evidence;
4. parse failure and evidence-token count.

UAS earns a narrow positive result only if, on the frozen test corpus, it both
improves exact-answer accuracy by at least 10 percentage points **and** does
not increase wrong-domain contamination. If either part fails, publish the
result as non-confirmation. Report all four outcomes even when the primary
gate passes.

## Stop rule and boundary

Do not write another hand-authored success corpus after this point. If a valid
independently sourced corpus does not show the gate, stop the general-UAS
behavioral claim and retain the existing narrower results. A pass would still
not prove that UAS improves factual truth, general intelligence, production
retrieval, or model internals; it would establish only the stated
representation effect under this corpus and model.

## Plain-language picture

This is a library checkout test. Flat retrieval is a shared table where books
with similar titles can be confused. UAS gives each book a shelf label and a
receipt. The test is fair only if the books came from outside the librarian,
the person writing the quiz is not the person choosing the shelf system, and
the marker does not know which checkout method was used.
