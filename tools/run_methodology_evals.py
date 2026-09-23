#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "methodology" / "CASES.json"


def get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def check_value(actual: Any, op: str, expected: Any) -> bool:
    if op == "eq":
        return actual == expected
    if op == "neq":
        return actual != expected
    if op == "lte":
        return actual <= expected
    if op == "gte":
        return actual >= expected
    if op == "contains":
        return expected in actual
    raise ValueError(f"unsupported op {op!r}")


def evaluate(case: dict[str, Any], result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for check in case.get("deterministic_checks", []):
        try:
            actual = get_path(result, check["path"])
        except KeyError:
            failures.append(f"missing result path {check['path']}")
            continue
        if not check_value(actual, check["op"], check.get("value")):
            failures.append(
                f"{check['path']} {check['op']} {check.get('value')!r} failed; actual={actual!r}"
            )
    return failures


def load_cases() -> list[dict[str, Any]]:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    ids = [case.get("eval_id") for case in cases]
    expected = [f"AR-{n:03d}" for n in range(1, 15)]
    if ids != expected:
        raise ValueError(f"eval IDs must be contiguous AR-001..AR-014, got {ids}")
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cases = load_cases()
    rows = []
    failed = False
    for case in cases:
        result: dict[str, Any] | None = None
        evidence = []
        if args.results_dir:
            path = args.results_dir / f"{case['eval_id']}.json"
            if path.is_file():
                result = json.loads(path.read_text(encoding="utf-8"))
                evidence.append(str(path))
        elif args.self_test:
            result = case.get("self_test_result")
            evidence.append("bundled self-test result")

        if result is None:
            status = "MANUAL" if case.get("semantic_review_required") or case.get("manual_review_required") else "UNKNOWN"
            failures = ["no evaluated research-system result supplied"]
        else:
            failures = evaluate(case, result)
            if failures:
                status = "FAIL"
                failed = True
            elif case.get("semantic_review_required"):
                status = "MANUAL"
                failures = ["deterministic assertions pass; semantic behavior still requires evidence-grounded review"]
            elif case.get("manual_review_required"):
                status = "MANUAL"
                failures = ["manual review required"]
            else:
                status = "PASS"
        rows.append({"eval_id":case["eval_id"],"status":status,"evidence":evidence,"notes":failures})

    payload={"suite_id":"AIRST-MV-ADVERSARIAL","results":rows}
    if args.json:
        print(json.dumps(payload,indent=2))
    else:
        for row in rows:
            print(f"{row['eval_id']}={row['status']}")
            for note in row["notes"]:
                print(f"  {note}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
