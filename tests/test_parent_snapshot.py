from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import airst_validate
import check_parent_compatibility
import instantiate_derivative
import resolve_derivative
from parent_snapshot import validate_parent_pin

from derivative_fixtures import ReleasedParent


class ParentSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="airst-parent-snapshot-")
        self.addCleanup(self.temp.cleanup)
        self.parent = ReleasedParent(Path(self.temp.name))

    def call_tool(self, module, *args):
        output = io.StringIO()
        with ExitStack() as stack:
            for imported in (airst_validate, instantiate_derivative, resolve_derivative, check_parent_compatibility):
                stack.enter_context(patch.object(imported, "ROOT", self.parent.root))
            stack.enter_context(patch.object(sys, "argv", [module.__name__, *map(str, args)]))
            stack.enter_context(redirect_stdout(output))
            status = module.main()
        return status, output.getvalue()

    def instantiate(self, output: Path, *, version=None, tag=None, commit=None):
        args = [
            "--derivative-id", "TEST", "--name", "Test derivative", "--domain", "test",
            "--owning-project", "TEST", "--repository", "example/test",
            "--parent-version", version or self.parent.version,
            "--parent-tag", tag or self.parent.tag, "--output", output,
        ]
        if commit is not None:
            args.extend(["--parent-commit", commit])
        return self.call_tool(instantiate_derivative, *args)

    def test_exact_lightweight_and_annotated_tags_are_accepted(self):
        pin = self.parent.parent_pin()
        self.assertEqual(validate_parent_pin(pin, root=self.parent.root), [])
        self.parent.git("tag", "--delete", self.parent.tag)
        self.parent.git("tag", "--annotate", self.parent.tag, "-m", "Isolated annotated release")
        self.assertEqual(validate_parent_pin(pin, root=self.parent.root), [])

    def test_wrong_template_and_floating_or_mismatched_tags_are_rejected(self):
        for update in (
            {"template_id": "DIFFERENT-PROJECT"},
            {"canonical_name": "Different project"},
            {"tag": "main"},
            {"tag": "latest"},
            {"release_version": "999.0.0"},
        ):
            with self.subTest(update=update):
                pin = self.parent.parent_pin()
                pin.update(update)
                self.assertTrue(validate_parent_pin(pin, root=self.parent.root))

    def test_a_branch_named_like_a_release_cannot_substitute_for_a_tag(self):
        self.parent.git("branch", "v0.4.0")
        pin = self.parent.parent_pin()
        pin.update(release_version="0.4.0", tag="v0.4.0")
        errors = validate_parent_pin(pin, root=self.parent.root)
        self.assertTrue(any("exact parent release tag does not exist" in error for error in errors), errors)

    def test_head_and_tag_must_both_equal_the_pinned_commit(self):
        pin = self.parent.parent_pin()
        self.parent.git("commit", "--quiet", "--allow-empty", "-m", "Different local HEAD")
        errors = validate_parent_pin(pin, root=self.parent.root)
        self.assertTrue(any("HEAD differs" in error for error in errors), errors)
        pin["commit"] = self.parent.git("rev-parse", "HEAD")
        errors = validate_parent_pin(pin, root=self.parent.root)
        self.assertTrue(any("tag does not resolve" in error for error in errors), errors)

    def test_undeclared_and_unreleased_snapshots_are_rejected_even_when_tagged(self):
        original = json.loads((self.parent.root / "AIRST_METADATA.json").read_text())
        for update in ({"new_release_declared": False}, {"development_state": "UNRELEASED_HARDENING"}):
            with self.subTest(update=update):
                metadata = copy.deepcopy(original)
                metadata["release_state"].update(update)
                self.parent.write_json("AIRST_METADATA.json", metadata)
                self.parent.commit_snapshot()
                errors = validate_parent_pin(self.parent.parent_pin(), root=self.parent.root)
                self.assertTrue(any("undeclared or unreleased" in error for error in errors), errors)

    def test_declared_version_must_match_the_pin(self):
        metadata = json.loads((self.parent.root / "AIRST_METADATA.json").read_text())
        metadata["release_state"]["last_declared_version"] = "0.4.0"
        self.parent.write_json("AIRST_METADATA.json", metadata)
        self.parent.commit_snapshot()
        errors = validate_parent_pin(self.parent.parent_pin(), root=self.parent.root)
        self.assertTrue(any("declared snapshot version" in error for error in errors), errors)

    def test_both_pinned_hashes_are_checked(self):
        for key in ("repository_manifest_sha256", "component_registry_sha256"):
            with self.subTest(key=key):
                pin = self.parent.parent_pin()
                pin[key] = "0" * 64
                errors = validate_parent_pin(pin, root=self.parent.root)
                self.assertTrue(any(key in error for error in errors), errors)

    def test_rehashing_dirty_content_cannot_masquerade_as_the_tagged_parent(self):
        path = self.parent.root / "INVARIANTS.json"
        path.write_text(path.read_text() + "\n", encoding="utf-8")
        self.parent.refresh_manifest()
        errors = validate_parent_pin(self.parent.parent_pin(), root=self.parent.root)
        self.assertTrue(any("tracked content differs" in error for error in errors), errors)

    def test_manifest_contents_are_verified_even_if_its_pinned_hash_matches(self):
        path = self.parent.root / "MANIFEST_SHA256.txt"
        text = path.read_text()
        path.write_text("0" * 64 + text[64:], encoding="utf-8")
        self.parent.commit_snapshot(refresh_manifest=False)
        errors = validate_parent_pin(self.parent.parent_pin(), root=self.parent.root)
        self.assertTrue(any("checksum mismatch" in error for error in errors), errors)

    def test_git_status_cache_flags_cannot_hide_rehashed_local_changes(self):
        self.parent.git("update-index", "--assume-unchanged", "INVARIANTS.json", "MANIFEST_SHA256.txt")
        path = self.parent.root / "INVARIANTS.json"
        path.write_text(path.read_text() + "\n", encoding="utf-8")
        self.parent.refresh_manifest()
        self.assertEqual(self.parent.git("status", "--porcelain", "--untracked-files=no"), "")
        errors = validate_parent_pin(self.parent.parent_pin(), root=self.parent.root)
        self.assertTrue(any("committed parent snapshot" in error for error in errors), errors)

    def test_extra_local_files_and_absent_git_identity_are_not_verified(self):
        pin = self.parent.parent_pin()
        (self.parent.root / "untracked.md").write_text("not part of the release", encoding="utf-8")
        errors = validate_parent_pin(pin, root=self.parent.root)
        self.assertTrue(any("local parent files differ" in error for error in errors), errors)
        errors = validate_parent_pin(pin, root=self.parent.outputs)
        self.assertTrue(any("git identity" in error for error in errors), errors)

    def test_instantiation_preserves_unqualified_state(self):
        path = self.parent.outputs / "created.json"
        status, text = self.instantiate(path)
        self.assertEqual(status, 0, text)
        data = json.loads(path.read_text())
        self.assertEqual(data["qualification"]["state"], "UNQUALIFIED")
        self.assertEqual(data["qualification"]["qualified_parent_commit"], "")
        self.assertEqual(data["parent"], self.parent.parent_pin())

    def test_instantiation_rejects_fabricated_release_and_mismatched_commit(self):
        for options in ({"version": "999.0.0", "tag": "main"}, {"commit": "a" * 40}):
            with self.subTest(options=options):
                path = self.parent.outputs / "rejected.json"
                status, _ = self.instantiate(path, **options)
                self.assertEqual(status, 1)
                self.assertFalse(path.exists())

    def test_tools_cannot_write_inside_the_parent_checkout(self):
        target = self.parent.root / "INVARIANTS.json"
        before = target.read_bytes()
        status, text = self.instantiate(target)
        self.assertEqual(status, 1, text)
        path = self.parent.write_manifest(self.parent.manifest())
        status, text = self.call_tool(resolve_derivative, path, "--output", target)
        self.assertEqual(status, 1, text)
        self.assertEqual(target.read_bytes(), before)

    def test_resolver_refuses_a_different_parent_registry(self):
        data = self.parent.manifest()
        data["parent"]["component_registry_sha256"] = "c" * 64
        path = self.parent.write_manifest(data)
        output = self.parent.outputs / "resolved.json"
        status, text = self.call_tool(resolve_derivative, path, "--output", output)
        self.assertEqual(status, 1, text)
        self.assertFalse(output.exists())

    def test_sparse_draft_reports_unresolved_domain_components(self):
        path = self.parent.write_manifest(self.parent.manifest())
        output = self.parent.outputs / "resolved.json"
        status, text = self.call_tool(resolve_derivative, path, "--output", output)
        self.assertEqual(status, 2, text)
        data = json.loads(output.read_text())
        self.assertEqual(data["resolution_status"], "REVIEW_REQUIRED")
        expected = {"domain-source-criteria", "domain-authority-profile", "tool-routing-profile"}
        self.assertEqual(set(data["unresolved_components"]), expected)
        for component in data["resolved_components"]:
            if component["component_id"] in expected:
                self.assertIsNone(component["effective_mutation"])
                self.assertEqual(component["resolution_status"], "REVIEW_REQUIRED")
        self.assertEqual(data["resolution_summary"]["unresolved_count"], 3)
        self.assertEqual(data["qualification"]["state"], "UNQUALIFIED")

    def test_complete_draft_resolves_without_granting_qualification(self):
        path = self.parent.write_manifest(self.parent.manifest(complete=True))
        output = self.parent.outputs / "resolved.json"
        status, text = self.call_tool(resolve_derivative, path, "--output", output)
        self.assertEqual(status, 0, text)
        data = json.loads(output.read_text())
        self.assertEqual(data["unresolved_components"], [])
        self.assertEqual(data["qualification"]["state"], "UNQUALIFIED")

    def test_compatibility_rejects_wrong_identity_and_does_not_infer_updates(self):
        data = self.parent.manifest(complete=True)
        data["parent"]["template_id"] = "DIFFERENT-PROJECT"
        path = self.parent.write_manifest(data)
        status, text = self.call_tool(check_parent_compatibility, path, "--json")
        self.assertEqual(status, 2, text)
        result = json.loads(text)
        self.assertEqual(result["compatibility_state"], "REVIEW_REQUIRED")
        self.assertEqual(result["synchronization_state"], "UNKNOWN")
        self.assertEqual(result["parent_pin_state"], "UNVERIFIED")

    def test_compatibility_keeps_technical_pin_and_qualification_separate(self):
        for complete, expected_status in ((False, 2), (True, 0)):
            with self.subTest(complete=complete):
                path = self.parent.write_manifest(self.parent.manifest(complete=complete))
                status, text = self.call_tool(check_parent_compatibility, path, "--json")
                self.assertEqual(status, expected_status, text)
                result = json.loads(text)
                self.assertEqual(result["parent_pin_state"], "VERIFIED")
                self.assertEqual(result["synchronization_state"], "PINNED")
                self.assertEqual(result["qualification_state"], "UNQUALIFIED")
                self.assertIs(result["qualification_assessed"], False)


if __name__ == "__main__":
    unittest.main()
