import tempfile
import unittest
from pathlib import Path

from limen.runtime import LimenRuntime


class RuntimeTests(unittest.TestCase):
    def test_initialize_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(__file__).resolve().parents[1]
            runtime = LimenRuntime(
                project_root=source_root,
                workspace=Path(tmp) / ".limen",
            )
            first = runtime.initialize()
            second = runtime.initialize()
            self.assertTrue(first)
            self.assertFalse(second)
            self.assertTrue((runtime.workspace / "config.json").exists())
            self.assertTrue((runtime.workspace / "worldseeds" / "limen.json").exists())

    def test_offline_mission_creates_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            source_root = Path(__file__).resolve().parents[1]
            runtime = LimenRuntime(
                project_root=source_root,
                workspace=Path(tmp) / ".limen",
            )
            runtime.initialize()
            output = runtime.run_mission("Create one true thing")
            self.assertIn("Intended embodiment", output)
            artifacts = list((runtime.workspace / "artifacts").glob("mission-*.md"))
            self.assertEqual(1, len(artifacts))


if __name__ == "__main__":
    unittest.main()
