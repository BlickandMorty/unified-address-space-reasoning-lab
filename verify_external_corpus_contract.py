"""Validate the preregistered independent-corpus contract; makes no model call."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KINDS = {"science_observation", "security_observation", "ai_evaluation"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"external corpus contract failed: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", type=Path, help="candidate corpus JSON, relative to this repository or absolute")
    args = parser.parse_args()
    path = args.corpus if args.corpus.is_absolute() else ROOT / args.corpus
    corpus = json.loads(path.read_text(encoding="utf-8"))
    if corpus.get("study") != "uas-independent-corpus-v1":
        fail("wrong study identifier")
    roles = corpus.get("roles", {})
    expected_roles = ("retrieval_implementer", "case_author", "blind_grader")
    if any(not isinstance(roles.get(role), str) or not roles[role].strip() for role in expected_roles):
        fail("all role IDs are required")
    if len({roles[role] for role in expected_roles}) != 3:
        fail("retrieval implementer, case author, and blind grader must be distinct")
    implementation = corpus.get("retrieval_implementation", {})
    if implementation.get("file") != "uas.py" or implementation.get("sha256") != sha256(ROOT / "uas.py"):
        fail("retrieval implementation receipt does not match frozen uas.py")
    records = corpus.get("source_records", [])
    cases = corpus.get("cases", [])
    if len(records) < 36 or len(cases) < 36:
        fail("need at least 36 source records and 36 held-out cases")
    record_ids = set()
    for record in records:
        required = ("record_id", "kind", "source_url", "publisher", "accessed_utc", "source_sha256", "excerpt", "license_note")
        if any(not record.get(key) for key in required):
            fail("a source record lacks required provenance")
        if record["record_id"] in record_ids:
            fail("duplicate source record ID")
        record_ids.add(record["record_id"])
        if record["kind"] not in KINDS:
            fail("invalid source record kind")
        if not str(record["source_url"]).startswith("https://"):
            fail("source URLs must be HTTPS public references")
        if len(str(record["source_sha256"])) != 64:
            fail("source receipt must be SHA-256")
    case_ids, domain_counts = set(), Counter()
    for case in cases:
        required = ("case_id", "kind", "question", "expected_answer", "required_record_id", "cross_domain_distractor_id", "requested_kind_policy")
        if any(not case.get(key) for key in required):
            fail("a case lacks required fields")
        if case["case_id"] in case_ids:
            fail("duplicate case ID")
        case_ids.add(case["case_id"])
        if case["kind"] not in KINDS or case["requested_kind_policy"] != case["kind"]:
            fail("case kind / policy kind mismatch")
        if case["required_record_id"] not in record_ids or case["cross_domain_distractor_id"] not in record_ids:
            fail("case references unknown source record")
        if case["required_record_id"] == case["cross_domain_distractor_id"]:
            fail("distractor must differ from required record")
        by_id = {record["record_id"]: record for record in records}
        if by_id[case["required_record_id"]]["kind"] != case["kind"]:
            fail("required record kind mismatch")
        if by_id[case["cross_domain_distractor_id"]]["kind"] == case["kind"]:
            fail("distractor is not cross-domain")
        domain_counts[case["kind"]] += 1
    if any(domain_counts[kind] < 12 for kind in KINDS):
        fail("need at least 12 held-out cases in each research stack")
    print(f"external corpus contract verified: {len(records)} sourced records, {len(cases)} held-out cases, {dict(sorted(domain_counts.items()))}")


if __name__ == "__main__":
    main()
