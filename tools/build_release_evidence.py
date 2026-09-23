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
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dist")
    args = parser.parse_args()

    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)
    commit = git("rev-parse", "HEAD")
    tag = os.environ.get("GITHUB_REF_NAME") or git("describe", "--tags", "--exact-match", commit)
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
