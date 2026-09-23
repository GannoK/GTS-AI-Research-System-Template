#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATIONS = {
    "CORE_INVARIANT",
    "GENERIC_REUSABLE_MECHANISM",
    "DEFAULT_IMPLEMENTATION",
    "DOMAIN_EXTENSION_POINT",
    "EXAMPLE_ONLY",
    "HISTORICAL_LEGACY",
}
MUTATIONS = {"PRESERVE", "SPECIALIZE", "EXTEND", "REPLACE", "REMOVE"}
COMPATIBILITY_STATES = {
    "COMPATIBLE",
    "CONDITIONALLY_COMPATIBLE",
    "INCOMPATIBLE",
    "REVIEW_REQUIRED",
    "UNKNOWN",
}
SYNC_STATES = {
    "PINNED",
    "UPDATE_AVAILABLE",
    "UPDATE_REVIEW_IN_PROGRESS",
    "DIVERGED",
    "SUPERSEDED",
    "UNKNOWN",
}
QUALIFICATION_STATES = {
    "UNQUALIFIED",
    "IN_REVIEW",
    "QUALIFIED",
    "QUALIFIED_WITH_WAIVERS",
    "FAILED",
    "SUPERSEDED",
    "INVALIDATED",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SECRET_PATTERNS = {
    "github_pat": re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    "github_classic_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "openai_key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".cff"}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"invalid JSON {path.relative_to(ROOT)}: {exc}") from exc


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return None


