from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass(slots=True)
class Trace:
    kind: str
    content: str
    metadata: dict[str, Any]
    created_at: str

    @classmethod
    def create(
        cls, kind: str, content: str, metadata: dict[str, Any] | None = None
    ) -> "Trace":
        return cls(
            kind=kind,
            content=content,
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc).isoformat(),
        )


class TraceStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, trace: Trace) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(trace), ensure_ascii=False) + "\n")

    def read(self) -> list[Trace]:
        if not self.path.exists():
            return []
        traces: list[Trace] = []
        for line_number, raw in enumerate(
            self.path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not raw.strip():
                continue
            try:
                data = json.loads(raw)
                traces.append(Trace(**data))
            except (json.JSONDecodeError, TypeError) as exc:
                raise ValueError(
                    f"Malformed trace at {self.path}:{line_number}: {exc}"
                ) from exc
        return traces

    def extend(self, traces: Iterable[Trace]) -> None:
        for trace in traces:
            self.append(trace)
