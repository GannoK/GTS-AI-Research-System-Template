# PR #9 repair and reconciliation record

Recorded: 2026-10-11 UTC / 2026-10-10 America/Los_Angeles.

This record preserves the later repair authorization and integration decisions. It does not replace the original [AIRST-HARDENING-001 plan](AIRST-HARDENING-001-PLAN.md) or establish a qualification result.

## Authorization and reference states

The user authorized repairing PR #9, reconciling it with current main, and merging the repaired result after verification. Release publication remains a separate action and is not authorized by this repair instruction.

| Reference | Commit |
|---|---|
| Original accepted hardening control base | `b1ec68c0052a1564187e7e48691baca89add803b` |
| PR #9 head reviewed before repair | `4daeca94e4b980d909c8946bcda751961ab188e4` |
| Approved v0.2.1 main integrated into the repair | `5c86f3229a317b4c51e7944eddb0f5540f645ff5` |

The original plan and acceptance checklist retain their original control-base references. Their earlier execution boundary describes that earlier authorization; this record identifies the subsequent repair and merge authorization without rewriting it.

## Accepted integration decisions

- Use the exact approved v0.2.1 README and setup text as the base, then add a separate path for derivative creators and maintainers.
- Preserve the v0.2.1 glossary, worked example, quick start, release notes, and prior historical licensing records. Add the v0.2.1 release notes to the protected historical-file registry.
- Keep v0.2.1 as the last declared release. Record v0.3.0 only as `next_planned_version`, with `UNRELEASED_POST_V0_2_1_HARDENING` and `new_release_declared: false` for the candidate.
- Use the standard `jsonschema` validator through the pinned maintainer dependencies. Missing dependencies must not silently bypass validation.
- Require existing, exactly pinned released parents for derivative creation and technical compatibility checks. Keep unresolved domain placeholders visible in draft resolutions; no tool may turn them into automatic qualification.
- Separate evaluation-harness self-tests, retained results from actual systems, and required human judgments. Missing evidence remains unresolved.
- Verify the repaired integration and retain its exact commit identity in the generated candidate evidence. This record contains no fabricated completion or review results.

## Release and qualification boundary

The repair does not declare v0.3.0, create a release tag, publish an archive, create a domain derivative, or authorize an autonomous research runtime. The unchanged historical v0.2.0 licensing baseline and v0.2.1 release record remain distinct from the unreleased hardening state.

The [acceptance controls](AIRST-HARDENING-001-ACCEPTANCE.json), [qualification domains](../assurance/CONTROL_DOMAINS.md), test results, and candidate bundle provide the evidence for review. Passing automated checks does not supply missing real-system evidence, complete a human review, or constitute release approval.
