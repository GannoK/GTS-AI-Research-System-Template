#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from generate_qualification_bundle import validate_bundle
from run_methodology_evals import read_json, require_valid

UNRESOLVED = {"FAIL", "MANUAL", "UNKNOWN", "WAIVED"}


def render_handoff(*, manifest: dict | None = None, qualification: dict | None = None) -> str:
    if manifest is None and qualification is None:
        raise ValueError("provide a derivative manifest, a qualification bundle, or both")
    # Validate everything before rendering. Missing data is never a clean control result.
    if manifest is not None:
        require_valid(manifest, ROOT / "schemas/derivative-mutation-manifest.schema.json")
    if qualification is not None:
        validate_bundle(qualification)
    lines = ["# GTS-AIRST Handoff", ""]
    if manifest is not None:
        lines += [f"Derivative: {manifest['derivative']['derivative_id']}",
                  f"Domain: {manifest['derivative']['domain']}",
                  f"Parent commit: {manifest['parent']['commit']}",
                  f"Qualification state: {manifest['qualification']['state']}", ""]
    if qualification is not None:
        lines += [f"Parent qualification state: {qualification['parent_qualification_state']}",
                  f"Derivative readiness: {qualification['derivative_readiness_state']}",
                  f"Release readiness: {qualification['release_readiness_state']}",
                  f"Implementation commit: {qualification['implementation_commit']}",
                  f"Working tree dirty: {qualification['repository_state']['dirty']}", ""]
        for title, field in [("Unresolved controls", "controls"), ("Unresolved acceptance criteria", "acceptance_controls")]:
            unresolved = [item for item in qualification[field] if item["status"] in UNRESOLVED]
            lines += [f"## {title}", ""]
            lines += [f"- {item['control_id']}: {item['status']} — {' '.join(item['notes'])}" for item in unresolved] if unresolved else ["- None"]
            lines.append("")
        lines += ["## Limitations", ""] + [f"- {note}" for note in qualification["known_limitations"]]
        lines += ["", "## Next action", "", qualification["proposed_next_action"], ""]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--derivative-manifest", type=Path)
    parser.add_argument("--qualification-bundle", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.derivative_manifest is None and args.qualification_bundle is None:
        parser.error("provide --derivative-manifest or --qualification-bundle")
    try:
        manifest = read_json(args.derivative_manifest) if args.derivative_manifest is not None else None
        qualification = read_json(args.qualification_bundle) if args.qualification_bundle is not None else None
        text = render_handoff(manifest=manifest, qualification=qualification)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"HANDOFF_GENERATE=FAIL: {exc}", file=sys.stderr)
        return 2
    print(f"HANDOFF_GENERATE=PASS output={args.output}; generation does not resolve pending qualification controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
