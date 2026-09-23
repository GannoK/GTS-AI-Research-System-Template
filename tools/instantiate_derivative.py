#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--derivative-id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--owning-project", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--parent-version", required=True)
    parser.add_argument("--parent-tag", required=True)
    parser.add_argument("--parent-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    commit = args.parent_commit
    if not commit:
        try:
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        except Exception:
            raise SystemExit("parent commit is required when git identity cannot be derived")
    if not SHA40.fullmatch(commit):
        raise SystemExit("parent commit must be a 40-character lowercase SHA")
    if args.parent_tag.upper().startswith("UNRELEASED"):
        raise SystemExit("qualified derivative instantiation requires an exact parent release tag")

    invariants = json.loads((ROOT / "INVARIANTS.json").read_text(encoding="utf-8"))
    manifest = {
        "schema_version": "1.0",
        "manifest_id": f"{args.derivative_id}-MUTATION-MANIFEST",
        "parent": {
            "template_id": "GTS-AIRST",
            "canonical_name": "GTS AI Research System Template",
            "release_version": args.parent_version,
            "tag": args.parent_tag,
            "commit": commit,
            "repository_manifest_sha256": sha256(ROOT / "MANIFEST_SHA256.txt"),
            "component_registry_sha256": sha256(ROOT / "COMPONENT_REGISTRY.json"),
        },
        "derivative": {
            "derivative_id": args.derivative_id,
            "name": args.name,
            "domain": args.domain,
            "owning_project": args.owning_project,
            "repository": args.repository,
            "development_state": "DRAFT",
        },
        "inheritance_policy": "PRESERVE_UNLESS_DECLARED",
        "preserved_invariants": [i["id"] for i in invariants["invariants"]],
        "mutations": [],
        "domain_extensions": [],
        "qualification": {
            "state": "UNQUALIFIED",
            "bundle_ref": "",
            "qualified_parent_commit": commit,
            "last_reviewed_at": "",
        },
        "upstream": {
            "compatibility_state": "UNKNOWN",
            "synchronization_state": "PINNED",
            "last_parent_review_version": args.parent_version,
            "last_parent_review_commit": commit,
            "known_incompatibilities": [],
        },
        "history": [{"revision": 1, "change": "Initial derivative instantiation", "decision_ref": ""}],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"DERIVATIVE_INSTANTIATE=PASS output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
