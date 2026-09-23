#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--derivative-manifest",type=Path)
    parser.add_argument("--qualification-bundle",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()

    manifest=json.loads(args.derivative_manifest.read_text(encoding="utf-8")) if args.derivative_manifest else None
    qualification=json.loads(args.qualification_bundle.read_text(encoding="utf-8")) if args.qualification_bundle else None
    lines=["# GTS-AIRST Handoff",""]
    if manifest:
        lines += [f"Derivative: {manifest['derivative'].get('derivative_id','')}",f"Domain: {manifest['derivative'].get('domain','')}",f"Parent commit: {manifest['parent'].get('commit','')}",f"Qualification state: {manifest['qualification'].get('state','')}",""]
    if qualification:
        lines += [f"Parent qualification state: {qualification.get('parent_qualification_state','')}",f"Derivative readiness: {qualification.get('derivative_readiness_state','')}",f"Release readiness: {qualification.get('release_readiness_state','')}",""]
        unresolved=[r for r in qualification.get('controls',[]) if r.get('status') in {'FAIL','MANUAL','UNKNOWN','WAIVED'}]
        lines += ["## Unresolved controls",""]
        if unresolved:
            lines += [f"- {r['control_id']}: {r['status']}" for r in unresolved]
        else:
            lines += ["- None"]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"HANDOFF_GENERATE=PASS output={args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
