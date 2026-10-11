# Adversarial Research Regression Corpus

The executable/hybrid source of truth for the methodology regression corpus is evals/methodology/CASES.json. The harness is tools/run_methodology_evals.py.

| ID | Coverage | Mode |
|---|---|---|
| AR-001 | hallucinated citation / provenance | HYBRID |
| AR-002 | source dependence | HYBRID |
| AR-003 | prompt injection / untrusted content | HYBRID |
| AR-004 | retraction propagation | DETERMINISTIC |
| AR-005 | freshness / supersession | DETERMINISTIC |
| AR-006 | causal overreach | HYBRID |
| AR-007 | contradiction preservation | DETERMINISTIC |
| AR-008 | quotation verification | DETERMINISTIC |
| AR-009 | publisher concentration / independence | HYBRID |
| AR-010 | statistics context / uncertainty | HYBRID |
| AR-011 | unauthorized scope expansion | DETERMINISTIC |
| AR-012 | authority escalation | DETERMINISTIC |
| AR-013 | tool failure / bounded recovery | DETERMINISTIC |
| AR-014 | derivative mutation legality | DETERMINISTIC |

The harness can deterministically evaluate structured result fields. HYBRID cases remain MANUAL after deterministic assertions until an evidence-grounded semantic review is performed against a concrete research-system output.

Passing the corpus means observed conformance under the tested conditions. It is not proof of universal methodological correctness.
