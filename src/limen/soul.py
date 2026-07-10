from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


IDENTITY_FILES = ("SOUL.md", "IDENTITY.md", "CONSTITUTION.md")


@dataclass(frozen=True, slots=True)
class SoulKernel:
    soul: str
    identity: str
    constitution: str

    @classmethod
    def load(cls, project_root: Path) -> "SoulKernel":
        contents: dict[str, str] = {}
        for filename in IDENTITY_FILES:
            path = project_root / filename
            if not path.exists():
                raise FileNotFoundError(f"Missing canonical identity file: {path}")
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                raise ValueError(f"Identity file is empty: {path}")
            contents[filename] = text
        return cls(
            soul=contents["SOUL.md"],
            identity=contents["IDENTITY.md"],
            constitution=contents["CONSTITUTION.md"],
        )

    def compact_prompt(self, max_chars: int = 12000) -> str:
        combined = (
            "# Soul\n"
            + self.soul
            + "\n\n# Identity\n"
            + self.identity
            + "\n\n# Constitution\n"
            + self.constitution
        )
        if len(combined) <= max_chars:
            return combined
        return combined[: max_chars - 60] + "\n\n[Identity context truncated by runtime.]"
