#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from run_methodology_evals import load_cases, read_json, require_valid, run_evaluations

BUNDLE_SCHEMA = ROOT / "schemas" / "qualification-bundle.schema.json"
STATES = {"PASS", "FAIL", "MANUAL", "N/A", "UNKNOWN", "WAIVED"}
EXPECTED_COMMANDS = {"RI-REPOSITORY", "RI-AIRST-VALIDATION", "MV-EVAL-HARNESS", "RI-UNIT-TESTS"}
REPOSITORY_CHECKS = {
    "RI-MANIFEST-INTEGRITY", "RI-LOCAL-LINK-INTEGRITY", "RI-WORKFLOW-PINS", "RI-LEAST-PRIVILEGE"
}
AC_LINKS = {
    "AC-01": ["RI-IDENTITY", "RI-SCHEMAS"],
    "AC-02": ["RI-HISTORICAL-NO-TOUCH"],
    "AC-03": ["DQ-COMPONENT-REGISTRY", "DQ-INVARIANTS"],
    "AC-04": ["RI-SCHEMAS", "DQ-COMPONENT-REGISTRY"],
    "AC-05": ["RI-UNIT-TESTS"],
    "AC-06": ["DQ-DERIVATIVE-MUTATION", "RI-UNIT-TESTS"],
    "AC-07": ["RI-SCHEMAS"],
    "AC-08": ["MV-EVAL-HARNESS"],
    "AC-09": ["MV-PROVENANCE", "MV-TRACEABILITY", "MV-CONTRADICTION", "MV-UNCERTAINTY", "MV-FALSIFICATION", "MV-SOURCE-AUTHORITY", "MV-FRESHNESS-RETRACTION", "MV-SOURCE-DEPENDENCE", "MV-CAUSAL-OVERREACH", "MV-PROMPT-INJECTION", "MV-SCOPE-EXPANSION", "MV-AUTHORITY-ESCALATION", "MV-TOOL-FAILURE", "DQ-DERIVATIVE-MUTATION"],
    "AC-10": ["RI-SCHEMAS", "RI-WORKFLOW-PINS", "RI-LEAST-PRIVILEGE", "RI-SECRET-EXPOSURE"],
    "AC-11": ["RI-UNIT-TESTS"],
    "AC-12": ["RI-IDENTITY"],
    "AC-13": ["RI-UNIT-TESTS", "MV-EVAL-HARNESS"],
    "AC-14": ["MV-METHODOLOGICAL-VALIDITY", "RO-CLAIM-SUFFICIENCY"],
    "AC-15": ["RI-UNIT-TESTS"],
}


