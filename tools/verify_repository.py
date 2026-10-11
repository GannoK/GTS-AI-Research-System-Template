#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from assurance_audit import audit as assurance_audit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "OPEN_THIS_FIRST.md",
    "LICENSE",
    "COPYRIGHT.md",
    "LICENSE_HISTORY.md",
    "THIRD_PARTY_NOTICES.md",
    "ATTRIBUTION.md",
    "PACK_METADATA.json",
    "MANIFEST_SHA256.txt",
    "SECURITY.md",
    "GOVERNANCE.md",
    "MAINTAINERS.md",
    "ASSURANCE.json",
    "LEGAL/IP_OWNERSHIP_POLICY.md",
    "LEGAL/CONTRIBUTOR_POLICY.md",
    "LEGAL/AI_ASSISTED_AUTHORSHIP_POLICY.md",
    "02_RESEARCH_KNOWLEDGE_TEMPLATE/60_EVIDENCE_LEDGER.md",
    "02_RESEARCH_KNOWLEDGE_TEMPLATE/70_CLAIMS_LEDGER.md",
    "02_RESEARCH_KNOWLEDGE_TEMPLATE/90_CANDIDATE_INTERPRETATIONS.md",
    "02_RESEARCH_KNOWLEDGE_TEMPLATE/100_RECOMMENDATIONS.md",
    "02_RESEARCH_KNOWLEDGE_TEMPLATE/110_ACCEPTED_DECISIONS.md",
    "07_TEMPLATES/10_RESEARCH_PROVENANCE_TEMPLATE.json",
    "07_TEMPLATES/11_CLAIM_EVIDENCE_GRAPH_TEMPLATE.json",
    "07_TEMPLATES/12_SOURCE_RECORD_TEMPLATE.json",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        fail(f"required file missing: {rel}")

meta = json.loads((ROOT / "PACK_METADATA.json").read_text(encoding="utf-8"))
if meta.get("license") != "Proprietary-All-Rights-Reserved":
    fail("PACK_METADATA.json license must be Proprietary-All-Rights-Reserved")
if meta.get("version") != "0.2.1":
    fail("PACK_METADATA.json version must be 0.2.1")
if meta.get("method_selection") != "ADOPT -> PROFILE -> EXTEND -> BUILD":
    fail("method-selection invariant changed")

manifest = ROOT / "MANIFEST_SHA256.txt"
seen = set()
for lineno, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw)
    if not match:
        fail(f"invalid manifest line {lineno}")
    expected, rel = match.groups()
    path = ROOT / rel
    if not path.is_file():
        fail(f"manifest file missing: {rel}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        fail(f"checksum mismatch: {rel}")
    seen.add(rel)

expected_files = {
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*")
    if p.is_file()
    and p.name != "MANIFEST_SHA256.txt"
    and ".git" not in p.parts
    and "__pycache__" not in p.parts
}
if seen != expected_files:
    missing = sorted(expected_files - seen)
    stale = sorted(seen - expected_files)
    if missing:
        print("Manifest missing entries:")
        for rel in missing:
            print(f"  {rel}")
    if stale:
        print("Manifest has stale entries:")
        for rel in stale:
            print(f"  {rel}")
    fail("manifest set does not exactly match repository files")

link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for md in ROOT.rglob("*.md"):
    text = md.read_text(encoding="utf-8", errors="replace")
    for match in link_pattern.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        local = target.split("#", 1)[0]
        if local and not (md.parent / local).resolve().exists():
            fail(f"broken local link in {md.relative_to(ROOT)}: {target}")

assurance_failures, manual_controls = assurance_audit()
if assurance_failures:
    for item in assurance_failures:
        print(f"ASSURANCE_FAIL: {item}")
    fail(f"assurance policy failures: {len(assurance_failures)}")

print(
    f"REPOSITORY_VERIFY=PASS files={len(expected_files)} "
    f"manual_controls={len(manual_controls)}"
)
