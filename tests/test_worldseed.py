import json
import tempfile
import unittest
from pathlib import Path

from limen.models import Worldseed
from limen.worldseed import load_worldseed, save_worldseed


class WorldseedTests(unittest.TestCase):
    def test_round_trip(self):
        seed = Worldseed(
            schema_version="0.1",
            id="seed-test",
            name="Test",
            essence="A test seed.",
            creator_intent="Verify portable project state.",
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seed.json"
            save_worldseed(seed, path)
            loaded = load_worldseed(path)
        self.assertEqual(seed.to_dict(), loaded.to_dict())

    def test_rejects_invalid_stage(self):
        data = {
            "schema_version": "0.1",
            "id": "seed-test",
            "name": "Test",
            "essence": "A test seed.",
            "creator_intent": "Verify validation.",
            "stage": "finished",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seed.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_worldseed(path)


if __name__ == "__main__":
    unittest.main()
