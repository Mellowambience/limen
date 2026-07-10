from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


VALID_STAGES = {
    "dream",
    "seed",
    "sprout",
    "rooted",
    "blooming",
    "bearing",
    "composting",
}


@dataclass(slots=True)
class Worldseed:
    schema_version: str
    id: str
    name: str
    essence: str
    creator_intent: str
    stage: str = "seed"
    promises: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    success_signals: list[str] = field(default_factory=list)
    active_missions: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    next_evolution: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Worldseed":
        required = ["schema_version", "id", "name", "essence", "creator_intent"]
        missing = [key for key in required if not str(data.get(key, "")).strip()]
        if missing:
            raise ValueError(f"Worldseed missing required fields: {', '.join(missing)}")
        stage = str(data.get("stage", "seed"))
        if stage not in VALID_STAGES:
            raise ValueError(
                f"Invalid Worldseed stage '{stage}'. Expected one of: "
                + ", ".join(sorted(VALID_STAGES))
            )
        return cls(
            schema_version=str(data["schema_version"]),
            id=str(data["id"]),
            name=str(data["name"]),
            essence=str(data["essence"]),
            creator_intent=str(data["creator_intent"]),
            stage=stage,
            promises=list(data.get("promises", [])),
            constraints=list(data.get("constraints", [])),
            success_signals=list(data.get("success_signals", [])),
            active_missions=list(data.get("active_missions", [])),
            artifacts=list(data.get("artifacts", [])),
            decisions=list(data.get("decisions", [])),
            risks=list(data.get("risks", [])),
            next_evolution=str(data.get("next_evolution", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "id": self.id,
            "name": self.name,
            "essence": self.essence,
            "creator_intent": self.creator_intent,
            "stage": self.stage,
            "promises": self.promises,
            "constraints": self.constraints,
            "success_signals": self.success_signals,
            "active_missions": self.active_missions,
            "artifacts": self.artifacts,
            "decisions": self.decisions,
            "risks": self.risks,
            "next_evolution": self.next_evolution,
        }


@dataclass(slots=True)
class Mission:
    id: str
    objective: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    status: str = "proposed"


@dataclass(slots=True)
class EvolutionProposal:
    id: str
    title: str
    target: str
    hypothesis: str
    rollback_plan: str
    status: str = "proposed"
