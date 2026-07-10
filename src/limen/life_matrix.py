from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


_DIMENSIONS: dict[str, tuple[str, ...]] = {
    "incentives": ("money", "reward", "profit", "bonus", "promotion", "attention"),
    "status": ("status", "rank", "prestige", "popular", "elite", "respect"),
    "belonging": ("belong", "tribe", "community", "accepted", "excluded", "loyal"),
    "identity": ("identity", "role", "image", "reputation", "persona", "brand"),
    "power": ("control", "authority", "power", "leverage", "permission", "gatekeeper"),
    "scarcity": ("scarce", "limited", "urgent", "deadline", "exclusive", "fear"),
    "narrative": ("story", "meaning", "purpose", "destiny", "failure", "success"),
    "reciprocity": ("owe", "favor", "gift", "return", "reciprocity", "debt"),
}


class LifeMatrix:
    """Grounded analysis of social systems and recurring human games.

    The Matrix is treated as a metaphor for overlapping incentives, identities,
    institutions, relationships, and narratives—not proof of a hidden simulation.
    """

    def __init__(self, workspace: Path):
        self.directory = workspace / "life_matrix"
        self.observations_path = self.directory / "observations.jsonl"

    def initialize(self) -> list[Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        if not self.observations_path.exists():
            self.observations_path.touch()
            return [self.observations_path]
        return []

    def analyze(self, scenario: str, *, context: str = "") -> dict[str, Any]:
        scenario = scenario.strip()
        if not scenario:
            raise ValueError("Scenario cannot be empty.")
        text = f"{scenario} {context}".lower()
        detected: list[dict[str, Any]] = []
        for dimension, terms in _DIMENSIONS.items():
            hits = sorted({term for term in terms if re.search(rf"\b{re.escape(term)}\b", text)})
            if hits:
                detected.append({"dimension": dimension, "signals": hits})

        questions = [
            "What does each participant want, fear, protect, and signal?",
            "Who benefits if the current rules remain invisible?",
            "Which choices are genuinely available, and which only appear available?",
            "What evidence would disconfirm the current interpretation?",
            "How can agency increase without reducing another person's humanity?",
        ]
        report = {
            "frame": "life-matrix / game-theory-lite",
            "scenario": scenario,
            "context": context.strip(),
            "detected_dimensions": detected,
            "strategic_questions": questions,
            "cautions": [
                "Do not infer secret coordination when ordinary incentives explain the pattern.",
                "Do not reduce people to pieces, archetypes, diagnoses, or enemies.",
                "Distinguish observation, interpretation, and speculation.",
                "Use insight to widen agency, not manipulate vulnerability.",
            ],
            "created_at": _now(),
        }
        self.initialize()
        with self.observations_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(report, ensure_ascii=False) + "\n")
        return report
