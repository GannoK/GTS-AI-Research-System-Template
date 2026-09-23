#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    parent = data["parent"]
    reasons=[]
    if parent.get("repository_manifest_sha256") != sha256(ROOT / "MANIFEST_SHA256.txt"):
        reasons.append("repository manifest hash differs from pinned parent")
    if parent.get("component_registry_sha256") != sha256(ROOT / "COMPONENT_REGISTRY.json"):
        reasons.append("component registry hash differs from pinned parent")
    head = git_head()
    if head and parent.get("commit") != head:
        reasons.append("local parent commit differs from pinned parent commit")

    if reasons:
        compatibility="REVIEW_REQUIRED"
        synchronization="UPDATE_AVAILABLE"
    else:
        compatibility="COMPATIBLE"
        synchronization="PINNED"
    payload={"compatibility_state":compatibility,"synchronization_state":synchronization,"reasons":reasons,"derived_git_head":head}
    if args.json:
        print(json.dumps(payload,indent=2))
    else:
        print(f"COMPATIBILITY={compatibility}")
        print(f"SYNCHRONIZATION={synchronization}")
        for reason in reasons:
            print(f"  {reason}")
    return 0 if compatibility=="COMPATIBLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