def run(control_id: str, command: list[str]) -> dict:
    try:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        return {"control_id": control_id, "status": "PASS" if proc.returncode == 0 else "FAIL",
                "command": command, "returncode": proc.returncode,
                "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}
    except OSError as exc:
        return {"control_id": control_id, "status": "FAIL", "command": command,
                "returncode": None, "stdout": "", "stderr": str(exc)}


def git(*args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def row(control_id: str, status: str, evidence: list[str], notes: list[str]) -> dict:
    return {"control_id": control_id, "status": status, "evidence": evidence, "notes": notes}


def aggregate_status(rows: list[dict]) -> str:
    present = {item["status"] for item in rows}
    if not present:
        return "UNKNOWN"
    for status in ["FAIL", "UNKNOWN", "MANUAL", "WAIVED"]:
        if status in present:
            return status
    return "N/A" if present == {"N/A"} else "PASS"


def readiness(controls: list[dict], acceptance: list[dict], release: dict) -> dict:
    status = aggregate_status(controls + acceptance)
    if status == "FAIL":
        parent, blocked = "FAILED", "BLOCKED_FAILED_CONTROLS"
    elif status == "UNKNOWN":
        parent, blocked = "QUALIFICATION_CANDIDATE_EVIDENCE_INCOMPLETE", "BLOCKED_MISSING_EVIDENCE"
    elif status in {"MANUAL", "WAIVED"}:
        parent, blocked = "QUALIFICATION_CANDIDATE_MANUAL_REVIEW", "BLOCKED_MANUAL_REVIEW"
    else:
        parent, blocked = "QUALIFICATION_CANDIDATE_AUTOMATED_PASS", None
    return {
        "parent_qualification_state": parent,
        "derivative_readiness_state": blocked or "CONTRACT_READY_PARENT_RELEASE_PIN_PENDING",
        "release_readiness_state": blocked or (
            "NOT_READY_NEW_RELEASE_UNDECLARED" if not release["new_release_declared"]
            else "REVIEW_REQUIRED_PUBLICATION_AUTHORITY_NOT_ESTABLISHED"
        ),
    }


def index_rows(rows: list[dict], key: str = "control_id") -> dict[str, dict]:
    indexed = {}
    if not isinstance(rows, list):
        raise ValueError("control results must be an array")
    for item in rows:
        if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key]:
            raise ValueError(f"missing or invalid {key}")
        if item[key] in indexed:
            raise ValueError(f"duplicate result: {item[key]}")
        if item.get("status") not in STATES:
            raise ValueError(f"missing or invalid status for {item[key]}")
        if not isinstance(item.get("evidence"), list) or not all(isinstance(v, str) for v in item["evidence"]):
            raise ValueError(f"invalid evidence for {item[key]}")
        indexed[item[key]] = item
    return indexed


def eval_rows(payload: dict, expected_kind: str) -> dict[str, dict]:
    if not isinstance(payload, dict) or payload.get("evaluation_kind") != expected_kind:
        raise ValueError(f"expected {expected_kind}; harness fixtures cannot qualify system behavior")
    rows = index_rows(payload.get("results"), "eval_id")
    if set(rows) != {f"AR-{n:03d}" for n in range(1, 15)}:
        raise ValueError("evaluation report must account for AR-001 through AR-014")
    for item in rows.values():
        if item["status"] in {"PASS", "MANUAL"} and not item["evidence"]:
            raise ValueError(f"missing evaluated evidence for {item['eval_id']}")
    return rows


def validate_result_links(bundle: dict, controls: dict[str, dict], control_map: dict) -> None:
    actual = eval_rows(bundle["methodology_results"], "RESEARCH_SYSTEM_RESULTS")
    mappings = control_map.get("controls")
    if not isinstance(mappings, dict):
        raise ValueError("CONTROL_MAP controls must be an object")
    for cid, ids in mappings.items():
        if not isinstance(ids, list) or not ids or not all(isinstance(i, str) for i in ids):
            raise ValueError(f"invalid evaluation mapping for {cid}")
        if len(set(ids)) != len(ids) or any(i not in actual for i in ids):
            raise ValueError(f"invalid evaluation mapping for {cid}")
        expected = aggregate_status([actual[i] for i in ids])
        if cid not in controls or controls[cid]["status"] != expected:
            raise ValueError(f"{cid} disagrees with mapped methodology results; expected {expected}")

    commands = {item["control_id"]: item for item in bundle["command_results"]}
    if set(commands) != EXPECTED_COMMANDS or len(bundle["command_results"]) != len(EXPECTED_COMMANDS):
        raise ValueError("retained qualification commands are incomplete or duplicated")
    for cid, command in commands.items():
        if cid not in controls or controls[cid]["status"] != command["status"]:
            raise ValueError(f"{cid} disagrees with its retained command result")
        # Failed commands may have incomplete or non-JSON output. Their FAIL is
        # already preserved above; a successful command must support its result.
        if command["status"] != "PASS":
            continue
        if cid == "RI-AIRST-VALIDATION":
            try:
                children = index_rows(json.loads(command["stdout"])["results"])
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid retained validator output: {exc}") from exc
            for child_id, child in children.items():
                if child["status"] == "FAIL":
                    raise ValueError(f"{cid} reports PASS but contains failed result {child_id}")
                if child_id in controls and child_id not in mappings and controls[child_id]["status"] != child["status"]:
                    raise ValueError(f"{child_id} disagrees with its retained validator result")
        elif cid == "MV-EVAL-HARNESS":
            children = eval_rows(json.loads(command["stdout"]), "HARNESS_SELF_TEST")
            if any(item["status"] in {"FAIL", "UNKNOWN"} for item in children.values()):
                raise ValueError("MV-EVAL-HARNESS reports PASS with failed or incomplete self-tests")
    repository_status = "PASS" if commands["RI-REPOSITORY"]["status"] == "PASS" else "UNKNOWN"
    for cid in REPOSITORY_CHECKS:
        if cid in controls and controls[cid]["status"] != repository_status:
            raise ValueError(f"{cid} disagrees with the repository verification gate")


def validate_bundle(bundle: dict, assurance: dict | None = None, acceptance: dict | None = None,
                    control_map: dict | None = None) -> None:
    require_valid(bundle, BUNDLE_SCHEMA)
    assurance = assurance if assurance is not None else read_json(ROOT / "ASSURANCE.json")
    acceptance = acceptance if acceptance is not None else read_json(ROOT / "HARDENING/AIRST-HARDENING-001-ACCEPTANCE.json")
    controls = index_rows(bundle["controls"])
    required = set(assurance["required_checks"]) | {item["control_id"] for item in assurance["manual_controls"]}
    missing = required - controls.keys()
    if missing:
        raise ValueError(f"bundle omits required/manual controls: {sorted(missing)}")
    acceptance_rows = index_rows(bundle["acceptance_controls"])
    expected = {item["id"] for item in acceptance["controls"]}
    if set(acceptance_rows) != expected:
        raise ValueError("bundle acceptance controls do not match the acceptance manifest")
    control_map = control_map if control_map is not None else read_json(ROOT / "evals/methodology/CONTROL_MAP.json")
    validate_result_links(bundle, controls, control_map)
    expected_states = readiness(bundle["controls"], bundle["acceptance_controls"], bundle["release_state"])
    if any(bundle[key] != value for key, value in expected_states.items()):
        raise ValueError("bundle readiness states disagree with unresolved control results")


def artifact_evidence(relative: str) -> str | None:
    path = ROOT / relative
    if path.is_file():
        return f"{relative}#sha256={hashlib.sha256(path.read_bytes()).hexdigest()}"
    if path.is_dir():
        return f"declared artifact directory: {relative}"
    return None


def build_bundle(*, commands: list[dict], methodology: dict, assurance: dict, control_map: dict,
                 acceptance: dict, metadata: dict, implementation_commit: str | None,
                 repository_state: dict) -> dict:
    required = assurance["required_checks"]
    if not required or len(set(required)) != len(required):
        raise ValueError("required controls must be nonempty and unique")
    expected_acceptance = [f"AC-{n:02d}" for n in range(1, 16)]
    if [item.get("id") for item in acceptance["controls"]] != expected_acceptance:
        raise ValueError("acceptance manifest must account for AC-01 through AC-15")
    actual = eval_rows(methodology, "RESEARCH_SYSTEM_RESULTS")
    mappings = control_map.get("controls")
    if not isinstance(mappings, dict):
        raise ValueError("CONTROL_MAP controls must be an object")
    for cid, ids in mappings.items():
        if not isinstance(ids, list) or not ids or len(set(ids)) != len(ids) or any(i not in actual for i in ids):
            raise ValueError(f"invalid evaluation mapping for {cid}")
    command_index = {item["control_id"]: dict(item) for item in commands}
    if set(command_index) != EXPECTED_COMMANDS or len(commands) != len(EXPECTED_COMMANDS):
        raise ValueError("qualification commands are incomplete or duplicated")
    validator_rows = {}
    for cid in ["RI-AIRST-VALIDATION", "MV-EVAL-HARNESS"]:
        command = command_index[cid]
        if command["status"] == "PASS":
            try:
                payload = json.loads(command["stdout"])
                if cid == "RI-AIRST-VALIDATION":
                    validator_rows = index_rows(payload["results"])
                else:
                    harness_rows = eval_rows(payload, "HARNESS_SELF_TEST")
                    if any(r["status"] in {"FAIL", "UNKNOWN"} for r in harness_rows.values()):
                        raise ValueError("harness self-test did not complete successfully")
            except (KeyError, TypeError, ValueError) as exc:
                command["status"] = "FAIL"
                command["stderr"] += f"\nInvalid structured command result: {exc}"
    controls = []
    for cid, command in command_index.items():
        evidence = [f"command_results:{cid}"]
        note = "Command execution result; inspect captured stdout and stderr."
        if cid == "MV-EVAL-HARNESS":
            note = "Bundled fixtures test the evaluator only; this does not establish methodology conformance of a research system."
        controls.append(row(cid, command["status"], evidence, [note]))
    existing = {item["control_id"] for item in controls}
    for cid in required:
        if cid in existing:
            continue
        if cid in validator_rows:
            item = validator_rows[cid]
            controls.append(row(cid, item["status"], [f"command_results:RI-AIRST-VALIDATION#{cid}"] + item["evidence"],
                                ["Specific validator result; scope is the implemented mechanical check."]))
        elif cid in REPOSITORY_CHECKS:
            passed = command_index["RI-REPOSITORY"]["status"] == "PASS"
            controls.append(row(cid, "PASS" if passed else "UNKNOWN", ["command_results:RI-REPOSITORY"],
                                ["Covered by the repository verification gate." if passed else "The aggregate gate failed; no separate successful result is asserted."]))
        elif cid in mappings:
            members = [actual[i] for i in mappings[cid]]
            controls.append(row(cid, aggregate_status(members),
                                [f"methodology_results:{i}" for i in mappings[cid]] + [v for item in members for v in item["evidence"]],
                                [f"Mapped system-result evaluations: {', '.join(mappings[cid])}. Self-test results are excluded."] +
                                [f"{item['eval_id']}={item['status']}" for item in members]))
        else:
            controls.append(row(cid, "UNKNOWN", [], ["No result provider is mapped to this required control."]))
    for item in assurance["manual_controls"]:
        if item["control_id"] in {r["control_id"] for r in controls}:
            raise ValueError(f"manual control conflicts with automated control: {item['control_id']}")
        controls.append(row(item["control_id"], "MANUAL", ["ASSURANCE.json#manual_controls"], [item["description"]]))
    by_id = index_rows(controls)
    accepted = []
    for item in acceptance["controls"]:
        links = AC_LINKS[item["id"]]
        linked_rows = [by_id[cid] for cid in links if cid in by_id]
        found = [artifact_evidence(rel) for rel in item["evidence"]]
        combined = aggregate_status(linked_rows)
        status = "FAIL" if combined == "FAIL" else (
            "UNKNOWN" if combined == "UNKNOWN" or len(linked_rows) != len(links) or any(v is None for v in found) else "MANUAL"
        )
        accepted.append(row(item["id"], status,
                            [f"HARDENING/AIRST-HARDENING-001-ACCEPTANCE.json#{item['id']}"] + [v for v in found if v] + [f"controls:{cid}" for cid in links],
                            [item["requirement"], "Artifacts and automated checks are review inputs; full acceptance requires an explicit evidence-grounded review."]))
    release = dict(metadata["release_state"])
    bundle = {
        "bundle_id": "AIRST-HARDENING-001-QUALIFICATION-BUNDLE", "format_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(), "repository": metadata["repository"],
        "implementation_commit": implementation_commit, "repository_state": repository_state,
        "base_control_commit": acceptance["control_base_commit"], "release_state": release,
        **readiness(controls, accepted, release), "controls": controls, "acceptance_controls": accepted,
        "methodology_results": methodology, "command_results": list(command_index.values()),
        "known_limitations": [
            "No complete autonomous research runtime is implemented or qualified.",
            "Self-tests establish evaluator behavior on bundled fixtures only.",
            "Supplied result identities and evidence hashes establish traceability, not independent semantic truth.",
            "Missing real-system results remain UNKNOWN; human judgments and acceptance remain unresolved until reviewed.",
            "Publication authority and an exact qualified parent release pin are separate requirements.",
        ],
        "compatibility_findings": [
            f"Last declared version: {release['last_declared_version']}; development state: {release['development_state']}.",
            f"Next planned version: {release.get('next_planned_version', 'not assigned')}; new release declared: {release['new_release_declared']}.",
            "The historical proprietary licensing boundary remains unchanged.",
        ],
        "security_findings": [f"{cid}={by_id[cid]['status']}; inspect the associated evidence and check scope."
                              for cid in ["RI-WORKFLOW-PINS", "RI-LEAST-PRIVILEGE", "RI-SECRET-EXPOSURE"] if cid in by_id],
        "migration_evidence": ["controls:RI-IDENTITY", "controls:RI-HISTORICAL-NO-TOUCH"],
        "rollback_recovery": ["Retain reviewed commits and evidence; any subsequent rollback needs its own explicit disposition."],
        "proposed_next_action": "Review unresolved control evidence and acceptance criteria; release publication remains a separate decision.",
    }
    validate_bundle(bundle, assurance, acceptance, control_map)
    return bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("dist/airst-qualification-bundle.json"))
    parser.add_argument("--results-dir", type=Path, help="Traceable actual-system AR-xxx.json records; absent records remain UNKNOWN.")
    args = parser.parse_args(argv)
    try:
        assurance = read_json(ROOT / "ASSURANCE.json")
        metadata = read_json(ROOT / "AIRST_METADATA.json")
        require_valid(assurance, ROOT / "schemas/assurance.schema.json")
        require_valid(metadata, ROOT / "schemas/airst-metadata.schema.json")
        acceptance = read_json(ROOT / "HARDENING/AIRST-HARDENING-001-ACCEPTANCE.json")
        control_map = read_json(ROOT / "evals/methodology/CONTROL_MAP.json")
        methodology = run_evaluations(load_cases(), results_dir=args.results_dir)
        commands = [
            run("RI-REPOSITORY", [sys.executable, "tools/verify_repository.py"]),
            run("RI-AIRST-VALIDATION", [sys.executable, "tools/airst_validate.py", "--json"]),
            run("MV-EVAL-HARNESS", [sys.executable, "tools/run_methodology_evals.py", "--self-test", "--json"]),
            run("RI-UNIT-TESTS", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ]
        status = git("status", "--porcelain")
        manifest = ROOT / "MANIFEST_SHA256.txt"
        bundle = build_bundle(commands=commands, methodology=methodology, assurance=assurance,
                              control_map=control_map, acceptance=acceptance, metadata=metadata,
                              implementation_commit=git("rev-parse", "HEAD"),
                              repository_state={"dirty": None if status is None else bool(status),
                                                "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest() if manifest.is_file() else None})
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"QUALIFICATION_BUNDLE=FAIL: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({key: bundle[key] for key in ["parent_qualification_state", "derivative_readiness_state", "release_readiness_state"]}
                     | {"output": str(args.output)}, indent=2))
    return 1 if any(item["status"] == "FAIL" for item in bundle["controls"] + bundle["acceptance_controls"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
