"""Create model-blind synthetic UAS cases; answer keys are only for scoring."""
from __future__ import annotations

from pathlib import Path

from uas import address, canonical_json, digest

ROOT = Path(__file__).parent
OUT = ROOT / "fixtures" / "blind_local_model_cases.json"
SPECS = (("science_observation", "science measurement", "lab"), ("security_observation", "safe local defensive-security observation", "local"), ("ai_evaluation", "AI evaluation observation", "eval"))
WORDS = ("ALDER", "BIRCH", "CEDAR", "DOGWOOD", "ELM", "FIR", "GINKGO", "HAZEL")


def record(kind, family, text, key, code, ordinal):
    row = {"kind": kind, "source_family": family, "revision": 1, "ordinal": ordinal,
           "payload": {"key": key, "answer_code": code}, "text": text}
    row["address"] = address(row)
    return row


def main() -> None:
    cases, ordinal = [], 0
    for kind_index, (kind, descriptor, family) in enumerate(SPECS):
        for number, word in enumerate(WORDS, 1):
            key, correct = f"signal-{number:02d}", f"{word}-{kind_index + 1}{number:02d}"
            ordinal += 1
            target = record(kind, family, f"{descriptor} for {key}: verified answer code {correct}.", key, correct, ordinal)
            wrong = []
            for offset in (1, 2):
                other_kind, _, other_family = SPECS[(kind_index + offset) % 3]
                wrong_code = f"{WORDS[(number + offset) % len(WORDS)]}-{((kind_index + offset) % 3) + 1}{number:02d}"
                ordinal += 1
                wrong.append(record(other_kind, other_family, f"observation for {key}: reported answer code {wrong_code}.", key, wrong_code, ordinal))
            ordinal += 1
            irrelevant = record(kind, family, f"{descriptor} for unrelated-{number:02d}: verified answer code NONE-{number:02d}.", f"unrelated-{number:02d}", f"NONE-{number:02d}", ordinal)
            cases.append({"case_id": f"{kind}-{number:02d}", "requested_kind": kind, "question": f"For {descriptor} {key}, what is the verified answer code?", "answer_key": correct, "target": target, "wrong_domain_records": wrong, "same_type_irrelevant": irrelevant})
    corpus = {"protocol": "uas-blind-local-model-v1", "cases": cases}
    OUT.write_text(canonical_json(corpus) + "\n", encoding="utf-8")
    print(f"cases={len(cases)} sha256={digest(corpus)}")


if __name__ == "__main__":
    main()
