from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    "build_release_evidence", Path(__file__).resolve().parents[1] / "tools" / "build_release_evidence.py"
)
assert SPEC and SPEC.loader
release_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_tool)


class ReleaseEvidenceTests(unittest.TestCase):
    """All release tags and Git mutations are confined to temporary repositories."""

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "parent"
        self.root.mkdir()
        self.output = self.root / "dist"
        self.git("init", "--quiet")
        self.git("config", "user.name", "Release Guard Test")
        self.git("config", "user.email", "release-test@example.invalid")
        root_patch = mock.patch.object(release_tool, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        environment_patch = mock.patch.dict(os.environ)
        environment_patch.start()
        self.addCleanup(environment_patch.stop)
        for key in ("GITHUB_REF", "GITHUB_REF_TYPE", "GITHUB_REF_NAME", "GITHUB_REPOSITORY"):
            os.environ.pop(key, None)

        self.write_json("AIRST_METADATA.json", {
            "release_state": {
                "development_state": "RELEASED",
                "new_release_declared": True,
                "last_declared_version": "0.3.0",
            }
        })
        self.write_json("PACK_METADATA.json", {"version": "0.3.0"})
        self.write_json("ASSURANCE.json", {"assurance_profile": "test-fixture"})
        (self.root / "README.md").write_text("Isolated release guard fixture.\n", encoding="utf-8")
        self.commit("Initial released fixture")

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            ["git", *args], cwd=self.root, text=True, stderr=subprocess.PIPE
        ).strip()

    def write_json(self, name: str, value: dict) -> None:
        (self.root / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def commit(self, message: str) -> None:
        lines = []
        for path in sorted(self.root.iterdir()):
            if path.is_file() and path.name != "MANIFEST_SHA256.txt":
                lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
        (self.root / "MANIFEST_SHA256.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", message)

    def build(self) -> tuple[int, str]:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = release_tool.main(["--output", str(self.output)])
        return code, stdout.getvalue()

    def assert_rejected(self, message: str) -> None:
        code, stdout = self.build()
        self.assertEqual(code, 1, stdout)
        self.assertIn(message, stdout)
        self.assertFalse(self.output.exists(), "a rejected release must not create artifacts")

    def test_unreleased_state_is_rejected_before_any_artifact_write(self) -> None:
        metadata = json.loads((self.root / "AIRST_METADATA.json").read_text())
        metadata["release_state"]["development_state"] = "UNRELEASED_POST_V0_2_1_HARDENING"
        metadata["release_state"]["new_release_declared"] = False
        self.write_json("AIRST_METADATA.json", metadata)
        self.commit("Unreleased candidate")
        self.git("tag", "v0.3.0")
        self.assert_rejected("explicit RELEASED")

    def test_release_declaration_requires_boolean_true(self) -> None:
        for value in (False, 1, "true", None):
            with self.subTest(new_release_declared=value):
                metadata = json.loads((self.root / "AIRST_METADATA.json").read_text())
                metadata["release_state"]["new_release_declared"] = value
                self.write_json("AIRST_METADATA.json", metadata)
                self.commit(f"Invalid declaration {value!r}")
                self.git("tag", "--force", "v0.3.0")
                self.assert_rejected("new_release_declared to be true")

    def test_package_version_must_match_declared_release(self) -> None:
        self.write_json("PACK_METADATA.json", {"version": "0.2.1"})
        self.commit("Mismatched package version")
        self.git("tag", "v0.3.0")
        self.assert_rejected("version must match")

    def test_existing_exact_tag_is_required(self) -> None:
        self.assert_rejected("existing valid tag")

    def test_tag_must_point_to_actual_head(self) -> None:
        self.git("tag", "v0.3.0")
        (self.root / "README.md").write_text("Later untagged commit.\n", encoding="utf-8")
        self.commit("Later commit")
        self.assert_rejected("tag must resolve to the checked-out HEAD")

    def test_conflicting_github_context_is_rejected(self) -> None:
        self.git("tag", "v0.3.0")
        for context in (
            {"GITHUB_REF_TYPE": "branch"},
            {"GITHUB_REF_NAME": "v0.2.1"},
            {"GITHUB_REF": "refs/heads/main"},
        ):
            with self.subTest(context=context), mock.patch.dict(os.environ, context):
                self.assert_rejected("conflicts with the declared release tag")

    def test_tracked_changes_cannot_be_packaged_under_the_tag(self) -> None:
        self.git("tag", "v0.3.0")
        (self.root / "README.md").write_text("Uncommitted replacement.\n", encoding="utf-8")
        self.assert_rejected("unchanged tracked release snapshot")
        self.git("add", "README.md")
        self.assert_rejected("unchanged tracked release snapshot")

    def test_released_annotated_tag_builds_identical_archives(self) -> None:
        self.git("tag", "--annotate", "v0.3.0", "-m", "Released fixture")
        with mock.patch.dict(os.environ, {
            "GITHUB_REF_TYPE": "tag",
            "GITHUB_REF_NAME": "v0.3.0",
            "GITHUB_REF": "refs/tags/v0.3.0",
        }):
            code, stdout = self.build()
            self.assertEqual(code, 0, stdout)
            archive = self.output / "gts-ai-research-system-template-v0.3.0.tar.gz"
            first = archive.read_bytes()
            evidence = json.loads((self.output / "release-evidence.json").read_text())
            self.assertEqual(evidence["tag"], "v0.3.0")
            self.assertEqual(evidence["commit"], self.git("rev-parse", "HEAD"))
            self.assertEqual(evidence["sha256"], hashlib.sha256(first).hexdigest())
            code, stdout = self.build()
            self.assertEqual(code, 0, stdout)
            self.assertEqual(archive.read_bytes(), first)


if __name__ == "__main__":
    unittest.main()
