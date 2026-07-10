import tempfile
import unittest
from pathlib import Path

from limen.spaces import JSpace, JSpaceHost, SpaceNavigator, SubspaceCue


class SpatialRealmTests(unittest.TestCase):
    def test_hyperspace_normalizes_branches_and_does_not_execute(self):
        with tempfile.TemporaryDirectory() as tmp:
            nav = SpaceNavigator(Path(tmp) / ".limen")
            result = nav.hyperspace.explore("Ship a truthful prototype", paths=5)
            self.assertEqual(len(result["branches"]), 5)
            self.assertAlmostEqual(
                sum(branch["amplitude"] for branch in result["branches"]),
                1.0,
                places=6,
            )
            self.assertFalse(result["execution_authorized"])
            self.assertLessEqual(result["selected"]["risk"], 0.35)

    def test_subspace_is_local_and_has_no_external_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            nav = SpaceNavigator(Path(tmp) / ".limen")
            nav.subspace.incubate(
                SubspaceCue.create(
                    "A recurring world motif",
                    salience=0.8,
                    domain="creation",
                )
            )
            state = nav.subspace.inspect()
            self.assertTrue(state["local_only"])
            self.assertFalse(state["external_action"])
            dream = nav.subspace.dream()
            self.assertFalse(dream["external_action"])
            self.assertIn("creation", dream["pattern"])

    def test_jspace_requires_explicit_authorization(self):
        with tempfile.TemporaryDirectory() as tmp:
            jspace = JSpace(Path(tmp) / ".limen")
            with self.assertRaises(PermissionError):
                JSpaceHost.create("Unknown", "secret", authorized=False)
            home = JSpaceHost.create(
                "Home",
                "home-pairing-secret",
                capabilities=["ollama"],
                home=True,
                authorized=True,
            )
            jspace.register(home)
            travel = JSpaceHost.create(
                "Travel",
                "travel-pairing-secret",
                capabilities=["cpu"],
                authorized=True,
            )
            jspace.register(travel)
            route = jspace.route("Travel")
            self.assertEqual(route["destination"]["name"], "Travel")
            self.assertEqual(route["return_anchor"]["name"], "Home")
            self.assertFalse(route["execution_authorized"])
            self.assertNotEqual(route["destination"]["fingerprint"], "travel-pairing-secret")


if __name__ == "__main__":
    unittest.main()
