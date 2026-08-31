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

## SYNTH implementation bridge

The local [SYNTH AI data lab](https://github.com/BlickandMorty/synth-ai-data-lab)
uses the four-part UAS address shape on its prompt, completion, annotation, and
external-context packets. The exact field mapping, reproducibility steps, and
important non-claims are in [SYNTH_PACKET_BRIDGE.md](SYNTH_PACKET_BRIDGE.md).
This is an implementation connection for provenance and reviewability, not a
new positive result from the retrieval studies in this repository.

## Study this in plain language

The project-by-project study guide, including human-brain analogies and the
important limits, is the [Research Atlas](https://github.com/BlickandMorty/three-stack-research-portfolio/blob/main/RESEARCH_ATLAS.md).
For this repo, start with `BLIND_MODEL_PROTOCOL.md`, then inspect the three
result reports in `results/`. Read the first Qwen result before the second: the
tie is why the type-erasure result must be interpreted narrowly.

## Local-model result: non-confirmation

The first frozen local-model comparison used the installed local `qwen3:4b`
model. It answered all 24 cases correctly under both the flat and UAS prompt
conditions, so the preregistered UAS-improvement gate did **not** pass. That is
worth keeping: this corpus did not expose a behavioral advantage once the model
could already resolve the simple wording. The saved outputs and result are in
`results/QWEN3_4B_BLIND_UAS_REPORT.md`; the next design must use independently
authored, genuinely ambiguous evidence instead of treating a clean demo as
research confirmation.

## Local-model result: metadata-loss ablation

A second, explicitly different experiment removed type metadata from a flat
three-record bundle while retaining it in a typed UAS bundle. On 24 frozen
cases, local Qwen3 4B scored 8/24 with type-erased text and 24/24 with typed
UAS records; wrong-domain answers fell from 16 to 0. This passed its
predeclared gate, but it has a deliberately narrow interpretation: preserving a
needed discriminator helps when the baseline has removed that discriminator.
It does not overturn the first tie or establish a general reasoning advantage.

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

## Independent-corpus gate (next study, not a result)

The next UAS study is now preregistered in
[`EXTERNAL_CORPUS_PREREGISTRATION.md`](EXTERNAL_CORPUS_PREREGISTRATION.md).
It cannot be filled with another hand-authored success fixture: an accepting
corpus must contain public third-party source receipts, distinct implementer /
case-author / blind-grader roles, a frozen `uas.py` hash, and at least 12
held-out cases from each stack. Validate a candidate corpus before any model
run with:

```powershell
python .\verify_external_corpus_contract.py path\to\candidate_corpus.json
```

The scaffold is deliberately not a positive result and has no portfolio chart.
Its job is to make the next result credible enough to matter, including if it
fails.

## Boundaries

- This is not a live 70B route, weight paging system, or proof of EML
  universality.
- It does not use private Epistemos code or data.
- A positive result would establish only that type-aware addressing helps under
  the explicit contamination conditions in this corpus. A later extension must
  test independently authored scientific and security records, then an LLM
  answer task with blinded grading.
