# Unified Address Space Reasoning Lab

This is the research version of an older Unified Address Space (UAS) idea.
The question is not whether I can rewrite a runtime in Rust. The question is:

> When an AI system has science observations, safe defensive-security traces,
> and AI-evaluation notes in one pool, does a typed, stable address space reduce
> evidence contamination compared with flat text retrieval?

Each synthetic record gets an address with four independent pieces:

`kind / content digest / source family / revision`

The address is identity, not where the bytes happen to live. An EML-derived
score is used only as a monotone ranking feature on retrieval candidates; it
does not prove anything about a model or replace the evidence.

## Pre-registered comparison

The corpus deliberately includes near-duplicate, same-key records with a
wrong value and mismatched type. We compare:

- **flat retrieval:** ranks all text records together;
- **UAS retrieval:** first resolves a requested type, then ranks only typed
  candidates and returns the full address/evidence link.

The primary metric is exact retrieval of the target record. The safety metric
is cross-domain contamination: returning a record whose type does not match
the query's requested type. This is a controlled retrieval experiment, not a
claim that an LLM becomes generally more intelligent.

## Why this fits the larger research

Eidos supplies provenance-aware retrieval. SCOPE-Rex supplies admission and
witness discipline. Answer packets are the result interface. UAS is the shared
addressing layer that lets a science measurement, a local security observation,
or a model-evaluation result be pulled through one explicit representation
without losing what it is or where it came from.

## Run

Python 3.10+; no external packages or network calls:

```powershell
python .\\generate_corpus.py
python .\\run_study.py
python .\\verify_claims.py
```

The public corpus is entirely synthetic. The study is designed to be easy to
falsify: if typed retrieval does not improve exact retrieval or reduce type
contamination on the frozen corpus, the report must say so.

## Boundaries

- This is not a live 70B route, weight paging system, or proof of EML
  universality.
- It does not use private Epistemos code or data.
- A positive result would establish only that type-aware addressing helps under
  the explicit contamination conditions in this corpus. A later extension must
  test independently authored scientific and security records, then an LLM
  answer task with blinded grading.
