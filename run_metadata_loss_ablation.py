"""Run the local-model type-erasure ablation with saved raw outputs."""
from __future__ import annotations

import json
from pathlib import Path

from run_blind_ollama_study import call
from uas import canonical_json, digest

ROOT = Path(__file__).parent
FIXTURE = ROOT / "fixtures" / "metadata_loss_ablation_cases.json"
OUT = ROOT / "results" / "qwen3_4b_metadata_loss_result.json"
REPORT = ROOT / "results" / "QWEN3_4B_METADATA_LOSS_REPORT.md"


def prompt(case, condition):
    if condition == "flat":
        records = "\n".join(f"RECORD: {record['text']}" for record in case["records"])
        intro = "Records are plain text; no type metadata is available."
    else:
        records = "\n".join(f"ADDRESS: {record['address']}\nKIND: {record['kind']}\nRECORD: {record['text']}" for record in case["records"])
        intro = f"Use the record whose KIND is {case['requested_kind']}."
    return f"{intro}\nQuestion: {case['question']}\nEvidence:\n{records}\nReturn JSON with the exact answer code in answer."


def summarize(rows):
    return {"correct": sum(row["correct"] for row in rows), "total": len(rows), "accuracy": sum(row["correct"] for row in rows) / len(rows), "wrong_domain": sum(row["wrong_domain"] for row in rows), "malformed": sum(row["answer"] is None for row in rows)}


def main():
    corpus = json.loads(FIXTURE.read_text(encoding="utf-8"))
    conditions = {}
    for condition in ("flat", "uas"):
        rows = []
        for case in corpus["cases"]:
            answer, raw = call(prompt(case, condition))
            wrong = {row["payload"]["code"] for row in case["records"] if row["payload"]["code"] != case["answer_key"]}
            rows.append({"case_id": case["case_id"], "answer": answer, "correct": answer == case["answer_key"], "wrong_domain": answer in wrong, "raw_output": raw})
        conditions[condition] = {"summary": summarize(rows), "rows": rows}
    flat, uas = conditions["flat"]["summary"], conditions["uas"]["summary"]
    gain = uas["accuracy"] - flat["accuracy"]
    positive = gain >= .15 and uas["wrong_domain"] < flat["wrong_domain"]
    result = {"study": "metadata-loss-ablation-v1", "model": "qwen3:4b", "fixture_sha256": digest(corpus), "results": conditions, "uas_minus_flat_accuracy": gain, "positive_gate": positive}
    OUT.write_text(canonical_json(result) + "\n", encoding="utf-8")
    lines = ["# Qwen3 4B Metadata-Loss Ablation — Result", "", "| Condition | Exact answers | Wrong-domain answers | Malformed |", "| --- | ---: | ---: | ---: |", f"| Flat type-erased bundle | {flat['correct']}/{flat['total']} ({flat['accuracy']:.1%}) | {flat['wrong_domain']} | {flat['malformed']} |", f"| Typed UAS bundle | {uas['correct']}/{uas['total']} ({uas['accuracy']:.1%}) | {uas['wrong_domain']} | {uas['malformed']} |", "", f"UAS minus flat accuracy: **{gain:+.1%}**.", f"Positive gate: **{'passed' if positive else 'not passed'}**.", f"Frozen fixture SHA-256: `{result['fixture_sha256']}`.", "", "This is an information-preservation ablation. It tests the expected consequence of removing versus retaining record type, not a general intelligence claim."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"flat": flat, "uas": uas, "gain": gain, "positive_gate": positive}, indent=2))


if __name__ == "__main__": main()
