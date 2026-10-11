#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from airst_validate import ValidationError, validate_derivative_manifest

ROOT = Path(__file__).resolve().parents[1]
QUALIFIED_STATES = {"QUALIFIED", "QUALIFIED_WITH_WAIVERS"}


def resolve_components(manifest: dict, registry: dict) -> tuple[list[dict], list[str]]:
    """Expand validated mutations without bypassing permissions by omission."""
    explicit = {m["component_id"]: m for m in manifest.get("mutations", [])}
    resolved: list[dict] = []
    unresolved: list[str] = []
    for component in registry["components"]:
        cid = component["component_id"]
        mutation = explicit.get(cid)
        if mutation is not None:
            action = mutation["mutation"]
            source = "DECLARED"
        elif "PRESERVE" in component["mutation_permissions"]:
            action = "PRESERVE"
            source = "INHERITED_BY_POLICY"
        else:
            action = None
            source = "EXPLICIT_MUTATION_REQUIRED"
            unresolved.append(cid)
        resolved.append({
            "component_id": cid,
            "classification": component["classification"],
            "effective_mutation": action,
            "resolution_source": source,
            "resolution_status": "REVIEW_REQUIRED" if action is None else "RESOLVED",
            "covered_invariants": component.get("covered_invariants", []),
        })
    return resolved, unresolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="resolved manifest path outside the parent checkout")
    args = parser.parse_args()

    if args.output.resolve().is_relative_to(ROOT.resolve()):
        print("FAIL: derivative output must be outside the parent checkout")
        return 1
    try:
        errors = validate_derivative_manifest(args.manifest)
    except (OSError, ValueError, ValidationError) as exc:
        print(f"FAIL: cannot validate derivative manifest: {exc}")
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "COMPONENT_REGISTRY.json").read_text(encoding="utf-8"))
    resolved, unresolved = resolve_components(manifest, registry)
    if unresolved and manifest["qualification"]["state"] in QUALIFIED_STATES:
        print("FAIL: qualified derivatives cannot contain unresolved component dispositions")
        return 1

    output = dict(manifest)
    output["resolved_components"] = resolved
    output["unresolved_components"] = unresolved
    output["resolution_status"] = "REVIEW_REQUIRED" if unresolved else "RESOLVED"
    output["resolution_summary"] = {
        "component_count": len(resolved),
        "declared_mutations": len(manifest.get("mutations", [])),
        "inherited_preserve": sum(c["resolution_source"] == "INHERITED_BY_POLICY" for c in resolved),
        "unresolved_count": len(unresolved),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    status = "REVIEW_REQUIRED" if unresolved else "PASS"
    print(f"DERIVATIVE_RESOLVE={status} output={args.output} components={len(resolved)} unresolved={len(unresolved)}")
    return 2 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
