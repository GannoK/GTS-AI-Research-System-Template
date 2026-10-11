#!/usr/bin/env python3
"""Validate technical parent identity without granting research qualification."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

TEMPLATE_ID = "GTS-AIRST"
CANONICAL_NAME = "GTS AI Research System Template"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
VERSION = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True, stderr=subprocess.PIPE
    ).strip()


def _manifest_errors(root: Path, tracked: set[str]) -> list[str]:
    errors: list[str] = []
    manifest = root / "MANIFEST_SHA256.txt"
    entries: dict[str, str] = {}
    try:
        lines = manifest.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return [f"cannot read parent repository manifest: {exc}"]
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            errors.append(f"invalid parent repository manifest line {number}")
            continue
        expected, rel = match.groups()
        relative = PurePosixPath(rel)
        if (
            relative.is_absolute()
            or relative.as_posix() != rel
            or any(part in {"..", ".git", "__pycache__"} for part in relative.parts)
            or relative.name == "MANIFEST_SHA256.txt"
            or "\x00" in rel
        ):
            errors.append(f"invalid parent repository manifest path: {rel!r}")
            continue
        if rel in entries:
            errors.append(f"duplicate parent repository manifest entry: {rel}")
            continue
        entries[rel] = expected
        path = root / rel
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            errors.append(f"parent manifest entry must be a regular snapshot file: {rel}")
            continue
        try:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            errors.append(f"cannot read parent manifest entry {rel}: {exc}")
            continue
        if actual != expected:
            errors.append(f"parent snapshot checksum mismatch: {rel}")

    expected_files = {
        rel for rel in tracked
        if PurePosixPath(rel).name != "MANIFEST_SHA256.txt"
        and "__pycache__" not in PurePosixPath(rel).parts
    }
    if set(entries) != expected_files:
        errors.append("parent repository manifest does not exactly cover the tracked snapshot")
    actual_files = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
        and path.name != "MANIFEST_SHA256.txt"
        and ".git" not in path.relative_to(root).parts
        and "__pycache__" not in path.relative_to(root).parts
    }
    if actual_files != expected_files:
        errors.append("local parent files differ from the tracked release snapshot")
    return errors


def validate_parent_pin(parent: dict, *, root: Path) -> list[str]:
    """Accept only the exact checked-out, declared and tagged parent snapshot.

    Success establishes technical pin integrity only. It does not establish
    methodological validity, human approval, or derivative qualification.
    """
    errors: list[str] = []
    if not isinstance(parent, dict):
        return ["derivative parent must be an object"]
    if parent.get("template_id") != TEMPLATE_ID:
        errors.append(f"derivative parent.template_id must be {TEMPLATE_ID}")
    if parent.get("canonical_name") != CANONICAL_NAME:
        errors.append(f"derivative parent.canonical_name must be {CANONICAL_NAME}")
    version = parent.get("release_version")
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        errors.append("derivative parent.release_version must identify an exact release version")
    tag = parent.get("tag")
    if not isinstance(tag, str) or tag != f"v{version}":
        errors.append("derivative parent.tag must equal v<release_version>, not a floating ref")
    commit = parent.get("commit")
    if not isinstance(commit, str) or not SHA40.fullmatch(commit):
        errors.append("derivative parent.commit must be a 40-character lowercase SHA")
    for key in ("repository_manifest_sha256", "component_registry_sha256"):
        value = parent.get(key)
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            errors.append(f"derivative parent.{key} must be a SHA-256")
    if errors:
        return errors

    root = Path(root).resolve()
    try:
        top = Path(_git(root, "rev-parse", "--show-toplevel")).resolve()
        if top != root:
            return ["parent root must be the checked-out repository root"]
        head = _git(root, "rev-parse", "--verify", "HEAD^{commit}")
        tracked = set(_git(root, "ls-tree", "--name-only", "-r", "-z", head).split("\x00")) - {""}
        dirty = _git(root, "status", "--porcelain", "--untracked-files=no")
    except (OSError, subprocess.CalledProcessError) as exc:
        return [f"cannot verify checked-out parent git identity: {exc}"]
    if head != commit:
        errors.append("local parent HEAD differs from pinned parent commit")
    if dirty:
        errors.append("local parent tracked content differs from its committed snapshot")
    try:
        tag_commit = _git(root, "rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}")
    except (OSError, subprocess.CalledProcessError):
        errors.append(f"exact parent release tag does not exist: refs/tags/{tag}")
    else:
        if tag_commit != commit:
            errors.append("parent release tag does not resolve to pinned parent commit")

    metadata_path = root / "AIRST_METADATA.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be an object")
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"cannot read parent release metadata: {exc}")
    else:
        if metadata.get("template_id") != TEMPLATE_ID or metadata.get("canonical_name") != CANONICAL_NAME:
            errors.append("checked-out parent metadata has a different template identity")
        release = metadata.get("release_state")
        if not isinstance(release, dict):
            errors.append("parent release_state must be declared")
        else:
            if release.get("last_declared_version") != version:
                errors.append("parent release version differs from declared snapshot version")
            if release.get("new_release_declared") is not True or release.get("development_state") != "RELEASED":
                errors.append("parent snapshot is undeclared or unreleased; an explicit RELEASED snapshot is required")

    for key, rel in (
        ("repository_manifest_sha256", "MANIFEST_SHA256.txt"),
        ("component_registry_sha256", "COMPONENT_REGISTRY.json"),
    ):
        path = root / rel
        if rel not in tracked or path.is_symlink():
            errors.append(f"parent pin file must be a tracked regular file: {rel}")
            continue
        try:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            errors.append(f"cannot read parent pin file {rel}: {exc}")
            continue
        if parent[key] != actual:
            errors.append(f"parent.{key} differs from the checked-out snapshot")
        try:
            committed = subprocess.check_output(
                ["git", "show", f"{head}:{rel}"], cwd=root, stderr=subprocess.PIPE
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append(f"cannot read committed parent pin file {rel}: {exc}")
            continue
        if parent[key] != hashlib.sha256(committed).hexdigest():
            errors.append(f"parent.{key} differs from the committed parent snapshot")
    errors.extend(_manifest_errors(root, tracked))
    return errors
