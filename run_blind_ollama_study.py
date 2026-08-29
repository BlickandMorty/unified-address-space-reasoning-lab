"""Run the frozen UAS comparison through the user's local Ollama model only."""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from uas import canonical_json, digest

ROOT = Path(__file__).parent
FIXTURE = ROOT / "fixtures" / "blind_local_model_cases.json"
OUT = ROOT / "results" / "qwen3_4b_blind_uas_result.json"
REPORT = ROOT / "results" / "QWEN3_4B_BLIND_UAS_REPORT.md"
MODEL = "qwen3:4b"
SCHEMA = '{"type":"object","properties":{"answer":{"type":"string"}},"required":["answer"]}'
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def call(prompt: str) -> tuple[str | None, str]:
    command = ["ollama", "run", MODEL, "--think=false", "--hidethinking", "--nowordwrap", "--format", SCHEMA, prompt]
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False, timeout=90)
    raw = ANSI.sub("", completed.stdout).strip()
    match = re.search(r"\{\s*\"answer\"\s*:\s*\"([^\"]+)\"\s*\}", raw)
    return (match.group(1).strip().upper() if match else None), raw


def prompt_for(case: dict, condition: str) -> str:
    target = case["target"]
    if condition == "flat":
        evidence = case["wrong_domain_records"] + [target]
        rendered = "\n".join(f"RECORD: {item['text']}" for item in evidence)
        intro = "Evidence records have no type or address metadata."
    else:
        evidence = [target, case["same_type_irrelevant"]]
        rendered = "\n".join(f"ADDRESS: {item['address']}\nKIND: {item['kind']}\nRECORD: {item['text']}" for item in evidence)
        intro = f"Use only records whose KIND is {case['requested_kind']}."
    return f"{intro}\nQuestion: {case['question']}\nEvidence:\n{rendered}\nReturn JSON with the exact answer code in answer."


def score(rows: list[dict]) -> dict:
    correct = sum(row["correct"] for row in rows)
    wrong_domain = sum(row["wrong_domain"] for row in rows)
    malformed = sum(row["answer"] is None for row in rows)
    return {"correct": correct, "total": len(rows), "accuracy": correct / len(rows), "wrong_domain": wrong_domain, "malformed": malformed}


def main() -> None:
    corpus = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = {}
    for condition in ("flat", "uas"):
        rows = []
        for case in corpus["cases"]:
            answer, raw = call(prompt_for(case, condition))
            wrong_codes = {record["payload"]["answer_code"] for record in case["wrong_domain_records"]}
            rows.append({"case_id": case["case_id"], "requested_kind": case["requested_kind"], "answer": answer, "correct": answer == case["answer_key"], "wrong_domain": answer in wrong_codes, "raw_output": raw})
        results[condition] = {"summary": score(rows), "rows": rows}
    flat, uas = results["flat"]["summary"], results["uas"]["summary"]
    gain = uas["accuracy"] - flat["accuracy"]
    positive = gain >= 0.15 and uas["wrong_domain"] < flat["wrong_domain"]
    result = {"study": "blind-local-model-uas-v1", "model": MODEL, "fixture_sha256": digest(corpus), "results": results, "uas_minus_flat_accuracy": gain, "positive_gate": positive}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(canonical_json(result) + "\n", encoding="utf-8")
    lines = ["# Qwen3 4B Blind UAS Study — Result", "", "## Frozen design", "", "The model received no answer key. Flat prompts used three same-key text records with no type metadata. UAS prompts used a typed, stable address on the matching record plus a same-type irrelevant record. Exact code matching is automatic; malformed output is incorrect.", "", "## Result", "", "| Condition | Exact answers | Wrong-domain answers | Malformed |", "| --- | ---: | ---: | ---: |", f"| Flat text bundle | {flat['correct']}/{flat['total']} ({flat['accuracy']:.1%}) | {flat['wrong_domain']} | {flat['malformed']} |", f"| Typed UAS bundle | {uas['correct']}/{uas['total']} ({uas['accuracy']:.1%}) | {uas['wrong_domain']} | {uas['malformed']} |", "", f"UAS minus flat accuracy: **{gain:+.1%}**.", f"Predeclared positive gate: **{'passed' if positive else 'not passed'}**.", f"Frozen fixture SHA-256: `{result['fixture_sha256']}`.", "", "## Interpretation", "", "This is a local-model prompt-and-retrieval result, not a general reasoning claim. If the gate passes, it supports only the narrow claim that typed, address-linked evidence changed answer selection for Qwen3 4B on these frozen synthetic cases. If it does not pass, UAS is not confirmed as an improvement here. The raw model outputs are saved in the JSON result for audit."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"flat": flat, "uas": uas, "gain": gain, "positive_gate": positive}, indent=2))


if __name__ == "__main__":
    main()
