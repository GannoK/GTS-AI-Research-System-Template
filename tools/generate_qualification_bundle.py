#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(control_id: str, command: list[str]) -> dict:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        "control_id": control_id,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def git(*args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("dist/airst-qualification-bundle.json"))
    args = parser.parse_args()

    controls = [
        run("RI-REPOSITORY", [sys.executable, "tools/verify_repository.py"]),
        run("RI-AIRST-VALIDATION", [sys.executable, "tools/airst_validate.py"]),
        run("MV-EVAL-HARNESS", [sys.executable, "tools/run_methodology_evals.py", "--self-test", "--json"]),
        run("RI-UNIT-TESTS", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
    ]

    assurance = json.loads((ROOT / "ASSURANCE.json").read_text(encoding="utf-8"))
    for item in assurance.get("manual_controls", []):
        if isinstance(item, str):
            control_id = item
            description = item
        else:
            control_id = item.get("control_id", "MANUAL-UNKNOWN")
            description = item.get("description", "manual review required")
        controls.append({
            "control_id": control_id,
            "status": "MANUAL",
            "command": None,
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "notes": description,
        })

    automated_fail = any(c["status"] == "FAIL" for c in controls)
    manual = any(c["status"] == "MANUAL" for c in controls)
    if automated_fail:
        parent_state = "FAILED"
    elif manual:
        parent_state = "QUALIFICATION_CANDIDATE_MANUAL_REVIEW"
    else:
        parent_state = "QUALIFICATION_CANDIDATE_AUTOMATED_PASS"

    derivative_readiness = "BLOCKED" if automated_fail else "CONTRACT_READY_PARENT_RELEASE_PIN_PENDING"
    release_readiness = "NOT_READY_VERSION_UNASSIGNED_AND_PUBLICATION_UNAUTHORIZED"

    bundle = {
        "bundle_id": "AIRST-HARDENING-001-QUALIFICATION-BUNDLE",
        "format_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "GannoK/GTS-AI-Research-System-Template",
        "implementation_commit": git("rev-parse", "HEAD"),
        "base_control_commit": "b1ec68c0052a1564187e7e48691baca89add803b",
        "parent_qualification_state": parent_state,
        "derivative_readiness_state": derivative_readiness,
        "release_readiness_state": release_readiness,
        "controls": controls,
        "known_limitations": [
            "No complete autonomous research runtime is implemented or qualified.",
            "Hybrid methodology eval cases require evidence-grounded semantic review against concrete system outputs.",
            "A new parent release/version has not been declared; actual derivatives remain blocked on an exact qualified release/tag pin.",
        ],
        "security_findings": [
            "Authority remains deny-by-default; tools/Skills/plugins/models/agents do not expand decision authority.",
            "Retrieved content remains untrusted data.",
            "Workflow action references are checked for immutable SHA pins and explicit permissions.",
            "Historical release artifacts are hash-protected against normalization.",
        ],
        "compatibility_findings": [
            "v0.2.0 retains its meaning as the declared proprietary/IP baseline.",
            "Current implementation is unreleased post-v0.2.0 hardening.",
            "Derivative compatibility and synchronization are represented separately.",
        ],
        "migration_evidence": [
            "Future-facing identity is validated against GTS-AIRST canonical metadata.",
            "Historical release notes and license-history hashes remain pinned to the accepted baseline.",
        ],
        "rollback_recovery": [
            "The hardening pass is isolated on feature/airst-hardening-001.",
            "Rollback before merge: close the PR and delete the feature branch; main remains at the accepted control state.",
            "Rollback after a future merge would require an explicit revert PR; this hardening charter does not authorize merge or destructive reset.",
        ],
        "proposed_next_action": "Operator qualification/review disposition; if accepted, separately authorize release/version disposition before creating the SEO derivative.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "parent_qualification_state": parent_state,
        "derivative_readiness_state": derivative_readiness,
        "release_readiness_state": release_readiness,
        "output": str(args.output),
    }, indent=2))
    return 1 if automated_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
