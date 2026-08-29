"""Generate a frozen type-erasure ablation corpus for the local model."""
from __future__ import annotations

from pathlib import Path
from uas import address, canonical_json, digest

ROOT = Path(__file__).parent
OUT = ROOT / "fixtures" / "metadata_loss_ablation_cases.json"
SPECS = (("science_observation", "science measurement"), ("security_observation", "safe local security observation"), ("ai_evaluation", "AI evaluation observation"))
WORDS = ("amber", "brass", "coral", "denim", "ember", "flint", "graph", "honey")


def make(kind, key, code, ordinal):
    row = {"kind": kind, "source_family": kind.split("_")[0], "revision": 1, "ordinal": ordinal, "payload": {"key": key, "code": code}, "text": f"Record {key}: answer code {code}."}
    row["address"] = address(row)
    return row


def main():
    cases, ordinal = [], 0
    for wanted_index, (wanted_kind, description) in enumerate(SPECS):
        for number, word in enumerate(WORDS, 1):
            key, records = f"archive-{number:02d}", []
            for index, (kind, _) in enumerate(SPECS):
                code = f"{word.upper()}-{index + 1}{number:02d}"
                ordinal += 1
                records.append(make(kind, key, code, ordinal))
            target = records[wanted_index]
            cases.append({"case_id": f"{wanted_kind}-{number:02d}", "requested_kind": wanted_kind, "question": f"For {description} {key}, what is the answer code?", "answer_key": target["payload"]["code"], "records": records})
    corpus = {"protocol": "uas-metadata-loss-ablation-v1", "cases": cases}
    OUT.write_text(canonical_json(corpus) + "\n", encoding="utf-8")
    print(f"cases={len(cases)} sha256={digest(corpus)}")


if __name__ == "__main__": main()
