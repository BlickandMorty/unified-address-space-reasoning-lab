# Qwen3 4B Metadata-Loss Ablation — Result

| Condition | Exact answers | Wrong-domain answers | Malformed |
| --- | ---: | ---: | ---: |
| Flat type-erased bundle | 8/24 (33.3%) | 16 | 0 |
| Typed UAS bundle | 24/24 (100.0%) | 0 | 0 |

UAS minus flat accuracy: **+66.7%**.
Positive gate: **passed**.
Frozen fixture SHA-256: `57e625384dafebbffedfbe7b3cc498687317af0f3d43732a9a33b64b5a858fa0`.

This is an information-preservation ablation. It tests the expected consequence of removing versus retaining record type, not a general intelligence claim.
