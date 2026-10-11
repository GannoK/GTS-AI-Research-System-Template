# GTS-AIRST Qualification Control Domains

Qualification is deliberately separated into four domains.

## RI — Repository Integrity

Question: is the repository structurally intact, reproducible, and safely configured?

Examples: manifest integrity, schema parseability, identity consistency, historical no-touch checks, pinned workflow dependencies, least privilege, tests, deterministic release evidence.

An RI PASS does not prove research methodology validity.

## MV — Methodology Validation

Question: does the research method behave according to its declared invariants under tested conditions?

Examples: provenance, traceability, contradiction preservation, uncertainty, falsification, source dependence, causal overreach, retraction propagation, prompt injection, authority boundaries.

A methodology eval PASS means observed conformance under tested conditions, not universal correctness.

## RO — Research-Output Qualification

Question: does a specific research result have adequate evidence for its stated claims and scope?

RO evaluates source identity, evidence extraction, claim sufficiency, contradiction handling, freshness, limitations, and required human/domain review. RI or MV results cannot automatically qualify a research output.

## DQ — Derivative Qualification

Question: does a domain derivative preserve parent invariants and correctly implement declared specialization?

DQ verifies parent pins, mutation legality, invariant coverage, domain authority/source criteria, inherited evals, domain evals, upstream compatibility, and qualification evidence.

## Result states

PASS, FAIL, MANUAL, N/A, UNKNOWN, WAIVED.

UNKNOWN never implies PASS. MANUAL requires recorded human evidence before promotion. WAIVED requires scope, rationale, authority, risk, and expiration/review trigger. IMPLEMENTED is not VERIFIED.
