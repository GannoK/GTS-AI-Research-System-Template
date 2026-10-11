#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_SLUG = "gts-ai-research-system-template"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.PIPE
    ).strip()


def declared_release_identity() -> tuple[str, str]:
    """Verify the released snapshot identity, not human qualification or approval."""
    metadata = json.loads((ROOT / "AIRST_METADATA.json").read_text(encoding="utf-8"))
    pack = json.loads((ROOT / "PACK_METADATA.json").read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or not isinstance(pack, dict):
        raise ValueError("release metadata must be JSON objects")
    release = metadata.get("release_state")
    if not isinstance(release, dict):
        raise ValueError("AIRST_METADATA.json must contain release_state")
    if release.get("development_state") != "RELEASED":
        raise ValueError("release evidence requires an explicit RELEASED development state")
    if release.get("new_release_declared") is not True:
        raise ValueError("release evidence requires new_release_declared to be true")
    version = release.get("last_declared_version")
    if not isinstance(version, str) or not version:
        raise ValueError("a nonempty declared release version is required")
    if pack.get("version") != version:
        raise ValueError("PACK_METADATA.json version must match the declared AIRST release")

    tag = f"v{version}"
    ref = f"refs/tags/{tag}"
    for key, expected in {
        "GITHUB_REF_TYPE": "tag",
        "GITHUB_REF_NAME": tag,
        "GITHUB_REF": ref,
    }.items():
        supplied = os.environ.get(key)
        if supplied is not None and supplied != expected:
            raise ValueError(f"{key} conflicts with the declared release tag")

    try:
        git("check-ref-format", ref)
        commit = git("rev-parse", "--verify", "HEAD^{commit}")
        tagged_commit = git("rev-parse", "--verify", f"{ref}^{{commit}}")
    except subprocess.CalledProcessError as exc:
        raise ValueError("the declared release needs an existing valid tag and HEAD commit") from exc
    if tagged_commit != commit:
        raise ValueError("the declared release tag must resolve to the checked-out HEAD")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise ValueError("release evidence requires an unchanged tracked release snapshot")
    return commit, tag


def deterministic_archive(prefix: str, tracked: list[str]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for rel in sorted(tracked):
            path = ROOT / rel
            if not path.is_file():
                continue
            info = tf.gettarinfo(str(path), arcname=f"{prefix}/{rel}")
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            with path.open("rb") as fh:
                tf.addfile(info, fh)
    return gzip.compress(buffer.getvalue(), compresslevel=9, mtime=0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dist")
    args = parser.parse_args(argv)

    try:
        commit, tag = declared_release_identity()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"RELEASE_EVIDENCE=FAIL: {exc}")
        return 1

    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    prefix = f"{PROJECT_SLUG}-{tag}"
    archive = out / f"{prefix}.tar.gz"

    tracked = git("ls-files").splitlines()
    archive.write_bytes(deterministic_archive(prefix, tracked))

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksums = out / "SHA256SUMS.txt"
    checksums.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")

    evidence = {
        "format_version": "1.0",
        "repository": os.environ.get("GITHUB_REPOSITORY", ""),
        "commit": commit,
        "tag": tag,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifact": archive.name,
        "sha256": digest,
        "assurance_profile": json.loads((ROOT / "ASSURANCE.json").read_text(encoding="utf-8")).get("assurance_profile"),
        "manifest_sha256": hashlib.sha256((ROOT / "MANIFEST_SHA256.txt").read_bytes()).hexdigest(),
    }
    (out / "release-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"RELEASE_EVIDENCE=PASS artifact={archive.name} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
