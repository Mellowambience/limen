import tempfile
import unittest
from datetime import date
from pathlib import Path

from limen.steward import LifeSteward, LifeTask


class LifeStewardTests(unittest.TestCase):
    def test_plan_prioritizes_care_and_revenue_without_exceeding_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            steward = LifeSteward(Path(tmp) / ".limen")
            steward.initialize()
            steward.add_task(
                LifeTask.create(
                    "Recovery block", domain="care", minutes=30, impact=5, energy_required=1
                )
            )
            steward.add_task(
                LifeTask.create(
                    "Tailor application", domain="work", minutes=60, impact=4, revenue=5
                )
            )
            steward.add_task(
                LifeTask.create(
                    "Huge optional task", domain="admin", minutes=400, impact=5
                )
            )
            plan = steward.plan_day(
                energy=3, available_minutes=150, day=date(2026, 7, 10)
            )
            titles = {item["title"] for item in plan["focus"]}
            self.assertIn("Recovery block", titles)
            self.assertIn("Tailor application", titles)
            self.assertNotIn("Huge optional task", titles)
            self.assertLessEqual(
                plan["focus_minutes"] + plan["recovery_minutes"],
                plan["available_minutes"],
            )


if __name__ == "__main__":
    unittest.main()
