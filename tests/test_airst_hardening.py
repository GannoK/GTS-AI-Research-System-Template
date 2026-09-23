from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("airst_validate", ROOT / "tools" / "airst_validate.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AirstHardeningTests(unittest.TestCase):
    def test_identity_has_no_manually_maintained_head(self):
        data = json.loads((ROOT / "AIRST_METADATA.json").read_text(encoding="utf-8"))
        paths = [path for path, _ in MODULE._walk_values(data)]
        self.assertFalse(any(path.endswith("current_head") or path.endswith("current_commit") for path in paths))
        self.assertEqual(data["commit_identity"], "DERIVE_FROM_GIT")

    def test_core_components_cannot_replace_or_remove(self):
        data = json.loads((ROOT / "COMPONENT_REGISTRY.json").read_text(encoding="utf-8"))
        for component in data["components"]:
            if component["classification"] == "CORE_INVARIANT":
                self.assertNotIn("REPLACE", component["mutation_permissions"])
                self.assertNotIn("REMOVE", component["mutation_permissions"])
                self.assertNotIn("SPECIALIZE", component["mutation_permissions"])

    def test_historical_hash_protection(self):
        self.assertEqual(MODULE.validate_historical_paths(), [])


if __name__ == "__main__":
    unittest.main()
