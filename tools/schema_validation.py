"""Validate local contracts with JSON Schema Draft 2020-12, without network retrieval."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import Unresolvable

DRAFT = "https://json-schema.org/draft/2020-12/schema"


def _load_schema(schema_path: Path) -> Any:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def check_schema(schema_path: Path) -> list[str]:
    try:
        schema = _load_schema(schema_path)
        if not isinstance(schema, dict) or schema.get("$schema") != DRAFT:
            return [f"{schema_path.name}: schema draft must be 2020-12"]
        if not isinstance(schema.get("$id"), str) or not schema["$id"]:
            return [f"{schema_path.name}: missing schema identity"]
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError, SchemaError) as exc:
        return [f"{schema_path.name}: invalid schema: {exc}"]
    return []


def validate_instance(data: Any, schema_path: Path) -> list[str]:
    errors = check_schema(schema_path)
    if errors:
        return errors
    try:
        # An explicit empty registry disables implicit remote resource retrieval.
        validator = Draft202012Validator(_load_schema(schema_path), registry=Registry())
        found = sorted(validator.iter_errors(data), key=lambda item: tuple(map(str, item.absolute_path)))
        return [
            f"{schema_path.name}:{'.'.join(map(str, item.absolute_path)) or '$'}: {item.message}"
            for item in found
        ]
    except (OSError, ValueError, Unresolvable) as exc:
        return [f"{schema_path.name}: validation could not be completed: {exc}"]
