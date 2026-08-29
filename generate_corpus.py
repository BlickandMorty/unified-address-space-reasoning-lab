"""Generate frozen, synthetic UAS records and contamination queries."""
from __future__ import annotations

from pathlib import Path

from uas import KINDS, address, canonical_json, digest

ROOT = Path(__file__).parent
OUT = ROOT / "fixtures" / "frozen_uas_corpus.json"
SPECS = (
    ("science_observation", "lab", "temperature measurement"),
    ("security_observation", "localhost", "loopback alert"),
    ("ai_evaluation", "eval", "reasoning evaluation"),
)


def make_record(kind: str, family: str, topic: str, number: int, value: str, ordinal: int) -> dict:
    record = {"kind": kind, "source_family": family, "revision": 1,
              "payload": {"key": f"k{number:02d}", "value": value}, "ordinal": ordinal,
              "text": f"{topic} key k{number:02d} observed value {value}"}
    record["address"] = address(record)
    return record


def main() -> None:
    records, queries = [], []
    ordinal = 0
    for number in range(1, 31):
        for kind, family, topic in SPECS:
            # Same key and lexical shape but a different type/value. It is
            # deliberately inserted first, so flat tie-breaking has to reveal
            # whether it can distinguish identity from merely similar text.
            wrong_kind, wrong_family, wrong_topic = SPECS[(number + len(kind)) % 3]
            if wrong_kind == kind:
                wrong_kind, wrong_family, wrong_topic = SPECS[(number + len(kind) + 1) % 3]
            ordinal += 1
            distractor = make_record(wrong_kind, wrong_family, topic, number,
                                     f"contaminated-{wrong_kind[:3]}-{number:02d}", ordinal)
            records.append(distractor)
            ordinal += 1
            value = f"verified-{kind[:3]}-{number:02d}"
            target = make_record(kind, family, topic, number, value, ordinal)
            records.append(target)
            queries.append({"query_id": f"q-{kind}-{number:02d}", "requested_kind": kind,
                            "text": f"{topic} key k{number:02d} observed value",
                            "target_address": target["address"]})
    corpus = {"protocol": "uas-retrieval-v1", "kinds": sorted(KINDS), "records": records, "queries": queries}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(canonical_json(corpus) + "\n", encoding="utf-8")
    print(f"records={len(records)} queries={len(queries)} sha256={digest(corpus)}")


if __name__ == "__main__":
    main()
