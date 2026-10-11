# GTS-AIRST Derivative Contract

A GTS-AIRST derivative is a version-pinned specialization of a qualified parent state. It preserves parent research invariants while allowing deliberate domain adaptation of mechanisms and defaults.

## Parent pin

Every qualified derivative must record the parent template ID, release version, release tag, exact parent commit, repository-manifest SHA-256, and component-registry SHA-256. A floating latest parent is not a valid qualification pin.

The tools verify those records against the parent actually checked out. Its canonical metadata must identify a released state: `release_state.development_state` is `RELEASED`, `new_release_declared` is `true`, and `last_declared_version` matches the pinned version. The existing `refs/tags/v<VERSION>` reference must resolve to the pinned commit and that checkout's `HEAD`; the repository contents and recorded hashes must agree. Writing a release label into a manifest does not create or verify that release.

The current post-v0.2.1 hardening checkout is unreleased. Its planned next version, v0.3.0, is not a valid released-parent pin. An actual release and the applicable qualification review must occur before it can support a qualified derivative.

A matching version, tag, commit, and hash establish technical pin consistency. They do not by themselves establish methodological validity, domain suitability, or a qualification decision.

Keep the checked-out parent unchanged. Write derivative manifests and resolution outputs in a separate derivative workspace outside the parent checkout; `--output` paths inside the parent are rejected.

## Inheritance

PRESERVE_UNLESS_DECLARED is the default. A derivative records only material mutations. A resolved manifest expands the sparse declaration so every parent component has an effective disposition.

The default applies only where preservation is permitted by the component registry. An omitted domain extension point that requires specialization remains unresolved; it must not silently inherit a generic placeholder as a qualified domain implementation.

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

## Drafts and qualification

A draft may contain unanswered domain questions, but it must report them. For an unresolved component, the resolver records `effective_mutation: null` and `resolution_status: REVIEW_REQUIRED`; it writes the draft resolution and exits with status `2`. Resolve each required domain disposition, supply the evidence for invariant coverage, and complete the applicable [qualification controls](assurance/CONTROL_DOMAINS.md) before claiming qualification.

The tools serve different purposes:

- [instantiate_derivative.py](tools/instantiate_derivative.py) prepares a manifest against an existing, exactly checked-out released parent.
- [resolve_derivative.py](tools/resolve_derivative.py) expands declarations into component dispositions and makes unresolved draft requirements visible.
- [check_parent_compatibility.py](tools/check_parent_compatibility.py) checks technical compatibility with the pinned parent. It does not award or change research qualification.

See [maintainer validation setup](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md#maintainer-validation-setup) for the Python environment and checks. A draft manifest, resolved component list, passing self-test, or successful compatibility check is not an accepted qualification decision.

## Upstream state

Compatibility and synchronization are independent.

Compatibility values: COMPATIBLE, CONDITIONALLY_COMPATIBLE, INCOMPATIBLE, REVIEW_REQUIRED, UNKNOWN.

Synchronization values: PINNED, UPDATE_AVAILABLE, UPDATE_REVIEW_IN_PROGRESS, DIVERGED, SUPERSEDED, UNKNOWN.

A derivative may remain intentionally PINNED to an older qualified parent while still being COMPATIBLE.

## Authority

A derivative may automate research procedures. It may not acquire authority to change parent invariants, weaken mandatory controls, convert recommendations into accepted decisions, broaden permissions, or canonicalize consequential architecture without the responsible operator/authority.
