#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from schema_validation import validate_instance

CASES = ROOT / "evals" / "methodology" / "CASES.json"
CASE_SCHEMA = ROOT / "schemas" / "methodology-evals.schema.json"
RESULT_SCHEMA = ROOT / "schemas" / "methodology-result.schema.json"
SUITE_ID = "AIRST-MV-ADVERSARIAL"


def read_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f"non-JSON numeric constant {value}")
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


def require_valid(data: Any, schema: Path) -> None:
    errors = validate_instance(data, schema)
    if errors:
        raise ValueError("; ".join(errors))


def get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def check_value(actual: Any, op: str, expected: Any) -> bool:
    # JSON booleans must not compare equal to Python's numeric 0 and 1.
    if isinstance(expected, bool) and type(actual) is not bool:
        return False
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        if type(actual) not in {int, float} or not math.isfinite(actual):
            return False
    if op in {"eq", "neq"}:
        equal = actual == expected and not (
            isinstance(actual, bool) != isinstance(expected, bool)
        )
        return equal if op == "eq" else not equal
    if op in {"lte", "gte"}:
        if type(actual) not in {int, float} or type(expected) not in {int, float}:
            raise ValueError("ordered comparisons require numbers")
        return actual <= expected if op == "lte" else actual >= expected
    if op == "contains":
        if not isinstance(actual, (str, list, dict)):
            raise ValueError("contains requires a string, array, or object")
        return expected in actual
    raise ValueError(f"unsupported op {op!r}")


def evaluate(case: dict[str, Any], result: dict[str, Any]) -> list[str]:
    require_valid(case, CASE_SCHEMA)
    if not isinstance(result, dict):
        return ["result must be a JSON object"]
    failures: list[str] = []
    for check in case["deterministic_checks"]:
        try:
            actual = get_path(result, check["path"])
        except KeyError:
            failures.append(f"missing result path {check['path']}")
            continue
        try:
            passed = check_value(actual, check["op"], check["value"])
        except (TypeError, ValueError) as exc:
            failures.append(f"invalid result at {check['path']}: {exc}")
            continue
        if not passed:
            failures.append(
                f"{check['path']} {check['op']} {check['value']!r} failed; actual={actual!r}"
            )
    return failures


def load_cases(path: Path | None = None) -> list[dict[str, Any]]:
    data = read_json(path or CASES)
    require_valid(data, CASE_SCHEMA)
    if "cases" not in data:
        raise ValueError("expected a complete evaluation suite")
    cases = data["cases"]
    ids = [case["eval_id"] for case in cases]
    expected = [f"AR-{n:03d}" for n in range(1, 15)]
    if ids != expected:
        raise ValueError(f"eval IDs must be contiguous AR-001..AR-014, got {ids}")
    for case in cases:
        errors = evaluate(case, case["self_test_result"])
        if errors:
            raise ValueError(f"{case['eval_id']} invalid self-test result: {'; '.join(errors)}")
    return cases


def load_result(path: Path, case_id: str, results_dir: Path) -> tuple[dict, list[str]]:
    record = read_json(path)
    require_valid(record, RESULT_SCHEMA)
    if record["eval_id"] != case_id:
        raise ValueError(f"result eval_id must be {case_id}")
    evidence = [f"{path}#sha256={hashlib.sha256(path.read_bytes()).hexdigest()}"]
    base = results_dir.resolve()
    for item in record["evidence"]:
        supplied = Path(item["path"])
        target = (base / supplied).resolve()
        if supplied.is_absolute() or not target.is_relative_to(base):
            raise ValueError("evidence paths must stay inside the results directory")
        if not target.is_file():
            raise ValueError(f"missing evidence file: {item['path']}")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            raise ValueError(f"evidence checksum mismatch: {item['path']}")
        evidence.append(f"{target}#sha256={digest}")
    evidence.append(f"system_id={record['system_id']}; run_id={record['run_id']}")
    return record["result"], evidence


def run_evaluations(
    cases: list[dict[str, Any]], *, results_dir: Path | None = None, self_test: bool = False
) -> dict:
    if self_test and results_dir is not None:
        raise ValueError("self-test and system-result evaluation are separate modes")
    if results_dir is not None and not results_dir.is_dir():
        raise ValueError(f"results directory does not exist: {results_dir}")
    rows = []
    for case in cases:
        require_valid(case, CASE_SCHEMA)
        result = None
        evidence: list[str] = []
        failures: list[str] = []
        if self_test:
            result = case["self_test_result"]
            evidence = ["bundled self-test result; not evidence about a research system"]
        elif results_dir is not None:
            path = results_dir / f"{case['eval_id']}.json"
            if path.exists():
                try:
                    result, evidence = load_result(path, case["eval_id"], results_dir)
                except (OSError, ValueError) as exc:
                    failures = [f"malformed or unverifiable result record: {exc}"]
        if failures:
            status = "FAIL"
        elif result is None:
            status = "UNKNOWN"
            failures = ["no evaluated research-system result supplied"]
        else:
            failures = evaluate(case, result)
            if failures:
                status = "FAIL"
            elif case["semantic_review_required"] or case["manual_review_required"]:
                status = "MANUAL"
                failures = ["assertions pass; evidence-grounded semantic/manual review remains required"]
            else:
                status = "PASS"
                failures = ["supplied assertions pass; trace hashes do not establish independent truth"]
        rows.append({"eval_id": case["eval_id"], "status": status, "evidence": evidence, "notes": failures})
    return {
        "format_version": "1.0",
        "suite_id": SUITE_ID,
        "evaluation_kind": "HARNESS_SELF_TEST" if self_test else "RESEARCH_SYSTEM_RESULTS",
        "results": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--results-dir", type=Path)
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        payload = run_evaluations(load_cases(), results_dir=args.results_dir, self_test=args.self_test)
    except (OSError, ValueError) as exc:
        payload = {"suite_id": SUITE_ID, "status": "FAIL", "errors": [str(exc)], "results": []}
        print(json.dumps(payload, indent=2) if args.json else f"METHODOLOGY_EVALS=FAIL: {exc}")
        return 2
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"EVALUATION_KIND={payload['evaluation_kind']}")
        for row in payload["results"]:
            print(f"{row['eval_id']}={row['status']}")
            for note in row["notes"]:
                print(f"  {note}")
    return 1 if any(row["status"] == "FAIL" for row in payload["results"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
