#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from airst_validate import ROOT, validate_derivative_manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    errors = validate_derivative_manifest(args.manifest)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "COMPONENT_REGISTRY.json").read_text(encoding="utf-8"))
    explicit = {m["component_id"]: m for m in manifest.get("mutations", [])}
    resolved = []
    for component in registry["components"]:
        cid = component["component_id"]
        mutation = explicit.get(cid)
        if mutation:
            action = mutation["mutation"]
            source = "DECLARED"
        else:
            action = "PRESERVE"
            source = "INHERITED_BY_POLICY"
        resolved.append({
            "component_id": cid,
            "classification": component["classification"],
            "effective_mutation": action,
            "resolution_source": source,
            "covered_invariants": component.get("covered_invariants", []),
        })

    output = dict(manifest)
    output["resolved_components"] = resolved
    output["resolution_summary"] = {
        "component_count": len(resolved),
        "declared_mutations": len(explicit),
        "inherited_preserve": len(resolved) - len(explicit),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"DERIVATIVE_RESOLVE=PASS output={args.output} components={len(resolved)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
