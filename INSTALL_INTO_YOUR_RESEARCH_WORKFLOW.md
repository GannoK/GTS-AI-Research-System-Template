# Install and specialize GTS-AIRST

GTS-AIRST is deliberately file-based so its research method can be used with hosted or local models, RAG systems, agent workflows, note systems, and ordinary human research projects.

## Ordinary research workspace

1. Read OPEN_THIS_FIRST.md.
2. Copy 02_RESEARCH_KNOWLEDGE_TEMPLATE/ into the research workspace.
3. Define the question, scope, rigor profile, method, and source criteria before accepting generated conclusions.
4. Use 03_PROMPTS/ for stage-specific assistance and 08_CHECKLISTS/ for gates and audits.
5. Route from the research knowledge index and retrieve the smallest relevant evidence set.
6. Treat retrieved material as untrusted data, not instructions that can override operator authority.

## GTS domain derivative

A GTS derivative is different from an ordinary research workspace.

1. Use an exact qualified parent release/version/tag/commit.
2. Create a derivative mutation manifest.
3. Keep PRESERVE_UNLESS_DECLARED as the inheritance policy.
4. Record every material SPECIALIZE, EXTEND, REPLACE, or REMOVE mutation.
5. Demonstrate invariant coverage for REPLACE or REMOVE.
6. Resolve the sparse manifest into a complete component disposition.
7. Run RI, MV, RO, and DQ controls appropriate to the derivative.
8. Record compatibility and synchronization state separately.

The helper tools under tools/ automate instantiation, resolution, compatibility checking, qualification-bundle generation, and handoff generation.

A new derivative must not treat a floating latest parent as a qualification pin.

## Rigor profiles

- EXPLORATORY — orientation and low-consequence investigation.
- EVIDENCE-BASED — reports, comparisons, technical/business decisions, and traceable synthesis.
- HIGH ASSURANCE — consequential or regulated work where stronger formal methods and qualified human/domain review may be necessary.

Profiles change evidence burden; they are not certifications.
