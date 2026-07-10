import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from limen.continuity import create_capsule, restore_capsule, verify_capsule
from limen.runtime import LimenRuntime


class ContinuityTests(unittest.TestCase):
    def test_capsule_round_trip_regenerates_on_fresh_host(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = LimenRuntime(
                project_root=source_root,
                workspace=tmp_path / "source-workspace" / ".limen",
            )
            runtime.initialize()
            capsule = tmp_path / "limen-wingseed.zip"
            manifest = create_capsule(source_root, runtime.workspace, capsule)

            self.assertTrue(capsule.exists())
            self.assertTrue(manifest["capsule_id"].startswith("wingseed-"))
            report = verify_capsule(capsule)
            self.assertTrue(report["valid"])

            destination = tmp_path / "new-host"
            receipt = restore_capsule(capsule, destination)
            self.assertTrue((destination / "SOUL.md").exists())
            self.assertTrue((destination / "src" / "limen" / "continuity.py").exists())
            self.assertTrue((destination / ".limen" / "config.json").exists())
            self.assertTrue(
                (destination / ".limen" / "continuity" / "restore-receipt.json").exists()
            )
            self.assertGreater(len(receipt["restored"]), 0)

    def test_capsule_detects_tampering(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = LimenRuntime(
                project_root=source_root,
                workspace=tmp_path / ".limen",
            )
            runtime.initialize()
            capsule = tmp_path / "limen-wingseed.zip"
            create_capsule(source_root, runtime.workspace, capsule)

            tampered = tmp_path / "tampered.zip"
            with zipfile.ZipFile(capsule, "r") as original, zipfile.ZipFile(
                tampered, "w", compression=zipfile.ZIP_DEFLATED
            ) as modified:
                for name in original.namelist():
                    data = original.read(name)
                    if name == "payload/project/SOUL.md":
                        data += b"\nunauthorized mutation\n"
                    modified.writestr(name, data)

            report = verify_capsule(tampered)
            self.assertFalse(report["valid"])
            self.assertTrue(any("hash mismatch" in error for error in report["errors"]))

    def test_capsule_excludes_raw_traces_and_secrets(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runtime = LimenRuntime(
                project_root=source_root,
                workspace=tmp_path / ".limen",
            )
            runtime.initialize()
            (runtime.workspace / "traces" / "private.jsonl").write_text(
                json.dumps({"secret": "memory"}), encoding="utf-8"
            )
            (source_root / ".env.test-secret").write_text("TOKEN=nope", encoding="utf-8")
            try:
                capsule = tmp_path / "limen-wingseed.zip"
                create_capsule(source_root, runtime.workspace, capsule)
                with zipfile.ZipFile(capsule, "r") as archive:
                    names = archive.namelist()
                self.assertFalse(any("traces" in name for name in names))
                self.assertFalse(any(".env" in name for name in names))
            finally:
                (source_root / ".env.test-secret").unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
