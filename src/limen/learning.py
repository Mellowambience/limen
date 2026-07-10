from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _bounded(value: float, *, name: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1.")
    return number


@dataclass(slots=True)
class KnowledgeRecord:
    subject: str
    claim: str
    confidence: float = 0.5
    source: str = "observation"
    status: str = "active"
    evidence: list[str] = field(default_factory=list)
    counterevidence: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: f"knowledge-{uuid.uuid4().hex[:10]}")
    learned_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def __post_init__(self) -> None:
        self.subject = self.subject.strip()
        self.claim = self.claim.strip()
        self.source = self.source.strip() or "observation"
        if not self.subject or not self.claim:
            raise ValueError("Knowledge subject and claim are required.")
        self.confidence = _bounded(self.confidence, name="confidence")
        if self.status not in {"active", "relearning", "unlearned", "quarantined"}:
            raise ValueError("Invalid knowledge status.")


class KnowledgeGarden:
    """Evidence-aware learning, relearning, and unlearning.

    Unlearning does not erase history. It retires a claim, preserves provenance,
    and records why the belief should no longer guide action.
    """

    def __init__(self, workspace: Path):
        self.directory = workspace / "knowledge"
        self.records_path = self.directory / "records.json"
        self.history_path = self.directory / "history.jsonl"

    def initialize(self) -> list[Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        if not self.records_path.exists():
            self.records_path.write_text("[]\n", encoding="utf-8")
            created.append(self.records_path)
        if not self.history_path.exists():
            self.history_path.touch()
            created.append(self.history_path)
        return created

    def _load(self) -> list[dict[str, Any]]:
        if not self.records_path.exists():
            self.initialize()
        data = json.loads(self.records_path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Knowledge records must be a JSON list.")
        return data

    def _save(self, records: list[dict[str, Any]]) -> None:
        self.records_path.write_text(
            json.dumps(records, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _event(self, kind: str, record: dict[str, Any], reason: str = "") -> None:
        event = {
            "kind": kind,
            "record_id": record["id"],
            "subject": record["subject"],
            "claim": record["claim"],
            "reason": reason.strip(),
            "created_at": _now(),
        }
        with self.history_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    def learn(self, record: KnowledgeRecord) -> dict[str, Any]:
        records = self._load()
        data = asdict(record)
        records.append(data)
        self._save(records)
        self._event("learned", data)
        return data

    def relearn(
        self,
        record_id: str,
        *,
        revised_claim: str,
        confidence: float,
        evidence: list[str] | None = None,
        reason: str = "",
    ) -> dict[str, Any]:
        revised_claim = revised_claim.strip()
        if not revised_claim:
            raise ValueError("Revised claim cannot be empty.")
        records = self._load()
        for record in records:
            if record.get("id") == record_id:
                record["claim"] = revised_claim
                record["confidence"] = _bounded(confidence, name="confidence")
                record["status"] = "active"
                record["evidence"] = list(evidence or record.get("evidence", []))
                record["updated_at"] = _now()
                self._save(records)
                self._event("relearned", record, reason)
                return record
        raise ValueError(f"Knowledge record not found: {record_id}")

    def unlearn(self, record_id: str, *, reason: str) -> dict[str, Any]:
        reason = reason.strip()
        if not reason:
            raise ValueError("Unlearning requires a reason.")
        records = self._load()
        for record in records:
            if record.get("id") == record_id:
                record["status"] = "unlearned"
                record["confidence"] = 0.0
                record["unlearning_reason"] = reason
                record["updated_at"] = _now()
                self._save(records)
                self._event("unlearned", record, reason)
                return record
        raise ValueError(f"Knowledge record not found: {record_id}")

    def inspect(self, *, include_unlearned: bool = False) -> dict[str, Any]:
        records = self._load()
        visible = records if include_unlearned else [
            item for item in records if item.get("status") != "unlearned"
        ]
        return {
            "discipline": "learn-relearn-unlearn",
            "epistemic_law": (
                "No belief is sacred merely because it is old; no novelty is true merely "
                "because it is exciting."
            ),
            "active_count": sum(item.get("status") == "active" for item in records),
            "unlearned_count": sum(item.get("status") == "unlearned" for item in records),
            "records": visible,
        }
