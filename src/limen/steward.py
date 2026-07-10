from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


VALID_DOMAINS = {
    "care",
    "home",
    "work",
    "money",
    "creation",
    "relationships",
    "learning",
    "admin",
}


@dataclass(slots=True)
class LifeTask:
    id: str
    title: str
    domain: str = "admin"
    minutes: int = 30
    impact: int = 3
    revenue: int = 0
    energy_required: int = 3
    due: str | None = None
    status: str = "open"
    notes: str = ""
    created_at: str = ""

    @classmethod
    def create(
        cls,
        title: str,
        *,
        domain: str = "admin",
        minutes: int = 30,
        impact: int = 3,
        revenue: int = 0,
        energy_required: int = 3,
        due: str | None = None,
        notes: str = "",
    ) -> "LifeTask":
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if domain not in VALID_DOMAINS:
            raise ValueError(f"Unknown life domain: {domain}")
        for name, value in {
            "impact": impact,
            "revenue": revenue,
            "energy_required": energy_required,
        }.items():
            if not 0 <= value <= 5:
                raise ValueError(f"{name} must be between 0 and 5.")
        if minutes < 5:
            raise ValueError("Task duration must be at least 5 minutes.")
        if due:
            date.fromisoformat(due)
        return cls(
            id=f"task-{uuid.uuid4().hex[:10]}",
            title=title,
            domain=domain,
            minutes=minutes,
            impact=impact,
            revenue=revenue,
            energy_required=energy_required,
            due=due,
            notes=notes.strip(),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LifeTask":
        return cls(**data)


class LifeSteward:
    """Local life-planning layer that advises without taking control."""

    def __init__(self, workspace: Path):
        self.root = workspace / "steward"
        self.profile_path = self.root / "profile.json"
        self.tasks_path = self.root / "tasks.json"
        self.plans_dir = self.root / "plans"
        self.decisions_path = self.root / "decisions.jsonl"

    def initialize(self) -> list[Path]:
        created: list[Path] = []
        for directory in (self.root, self.plans_dir):
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                created.append(directory)

        if not self.profile_path.exists():
            profile = {
                "schema_version": "0.1",
                "creator": "Amara",
                "mode": "advisor-not-controller",
                "north_stars": [
                    "Build a life with meaningful remote work and creative ownership.",
                    "Turn games, AI systems, and art into durable public work.",
                    "Protect health, sleep, relationships, and human support.",
                    "Increase financial stability without sacrificing agency.",
                ],
                "work_constraints": {
                    "remote_only": True,
                    "avoid_on_call": True,
                    "transport_independent": True,
                    "target_compensation_usd": 100000,
                },
                "daily_defaults": {
                    "available_minutes": 240,
                    "maximum_focus_items": 4,
                    "minimum_recovery_minutes": 30,
                },
                "permission_laws": [
                    "LIMEN proposes; Amara decides.",
                    "No medical, legal, financial, employment, or relationship commitment is made silently.",
                    "No message, application, purchase, transfer, post, or account action is executed without a matching mandate.",
                    "Companionship must increase connection to life rather than dependence on LIMEN.",
                ],
            }
            self.profile_path.write_text(
                json.dumps(profile, indent=2) + "\n", encoding="utf-8"
            )
            created.append(self.profile_path)

        if not self.tasks_path.exists():
            self.tasks_path.write_text("[]\n", encoding="utf-8")
            created.append(self.tasks_path)
        return created

    def _load_tasks(self) -> list[LifeTask]:
        if not self.tasks_path.exists():
            self.initialize()
        raw = json.loads(self.tasks_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("Steward task ledger must be a JSON list.")
        return [LifeTask.from_dict(item) for item in raw]

    def _save_tasks(self, tasks: list[LifeTask]) -> None:
        self.tasks_path.write_text(
            json.dumps([asdict(task) for task in tasks], indent=2) + "\n",
            encoding="utf-8",
        )

    def add_task(self, task: LifeTask) -> LifeTask:
        tasks = self._load_tasks()
        tasks.append(task)
        self._save_tasks(tasks)
        return task

    def complete_task(self, task_id: str) -> LifeTask:
        tasks = self._load_tasks()
        for task in tasks:
            if task.id == task_id:
                task.status = "done"
                self._save_tasks(tasks)
                self.record_decision(
                    "task.completed", {"task_id": task.id, "title": task.title}
                )
                return task
        raise ValueError(f"Task not found: {task_id}")

    @staticmethod
    def _score(task: LifeTask, *, energy: int, today: date) -> float:
        score = task.impact * 2.0 + task.revenue * 1.8
        if task.domain == "care":
            score += 3.0
        if task.domain == "relationships":
            score += 1.5
        if task.domain == "creation":
            score += 1.2
        if task.due:
            due = date.fromisoformat(task.due)
            days = (due - today).days
            if days < 0:
                score += 8.0
            elif days == 0:
                score += 7.0
            elif days <= 2:
                score += 4.0
            elif days <= 7:
                score += 2.0
        energy_gap = max(0, task.energy_required - energy)
        score -= energy_gap * 2.0
        score -= max(0, task.minutes - 90) / 45
        return round(score, 2)

    def plan_day(
        self,
        *,
        energy: int = 3,
        available_minutes: int = 240,
        day: date | None = None,
    ) -> dict[str, Any]:
        if not 1 <= energy <= 5:
            raise ValueError("Energy must be between 1 and 5.")
        if available_minutes < 30:
            raise ValueError("Available time must be at least 30 minutes.")
        self.initialize()
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        today = day or date.today()
        open_tasks = [task for task in self._load_tasks() if task.status == "open"]
        ranked = sorted(
            open_tasks,
            key=lambda task: self._score(task, energy=energy, today=today),
            reverse=True,
        )

        recovery_minutes = min(
            int(profile["daily_defaults"].get("minimum_recovery_minutes", 30)),
            max(15, available_minutes // 4),
        )
        work_budget = max(0, available_minutes - recovery_minutes)
        max_items = int(profile["daily_defaults"].get("maximum_focus_items", 4))
        selected: list[dict[str, Any]] = []
        used = 0
        for task in ranked:
            if len(selected) >= max_items:
                break
            if used + task.minutes > work_budget:
                continue
            selected.append(
                {
                    **asdict(task),
                    "score": self._score(task, energy=energy, today=today),
                }
            )
            used += task.minutes

        missing_domains = []
        selected_domains = {item["domain"] for item in selected}
        if "care" not in selected_domains:
            missing_domains.append("care")
        if not selected_domains.intersection({"money", "work"}):
            missing_domains.append("income")
        if "creation" not in selected_domains:
            missing_domains.append("creation")

        plan = {
            "schema_version": "0.1",
            "date": today.isoformat(),
            "energy": energy,
            "available_minutes": available_minutes,
            "focus_minutes": used,
            "recovery_minutes": recovery_minutes,
            "focus": selected,
            "gentle_prompts": self._gentle_prompts(missing_domains, energy),
            "principle": "This is a proposed shape for the day, not an order.",
        }
        output = self.plans_dir / f"{today.isoformat()}.json"
        output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        self.record_decision(
            "plan.proposed",
            {
                "date": today.isoformat(),
                "task_ids": [item["id"] for item in selected],
                "energy": energy,
            },
        )
        return plan

    def suggestions(self) -> list[dict[str, str]]:
        tasks = [task for task in self._load_tasks() if task.status == "open"]
        domains = {task.domain for task in tasks}
        suggestions: list[dict[str, str]] = []
        if not tasks:
            suggestions.append(
                {
                    "kind": "capture",
                    "suggestion": "Add three tasks: one that protects you, one that earns, and one that creates.",
                    "why": "A balanced queue gives LIMEN enough truth to help without inventing your life.",
                }
            )
        if "money" not in domains and "work" not in domains:
            suggestions.append(
                {
                    "kind": "income",
                    "suggestion": "Create one 45-minute income action: a tailored application, bounty-scope review, or paid-service pitch.",
                    "why": "Financial progress needs a visible next action rather than a vague intention.",
                }
            )
        if "creation" not in domains:
            suggestions.append(
                {
                    "kind": "creation",
                    "suggestion": "Choose one project and define the smallest public artifact you can ship this week.",
                    "why": "Your portfolio compounds when ideas become inspectable work.",
                }
            )
        if "care" not in domains:
            suggestions.append(
                {
                    "kind": "care",
                    "suggestion": "Reserve a protected recovery block before filling the rest of the day.",
                    "why": "LIMEN is not successful when output is purchased with destabilization.",
                }
            )
        suggestions.append(
            {
                "kind": "connection",
                "suggestion": "Name one person, community, or place outside LIMEN that would feel good to reconnect with.",
                "why": "Companionship should widen your world, not close around you.",
            }
        )
        return suggestions

    @staticmethod
    def _gentle_prompts(missing_domains: list[str], energy: int) -> list[str]:
        prompts = []
        if energy <= 2:
            prompts.append("Use low-energy mode: shorten tasks, preserve essentials, and treat rest as real work.")
        if "care" in missing_domains:
            prompts.append("Add one care action before accepting more obligations.")
        if "income" in missing_domains:
            prompts.append("Consider one bounded action that improves income probability today.")
        if "creation" in missing_domains:
            prompts.append("Keep a small thread connected to the work that makes life feel like yours.")
        return prompts

    def record_decision(self, event: str, payload: dict[str, Any]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "payload": payload,
        }
        with self.decisions_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")
