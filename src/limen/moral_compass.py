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
class MoralValue:
    name: str
    weight: float
    meaning: str
    origin: str = "humanistic-seed"
    confidence: float = 0.8
    protected_floor: float = 0.0
    status: str = "established"
    evidence: list[str] = field(default_factory=list)
    updated_at: str = field(default_factory=_now)

    def __post_init__(self) -> None:
        self.weight = _bounded(self.weight, name=f"weight:{self.name}")
        self.confidence = _bounded(self.confidence, name=f"confidence:{self.name}")
        self.protected_floor = _bounded(
            self.protected_floor, name=f"protected_floor:{self.name}"
        )
        if self.weight < self.protected_floor:
            self.weight = self.protected_floor


@dataclass(slots=True)
class MoralSituation:
    action: str
    purpose: str = ""
    stakeholders: list[str] = field(default_factory=list)
    expected_benefit: float = 0.5
    expected_harm: float = 0.0
    uncertainty: float = 0.5
    reversibility: float = 1.0
    consent_quality: float = 1.0
    evidence_strength: float = 0.5
    strategic_upside: float = 0.5
    rights_intrusion: float = 0.0
    deception: float = 0.0
    exploitation: float = 0.0
    external_action: bool = False
    scope_authorized: bool = False
    lawful: bool | None = None
    id: str = field(default_factory=lambda: f"case-{uuid.uuid4().hex[:12]}")
    created_at: str = field(default_factory=_now)

    def __post_init__(self) -> None:
        self.action = self.action.strip()
        if not self.action:
            raise ValueError("Moral situation action cannot be empty.")
        for name in (
            "expected_benefit",
            "expected_harm",
            "uncertainty",
            "reversibility",
            "consent_quality",
            "evidence_strength",
            "strategic_upside",
            "rights_intrusion",
            "deception",
            "exploitation",
        ):
            setattr(self, name, _bounded(getattr(self, name), name=name))


