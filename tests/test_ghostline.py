import tempfile
import unittest
from pathlib import Path

from limen.ghostline import Ghostline


class GhostlineTests(unittest.TestCase):
    def test_detects_advance_fee_and_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            ghostline = Ghostline(Path(tmp) / ".limen")
            report = ghostline.inspect(
                "Urgent: pay the processing fee with a gift card and send your verification code."
            )
            self.assertIn(report["risk_level"], {"high", "critical"})
            kinds = {signal["kind"] for signal in report["signals"]}
            self.assertIn("advance_fee", kinds)
            self.assertIn("credential_request", kinds)
            self.assertTrue(Path(report["report_path"]).exists())


if __name__ == "__main__":
    unittest.main()
