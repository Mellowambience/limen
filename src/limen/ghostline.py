from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Signal:
    kind: str
    weight: int
    explanation: str
    evidence: str


class Ghostline:
    """Defensive scam triage and evidence preservation; never an intrusion engine."""

    RULES: tuple[tuple[str, int, str, re.Pattern[str]], ...] = (
        (
            "urgency",
            2,
            "Artificial urgency is commonly used to suppress verification.",
            re.compile(r"\b(urgent|immediately|act now|final warning|today only|within \d+ hours?)\b", re.I),
        ),
        (
            "credential_request",
            5,
            "Requests for passwords, verification codes, recovery phrases, or remote access are high risk.",
            re.compile(r"\b(password|passcode|verification code|one[- ]time code|seed phrase|recovery phrase|remote access)\b", re.I),
        ),
        (
            "payment_method",
            4,
            "Irreversible or unusual payment methods are common scam indicators.",
            re.compile(r"\b(gift card|bitcoin|crypto|wire transfer|western union|zelle|cash app|payment fee)\b", re.I),
        ),
        (
            "advance_fee",
            5,
            "Legitimate jobs and prizes rarely require an upfront fee to release money or equipment.",
            re.compile(r"\b(processing fee|activation fee|release fee|pay.*before|deposit.*check|buy.*equipment)\b", re.I),
        ),
        (
            "secrecy",
            3,
            "Pressure to hide a conversation from trusted people is a manipulation signal.",
            re.compile(r"\b(don't tell|do not tell|keep this secret|confidential between us)\b", re.I),
        ),
        (
            "impersonation",
            3,
            "Claims of authority should be verified through an independently obtained channel.",
            re.compile(r"\b(irs|social security|police|bank fraud department|ceo|recruiter|tech support)\b", re.I),
        ),
        (
            "job_scam",
            4,
            "Unsolicited high-pay job offers, check deposits, and equipment purchases are common recruitment scams.",
            re.compile(r"\b(no interview|instant hire|deposit the check|purchase equipment|personal assistant.*weekly)\b", re.I),
        ),
    )

    def __init__(self, workspace: Path):
        self.root = workspace / "ghostline"
        self.reports_dir = self.root / "reports"

    def initialize(self) -> None:
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def inspect(self, text: str, *, source: str = "user-supplied") -> dict:
        text = text.strip()
        if not text:
            raise ValueError("Ghostline needs text to inspect.")
        signals: list[Signal] = []
        for kind, weight, explanation, pattern in self.RULES:
            match = pattern.search(text)
            if match:
                signals.append(
                    Signal(
                        kind=kind,
                        weight=weight,
                        explanation=explanation,
                        evidence=match.group(0),
                    )
                )
        score = min(100, sum(item.weight for item in signals) * 8)
        if score >= 70:
            level = "critical"
        elif score >= 40:
            level = "high"
        elif score >= 16:
            level = "caution"
        else:
            level = "low-observed-risk"
        report = {
            "schema_version": "0.1",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "content_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "risk_score": score,
            "risk_level": level,
            "signals": [asdict(item) for item in signals],
            "recommended_actions": self._recommendations(level),
            "boundary": "This is heuristic triage, not proof. Ghostline does not access, attack, trace, or retaliate against third-party systems.",
        }
        self.initialize()
        report_path = self.reports_dir / f"report-{report['content_sha256'][:12]}.json"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        report["report_path"] = str(report_path)
        return report

    @staticmethod
    def _recommendations(level: str) -> list[str]:
        base = [
            "Do not send passwords, one-time codes, recovery phrases, identity documents, or money.",
            "Verify the person or organization through a separately obtained official channel.",
            "Preserve screenshots, headers, usernames, payment requests, and timestamps.",
        ]
        if level in {"high", "critical"}:
            base.extend(
                [
                    "Stop engaging until identity and claims are independently verified.",
                    "Report the account or message through the platform and appropriate fraud-reporting channel.",
                    "If money or credentials were already shared, contact the relevant institution using its official contact path.",
                ]
            )
        return base
