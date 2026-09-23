#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT_STATES = {"PASS", "FAIL", "MANUAL", "N/A", "UNKNOWN", "WAIVED"}
CONTROL_DOMAINS = {"RI", "MV", "RO", "DQ"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
USES = re.compile(r"^\s*-?\s*uses:\s*([^@\s]+)@([^\s#]+)", re.MULTILINE)


def is_full_sha(ref: str) -> bool:
    return bool(SHA40.fullmatch(ref))


def workflow_findings(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    findings: list[str] = []
    try:
        display = path.relative_to(ROOT).as_posix()
    except ValueError:
        display = path.as_posix()
    for action, ref in USES.findall(text):
        if action.startswith("./"):
            continue
        if not is_full_sha(ref):
            findings.append(f"{display}: unpinned action {action}@{ref}")
    if "permissions:" not in text:
        findings.append(f"{display}: missing explicit permissions")
    if "actions/checkout@" in text and "persist-credentials: false" not in text:
        findings.append(f"{display}: checkout must disable credential persistence")
    return findings


def audit() -> tuple[list[str], list[str]]:
    failures: list[str] = []
    manual: list[str] = []

    required = [
        "ASSURANCE.json",
        "GOVERNANCE.md",
        "MAINTAINERS.md",
        "SECURITY.md",
        "AIRST_METADATA.json",
        "INVARIANTS.json",
        "COMPONENT_REGISTRY.json",
        "HISTORICAL_PATHS.json",
        "DERIVATIVE_CONTRACT.md",
        "07_TEMPLATES/10_RESEARCH_PROVENANCE_TEMPLATE.json",
        "07_TEMPLATES/11_CLAIM_EVIDENCE_GRAPH_TEMPLATE.json",
        "07_TEMPLATES/12_SOURCE_RECORD_TEMPLATE.json",
        "07_TEMPLATES/13_DERIVATIVE_MUTATION_MANIFEST_TEMPLATE.json",
        "evals/methodology/CASES.json",
        "evals/methodology/CONTROL_MAP.json",
    ]
    for rel in required:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required assurance artifact: {rel}")

    try:
        manifest = json.loads((ROOT / "ASSURANCE.json").read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"ASSURANCE.json invalid: {exc}")
        manifest = {}

    states = set(manifest.get("result_states", []))
    if states != RESULT_STATES:
        failures.append(f"ASSURANCE.json result_states must equal {sorted(RESULT_STATES)}")

    domains = set(manifest.get("control_domains", {}))
    if domains != CONTROL_DOMAINS:
        failures.append(f"ASSURANCE.json control_domains must equal {sorted(CONTROL_DOMAINS)}")

    for control in manifest.get("required_checks", []):
        prefix = str(control).split("-", 1)[0]
        if prefix not in CONTROL_DOMAINS:
            failures.append(f"required control lacks RI/MV/RO/DQ domain: {control}")

    for item in manifest.get("manual_controls", []):
        if isinstance(item, dict):
            cid = str(item.get("control_id", "MANUAL-UNKNOWN"))
            description = str(item.get("description", "manual review required"))
            manual.append(f"{cid}: {description}")
        else:
            manual.append(str(item))

    workflows = ROOT / ".github" / "workflows"
    if workflows.is_dir():
        for path in sorted(workflows.glob("*.y*ml")):
            failures.extend(workflow_findings(path))

    return failures, manual


def main() -> int:
    failures, manual = audit()
    for item in manual:
        print(f"MANUAL: {item}")
    for item in failures:
        print(f"FAIL: {item}")
    if failures:
        print(f"ASSURANCE_AUDIT=FAIL failures={len(failures)} manual={len(manual)}")
        return 1
    print(f"ASSURANCE_AUDIT=PASS failures=0 manual={len(manual)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
