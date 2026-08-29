"""Verify that the committed local-model report agrees with its raw saved result."""
from __future__ import annotations

import json
from pathlib import Path

from uas import digest

ROOT = Path(__file__).parent


def main() -> None:
    corpus = json.loads((ROOT / "fixtures" / "blind_local_model_cases.json").read_text(encoding="utf-8"))
    result = json.loads((ROOT / "results" / "qwen3_4b_blind_uas_result.json").read_text(encoding="utf-8"))
    report = (ROOT / "results" / "QWEN3_4B_BLIND_UAS_REPORT.md").read_text(encoding="utf-8")
    if result["fixture_sha256"] != digest(corpus):
        raise SystemExit("fixture hash mismatch")
    flat, uas = result["results"]["flat"]["summary"], result["results"]["uas"]["summary"]
    required = (f"Flat text bundle | {flat['correct']}/{flat['total']} ({flat['accuracy']:.1%})", f"Typed UAS bundle | {uas['correct']}/{uas['total']} ({uas['accuracy']:.1%})", "Predeclared positive gate: **not passed**.")
    if missing := [text for text in required if text not in report]:
        raise SystemExit("report mismatch: " + "; ".join(missing))
    print("verified: saved local-model artifact, fixture, and report agree")


if __name__ == "__main__":
    main()
