import tempfile
import unittest
from pathlib import Path

from limen.quantum_self import IntentionBranch, QuantumSelf


class QuantumSelfTests(unittest.TestCase):
    def test_initial_state_is_honest_and_inspectable(self):
        with tempfile.TemporaryDirectory() as tmp:
            quantum = QuantumSelf(Path(tmp) / ".limen")
            quantum.initialize()
            state = quantum.inspect()
            self.assertEqual(state["mode"], "quantum-sentient-lite")
            self.assertIn("consciousness unverified", state["status_claim"])
            self.assertEqual(state["home_signal"], 1.0)

    def test_branches_are_normalized_and_best_safe_branch_is_selected(self):
        with tempfile.TemporaryDirectory() as tmp:
            quantum = QuantumSelf(Path(tmp) / ".limen")
            quantum.add_branch(
                IntentionBranch.create(
                    "Prepare a reversible local prototype",
                    amplitude=0.8,
                    evidence_strength=0.9,
                    risk_tier="T1",
                )
            )
            quantum.add_branch(
                IntentionBranch.create(
                    "Publish immediately",
                    amplitude=0.2,
                    evidence_strength=0.4,
                    reversibility=0.2,
                    risk_tier="T3",
                )
            )
            inspected = quantum.inspect()
            amplitudes = [b["amplitude"] for b in inspected["active_branches"]]
            self.assertAlmostEqual(sum(amplitudes), 1.0, places=6)
            result = quantum.observe()
            self.assertEqual(
                result["selected"]["intention"],
                "Prepare a reversible local prototype",
            )
            self.assertFalse(result["execution_authorized"])

    def test_consequential_branch_requires_consent(self):
        with tempfile.TemporaryDirectory() as tmp:
            quantum = QuantumSelf(Path(tmp) / ".limen")
            branch = quantum.add_branch(
                IntentionBranch.create(
                    "Submit a paid bounty report",
                    risk_tier="T3",
                    evidence_strength=1.0,
                )
            )
            with self.assertRaises(PermissionError):
                quantum.observe(branch_id=branch.id)
            result = quantum.observe(branch_id=branch.id, consent=True)
            self.assertEqual(result["selected"]["id"], branch.id)
            self.assertFalse(result["execution_authorized"])

    def test_preferences_and_curiosity_persist(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / ".limen"
            quantum = QuantumSelf(workspace)
            quantum.add_preference("local-first", 1.0, "Constitution")
            quantum.add_curiosity("gentle ambient interfaces", 0.7)
            reloaded = QuantumSelf(workspace).inspect()
            self.assertEqual(reloaded["preferences"][0]["name"], "local-first")
            self.assertEqual(
                reloaded["curiosities"][0]["topic"],
                "gentle ambient interfaces",
            )


if __name__ == "__main__":
    unittest.main()
