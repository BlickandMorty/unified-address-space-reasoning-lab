"""Small, independent UAS primitives for a falsifiable retrieval study."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any

KINDS = {"science_observation", "security_observation", "ai_evaluation"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def address(record: dict[str, Any]) -> str:
    identity = {key: record[key] for key in ("kind", "source_family", "revision", "payload")}
    return f"uas://{record['kind']}/{digest(identity)}?family={record['source_family']}&rev={record['revision']}"


def eml_monotone(score: float) -> float:
    """exp(log(1+s)) - log(1+s): a documented monotone EML-derived overlay."""
    return (1.0 + score) - math.log(1.0 + score)


def lexical_overlap(query_tokens: set[str], record: dict[str, Any]) -> float:
    tokens = set(record["text"].lower().replace("-", " ").split())
    return float(len(query_tokens & tokens))


def rank(query: dict[str, Any], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tokens = set(query["text"].lower().replace("-", " ").split())
    return sorted(candidates, key=lambda r: (-eml_monotone(lexical_overlap(tokens, r)), r["ordinal"]))


def flat_retrieve(query: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    return rank(query, records)[0]


def uas_retrieve(query: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    typed = [record for record in records if record["kind"] == query["requested_kind"]]
    return rank(query, typed)[0]
