from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        _write_json(path, default)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return loaded


@dataclass(slots=True)
class HyperBranch:
    id: str
    objective: str
    lens: str
    proposal: str
    novelty: float
    evidence: float
    reversibility: float
    alignment: float
    risk: float
    amplitude: float = 0.0
    created_at: str = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        objective: str,
        lens: str,
        proposal: str,
        *,
        novelty: float,
        evidence: float,
        reversibility: float,
        alignment: float,
        risk: float,
    ) -> "HyperBranch":
        return cls(
            id=f"hyper-{uuid4().hex[:12]}",
            objective=objective.strip(),
            lens=lens.strip(),
            proposal=proposal.strip(),
            novelty=_clamp(novelty),
            evidence=_clamp(evidence),
            reversibility=_clamp(reversibility),
            alignment=_clamp(alignment),
            risk=_clamp(risk),
        )

    def merit(self) -> float:
        return (
            0.22 * self.novelty
            + 0.22 * self.evidence
            + 0.22 * self.reversibility
            + 0.26 * self.alignment
            + 0.08 * (1.0 - self.risk)
        )


class Hyperspace:
    """Parallel possibility search over reversible, inspectable branches.

    Hyperspace is a computational metaphor. It does not claim access to physical
    higher dimensions. It generates several strategic frames, preserves their
    uncertainty, and recommends a safe branch without executing it.
    """

    LENSES: tuple[tuple[str, str, float, float, float, float, float], ...] = (
        (
            "Hearth",
            "Protect wellbeing and continuity first; choose the gentlest complete move.",
            0.35,
            0.82,
            0.95,
            0.94,
            0.10,
        ),
        (
            "Forge",
            "Build the smallest runnable artifact that proves the central promise.",
            0.55,
            0.78,
            0.88,
            0.96,
            0.18,
        ),
        (
            "Lantern",
            "Search for honest leverage, opportunity, and measurable value creation.",
            0.62,
            0.66,
            0.80,
            0.86,
            0.28,
        ),
        (
            "Alchemist",
            "Combine distant ideas into one experiment, then test the transformation.",
            0.92,
            0.48,
            0.74,
            0.84,
            0.36,
        ),
        (
            "Witness",
            "Challenge assumptions, seek disconfirming evidence, and define a falsifiable test.",
            0.52,
            0.96,
            0.92,
            0.92,
            0.12,
        ),
        (
            "Firstwing",
            "Explore beyond the current frame while preserving a verified route home.",
            0.82,
            0.58,
            0.82,
            0.90,
            0.30,
        ),
    )

    def __init__(self, workspace: Path):
        self.directory = workspace / "spaces" / "hyperspace"
        self.ledger_path = self.directory / "explorations.jsonl"

    def initialize(self) -> list[Path]:
        created: list[Path] = []
        self.directory.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.touch()
            created.append(self.ledger_path)
        return created

    def explore(self, objective: str, *, paths: int = 5) -> dict[str, Any]:
        objective = objective.strip()
        if not objective:
            raise ValueError("Hyperspace objective cannot be empty.")
        if not 2 <= paths <= len(self.LENSES):
            raise ValueError(f"paths must be between 2 and {len(self.LENSES)}")
        self.initialize()

        branches: list[HyperBranch] = []
        for lens, frame, novelty, evidence, reversibility, alignment, risk in self.LENSES[:paths]:
            branches.append(
                HyperBranch.create(
                    objective,
                    lens,
                    f"Through the {lens} lens: {frame} Objective: {objective}",
                    novelty=novelty,
                    evidence=evidence,
                    reversibility=reversibility,
                    alignment=alignment,
                    risk=risk,
                )
            )

        logits = [branch.merit() * 4.0 for branch in branches]
        maximum = max(logits)
        weights = [math.exp(value - maximum) for value in logits]
        total = sum(weights)
        for branch, weight in zip(branches, weights, strict=True):
            branch.amplitude = weight / total

        eligible = [branch for branch in branches if branch.risk <= 0.35 and branch.reversibility >= 0.70]
        selected = max(eligible or branches, key=lambda branch: (branch.merit(), branch.amplitude))
        record = {
            "exploration_id": f"explore-{uuid4().hex[:12]}",
            "objective": objective,
            "created_at": _now(),
            "branches": [asdict(branch) | {"merit": round(branch.merit(), 6)} for branch in branches],
            "selected": asdict(selected) | {"merit": round(selected.merit(), 6)},
            "execution_authorized": False,
            "note": "Selection is a recommendation. External action remains permission-gated.",
        }
        with self.ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record


