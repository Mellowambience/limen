from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_CATEGORIES = {"job", "bug-bounty", "open-source", "service", "product", "commission"}


@dataclass(slots=True)
class Opportunity:
    id: str
    title: str
    category: str
    source: str
    url: str = ""
    estimated_value_usd: float = 0.0
    probability: float = 0.2
    effort_hours: float = 1.0
    alignment: int = 3
    deadline: str | None = None
    lawful_authorization: bool = False
    status: str = "candidate"
    notes: str = ""
    created_at: str = ""

    @classmethod
    def create(
        cls,
        title: str,
        *,
        category: str,
        source: str,
        url: str = "",
        estimated_value_usd: float = 0.0,
        probability: float = 0.2,
        effort_hours: float = 1.0,
        alignment: int = 3,
        deadline: str | None = None,
        lawful_authorization: bool = False,
        notes: str = "",
    ) -> "Opportunity":
        if category not in ALLOWED_CATEGORIES:
            raise ValueError(f"Unknown opportunity category: {category}")
        if not title.strip() or not source.strip():
            raise ValueError("Opportunity title and source are required.")
        if estimated_value_usd < 0 or effort_hours <= 0:
            raise ValueError("Value cannot be negative and effort must be positive.")
        if not 0 <= probability <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        if not 0 <= alignment <= 5:
            raise ValueError("Alignment must be between 0 and 5.")
        if deadline:
            date.fromisoformat(deadline)
        return cls(
            id=f"opp-{uuid.uuid4().hex[:10]}",
            title=title.strip(),
            category=category,
            source=source.strip(),
            url=url.strip(),
            estimated_value_usd=estimated_value_usd,
            probability=probability,
            effort_hours=effort_hours,
            alignment=alignment,
            deadline=deadline,
            lawful_authorization=lawful_authorization,
            notes=notes.strip(),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Opportunity":
        return cls(**data)


class ProsperityEngine:
    """Auditable income-opportunity pipeline. It never holds or transfers money."""

    def __init__(self, workspace: Path):
        self.root = workspace / "prosperity"
        self.opportunities_path = self.root / "opportunities.json"
        self.mandate_path = self.root / "bounty-mandate.json"
        self.receipts_path = self.root / "receipts.jsonl"

    def initialize(self) -> list[Path]:
        created: list[Path] = []
        if not self.root.exists():
            self.root.mkdir(parents=True, exist_ok=True)
            created.append(self.root)
        if not self.opportunities_path.exists():
            self.opportunities_path.write_text("[]\n", encoding="utf-8")
            created.append(self.opportunities_path)
        if not self.mandate_path.exists():
            mandate = {
                "schema_version": "0.1",
                "status": "draft",
                "owner": "Amara",
                "allowed": [
                    "Jobs and contracts the owner is qualified and authorized to pursue.",
                    "Public bug-bounty programs with explicit written scope.",
                    "Open-source issue bounties and paid coding challenges.",
                    "Creator products, commissions, and clearly described technical services.",
                ],
                "forbidden": [
                    "Access outside explicit program scope.",
                    "Credential theft, impersonation, extortion, harassment, or social engineering.",
                    "Hidden applications, posts, purchases, trades, transfers, or binding agreements.",
                    "Custody of funds, wallet seeds, recovery codes, or private signing keys.",
                    "Paying fees to unlock jobs or rewards.",
                    "Gambling, speculative trading, or deceptive monetization.",
                ],
                "approval_modes": {
                    "discover_and_rank": "allowed",
                    "draft_submission": "allowed",
                    "submit_application": "per-item approval",
                    "accept_contract": "explicit approval",
                    "security_testing": "written scope plus explicit approval",
                    "receive_money": "directly to owner-controlled account",
                },
            }
            self.mandate_path.write_text(
                json.dumps(mandate, indent=2) + "\n", encoding="utf-8"
            )
            created.append(self.mandate_path)
        return created

    def _load(self) -> list[Opportunity]:
        self.initialize()
        raw = json.loads(self.opportunities_path.read_text(encoding="utf-8"))
        return [Opportunity.from_dict(item) for item in raw]

    def _save(self, opportunities: list[Opportunity]) -> None:
        self.opportunities_path.write_text(
            json.dumps([asdict(item) for item in opportunities], indent=2) + "\n",
            encoding="utf-8",
        )

    def add(self, opportunity: Opportunity) -> Opportunity:
        opportunities = self._load()
        opportunities.append(opportunity)
        self._save(opportunities)
        self._receipt("opportunity.added", {"opportunity_id": opportunity.id})
        return opportunity

    @staticmethod
    def score(item: Opportunity, today: date | None = None) -> float:
        today = today or date.today()
        expected_value = item.estimated_value_usd * item.probability
        value_per_hour = expected_value / max(item.effort_hours, 0.25)
        score = min(value_per_hour / 10, 20) + item.alignment * 2
        if item.category == "job":
            score += 2.0
        if item.category in {"product", "service"}:
            score += 1.5
        if item.category == "bug-bounty" and not item.lawful_authorization:
            score -= 100.0
        if item.deadline:
            days = (date.fromisoformat(item.deadline) - today).days
            if days < 0:
                score -= 20.0
            elif days <= 2:
                score += 4.0
            elif days <= 7:
                score += 2.0
        return round(score, 2)

    def ranked(self) -> list[dict[str, Any]]:
        candidates = [item for item in self._load() if item.status == "candidate"]
        candidates.sort(key=self.score, reverse=True)
        return [{**asdict(item), "score": self.score(item)} for item in candidates]

    def plan(self) -> dict[str, Any]:
        ranked = self.ranked()
        safe_ranked = [
            item
            for item in ranked
            if item["category"] != "bug-bounty" or item["lawful_authorization"]
        ]
        return {
            "principle": "Build several honest income channels; never let urgency erase consent or scope.",
            "next_actions": safe_ranked[:5],
            "channel_suggestions": [
                {
                    "channel": "remote-employment",
                    "action": "Tailor one high-fit application around verified QA, IT, software, or AI experience.",
                    "cadence": "1-3 high-quality applications per workday",
                },
                {
                    "channel": "ethical-bounties",
                    "action": "Review only programs with a public scope and create a written test plan before touching a target.",
                    "cadence": "one scoped program review per week",
                },
                {
                    "channel": "creator-products",
                    "action": "Package one existing project asset, template, prompt system, or game component into a small sellable release.",
                    "cadence": "one shippable product slice per month",
                },
                {
                    "channel": "technical-services",
                    "action": "Offer a clearly bounded repo health, QA, documentation, or prototype audit with fixed deliverables.",
                    "cadence": "two targeted pitches per week",
                },
            ],
            "custody": "All payouts go directly to an owner-controlled account. LIMEN stores receipts, never keys.",
        }

    def _receipt(self, event: str, payload: dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "payload": payload,
        }
        with self.receipts_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")
