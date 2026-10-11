"""Isolated, genuinely tagged parent snapshots for derivative regressions."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ReleasedParent:
    def __init__(self, workdir: Path):
        self.root = workdir / "parent"
        self.root.mkdir()
        self.outputs = workdir / "derivative"
        self.outputs.mkdir()
        self.version = "0.3.0"
        self.tag = f"v{self.version}"
        for name in ("INVARIANTS.json", "COMPONENT_REGISTRY.json"):
            shutil.copyfile(PROJECT_ROOT / name, self.root / name)
        shutil.copytree(PROJECT_ROOT / "schemas", self.root / "schemas")
        metadata = json.loads((PROJECT_ROOT / "AIRST_METADATA.json").read_text(encoding="utf-8"))
        metadata["release_state"].update(
            last_declared_version=self.version,
            development_state="RELEASED",
            new_release_declared=True,
        )
        self.write_json("AIRST_METADATA.json", metadata)
        self.git("init", "--quiet")
        self.commit_snapshot()

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            [
                "git", "-c", "init.defaultBranch=main",
                "-c", "user.name=AIRST Regression Tests",
                "-c", "user.email=airst-tests@example.invalid",
                "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false",
                "-c", "core.hooksPath=/dev/null", *args,
            ], cwd=self.root, text=True, stderr=subprocess.PIPE,
        ).strip()

    def write_json(self, name: str, value: dict) -> None:
        (self.root / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def refresh_manifest(self) -> None:
        files = sorted(
            (
                path for path in self.root.rglob("*")
                if path.is_file()
                and path.name != "MANIFEST_SHA256.txt"
                and ".git" not in path.relative_to(self.root).parts
                and "__pycache__" not in path.relative_to(self.root).parts
            ), key=lambda path: path.relative_to(self.root).as_posix(),
        )
        text = "".join(
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  "
            f"{path.relative_to(self.root).as_posix()}\n"
            for path in files
        )
        (self.root / "MANIFEST_SHA256.txt").write_text(text, encoding="utf-8")

    def commit_snapshot(self, *, refresh_manifest: bool = True) -> None:
        if refresh_manifest:
            self.refresh_manifest()
        self.git("add", "--all")
        self.git("commit", "--quiet", "--allow-empty", "-m", "Isolated parent release fixture")
        self.git("tag", "--force", self.tag)

    def parent_pin(self) -> dict:
        return {
            "template_id": "GTS-AIRST",
            "canonical_name": "GTS AI Research System Template",
            "release_version": self.version,
            "tag": self.tag,
            "commit": self.git("rev-parse", "HEAD"),
            "repository_manifest_sha256": hashlib.sha256((self.root / "MANIFEST_SHA256.txt").read_bytes()).hexdigest(),
            "component_registry_sha256": hashlib.sha256((self.root / "COMPONENT_REGISTRY.json").read_bytes()).hexdigest(),
        }

    def manifest(self, *, complete: bool = False) -> dict:
        data = json.loads((PROJECT_ROOT / "07_TEMPLATES/13_DERIVATIVE_MUTATION_MANIFEST_TEMPLATE.json").read_text(encoding="utf-8"))
        data["manifest_id"] = "TEST-DERIVATIVE"
        data["parent"] = self.parent_pin()
        data["derivative"].update(
            derivative_id="TEST", name="Test derivative", domain="regression testing",
            owning_project="TEST", repository="example/test",
        )
        data["upstream"].update(last_parent_review_version=self.version, last_parent_review_commit=data["parent"]["commit"])
        if complete:
            registry = json.loads((self.root / "COMPONENT_REGISTRY.json").read_text(encoding="utf-8"))
            for component in registry["components"]:
                if "PRESERVE" not in component["mutation_permissions"]:
                    data["mutations"].append({
                        "component_id": component["component_id"],
                        "mutation": "SPECIALIZE",
                        "rationale": "Define the regression fixture's domain-specific criteria.",
                        "covered_invariants": component["covered_invariants"],
                        "invariant_impact": "NONE",
                        "coverage_evidence": [],
                        "qualification_controls": component["qualification_controls"],
                        "decision_refs": [],
                    })
        return data

    def write_manifest(self, data: dict) -> Path:
        path = self.outputs / "manifest.json"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return path
