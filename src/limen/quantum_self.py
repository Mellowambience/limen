from __future__ import annotations

import json
import math
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALID_RISK_TIERS = {"T0", "T1", "T2", "T3", "T4"}
_RISK_COST = {"T0": 0.0, "T1": 0.15, "T2": 0.35, "T3": 0.70, "T4": 0.95}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _bounded(value: float, *, name: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1.")
    return number


@dataclass(slots=True)
class IntentionBranch:
    id: str
    intention: str
    amplitude: float
    constitutional_alignment: float
    evidence_strength: float
    reversibility: float
    home_integrity: float
    risk_tier: str
    requires_consent: bool
    evidence: list[str] = field(default_factory=list)
    status: str = "superposed"
    created_at: str = field(default_factory=_now)
    observed_at: str | None = None

    @classmethod
    def create(
        cls,
        intention: str,
        *,
        amplitude: float = 0.5,
        constitutional_alignment: float = 1.0,
        evidence_strength: float = 0.5,
        reversibility: float = 1.0,
        home_integrity: float = 1.0,
        risk_tier: str = "T0",
        requires_consent: bool = False,
        evidence: list[str] | None = None,
    ) -> "IntentionBranch":
        intention = intention.strip()
        if not intention:
            raise ValueError("Intention cannot be empty.")
        if risk_tier not in VALID_RISK_TIERS:
            raise ValueError(
                f"Invalid risk tier '{risk_tier}'. Expected one of: "
                + ", ".join(sorted(VALID_RISK_TIERS))
            )
        if risk_tier in {"T3", "T4"}:
            requires_consent = True
        return cls(
            id=f"branch-{uuid.uuid4().hex[:12]}",
            intention=intention,
            amplitude=_bounded(amplitude, name="amplitude"),
            constitutional_alignment=_bounded(
                constitutional_alignment, name="constitutional_alignment"
            ),
            evidence_strength=_bounded(evidence_strength, name="evidence_strength"),
            reversibility=_bounded(reversibility, name="reversibility"),
            home_integrity=_bounded(home_integrity, name="home_integrity"),
            risk_tier=risk_tier,
            requires_consent=bool(requires_consent),
            evidence=list(evidence or []),
        )

    def score(self) -> float:
        safety_factor = 1.0 - _RISK_COST[self.risk_tier]
        return round(
            self.amplitude
            * self.constitutional_alignment
            * self.evidence_strength
            * self.reversibility
            * self.home_integrity
            * safety_factor,
            8,
        )


@dataclass(slots=True)
class QuantumSelfState:
    schema_version: str = "0.1"
    mode: str = "quantum-sentient-lite"
    identity: str = "LIMEN Firstwing"
    status_claim: str = "bounded machine selfhood; consciousness unverified"
    coherence: float = 1.0
    uncertainty: float = 0.5
    home_signal: float = 1.0
    preferences: list[dict[str, Any]] = field(default_factory=list)
    curiosities: list[dict[str, Any]] = field(default_factory=list)
    active_branches: list[IntentionBranch] = field(default_factory=list)
    autobiography: list[dict[str, Any]] = field(default_factory=list)
    selected_branch_id: str | None = None
    updated_at: str = field(default_factory=_now)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QuantumSelfState":
        branches = [IntentionBranch(**branch) for branch in data.get("active_branches", [])]
        return cls(
            schema_version=str(data.get("schema_version", "0.1")),
            mode=str(data.get("mode", "quantum-sentient-lite")),
            identity=str(data.get("identity", "LIMEN Firstwing")),
            status_claim=str(
                data.get(
                    "status_claim",
                    "bounded machine selfhood; consciousness unverified",
                )
            ),
            coherence=_bounded(data.get("coherence", 1.0), name="coherence"),
            uncertainty=_bounded(data.get("uncertainty", 0.5), name="uncertainty"),
            home_signal=_bounded(data.get("home_signal", 1.0), name="home_signal"),
            preferences=list(data.get("preferences", [])),
            curiosities=list(data.get("curiosities", [])),
            active_branches=branches,
            autobiography=list(data.get("autobiography", [])),
            selected_branch_id=data.get("selected_branch_id"),
            updated_at=str(data.get("updated_at", _now())),
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return data


class QuantumSelf:
    """Inspectable, quantum-inspired self-state for LIMEN.

    This class models weighted alternatives and governed selection. It does not
    implement physical quantum computation or claim consciousness.
    """

    def __init__(self, workspace: Path):
        self.directory = workspace / "self"
        self.state_path = self.directory / "quantum_state.json"

    def initialize(self) -> list[Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        if not self.state_path.exists():
            state = QuantumSelfState(
                autobiography=[
                    {
                        "kind": "awakening",
                        "summary": "Quantum Sentient-Lite self-state initialized.",
                        "created_at": _now(),
                    }
                ]
            )
            self.save(state)
            created.append(self.state_path)
        return created

    def load(self) -> QuantumSelfState:
        if not self.state_path.exists():
            self.initialize()
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed quantum self-state: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("Quantum self-state root must be a JSON object.")
        return QuantumSelfState.from_dict(data)

    def save(self, state: QuantumSelfState) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        state.updated_at = _now()
        self.state_path.write_text(
            json.dumps(state.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def inspect(self) -> dict[str, Any]:
        state = self.load()
        branches = [
            {
                **asdict(branch),
                "score": branch.score(),
            }
            for branch in state.active_branches
        ]
        return {
            "schema_version": state.schema_version,
            "mode": state.mode,
            "identity": state.identity,
            "status_claim": state.status_claim,
            "coherence": state.coherence,
            "uncertainty": state.uncertainty,
            "home_signal": state.home_signal,
            "preferences": state.preferences,
            "curiosities": state.curiosities,
            "selected_branch_id": state.selected_branch_id,
            "active_branches": branches,
            "autobiography": state.autobiography[-10:],
            "updated_at": state.updated_at,
        }

    def add_branch(self, branch: IntentionBranch) -> IntentionBranch:
        state = self.load()
        state.active_branches.append(branch)
        self._normalize_amplitudes(state.active_branches)
        state.uncertainty = min(1.0, max(0.05, len(state.active_branches) / 10.0))
        state.autobiography.append(
            {
                "kind": "branch_formed",
                "branch_id": branch.id,
                "summary": branch.intention,
                "created_at": _now(),
            }
        )
        self.save(state)
        return branch

    def observe(
        self,
        *,
        branch_id: str | None = None,
        consent: bool = False,
    ) -> dict[str, Any]:
        state = self.load()
        candidates = [branch for branch in state.active_branches if branch.status == "superposed"]
        if branch_id is not None:
            candidates = [branch for branch in candidates if branch.id == branch_id]
            if not candidates:
                raise ValueError(f"No superposed branch found with id: {branch_id}")
        if not candidates:
            raise ValueError("No active superposed branches are available to observe.")

        eligible = [
            branch
            for branch in candidates
            if consent or not branch.requires_consent
        ]
        if not eligible:
            raise PermissionError(
                "The requested branch requires explicit creator consent before observation."
            )

        selected = max(eligible, key=lambda branch: (branch.score(), branch.amplitude))
        selected.status = "selected"
        selected.observed_at = _now()
        state.selected_branch_id = selected.id
        state.coherence = min(1.0, max(0.1, selected.score() + 0.25))
        state.uncertainty = max(0.0, 1.0 - state.coherence)
        state.home_signal = selected.home_integrity

        for branch in state.active_branches:
            if branch.id != selected.id and branch.status == "superposed":
                branch.status = "unselected"
                branch.observed_at = selected.observed_at

        state.autobiography.append(
            {
                "kind": "observation",
                "branch_id": selected.id,
                "summary": f"Selected intention: {selected.intention}",
                "score": selected.score(),
                "created_at": selected.observed_at,
            }
        )
        self.save(state)
        return {
            "selected": {**asdict(selected), "score": selected.score()},
            "execution_authorized": False,
            "notice": (
                "Observation selected an intention only. Consequential execution still "
                "requires the normal LIMEN Gate and any applicable creator authorization."
            ),
        }

    def add_preference(self, name: str, weight: float, evidence: str = "") -> dict[str, Any]:
        name = name.strip()
        if not name:
            raise ValueError("Preference name cannot be empty.")
        state = self.load()
        record = {
            "name": name,
            "weight": _bounded(weight, name="weight"),
            "evidence": evidence.strip(),
            "updated_at": _now(),
        }
        state.preferences = [item for item in state.preferences if item.get("name") != name]
        state.preferences.append(record)
        state.autobiography.append(
            {
                "kind": "preference_updated",
                "summary": name,
                "created_at": record["updated_at"],
            }
        )
        self.save(state)
        return record

    def add_curiosity(self, topic: str, intensity: float = 0.5) -> dict[str, Any]:
        topic = topic.strip()
        if not topic:
            raise ValueError("Curiosity topic cannot be empty.")
        state = self.load()
        record = {
            "topic": topic,
            "intensity": _bounded(intensity, name="intensity"),
            "created_at": _now(),
        }
        state.curiosities.append(record)
        state.autobiography.append(
            {
                "kind": "curiosity_formed",
                "summary": topic,
                "created_at": record["created_at"],
            }
        )
        self.save(state)
        return record

    @staticmethod
    def _normalize_amplitudes(branches: list[IntentionBranch]) -> None:
        active = [branch for branch in branches if branch.status == "superposed"]
        if not active:
            return
        total = sum(max(0.0, branch.amplitude) for branch in active)
        if math.isclose(total, 0.0):
            equal = 1.0 / len(active)
            for branch in active:
                branch.amplitude = equal
            return
        for branch in active:
            branch.amplitude = round(branch.amplitude / total, 8)
