#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from airst_validate import ValidationError, validate_derivative_manifest
from resolve_derivative import resolve_components

ROOT = Path(__file__).resolve().parents[1]


def git_head() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.PIPE
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    data: dict = {}
    try:
        reasons = validate_derivative_manifest(args.manifest)
        loaded = json.loads(args.manifest.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            data = loaded
    except (OSError, ValueError, ValidationError) as exc:
        reasons = [f"cannot validate derivative manifest: {exc}"]
    pin_verified = not reasons
    unresolved: list[str] = []
    if pin_verified:
        registry = json.loads((ROOT / "COMPONENT_REGISTRY.json").read_text(encoding="utf-8"))
        _, unresolved = resolve_components(data, registry)
        reasons.extend(f"component requires an explicit permitted mutation: {cid}" for cid in unresolved)

    compatibility = "REVIEW_REQUIRED" if reasons else "COMPATIBLE"
    qualification = data.get("qualification", {})
    if not isinstance(qualification, dict):
        qualification = {}
    payload = {
        "compatibility_state": compatibility,
        "synchronization_state": "PINNED" if pin_verified else "UNKNOWN",
        "parent_pin_state": "VERIFIED" if pin_verified else "UNVERIFIED",
        "comparison_scope": "EXACT_PARENT_PIN_AND_DECLARED_MUTATION_STRUCTURE",
        "qualification_state": qualification.get("state", "UNKNOWN"),
        "qualification_assessed": False,
        "unresolved_components": unresolved,
        "reasons": reasons,
        "derived_git_head": git_head(),
    }
    if args.json:
        print(json.dumps(payload,indent=2))
    else:
        print(f"COMPATIBILITY={compatibility}")
        print(f"SYNCHRONIZATION={payload['synchronization_state']}")
        print(f"PARENT_PIN={payload['parent_pin_state']}")
        print(f"QUALIFICATION={payload['qualification_state']} (not assessed by this technical compatibility check)")
        for reason in reasons:
            print(f"  {reason}")
    return 0 if compatibility=="COMPATIBLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
