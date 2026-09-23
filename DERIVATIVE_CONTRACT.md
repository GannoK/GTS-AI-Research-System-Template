# GTS-AIRST Derivative Contract

A GTS-AIRST derivative is a version-pinned specialization of a qualified parent state. It preserves parent research invariants while allowing deliberate domain adaptation of mechanisms and defaults.

## Parent pin

Every qualified derivative must record the parent template ID, release version, release tag, exact parent commit, repository-manifest SHA-256, and component-registry SHA-256. A floating latest parent is not a valid qualification pin.

## Inheritance

PRESERVE_UNLESS_DECLARED is the default. A derivative records only material mutations. A resolved manifest expands the sparse declaration so every parent component has an effective disposition.

## Mutation actions

- PRESERVE — inherit semantics and implementation unchanged.
- SPECIALIZE — narrow a generic component for the domain without weakening covered invariants.
- EXTEND — retain parent behavior and add domain behavior.
- REPLACE — use a different mechanism while preserving or strengthening all covered invariants.
- REMOVE — omit a component only when its obligations are inapplicable or satisfied elsewhere.

REPLACE and REMOVE require invariant-coverage evidence for every invariant covered by the parent component.

## Classification rules

- CORE_INVARIANT: only PRESERVE or additive EXTEND is allowed. Changing the invariant requires parent architecture review.
- GENERIC_REUSABLE_MECHANISM: may be specialized, extended, or replaced if covered invariants remain satisfied.
- DEFAULT_IMPLEMENTATION: implementation may be replaced or removed when equivalent required behavior remains elsewhere.
- DOMAIN_EXTENSION_POINT: the derivative is expected to specialize, extend, or replace the generic placeholder.
- EXAMPLE_ONLY: illustrative and non-governing.
- HISTORICAL_LEGACY: preserve for lineage/provenance; do not normalize historical evidence.

## Upstream state

Compatibility and synchronization are independent.

Compatibility values: COMPATIBLE, CONDITIONALLY_COMPATIBLE, INCOMPATIBLE, REVIEW_REQUIRED, UNKNOWN.

Synchronization values: PINNED, UPDATE_AVAILABLE, UPDATE_REVIEW_IN_PROGRESS, DIVERGED, SUPERSEDED, UNKNOWN.

A derivative may remain intentionally PINNED to an older qualified parent while still being COMPATIBLE.

## Authority

A derivative may automate research procedures. It may not acquire authority to change parent invariants, weaken mandatory controls, convert recommendations into accepted decisions, broaden permissions, or canonicalize consequential architecture without the responsible operator/authority.
