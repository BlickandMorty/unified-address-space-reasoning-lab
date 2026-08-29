# Unified Address Space Retrieval Study — Result

## Design

This frozen synthetic corpus contains 180 records: 90 target records and 90 lexically near-identical, wrong-type contamination records. There are 90 queries across science, safe defensive security, and AI evaluation. Flat retrieval ranks every text record. UAS retrieval filters by requested type before applying the same ranking function.

## Result

| Method | Exact target retrieval | Cross-domain contamination |
| --- | ---: | ---: |
| Flat text ranking | 0/90 (0.0%) | 90/90 (100.0%) |
| Typed UAS retrieval | 90/90 (100.0%) | 0/90 (0.0%) |

Frozen corpus SHA-256: `8e6a186bfb07359de2bbc4333fbbc92df49c26fae9c8f2bc60d35f9403b25a26`.

## Interpretation

On this intentionally adversarial type-confusion corpus, the address-space policy is expected to prevent wrong-type evidence from being selected. That is an engineering result about the stated policy, not proof that an AI model reasons better or that it will help on natural data. The next serious test is a blind corpus written independently of the retrieval implementation, followed by a local-model answer experiment where graders only see the final answer and cited addresses.

## Reproduce

```powershell
python .\generate_corpus.py
python .\run_study.py
python .\verify_claims.py
```
