from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import airst_validate
from schema_validation import DRAFT, check_schema, validate_instance


class SchemaContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "schemas", self.root / "schemas")
        for name in ("AIRST_METADATA.json", "PACK_METADATA.json", "INVARIANTS.json",
                     "COMPONENT_REGISTRY.json", "ASSURANCE.json", "CITATION.cff"):
            shutil.copy2(ROOT / name, self.root / name)
        self.root_patch = patch.object(airst_validate, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def change(self, name, edit):
        path = self.root / name
        value = json.loads(path.read_text())
        edit(value)
        path.write_text(json.dumps(value))

    def test_incomplete_metadata_and_registry_are_rejected(self):
        self.change("AIRST_METADATA.json", lambda value: value.pop("commit_identity"))
        self.change("COMPONENT_REGISTRY.json", lambda value: value["components"][0].pop("dependencies"))
        errors = airst_validate.validate_schema_documents()
        self.assertTrue(any("commit_identity" in error for error in errors))
        self.assertTrue(any("dependencies" in error for error in errors))
        self.assertTrue(airst_validate.validate_identity())
        inv_errors, ids = airst_validate.validate_invariants()
        self.assertEqual(inv_errors, [])
        reg_errors, components = airst_validate.validate_component_registry(ids)
        self.assertTrue(reg_errors)
        self.assertEqual(components, {})

    def test_invariant_statement_must_be_text(self):
        self.change("INVARIANTS.json", lambda value: value["invariants"][0].update(statement=True))
        errors, ids = airst_validate.validate_invariants()
        self.assertTrue(any("statement" in error for error in errors))
        self.assertEqual(ids, set())

    def test_unknown_assurance_status_is_rejected(self):
        self.change("ASSURANCE.json", lambda value: value["result_states"].append("FIAL"))
        self.assertTrue(any("FIAL" in error for error in airst_validate.validate_schema_documents()))

    def test_declared_versions_and_license_cannot_drift(self):
        self.assertEqual(airst_validate.validate_identity(), [])
        self.change("PACK_METADATA.json", lambda value: value.update(version="999.0.0", license="unreviewed"))
        errors = airst_validate.validate_identity()
        self.assertTrue(any("version" in error for error in errors))
        self.assertTrue(any("license" in error for error in errors))

    def test_missing_derivative_sections_and_wrong_types_fail_in_template_mode(self):
        base = json.loads((ROOT / "07_TEMPLATES/13_DERIVATIVE_MUTATION_MANIFEST_TEMPLATE.json").read_text())
        cases = []
        for key in ("schema_version", "manifest_id", "preserved_invariants", "history"):
            value = copy.deepcopy(base)
            value.pop(key)
            cases.append(value)
        value = copy.deepcopy(base)
        value["qualification"]["bundle_ref"] = False
        cases.append(value)
        for value in cases:
            with self.subTest(value=value):
                path = self.root / "derivative.json"
                path.write_text(json.dumps(value))
                self.assertTrue(airst_validate.validate_derivative_manifest(path, allow_template=True))

    def test_template_mode_cannot_claim_qualified_or_populated_parent(self):
        base = json.loads((ROOT / "07_TEMPLATES/13_DERIVATIVE_MUTATION_MANIFEST_TEMPLATE.json").read_text())
        for change in (lambda value: value["qualification"].update(state="QUALIFIED"),
                       lambda value: value["parent"].update(commit="a" * 40)):
            value = copy.deepcopy(base)
            change(value)
            path = self.root / "template.json"
            path.write_text(json.dumps(value))
            self.assertTrue(airst_validate.validate_derivative_manifest(path, allow_template=True))

    def test_external_invalid_json_reports_failure_without_traceback(self):
        path = self.root / "outside-repository.json"
        path.write_text("{")
        with patch.object(airst_validate, "ROOT", ROOT):
            errors = airst_validate.validate_derivative_manifest(path)
        self.assertTrue(any("invalid JSON" in error for error in errors))

    def test_schema_definition_is_actually_checked(self):
        path = self.root / "bad.schema.json"
        path.write_text(json.dumps({"$schema": DRAFT, "$id": "urn:test:bad", "type": "invented-type"}))
        self.assertTrue(check_schema(path))

    def test_unresolved_remote_references_fail_without_network_access(self):
        path = self.root / "remote.schema.json"
        path.write_text(json.dumps({"$schema": DRAFT, "$id": "urn:test:remote", "$ref": "https://example.invalid/schema"}))
        with patch("urllib.request.urlopen", side_effect=AssertionError("network access attempted")):
            errors = validate_instance({}, path)
        self.assertTrue(errors)
        self.assertTrue(any("could not be completed" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
