# GTS-AIRST Governance

GTS AI Research System Template is maintained as the reusable parent template for GTS domain-specialized AI-assisted research systems. The GitHub repository may be publicly inspectable while current distributions remain governed by the repository license.

## Decision model

- Routine corrections and implementation improvements may be merged after required verification and review.
- Changes to core research invariants, evidence semantics, licensing, provenance rules, authority boundaries, or security posture require explicit maintainer/operator review.
- Material architectural changes must state the problem, evidence, tradeoffs, compatibility/migration impact, and qualification evidence.
- Human judgment requirements must not be silently converted into automated PASS results.
- A derivative may specialize mechanisms but may not silently weaken parent invariants.

## Authority

Research automation may decompose questions, route to allowed sources/tools, collect evidence, identify contradictions/gaps, update research state, and propose interpretations or recommendations.

It does not gain authority to accept consequential decisions, broaden permissions, canonicalize architecture/policy, publish externally where approval is required, or weaken mandatory controls.

## Qualification

Repository integrity (RI), methodology validation (MV), research-output qualification (RO), and derivative qualification (DQ) are separate control domains. Passing one domain does not imply another.

## Releases

A release must be traceable to a repository commit, pass required automated checks, preserve historical lineage and the checksum manifest, record unresolved MANUAL/UNKNOWN/WAIVED controls, and receive the required operator release disposition.
