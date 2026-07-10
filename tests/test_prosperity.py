import tempfile
import unittest
from pathlib import Path

from limen.prosperity import Opportunity, ProsperityEngine


class ProsperityTests(unittest.TestCase):
    def test_unauthorized_bug_bounty_is_not_recommended(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = ProsperityEngine(Path(tmp) / ".limen")
            engine.initialize()
            engine.add(
                Opportunity.create(
                    "Unknown target",
                    category="bug-bounty",
                    source="random message",
                    estimated_value_usd=5000,
                    probability=0.8,
                    effort_hours=1,
                    alignment=5,
                    lawful_authorization=False,
                )
            )
            self.assertEqual([], engine.plan()["next_actions"])

    def test_expected_value_affects_ranking(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = ProsperityEngine(Path(tmp) / ".limen")
            engine.initialize()
            engine.add(
                Opportunity.create(
                    "Small service",
                    category="service",
                    source="owner",
                    estimated_value_usd=100,
                    probability=0.8,
                    effort_hours=2,
                    alignment=4,
                    lawful_authorization=True,
                )
            )
            engine.add(
                Opportunity.create(
                    "Long low-probability project",
                    category="product",
                    source="owner",
                    estimated_value_usd=100,
                    probability=0.1,
                    effort_hours=20,
                    alignment=4,
                    lawful_authorization=True,
                )
            )
            ranked = engine.ranked()
            self.assertEqual("Small service", ranked[0]["title"])


if __name__ == "__main__":
    unittest.main()
