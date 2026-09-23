# AIRST-HARDENING-001 — Bounded Implementation Plan

Status: EXECUTION_AUTHORIZED
Control baseline: AIRST-BASELINE-001-v0.1
Accepted refinement: AIRST-REFINEMENT-001-v0.1
Pinned base commit: `b1ec68c0052a1564187e7e48691baca89add803b`

## Execution boundary

Implement the accepted parent-template refinement through qualification on one dedicated branch and one reviewable pull request.

Not authorized:
- autonomous research-runtime implementation;
- SEO derivative creation;
- release publication or version declaration;
- destructive or production actions;
- weakening operator authority or accepted research invariants.

## Implementation sequence

1. Establish canonical GTS-AIRST identity/lineage metadata and schemas.
2. Add a machine-readable invariant/component registry and validation rules.
3. Add the derivative contract, mutation schema, instantiation/resolution/compatibility tooling, and invariant-coverage checks.
4. Separate assurance controls into RI, MV, RO, and DQ domains.
5. Materialize adversarial research cases as executable/hybrid eval fixtures and a deterministic harness.
6. Harden execution/security assumptions: allowlists, untrusted-content boundaries, least privilege, immutable workflow pins, schema/manifest checks, historical no-touch protections, deterministic failure states.
7. Add operator-effort automation for derivative instantiation, manifest resolution, compatibility checking, qualification bundles, identity synchronization/validation, and handoff generation.
8. Migrate future-facing identity references while preserving historical release evidence unchanged.
9. Integrate validators/evals into CI.
10. Generate and inspect a qualification bundle for the candidate; open one PR without merging.

## Qualification rule

IMPLEMENTED != VERIFIED.

A candidate is not complete until every required control is reported as PASS, FAIL, MANUAL, UNKNOWN, WAIVED, or N/A with supporting evidence.

## Stop conditions

Stop for operator disposition only if implementation requires:
- changing a core invariant;
- material scope expansion;
- weakening a security/authority boundary;
- destruction of historical provenance;
- destructive action;
- consequential unresolved ambiguity;
- or an architectural blocker discovered during qualification.
