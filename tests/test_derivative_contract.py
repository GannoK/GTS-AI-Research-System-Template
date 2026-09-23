from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("airst_validate", ROOT / "tools" / "airst_validate.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def base_manifest():
    invariants=json.loads((ROOT / "INVARIANTS.json").read_text(encoding="utf-8"))
    return {
        "schema_version":"1.0","manifest_id":"TEST-DERIVATIVE",
        "parent":{"template_id":"GTS-AIRST","canonical_name":"GTS AI Research System Template","release_version":"0.2.0","tag":"v0.2.0-test","commit":"a"*40,"repository_manifest_sha256":"b"*64,"component_registry_sha256":"c"*64},
        "derivative":{"derivative_id":"TEST","name":"Test","domain":"test","owning_project":"TEST","repository":"example/test","development_state":"DRAFT"},
        "inheritance_policy":"PRESERVE_UNLESS_DECLARED",
        "preserved_invariants":[i["id"] for i in invariants["invariants"]],
        "mutations":[],"domain_extensions":[],
        "qualification":{"state":"UNQUALIFIED","bundle_ref":"","qualified_parent_commit":"","last_reviewed_at":""},
        "upstream":{"compatibility_state":"UNKNOWN","synchronization_state":"PINNED","last_parent_review_version":"0.2.0","last_parent_review_commit":"a"*40,"known_incompatibilities":[]},
        "history":[]
    }


class DerivativeContractTests(unittest.TestCase):
    def validate(self, data):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"manifest.json"
            p.write_text(json.dumps(data),encoding="utf-8")
            return MODULE.validate_derivative_manifest(p)

    def test_valid_sparse_manifest(self):
        self.assertEqual(self.validate(base_manifest()), [])

    def test_core_replacement_is_rejected(self):
        data=base_manifest()
        data["mutations"]=[{"component_id":"core-research-invariants","mutation":"REPLACE","rationale":"test","covered_invariants":data["preserved_invariants"],"invariant_impact":"REQUIRES_REVIEW","coverage_evidence":["test"],"qualification_controls":[],"decision_refs":[]}]
        errors=self.validate(data)
        self.assertTrue(any("not permitted" in e for e in errors))

    def test_replace_requires_coverage_evidence(self):
        data=base_manifest()
        data["mutations"]=[{"component_id":"source-register","mutation":"REPLACE","rationale":"test","covered_invariants":[],"invariant_impact":"NONE","coverage_evidence":[],"qualification_controls":[],"decision_refs":[]}]
        errors=self.validate(data)
        self.assertTrue(any("requires coverage_evidence" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
