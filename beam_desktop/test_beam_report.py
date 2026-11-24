import tempfile
import unittest
from pathlib import Path

from beam_analysis import BeamLoad, BeamState, analyze
from beam_report import create_calculation_sheet


class BeamReportTests(unittest.TestCase):
    def test_calculation_sheet_creates_a_pdf(self) -> None:
        analysis = analyze(
            BeamState(
                support="simply-supported",
                span=20,
                loads=(BeamLoad("uniform", 1, start=0, end=20),),
                material="steel",
                section="W12x26",
                deflection_limit=360,
            )
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "calculation-sheet.pdf"
            create_calculation_sheet(path, analysis)
            content = path.read_bytes()

        self.assertTrue(content.startswith(b"%PDF-"))
        self.assertIn(b"/Type /Page", content)
        self.assertGreater(len(content), 5_000)


if __name__ == "__main__":
    unittest.main()
