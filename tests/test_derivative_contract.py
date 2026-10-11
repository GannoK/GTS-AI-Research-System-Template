from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import airst_validate as MODULE

from derivative_fixtures import ReleasedParent


class DerivativeContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="airst-derivative-contract-")
        self.addCleanup(self.temp.cleanup)
        self.parent = ReleasedParent(Path(self.temp.name))

    def validate(self, data):
        path = self.parent.write_manifest(data)
        with patch.object(MODULE, "ROOT", self.parent.root):
            return MODULE.validate_derivative_manifest(path)

    def test_valid_sparse_unqualified_manifest(self):
        self.assertEqual(self.validate(self.parent.manifest()), [])

    def test_core_replacement_is_rejected(self):
        data = self.parent.manifest()
        data["mutations"] = [{
            "component_id": "core-research-invariants", "mutation": "REPLACE",
            "rationale": "Regression fixture", "covered_invariants": data["preserved_invariants"],
            "invariant_impact": "REQUIRES_REVIEW", "coverage_evidence": ["test"],
            "qualification_controls": [], "decision_refs": [],
        }]
        errors = self.validate(data)
        self.assertTrue(any("not permitted" in error for error in errors), errors)

    def test_replace_requires_coverage_evidence(self):
        data = self.parent.manifest()
        data["mutations"] = [{
            "component_id": "source-register", "mutation": "REPLACE",
            "rationale": "Regression fixture", "covered_invariants": [],
            "invariant_impact": "NONE", "coverage_evidence": [],
            "qualification_controls": [], "decision_refs": [],
        }]
        errors = self.validate(data)
        self.assertTrue(any("coverage_evidence" in error for error in errors), errors)

    def test_parent_pin_mismatch_is_rejected(self):
        data = self.parent.manifest()
        data["parent"]["component_registry_sha256"] = "c" * 64
        errors = self.validate(data)
        self.assertTrue(any("component_registry_sha256" in error for error in errors), errors)

    def test_missing_schema_fields_are_rejected(self):
        data = self.parent.manifest()
        del data["manifest_id"]
        errors = self.validate(data)
        self.assertTrue(any("manifest_id" in error for error in errors), errors)

    def test_unresolved_domain_components_cannot_claim_qualification(self):
        data = self.parent.manifest()
        data["qualification"].update(
            state="QUALIFIED", bundle_ref="review/qualification.json",
            qualified_parent_commit=data["parent"]["commit"], last_reviewed_at="2026-01-01T00:00:00Z",
        )
        errors = self.validate(data)
        self.assertTrue(errors, "unresolved domain placeholders must not validate as QUALIFIED")


if __name__ == "__main__":
    unittest.main()
