#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from parent_snapshot import CANONICAL_NAME, TEMPLATE_ID, validate_parent_pin

ROOT = Path(__file__).resolve().parents[1]


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
    parser.add_argument("--output", type=Path, required=True, help="manifest path in a derivative workspace outside the parent checkout")
    args = parser.parse_args()

    if args.output.resolve().is_relative_to(ROOT.resolve()):
        print("FAIL: derivative output must be outside the parent checkout")
        return 1
    for key in ("derivative_id", "name", "domain", "owning_project", "repository"):
        if not getattr(args, key).strip():
            print(f"FAIL: derivative {key} must not be empty")
            return 1
    commit = args.parent_commit
    if not commit:
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.PIPE
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            print("FAIL: a checked-out parent git identity is required")
            return 1

    try:
        parent = {
            "template_id": TEMPLATE_ID,
            "canonical_name": CANONICAL_NAME,
            "release_version": args.parent_version,
            "tag": args.parent_tag,
            "commit": commit,
            "repository_manifest_sha256": sha256(ROOT / "MANIFEST_SHA256.txt"),
            "component_registry_sha256": sha256(ROOT / "COMPONENT_REGISTRY.json"),
        }
    except OSError as exc:
        print(f"FAIL: cannot read the parent snapshot: {exc}")
        return 1
    errors = validate_parent_pin(parent, root=ROOT)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    invariants = json.loads((ROOT / "INVARIANTS.json").read_text(encoding="utf-8"))
    manifest = {
        "schema_version": "1.0",
        "manifest_id": f"{args.derivative_id}-MUTATION-MANIFEST",
        "parent": parent,
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
            "qualified_parent_commit": "",
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