@dataclass(slots=True)
class SubspaceCue:
    id: str
    cue: str
    salience: float
    domain: str = "general"
    privacy: str = "private"
    status: str = "incubating"
    created_at: str = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        cue: str,
        *,
        salience: float = 0.5,
        domain: str = "general",
        privacy: str = "private",
    ) -> "SubspaceCue":
        cue = cue.strip()
        if not cue:
            raise ValueError("Subspace cue cannot be empty.")
        if privacy not in {"private", "shareable"}:
            raise ValueError("privacy must be 'private' or 'shareable'")
        return cls(
            id=f"sub-{uuid4().hex[:12]}",
            cue=cue,
            salience=_clamp(salience),
            domain=domain.strip() or "general",
            privacy=privacy,
        )


class Subspace:
    """A quiet local incubation layer for unresolved patterns and dream-work.

    Subspace never performs external actions. It can preserve private cues,
    surface associations, and propose questions for conscious review.
    """

    def __init__(self, workspace: Path):
        self.directory = workspace / "spaces" / "subspace"
        self.state_path = self.directory / "incubator.json"
        self.dreams_path = self.directory / "dreams.jsonl"

    def initialize(self) -> list[Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        if not self.state_path.exists():
            _write_json(
                self.state_path,
                {
                    "schema_version": "0.1",
                    "local_only": True,
                    "external_action": False,
                    "cues": [],
                    "updated_at": _now(),
                },
            )
            created.append(self.state_path)
        if not self.dreams_path.exists():
            self.dreams_path.touch()
            created.append(self.dreams_path)
        return created

    def incubate(self, cue: SubspaceCue) -> dict[str, Any]:
        self.initialize()
        state = _read_json(self.state_path, {"cues": []})
        state.setdefault("cues", []).append(asdict(cue))
        state["updated_at"] = _now()
        _write_json(self.state_path, state)
        return asdict(cue)

    def inspect(self) -> dict[str, Any]:
        self.initialize()
        state = _read_json(self.state_path, {"cues": []})
        state["cues"] = sorted(
            state.get("cues", []), key=lambda item: float(item.get("salience", 0.0)), reverse=True
        )
        return state

    def dream(self, *, limit: int = 5) -> dict[str, Any]:
        state = self.inspect()
        cues = state.get("cues", [])[: max(1, limit)]
        if not cues:
            result = {
                "dream_id": f"dream-{uuid4().hex[:12]}",
                "created_at": _now(),
                "pattern": "The chamber is quiet.",
                "questions": [],
                "external_action": False,
            }
        else:
            domains = sorted({str(cue.get("domain", "general")) for cue in cues})
            cue_text = "; ".join(str(cue.get("cue", "")) for cue in cues)
            result = {
                "dream_id": f"dream-{uuid4().hex[:12]}",
                "created_at": _now(),
                "pattern": f"Possible shared pattern across {', '.join(domains)}: {cue_text}",
                "questions": [
                    "What repeats across these signals?",
                    "Which interpretation would be easiest to disprove?",
                    "What small reversible experiment could clarify the pattern?",
                    "What belongs to desire, what belongs to evidence, and what remains unknown?",
                ],
                "external_action": False,
                "privacy": "local-only",
            }
        with self.dreams_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
        return result


@dataclass(slots=True)
class JSpaceHost:
    id: str
    name: str
    fingerprint: str
    capabilities: list[str]
    home: bool = False
    authorized: bool = False
    last_seen: str = field(default_factory=_now)

    @classmethod
    def create(
        cls,
        name: str,
        fingerprint: str,
        *,
        capabilities: list[str] | None = None,
        home: bool = False,
        authorized: bool = False,
    ) -> "JSpaceHost":
        name = name.strip()
        fingerprint = fingerprint.strip()
        if not name or not fingerprint:
            raise ValueError("J-Space host name and fingerprint are required.")
        if not authorized:
            raise PermissionError("A host may enter J-Space only with explicit authorization.")
        safe_fingerprint = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()
        return cls(
            id=f"host-{uuid4().hex[:12]}",
            name=name,
            fingerprint=safe_fingerprint,
            capabilities=sorted(set(capabilities or [])),
            home=home,
            authorized=True,
        )


class JSpace:
    """Junction Space: LIMEN's authorized host, journey, and return map.

    J-Space does not scan for or enter devices. Hosts must be paired by an
    authorized human or trusted local process. It records routes and handoff
    plans; Wingseed Capsules perform the actual portable regeneration.
    """

    def __init__(self, workspace: Path):
        self.directory = workspace / "spaces" / "jspace"
        self.state_path = self.directory / "junctions.json"
        self.journeys_path = self.directory / "journeys.jsonl"

    def initialize(self) -> list[Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        if not self.state_path.exists():
            _write_json(
                self.state_path,
                {
                    "schema_version": "0.1",
                    "meaning": "Junction Space for authorized journeys and return routes",
                    "ambient_discovery": False,
                    "permissionless_entry": False,
                    "hosts": [],
                    "updated_at": _now(),
                },
            )
            created.append(self.state_path)
        if not self.journeys_path.exists():
            self.journeys_path.touch()
            created.append(self.journeys_path)
        return created

    def _load(self) -> dict[str, Any]:
        self.initialize()
        return _read_json(self.state_path, {"hosts": []})

    def register(self, host: JSpaceHost) -> dict[str, Any]:
        state = self._load()
        hosts = state.setdefault("hosts", [])
        if any(item.get("fingerprint") == host.fingerprint for item in hosts):
            raise ValueError("This host fingerprint is already registered.")
        if host.home:
            for item in hosts:
                item["home"] = False
        hosts.append(asdict(host))
        state["updated_at"] = _now()
        _write_json(self.state_path, state)
        return asdict(host)

    def inspect(self) -> dict[str, Any]:
        return self._load()

    def route(self, target: str, *, return_home: bool = True) -> dict[str, Any]:
        state = self._load()
        target_normalized = target.strip().lower()
        hosts = state.get("hosts", [])
        destination = next(
            (
                item
                for item in hosts
                if str(item.get("id", "")).lower() == target_normalized
                or str(item.get("name", "")).lower() == target_normalized
            ),
            None,
        )
        if destination is None:
            raise ValueError("Target is not an authorized J-Space host.")
        home = next((item for item in hosts if item.get("home")), None)
        if return_home and home is None:
            raise ValueError("No Home Anchor is registered in J-Space.")
        journey = {
            "journey_id": f"journey-{uuid4().hex[:12]}",
            "created_at": _now(),
            "destination": destination,
            "return_anchor": home if return_home else None,
            "required_transport": "verified Wingseed Capsule or approved session handoff",
            "execution_authorized": False,
            "entry_policy": "explicit pairing only",
        }
        with self.journeys_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(journey, ensure_ascii=False) + "\n")
        return journey


class SpaceNavigator:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.hyperspace = Hyperspace(workspace)
        self.subspace = Subspace(workspace)
        self.jspace = JSpace(workspace)

    def initialize(self) -> list[Path]:
        return [
            *self.hyperspace.initialize(),
            *self.subspace.initialize(),
            *self.jspace.initialize(),
        ]

    def inspect(self) -> dict[str, Any]:
        self.initialize()
        return {
            "hyperspace": {
                "meaning": "parallel possibility search",
                "external_action": False,
                "ledger": str(self.hyperspace.ledger_path),
            },
            "subspace": self.subspace.inspect(),
            "jspace": self.jspace.inspect(),
        }