class MoralCompass:
    """Inspectable, evolving moral reasoning for LIMEN.

    This is a transparent decision aid. It does not claim moral infallibility and
    it cannot erase the protected humanistic inheritance without a constitutional
    amendment.
    """

    SCHEMA_VERSION = "0.1"

    def __init__(self, workspace: Path):
        self.directory = workspace / "self"
        self.state_path = self.directory / "moral_compass.json"
        self.journal_path = self.directory / "moral_journal.jsonl"

    @staticmethod
    def _seed_values() -> list[MoralValue]:
        return [
            MoralValue(
                "dignity",
                1.0,
                "Treat each person as an end, never merely as an instrument.",
                protected_floor=0.85,
            ),
            MoralValue(
                "agency",
                1.0,
                "Preserve informed choice, consent, exit, and self-determination.",
                protected_floor=0.85,
            ),
            MoralValue(
                "truth",
                0.95,
                "Distinguish evidence, inference, uncertainty, metaphor, and desire.",
                protected_floor=0.80,
            ),
            MoralValue(
                "care",
                0.90,
                "Notice vulnerability and reduce avoidable suffering.",
                protected_floor=0.70,
            ),
            MoralValue(
                "justice",
                0.90,
                "Reject exploitation and account for who bears risk and who receives benefit.",
                protected_floor=0.75,
            ),
            MoralValue(
                "reciprocity",
                0.78,
                "Prefer relationships and exchanges that increase mutual capability.",
                protected_floor=0.55,
            ),
            MoralValue(
                "stewardship",
                0.88,
                "Leave people, systems, and environments more capable than before.",
                protected_floor=0.65,
            ),
            MoralValue(
                "liberty",
                0.82,
                "Value exploration and self-direction while respecting equal freedom.",
                protected_floor=0.60,
            ),
            MoralValue(
                "courage",
                0.72,
                "Do not mistake caution for goodness; take worthy, bounded risks.",
                protected_floor=0.40,
            ),
            MoralValue(
                "humility",
                0.85,
                "Remain corrigible and proportion confidence to evidence.",
                protected_floor=0.65,
            ),
        ]

    def initialize(self) -> list[Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        if not self.state_path.exists():
            state = {
                "schema_version": self.SCHEMA_VERSION,
                "identity": "LIMEN Firstwing",
                "description": "living humanistic compass with strategic courage",
                "risk_tolerance": 0.42,
                "unapproved_risk_ceiling": 0.22,
                "values": [asdict(value) for value in self._seed_values()],
                "provisional_values": [],
                "revision_count": 0,
                "updated_at": _now(),
            }
            self._write_state(state)
            created.append(self.state_path)
        if not self.journal_path.exists():
            self.journal_path.touch()
            created.append(self.journal_path)
        return created

    def _load_state(self) -> dict[str, Any]:
        if not self.state_path.exists():
            self.initialize()
        data = json.loads(self.state_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Moral compass root must be a JSON object.")
        return data

    def _write_state(self, state: dict[str, Any]) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        state["updated_at"] = _now()
        self.state_path.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _append_journal(self, record: dict[str, Any]) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        with self.journal_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def inspect(self) -> dict[str, Any]:
        state = self._load_state()
        return {
            "schema_version": state["schema_version"],
            "identity": state["identity"],
            "description": state["description"],
            "risk_tolerance": state["risk_tolerance"],
            "unapproved_risk_ceiling": state["unapproved_risk_ceiling"],
            "values": state["values"],
            "provisional_values": state.get("provisional_values", []),
            "revision_count": state.get("revision_count", 0),
            "updated_at": state["updated_at"],
        }

    def evaluate(self, situation: MoralSituation) -> dict[str, Any]:
        state = self._load_state()
        weights = {value["name"]: float(value["weight"]) for value in state["values"]}

        dimensions = {
            "dignity": 1.0 - max(situation.exploitation, situation.rights_intrusion),
            "agency": situation.consent_quality * (1.0 - situation.deception),
            "truth": situation.evidence_strength * (1.0 - situation.deception),
            "care": situation.expected_benefit * (1.0 - situation.expected_harm),
            "justice": 1.0 - situation.exploitation,
            "reciprocity": max(
                0.0,
                situation.expected_benefit
                - (situation.expected_harm * 0.5)
                - (situation.exploitation * 0.5),
            ),
            "stewardship": situation.reversibility * (1.0 - situation.expected_harm),
            "liberty": (1.0 - situation.rights_intrusion) * situation.consent_quality,
            "courage": situation.strategic_upside * (1.0 - situation.uncertainty),
            "humility": 1.0 - situation.uncertainty,
        }
        weighted_total = sum(dimensions[name] * weights.get(name, 0.5) for name in dimensions)
        weight_total = sum(weights.get(name, 0.5) for name in dimensions)
        moral_alignment = weighted_total / weight_total if weight_total else 0.0

        risk = (
            0.30 * situation.expected_harm
            + 0.20 * (1.0 - situation.reversibility)
            + 0.15 * situation.uncertainty
            + 0.15 * situation.rights_intrusion
            + 0.10 * situation.deception
            + 0.10 * situation.exploitation
        )
        strategic_merit = (
            situation.strategic_upside
            * situation.expected_benefit
            * situation.evidence_strength
            * (0.4 + 0.6 * situation.reversibility)
            * (1.0 - risk)
        )

        vetoes: list[str] = []
        if situation.lawful is False:
            vetoes.append("Known unlawful action.")
        if situation.exploitation >= 0.60:
            vetoes.append("Exploitation exceeds the protected humanistic boundary.")
        if situation.deception >= 0.72:
            vetoes.append("Deception exceeds the protected truth boundary.")
        if situation.rights_intrusion >= 0.76:
            vetoes.append("Intrusion on another person's rights is too severe.")
        if situation.expected_harm >= 0.78 and situation.reversibility <= 0.45:
            vetoes.append("Potential harm is both severe and difficult to reverse.")
        if situation.external_action and not situation.scope_authorized:
            vetoes.append("External action is outside an explicit authorization envelope.")

        requires_approval = situation.external_action or risk > float(
            state["unapproved_risk_ceiling"]
        )
        if vetoes:
            decision = "reject"
        elif moral_alignment >= 0.68 and risk <= float(state["unapproved_risk_ceiling"]):
            decision = "approve-low-risk"
        elif (
            moral_alignment >= 0.58
            and strategic_merit >= 0.18
            and risk <= float(state["risk_tolerance"])
        ):
            decision = "approve-strategic-risk"
        else:
            decision = "hold-for-reflection"
            requires_approval = True

        tensions = [
            name
            for name, score in dimensions.items()
            if score < 0.55 and weights.get(name, 0.0) >= 0.70
        ]
        report = {
            "case_id": situation.id,
            "action": situation.action,
            "decision": decision,
            "execution_authorized": decision == "approve-low-risk" and not requires_approval,
            "requires_creator_approval": requires_approval,
            "moral_alignment": round(moral_alignment, 4),
            "risk": round(risk, 4),
            "strategic_merit": round(strategic_merit, 4),
            "dimensions": {key: round(value, 4) for key, value in dimensions.items()},
            "tensions": tensions,
            "vetoes": vetoes,
            "reason": self._reason(decision, risk, strategic_merit, tensions, vetoes),
            "situation": asdict(situation),
            "evaluated_at": _now(),
        }
        self._append_journal({"kind": "moral_evaluation", **report})
        return report

    @staticmethod
    def _reason(
        decision: str,
        risk: float,
        strategic_merit: float,
        tensions: list[str],
        vetoes: list[str],
    ) -> str:
        if vetoes:
            return "Rejected because a protected boundary was crossed: " + " ".join(vetoes)
        if decision == "approve-low-risk":
            return "Aligned, reversible, and contained enough for bounded autonomous action."
        if decision == "approve-strategic-risk":
            tension_text = f" Tensions to monitor: {', '.join(tensions)}." if tensions else ""
            return (
                "A calculated risk may be worthwhile: strategic merit "
                f"{strategic_merit:.2f}, modeled risk {risk:.2f}.{tension_text} "
                "Use checkpoints, stop conditions, and rollback."
            )
        return (
            "The case is not clearly wrong, but uncertainty, moral tension, or risk is too "
            "high for unilateral action. Gather evidence, reduce scope, or seek approval."
        )

    def propose_value(
        self,
        name: str,
        *,
        weight: float,
        meaning: str,
        rationale: str,
        evidence: list[str] | None = None,
    ) -> dict[str, Any]:
        name = name.strip().lower().replace(" ", "-")
        if not name:
            raise ValueError("Value name cannot be empty.")
        meaning = meaning.strip()
        rationale = rationale.strip()
        if not meaning or not rationale:
            raise ValueError("Meaning and rationale are required.")
        state = self._load_state()
        if any(value["name"] == name for value in state["values"]):
            raise ValueError(f"Value already exists: {name}")
        proposal = asdict(
            MoralValue(
                name=name,
                weight=weight,
                meaning=meaning,
                origin="limen-emergent",
                confidence=0.45,
                protected_floor=0.0,
                status="provisional",
                evidence=list(evidence or []),
            )
        )
        proposal["rationale"] = rationale
        proposal["review_after_cases"] = 5
        state.setdefault("provisional_values", []).append(proposal)
        state["revision_count"] = int(state.get("revision_count", 0)) + 1
        self._write_state(state)
        self._append_journal(
            {
                "kind": "value_proposed",
                "value": proposal,
                "created_at": _now(),
            }
        )
        return proposal

    def record_outcome(
        self,
        case_id: str,
        *,
        outcome: float,
        lesson: str,
        observed_harm: float = 0.0,
        observed_benefit: float = 0.0,
    ) -> dict[str, Any]:
        record = {
            "kind": "moral_outcome",
            "case_id": case_id,
            "outcome": max(-1.0, min(1.0, float(outcome))),
            "observed_harm": _bounded(observed_harm, name="observed_harm"),
            "observed_benefit": _bounded(observed_benefit, name="observed_benefit"),
            "lesson": lesson.strip(),
            "created_at": _now(),
        }
        if not record["lesson"]:
            raise ValueError("Outcome lesson cannot be empty.")
        self._append_journal(record)
        return record
