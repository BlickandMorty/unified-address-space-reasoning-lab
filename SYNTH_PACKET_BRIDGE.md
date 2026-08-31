# SYNTH packet bridge

SYNTH is the local AI data and evaluation lab that now uses the UAS address
shape as a provenance field on its packets. This document records the bridge
so it can be inspected as an implementation relationship, not treated as a
new UAS research result.

## What maps directly

| UAS concept | SYNTH packet field | Meaning in the lab |
|---|---|---|
| `kind` | `address.kind` and `type` | Distinguishes prompt, completion, search query, tool call, red-team context, and other packet classes. |
| `content digest` | `address.contentDigest` | SHA-256 digest of the packet's recorded content fields. |
| `source family` | `address.sourceFamily` | Records whether the packet came from a user, agent, system, evaluator, or benchmark source. |
| `revision` | `address.revision` | Makes the current address representation explicit. |
| integrity check | `integrityHash` | Lets a later review identify the exact saved packet it refers to. |

SYNTH also records `parentPacketId` for prompt → completion lineage and places
packets under an optional `Experiment` → `Run` structure. Those are SYNTH
workflow features, not additions to the claims tested in this repository.

## Why the bridge is useful

An annotation is only meaningful when the original input and output can still
be found. In SYNTH, a review or preference record is attached to concrete
completion packet IDs. The address and digest make it possible to check which
record was reviewed, while the parent link makes the input/output relationship
visible.

For external context such as a search query or a tool result, SYNTH can retain
the typed packet, a source locator supplied by the user, and a note that the
material was recorded rather than independently verified. This supports
provenance discipline; it does not validate the external claim.

## Boundaries

- This bridge does **not** rerun or extend the blind retrieval studies here.
- A SYNTH address does not prove factual correctness, consent, licensing, or
  causal validity.
- Saving a packet is not the same as verifying its source.
- The lab's local annotation and dataset exports are separate from model-weight
  training; any post-training run still needs a sufficiently large, reviewed,
  appropriately licensed dataset.

## Reproduce the bridge locally

1. Start SYNTH from `C:\Users\jojo\Projects\SYNTH` with
   `./scripts/start-synth.ps1`.
2. Run a local prompt in the Data Lab, or capture a typed external-context
   packet in Packet Explorer.
3. Inspect the Packet Explorer detail panel. It displays the UAS address and
   integrity digest for the saved record.
4. Run the same prompt through two real local targets, then use Annotation
   Studio to create an eligible human preference pair.

The current SYNTH code and its local setup instructions are in
[`BlickandMorty/synth-ai-data-lab`](https://github.com/BlickandMorty/synth-ai-data-lab).
