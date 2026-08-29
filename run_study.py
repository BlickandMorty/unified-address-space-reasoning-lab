"""Compare flat and UAS retrieval on the frozen contamination corpus."""
from __future__ import annotations

import json
from pathlib import Path

from uas import canonical_json, digest, flat_retrieve, uas_retrieve

ROOT = Path(__file__).parent
FIXTURE = ROOT / "fixtures" / "frozen_uas_corpus.json"
REPORT = ROOT / "results" / "UAS_RETRIEVAL_REPORT.md"
MACHINE = ROOT / "results" / "uas_retrieval_result.json"


def metrics(name: str, retrieve, queries, records) -> dict:
    exact = contamination = 0
    examples = []
    for query in queries:
        result = retrieve(query, records)
        exact += result["address"] == query["target_address"]
        contamination += result["kind"] != query["requested_kind"]
        if len(examples) < 3:
            examples.append({"query_id": query["query_id"], "requested_kind": query["requested_kind"],
                             "returned_kind": result["kind"], "returned_address": result["address"]})
    return {"method": name, "n": len(queries), "exact": exact, "exact_rate": exact / len(queries),
            "cross_domain_contamination": contamination, "contamination_rate": contamination / len(queries),
            "examples": examples}


def main() -> None:
    raw = FIXTURE.read_text(encoding="utf-8")
    corpus = json.loads(raw)
    flat = metrics("flat", flat_retrieve, corpus["queries"], corpus["records"])
    uas = metrics("uas", uas_retrieve, corpus["queries"], corpus["records"])
    result = {"fixture_sha256": digest(corpus), "flat": flat, "uas": uas}
    MACHINE.parent.mkdir(exist_ok=True)
    MACHINE.write_text(canonical_json(result) + "\n", encoding="utf-8")
    lines = [
        "# Unified Address Space Retrieval Study — Result", "",
        "## Design", "",
        "This frozen synthetic corpus contains 180 records: 90 target records and 90 lexically near-identical, wrong-type contamination records. There are 90 queries across science, safe defensive security, and AI evaluation. Flat retrieval ranks every text record. UAS retrieval filters by requested type before applying the same ranking function.", "",
        "## Result", "",
        "| Method | Exact target retrieval | Cross-domain contamination |", "| --- | ---: | ---: |",
        f"| Flat text ranking | {flat['exact']}/{flat['n']} ({flat['exact_rate']:.1%}) | {flat['cross_domain_contamination']}/{flat['n']} ({flat['contamination_rate']:.1%}) |",
        f"| Typed UAS retrieval | {uas['exact']}/{uas['n']} ({uas['exact_rate']:.1%}) | {uas['cross_domain_contamination']}/{uas['n']} ({uas['contamination_rate']:.1%}) |", "",
        f"Frozen corpus SHA-256: `{result['fixture_sha256']}`.", "",
        "## Interpretation", "",
        "On this intentionally adversarial type-confusion corpus, the address-space policy is expected to prevent wrong-type evidence from being selected. That is an engineering result about the stated policy, not proof that an AI model reasons better or that it will help on natural data. The next serious test is a blind corpus written independently of the retrieval implementation, followed by a local-model answer experiment where graders only see the final answer and cited addresses.", "",
        "## Reproduce", "", "```powershell", "python .\\generate_corpus.py", "python .\\run_study.py", "python .\\verify_claims.py", "```"
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(canonical_json(result))


if __name__ == "__main__":
    main()
