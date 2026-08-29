"""Check that the metadata-loss report faithfully states its saved result."""
from __future__ import annotations

import json
from pathlib import Path

from uas import digest

ROOT = Path(__file__).parent


def main() -> None:
    corpus = json.loads((ROOT / "fixtures" / "metadata_loss_ablation_cases.json").read_text(encoding="utf-8"))
    result = json.loads((ROOT / "results" / "qwen3_4b_metadata_loss_result.json").read_text(encoding="utf-8"))
    report = (ROOT / "results" / "QWEN3_4B_METADATA_LOSS_REPORT.md").read_text(encoding="utf-8")
    if result["fixture_sha256"] != digest(corpus):
        raise SystemExit("fixture hash mismatch")
    flat, uas = result["results"]["flat"]["summary"], result["results"]["uas"]["summary"]
    required = (f"Flat type-erased bundle | {flat['correct']}/{flat['total']} ({flat['accuracy']:.1%})", f"Typed UAS bundle | {uas['correct']}/{uas['total']} ({uas['accuracy']:.1%})", "Positive gate: **passed**.")
    if missing := [text for text in required if text not in report]:
        raise SystemExit("report mismatch: " + "; ".join(missing))
    print("verified: metadata-loss fixture, raw result, and report agree")


if __name__ == "__main__": main()