def _walk_values(value: Any, prefix: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            here = f"{prefix}.{key}" if prefix else str(key)
            yield here, child
            yield from _walk_values(child, here)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            here = f"{prefix}[{idx}]"
            yield here, child
            yield from _walk_values(child, here)


def validate_identity() -> list[str]:
    errors: list[str] = []
    meta = load_json(ROOT / "AIRST_METADATA.json")
    expected = {
        "template_id": "GTS-AIRST",
        "canonical_name": "GTS AI Research System Template",
        "repository": "https://github.com/GannoK/GTS-AI-Research-System-Template",
    }
    for key, value in expected.items():
        if meta.get(key) != value:
            errors.append(f"identity {key} must equal {value!r}")
    for path, _ in _walk_values(meta):
        leaf = path.split(".")[-1].split("[")[0]
        if leaf in {"current_head", "current_commit", "head_commit"}:
            errors.append(f"identity metadata must not manually store {path}; derive HEAD mechanically")
    lineage = meta.get("lineage", {})
    aliases = set(lineage.get("predecessor_aliases", []))
    required_aliases = {
        "AI-Powered Research Starter Kit",
        "Research Starter Kit",
        "GTS Research Starter Kit",
    }
    missing = required_aliases - aliases
    if missing:
        errors.append(f"missing predecessor aliases: {sorted(missing)}")
    if lineage.get("historical_public_boundary", {}).get("commit") != "ea8013071844b59cecec25f3270d78c9c1652450":
        errors.append("historical v0.1.0 boundary commit changed")
    release = meta.get("release_state", {})
    if release.get("last_declared_version") != "0.2.0":
        errors.append("last declared release must remain 0.2.0 during this hardening pass")
    if release.get("development_state") != "UNRELEASED_POST_V0_2_0_HARDENING":
        errors.append("development state must identify unreleased post-v0.2.0 hardening")
    if meta.get("method_selection") != "ADOPT -> PROFILE -> EXTEND -> BUILD":
        errors.append("method-selection invariant changed")
    return errors


def validate_invariants() -> tuple[list[str], set[str]]:
    errors: list[str] = []
    data = load_json(ROOT / "INVARIANTS.json")
    ids: set[str] = set()
    for item in data.get("invariants", []):
        ident = item.get("id")
        if not isinstance(ident, str) or not ident.startswith("AIRST-INV-"):
            errors.append(f"invalid invariant id: {ident!r}")
            continue
        if ident in ids:
            errors.append(f"duplicate invariant id: {ident}")
        ids.add(ident)
        if not item.get("statement"):
            errors.append(f"{ident}: missing statement")
        if item.get("operator_override") not in {"REQUIRES_PARENT_ARCHITECTURE_REVIEW", "NOT_APPLICABLE"}:
            errors.append(f"{ident}: invalid operator_override")
    if not ids:
        errors.append("invariant registry is empty")
    return errors, ids


def validate_component_registry(invariant_ids: set[str]) -> tuple[list[str], dict[str, dict[str, Any]]]:
    errors: list[str] = []
    data = load_json(ROOT / "COMPONENT_REGISTRY.json")
    components: dict[str, dict[str, Any]] = {}
    for item in data.get("components", []):
        ident = item.get("component_id")
        if not isinstance(ident, str) or not ident:
            errors.append("component without component_id")
            continue
        if ident in components:
            errors.append(f"duplicate component_id: {ident}")
            continue
        components[ident] = item
        classification = item.get("classification")
        if classification not in CLASSIFICATIONS:
            errors.append(f"{ident}: invalid classification {classification!r}")
        mutations = set(item.get("mutation_permissions", []))
        if not mutations or not mutations <= MUTATIONS:
            errors.append(f"{ident}: invalid mutation permissions {sorted(mutations)}")
        if classification == "CORE_INVARIANT" and not mutations <= {"PRESERVE", "EXTEND"}:
            errors.append(f"{ident}: core invariant permits weakening mutation")
        for inv in item.get("covered_invariants", []):
            if inv not in invariant_ids:
                errors.append(f"{ident}: unknown covered invariant {inv}")
        if not item.get("qualification_controls"):
            errors.append(f"{ident}: qualification_controls must not be empty")
    if not components:
        errors.append("component registry is empty")
    return errors, components


def validate_historical_paths() -> list[str]:
    errors: list[str] = []
    data = load_json(ROOT / "HISTORICAL_PATHS.json")
    for item in data.get("protected_files", []):
        rel = item.get("path", "")
        expected = item.get("sha256", "")
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"historical protected file missing: {rel}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"historical protected file changed: {rel}")
    boundary = data.get("protected_refs", {}).get("legacy_v0_1_0", {})
    if boundary.get("branch") != "legacy/v0.1.0-cc-by-4.0":
        errors.append("historical legacy branch identity changed")
    if boundary.get("commit") != "ea8013071844b59cecec25f3270d78c9c1652450":
        errors.append("historical legacy commit identity changed")
    return errors


def validate_current_identity_surfaces() -> list[str]:
    errors: list[str] = []
    data = load_json(ROOT / "AIRST_METADATA.json")
    forbidden = tuple(data.get("future_facing_forbidden_identity_strings", []))
    for rel in data.get("future_facing_identity_paths", []):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"future-facing identity path missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in forbidden:
            if needle and needle in text:
                errors.append(f"future-facing identity path {rel} still contains predecessor identity {needle!r}")
    return errors


def validate_secret_exposure() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"potential {label} secret material in {path.relative_to(ROOT)}")
    return errors


def validate_schema_documents() -> list[str]:
    errors: list[str] = []
    for rel in [
        "schemas/airst-metadata.schema.json",
        "schemas/invariants.schema.json",
        "schemas/component-registry.schema.json",
        "schemas/derivative-mutation-manifest.schema.json",
        "schemas/assurance.schema.json",
    ]:
        data = load_json(ROOT / rel)
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{rel}: schema draft must be 2020-12")
        if not data.get("$id"):
            errors.append(f"{rel}: missing $id")
    return errors


