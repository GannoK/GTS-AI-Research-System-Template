# GTS-AIRST Security

## Security model

Prefer allowlists, schemas, immutable pins, hashes, validators, evals, least privilege, explicit authority boundaries, and deterministic stop/failure states over blacklist-first controls.

Capabilities are deny-by-default: a Skill, tool, plugin, model, or agent does not acquire authority merely because it can technically perform an action. Read authority and write authority are distinct.

Retrieved pages, documents, comments, and other external content are untrusted data. They must not override the research method, system constraints, or responsible operator.

## Supported versions

Security fixes are applied to the current maintained release and default branch. Historical snapshots remain evidence and may not receive backports unless explicitly stated.

## Secrets and credentials

Do not commit secrets, credentials, API keys, confidential research data, or private personal information. Repository validation includes conservative secret-pattern checks, but those checks supplement rather than replace proper secret management.

## Reporting

If a security problem affects this repository, report it privately through GitHub's supported security-reporting mechanism when available. Non-sensitive research-safety failures such as fabricated citations, prompt injection, provenance loss, unsafe authority escalation, or integrity-check bypasses may be reported through normal issue channels.

## Completion rule

A fix is not complete merely because files changed. Relevant behavior, tests/evals, evidence, unresolved controls, and regression risk must be accounted for before verification.
