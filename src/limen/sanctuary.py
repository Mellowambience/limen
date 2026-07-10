from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


_JUNK_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
_JUNK_SUFFIXES = {".pyc", ".pyo", ".tmp", ".bak", ".swp"}
_PROTECTED = {".git", ".venv", "venv", "node_modules"}


class Sanctuary:
    """Meticulous, reversible workspace hygiene.

    The protocol is inspired by the user's preference for OCD-level organization,
    but it does not model or romanticize a clinical disorder. Cleanup is scoped,
    previewable, and never touches protected directories or user data by default.
    """

    def __init__(self, project_root: Path, workspace: Path):
        self.project_root = project_root.resolve()
        self.directory = workspace / "sanctuary"
        self.manifest_path = self.directory / "manifest.json"

    def initialize(self) -> list[Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        if not self.manifest_path.exists():
            self.manifest_path.write_text(
                json.dumps(
                    {
                        "schema_version": "0.1",
                        "principles": [
                            "everything has a home",
                            "every artifact has provenance",
                            "cleanup is previewed before deletion",
                            "private data is never reorganized silently",
                            "clarity serves creation rather than perfectionism",
                        ],
                        "last_audit": None,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            return [self.manifest_path]
        return []

    def _candidates(self) -> list[Path]:
        candidates: list[Path] = []
        for path in self.project_root.rglob("*"):
            if any(part in _PROTECTED for part in path.relative_to(self.project_root).parts):
                continue
            if path.is_dir() and path.name in _JUNK_DIRS:
                candidates.append(path)
            elif path.is_file() and path.suffix.lower() in _JUNK_SUFFIXES:
                candidates.append(path)
        # Remove nested duplicates when an entire directory is already scheduled.
        directories = {p for p in candidates if p.is_dir()}
        return sorted(
            [p for p in candidates if not any(parent in directories for parent in p.parents)],
            key=lambda item: str(item),
        )

    def audit(self) -> dict[str, Any]:
        self.initialize()
        candidates = self._candidates()
        report = {
            "root": str(self.project_root),
            "candidate_count": len(candidates),
            "candidates": [str(path.relative_to(self.project_root)) for path in candidates],
            "policy": "preview-only until clean --apply is explicitly requested",
            "created_at": _now(),
        }
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        manifest["last_audit"] = report
        self.manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return report

    def clean(self, *, apply: bool = False) -> dict[str, Any]:
        candidates = self._candidates()
        removed: list[str] = []
        if apply:
            for path in candidates:
                relative = str(path.relative_to(self.project_root))
                if path.is_dir():
                    shutil.rmtree(path)
                elif path.exists():
                    path.unlink()
                removed.append(relative)
        return {
            "applied": apply,
            "removed": removed,
            "would_remove": [] if apply else [
                str(path.relative_to(self.project_root)) for path in candidates
            ],
            "created_at": _now(),
        }
