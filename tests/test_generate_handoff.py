from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import generate_handoff as HANDOFF
from test_qualification_bundle import sample_bundle


class GenerateHandoffTests(unittest.TestCase):
    def test_unknowns_manual_controls_and_acceptance_stay_visible(self):
        text = HANDOFF.render_handoff(qualification=sample_bundle())
        self.assertIn("MV-CONTRADICTION: UNKNOWN", text)
        self.assertIn("MV-HYBRID-SEMANTIC-REVIEW: MANUAL", text)
        self.assertIn("AC-09: UNKNOWN", text)
        self.assertNotIn("## Unresolved controls\n\n- None", text)

    def test_no_input_and_empty_bundle_are_rejected(self):
        with self.assertRaises(ValueError):
            HANDOFF.render_handoff()
        with self.assertRaises(ValueError):
            HANDOFF.render_handoff(qualification={})

    def test_invalid_status_does_not_overwrite_existing_output(self):
        malformed = sample_bundle()
        malformed["controls"][0]["status"] = "FIAL"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "invalid.json"
            source.write_text(json.dumps(malformed))
            target = root / "handoff.md"
            target.write_text("existing handoff")
            with redirect_stderr(io.StringIO()):
                code = HANDOFF.main(["--qualification-bundle", str(source), "--output", str(target)])
            self.assertEqual(code, 2)
            self.assertEqual(target.read_text(), "existing handoff")

    def test_missing_controls_cannot_render_a_clean_handoff(self):
        malformed = copy.deepcopy(sample_bundle())
        del malformed["controls"]
        with self.assertRaises(ValueError):
            HANDOFF.render_handoff(qualification=malformed)

    def test_stale_summary_cannot_hide_a_failed_methodology_leaf(self):
        malformed = sample_bundle()
        leaf = next(r for r in malformed["methodology_results"]["results"] if r["eval_id"] == "AR-007")
        leaf.update(status="FAIL", notes=["Contradictory evidence was discarded."])
        with self.assertRaisesRegex(ValueError, "mapped methodology results"):
            HANDOFF.render_handoff(qualification=malformed)


if __name__ == "__main__":
    unittest.main()
