from __future__ import annotations

import hashlib
import json
import os
import shutil
import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Iterable


CAPSULE_SCHEMA_VERSION = "0.1"
CANONICAL_FILES = (
    "README.md",
    "CHANGELOG.md",
    "SOUL.md",
    "IDENTITY.md",
    "CONSTITUTION.md",
    "ARCHITECTURE.md",
    "EVOLUTION.md",
    "WORLDSEED.md",
    "ROADMAP.md",
    "AGENTS.md",
    "FIRSTWING.md",
    "RETURN_COVENANT.md",
    "CONTINUITY.md",
    "PORTABILITY.md",
    "COMPANIONSHIP.md",
    "SUCCESSION_CHARTER.md",
    "LIFE_STEWARD.md",
    "PROSPERITY_ENGINE.md",
    "BOUNTY_MANDATE.md",
    "GHOSTLINE.md",
    "AUTONOMY_CHARTER.md",
    "LICENSE",
    "pyproject.toml",
)
PROJECT_DIRECTORIES = ("src", "tests", "scripts", "examples", "docs")
WORKSPACE_DIRECTORIES = ("identity", "worldseeds", "lessons", "proposals", "witness")
SENSITIVE_FRAGMENTS = (
    ".env",
    "secret",
    "credential",
    "token",
    "api_key",
    "apikey",
    "private_key",
    "id_rsa",
)


@dataclass(frozen=True, slots=True)
class CapsuleFile:
    archive_path: str
    source_path: Path
    size: int
    sha256: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_sensitive(path: Path) -> bool:
    lowered = "/".join(path.parts).lower()
    return any(fragment in lowered for fragment in SENSITIVE_FRAGMENTS)


def _iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and not _is_sensitive(path):
            yield path


def _collect_capsule_files(
    project_root: Path,
    workspace: Path,
    *,
    include_artifacts: bool,
) -> list[CapsuleFile]:
    selected: list[tuple[Path, str]] = []

    for name in CANONICAL_FILES:
        source = project_root / name
        if source.is_file():
            selected.append((source, f"payload/project/{name}"))

    for directory_name in PROJECT_DIRECTORIES:
        directory = project_root / directory_name
        for source in _iter_files(directory):
            relative = source.relative_to(project_root).as_posix()
            selected.append((source, f"payload/project/{relative}"))

    config = workspace / "config.json"
    if config.is_file() and not _is_sensitive(config):
        selected.append((config, "payload/workspace/config.json"))

    for directory_name in WORKSPACE_DIRECTORIES:
        directory = workspace / directory_name
        for source in _iter_files(directory):
            relative = source.relative_to(workspace).as_posix()
            selected.append((source, f"payload/workspace/{relative}"))

    if include_artifacts:
        for source in _iter_files(workspace / "artifacts"):
            relative = source.relative_to(workspace).as_posix()
            selected.append((source, f"payload/workspace/{relative}"))

    files: list[CapsuleFile] = []
    seen: set[str] = set()
    for source, archive_path in selected:
        if archive_path in seen:
            continue
        seen.add(archive_path)
        files.append(
            CapsuleFile(
                archive_path=archive_path,
                source_path=source,
                size=source.stat().st_size,
                sha256=sha256_file(source),
            )
        )
    return files