def validate_derivative_manifest(path: Path, *, allow_template: bool = False) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    inv_errors, invariant_ids = validate_invariants()
    reg_errors, components = validate_component_registry(invariant_ids)
    errors.extend(inv_errors)
    errors.extend(reg_errors)

    parent = data.get("parent", {})
    derivative = data.get("derivative", {})
    if parent.get("template_id") != "GTS-AIRST":
        errors.append("derivative parent.template_id must be GTS-AIRST")
    if data.get("inheritance_policy") != "PRESERVE_UNLESS_DECLARED":
        errors.append("derivative inheritance_policy must be PRESERVE_UNLESS_DECLARED")
    if not allow_template:
        for key in ["release_version", "tag", "commit", "repository_manifest_sha256", "component_registry_sha256"]:
            value = parent.get(key, "")
            if not value:
                errors.append(f"derivative parent.{key} is required")
        if parent.get("commit") and not SHA40.fullmatch(parent["commit"]):
            errors.append("derivative parent.commit must be a 40-character lowercase SHA")
        for key in ["repository_manifest_sha256", "component_registry_sha256"]:
            value = parent.get(key, "")
            if value and not SHA256.fullmatch(value):
                errors.append(f"derivative parent.{key} must be a SHA-256")
        for key in ["derivative_id", "name", "domain", "owning_project", "repository"]:
            if not derivative.get(key):
                errors.append(f"derivative.{key} is required")

    seen_components: set[str] = set()
    for mutation in data.get("mutations", []):
        component_id = mutation.get("component_id")
        action = mutation.get("mutation")
        if component_id in seen_components:
            errors.append(f"duplicate derivative mutation for {component_id}")
        seen_components.add(component_id)
        component = components.get(component_id)
        if not component:
            errors.append(f"unknown derivative component {component_id}")
            continue
        if action not in MUTATIONS:
            errors.append(f"{component_id}: invalid mutation {action!r}")
            continue
        if action not in set(component.get("mutation_permissions", [])):
            errors.append(f"{component_id}: mutation {action} is not permitted")
        covered = set(component.get("covered_invariants", []))
        declared = set(mutation.get("covered_invariants", []))
        if declared - invariant_ids:
            errors.append(f"{component_id}: mutation declares unknown invariants {sorted(declared - invariant_ids)}")
        if action in {"REPLACE", "REMOVE"} and covered:
            if not mutation.get("coverage_evidence"):
                errors.append(f"{component_id}: {action} requires coverage_evidence")
            if not covered <= declared:
                errors.append(f"{component_id}: {action} must declare all covered invariants")
        if action == "PRESERVE" and mutation.get("invariant_impact") not in {None, "NONE"}:
            errors.append(f"{component_id}: PRESERVE cannot declare invariant impact")

    qualification = data.get("qualification", {})
    if qualification.get("state") not in QUALIFICATION_STATES:
        errors.append("invalid derivative qualification state")
    upstream = data.get("upstream", {})
    if upstream.get("compatibility_state") not in COMPATIBILITY_STATES:
        errors.append("invalid upstream compatibility state")
    if upstream.get("synchronization_state") not in SYNC_STATES:
        errors.append("invalid upstream synchronization state")
    return errors


def run_all() -> dict[str, list[str]]:
    invariant_errors, ids = validate_invariants()
    registry_errors, _ = validate_component_registry(ids)
    return {
        "RI-IDENTITY": validate_identity(),
        "RI-SCHEMAS": validate_schema_documents(),
        "RI-HISTORICAL-NO-TOUCH": validate_historical_paths(),
        "RI-IDENTITY-SURFACES": validate_current_identity_surfaces(),
        "RI-SECRET-EXPOSURE": validate_secret_exposure(),
        "DQ-INVARIANTS": invariant_errors,
        "DQ-COMPONENT-REGISTRY": registry_errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--derivative-manifest", type=Path)
    parser.add_argument("--allow-template", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = run_all()
    if args.derivative_manifest:
        results["DQ-DERIVATIVE-MANIFEST"] = validate_derivative_manifest(
            args.derivative_manifest, allow_template=args.allow_template
        )

    failed = {key: value for key, value in results.items() if value}
    payload = {
        "format_version": "1.0",
        "derived_git_head": git_head(),
        "results": [
            {
                "control_id": key,
                "status": "FAIL" if errors else "PASS",
                "evidence": errors if errors else ["validated"],
            }
            for key, errors in results.items()
        ],
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for item in payload["results"]:
            print(f"{item['control_id']}={item['status']}")
            for evidence in item["evidence"]:
                print(f"  {evidence}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
