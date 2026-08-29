"""Rerun and refuse stale stated results."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "generate_corpus.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "run_study.py")], check=True)
    report = (ROOT / "results" / "UAS_RETRIEVAL_REPORT.md").read_text(encoding="utf-8")
    required = ("Flat text ranking | 0/90 (0.0%) | 90/90 (100.0%)", "Typed UAS retrieval | 90/90 (100.0%) | 0/90 (0.0%)")
    if missing := [item for item in required if item not in report]:
        raise SystemExit("stated result mismatch: " + "; ".join(missing))
    print("verified: deterministic corpus and stated results agree")


if __name__ == "__main__":
    main()