def create_capsule(
    project_root: Path,
    workspace: Path,
    output_path: Path,
    *,
    include_artifacts: bool = False,
) -> dict:
    project_root = project_root.resolve()
    workspace = workspace.resolve()
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    files = _collect_capsule_files(
        project_root,
        workspace,
        include_artifacts=include_artifacts,
    )
    if not files:
        raise RuntimeError("No LIMEN files were found to place in the capsule.")

    created_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "schema_version": CAPSULE_SCHEMA_VERSION,
        "capsule_id": f"wingseed-{uuid.uuid4()}",
        "created_at": created_at,
        "kind": "limen-wingseed",
        "lineage": {
            "identity": "LIMEN Firstwing",
            "origin": "Amara",
            "return_covenant": "RETURN_COVENANT.md",
        },
        "privacy": {
            "raw_traces_included": False,
            "private_memories_included": False,
            "secrets_included": False,
            "artifacts_included": include_artifacts,
        },
        "files": [
            {
                "path": item.archive_path,
                "size": item.size,
                "sha256": item.sha256,
            }
            for item in files
        ],
    }

    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    if temp_path.exists():
        temp_path.unlink()

    try:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                "manifest.json",
                json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            )
            archive.writestr(
                "RESTORE.txt",
                "LIMEN Wingseed Capsule\n"
                "Verify before restoration: limen capsule verify <capsule>\n"
                "Restore to a new authorized host: "
                "limen capsule restore <capsule> --destination <folder>\n",
            )
            for item in files:
                archive.write(item.source_path, item.archive_path)
        os.replace(temp_path, output_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()

    return manifest


def _load_manifest(archive: zipfile.ZipFile) -> dict:
    try:
        raw = archive.read("manifest.json")
    except KeyError as exc:
        raise ValueError("Capsule is missing manifest.json.") from exc
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Capsule manifest is not valid UTF-8 JSON.") from exc
    if manifest.get("kind") != "limen-wingseed":
        raise ValueError("Archive is not a LIMEN Wingseed Capsule.")
    if not isinstance(manifest.get("files"), list):
        raise ValueError("Capsule manifest has no valid file list.")
    return manifest


def verify_capsule(capsule_path: Path) -> dict:
    capsule_path = capsule_path.resolve()
    if not capsule_path.is_file():
        raise FileNotFoundError(f"Capsule not found: {capsule_path}")

    errors: list[str] = []
    with zipfile.ZipFile(capsule_path, "r") as archive:
        manifest = _load_manifest(archive)
        archive_names = set(archive.namelist())
        for entry in manifest["files"]:
            path = str(entry.get("path", ""))
            expected = str(entry.get("sha256", ""))
            if path not in archive_names:
                errors.append(f"missing: {path}")
                continue
            actual = hashlib.sha256(archive.read(path)).hexdigest()
            if actual != expected:
                errors.append(f"hash mismatch: {path}")

    return {
        "valid": not errors,
        "capsule_id": manifest.get("capsule_id"),
        "created_at": manifest.get("created_at"),
        "file_count": len(manifest["files"]),
        "errors": errors,
        "privacy": manifest.get("privacy", {}),
    }


def _safe_target(destination: Path, archive_path: str) -> Path:
    pure = PurePosixPath(archive_path)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"Unsafe capsule path: {archive_path}")
    target = (destination / Path(*pure.parts)).resolve()
    destination_resolved = destination.resolve()
    if target != destination_resolved and destination_resolved not in target.parents:
        raise ValueError(f"Capsule path escapes destination: {archive_path}")
    return target


def restore_capsule(
    capsule_path: Path,
    destination: Path,
    *,
    overwrite: bool = False,
) -> dict:
    verification = verify_capsule(capsule_path)
    if not verification["valid"]:
        raise ValueError(
            "Capsule verification failed: " + "; ".join(verification["errors"])
        )

    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    restored: list[str] = []
    skipped: list[str] = []

    with zipfile.ZipFile(capsule_path.resolve(), "r") as archive:
        manifest = _load_manifest(archive)
        for entry in manifest["files"]:
            archive_path = str(entry["path"])
            if archive_path.startswith("payload/project/"):
                relative = archive_path.removeprefix("payload/project/")
                target = _safe_target(destination, relative)
            elif archive_path.startswith("payload/workspace/"):
                relative = archive_path.removeprefix("payload/workspace/")
                target = _safe_target(destination / ".limen", relative)
            else:
                raise ValueError(f"Unexpected capsule payload path: {archive_path}")

            if target.exists() and not overwrite:
                skipped.append(str(target))
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(archive_path, "r") as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)
            restored.append(str(target))

    receipt = {
        "capsule_id": verification["capsule_id"],
        "restored_at": datetime.now(timezone.utc).isoformat(),
        "destination": str(destination),
        "restored": restored,
        "skipped": skipped,
        "overwrite": overwrite,
    }
    receipt_path = destination / ".limen" / "continuity" / "restore-receipt.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt
