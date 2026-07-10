from __future__ import annotations

import json
from pathlib import Path

from .models import Worldseed


def load_worldseed(path: Path) -> Worldseed:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Worldseed not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid Worldseed JSON at {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Worldseed root must be a JSON object.")
    return Worldseed.from_dict(data)


def save_worldseed(worldseed: Worldseed, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(worldseed.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
