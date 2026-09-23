# GTS AI Research System Template

A reusable parent template for rigorous, evidence-driven, AI-assisted research systems.

GTS-AIRST defines reusable research invariants, state/provenance structures, qualification controls, derivative contracts, and reference implementations without treating model output, search results, or citations as proof.

> **Identity and release state:** The current canonical identity is **GTS AI Research System Template (GTS-AIRST)** at `GannoK/GTS-AI-Research-System-Template`. The last declared release remains **v0.2.0 — Proprietary Baseline**; current `main` contains unreleased post-v0.2.0 hardening. Historical v0.1.0 CC BY 4.0 grants remain traceable and are not rewritten. See `AIRST_METADATA.json`, `LICENSE`, and `LICENSE_HISTORY.md`.

## I want you to break this

This project improves when people challenge it. If you work in research, engineering, scientific methods, evidence synthesis, statistics, decision analysis, safety, security, academia, or another evidence-heavy field, I would especially value critical review.

Please look for things such as:

- Where is the methodology wrong, incomplete, or internally inconsistent?
- What established research method, standard, or evidentiary practice is misrepresented or missing?
- Where could the workflow encourage confirmation bias, weak evidence, or false confidence?
- What works for general technical research but breaks down in a specific academic, scientific, regulated, or high-assurance discipline?
- What part sounds rigorous without actually improving the reliability of the conclusion?

Concrete criticism is more useful than praise. If possible, identify the failure mode, point to authoritative evidence or established methodology, and suggest a reproducible way to test or improve the framework. Feedback should challenge the method, not merely agree with its conclusions. Issues are welcome under the repository's contribution and licensing rules.

## The problem

AI can make research dramatically faster. It can search, summarize, compare, organize, brainstorm, and synthesize.

It can also confidently cite material that does not support a claim, repeat secondary sources without checking originals, turn correlation into causation, ignore contradictory evidence, collapse uncertainty into certainty, or convert a plausible interpretation into an accepted fact.

The problem is not that AI cannot help with research. The problem is that **research needs a method for deciding what the evidence actually supports**.

## Revelation is not verification

Telling an LLM, **“Research this and tell me the truth,”** without checking its sources is like starting a religion because one guy woke up from a dream and said:

> **“God told me.”**

No scripture. No witnesses. No corroboration.

Just confidence.

The problem is not that the revelation was not delivered confidently enough. The problem is that a defensible conclusion requires evidence, provenance, corroboration, competing explanations, and a serious attempt to determine whether you might be wrong.

AI can help enormously with that process.

**But it cannot replace the process.**

A second way to think about it:

> Asking an LLM to **“research this and tell me the truth”** without a research methodology is like asking a detective to solve a murder by interviewing one witness and then writing the closing argument.

**One witness is not an investigation. One citation is not a conclusion.**

And asking AI to **“find sources proving I’m right”** is not research methodology.

**It is building a prosecution.**

Three rules worth remembering:

- **Revelation is not verification.**
- **One citation is not a conclusion.**
- **Research the question—not your preferred answer.**

A useful operating principle for AI-assisted research is:

> **AI output is a lead until evidence supports the relevant conclusion.**

## Core rules

> **AI is not a source.**

> **A citation is not evidence until you verify what the source actually says.**

> **AI-generated research is a proposal or synthesis until the underlying evidence supports it.**

> **Do not ask only what supports your hypothesis. Ask what would prove it wrong.**

## Standards and methodology foundations

This kit is not based on a single invented "AI research method." It is a beginner-usable synthesis of established practices from research methodology, systems engineering, architecture, decision analysis, assurance, software engineering, and scientific reasoning.

Representative intellectual and organizational foundations include:

- **INCOSE Systems Engineering Handbook** — life-cycle thinking, requirements discipline, verification, validation, risk, and traceability.
- **NASA Systems Engineering Handbook** and **NASA Risk-Informed Decision Making Handbook** — staged engineering, trade studies, uncertainty, risk, decision framing, and evidence-based gates.
- **ISO/IEC/IEEE 15288** — system life-cycle processes and disciplined engineering activities.
- **ISO/IEC/IEEE 42010** — architecture descriptions organized around stakeholders, concerns, viewpoints, and explicit architectural rationale.
- **ISO/IEC 25010** and the **ISO/IEC/IEEE 15026 family** — quality characteristics, assurance concepts, and evidence-supported confidence.
- **Carnegie Mellon Software Engineering Institute** methods such as QAW, ADD, ATAM, SAAM, and CBAM — quality attributes, architecture tradeoffs, structured review, and cost/benefit reasoning.
- **Architecture Decision Records (ADRs)** — preserving the context, rationale, consequences, and status of consequential decisions.
- **Set-Based Design** and Ward, Liker, Cristiano & Sobek's work on the "Second Toyota Paradox" — keeping multiple viable alternatives open until evidence justifies convergence.
- **Influence diagrams, sensitivity analysis, Value of Information, and formal decision analysis** — making uncertainty and decision consequences explicit instead of hiding them inside prose.
- **RAND Robust Decision Making** — looking for strategies that remain acceptable across uncertain futures rather than optimizing for one assumed future.
- **Design Structure Matrices and related dependency-mapping methods** — making coupling, interaction, and change propagation visible.
- **Evolutionary architecture and fitness functions** — continuously checking whether an evolving system still satisfies important architectural properties.
- **STAMP/STPA safety-analysis methods** — reasoning about unsafe control actions, interactions, and system-level hazards in consequential systems.
- **Design Science Research Methodology and empirical software-engineering practices** — separating problem framing, artifact design, evaluation, evidence collection, and conclusions.
- **Scientific falsification, corroboration, provenance, uncertainty recording, and competing-hypothesis analysis** — actively asking what would disprove a claim rather than searching only for supporting evidence.

Where the research concerns software, security, AI, or technology governance, the kit can also profile applicable authorities such as **NIST, OWASP, CISA, OpenSSF, IETF, W3C, IEEE, ISO/IEC, and domain-specific standards bodies**. The applicable authority depends on the research question; no single standards list is treated as universally sufficient.

These sources are **foundations and reference points**, not a claim that this kit is itself an ISO, NASA, INCOSE, NIST, scientific, or regulatory standard. A domain's authoritative methods and standards remain authoritative over summaries or profiles in this repository.

The method-selection rule is deliberately conservative:

> **ADOPT → PROFILE → EXTEND → BUILD**
>
> Adopt a mature method when one already fits. Profile it to the actual question, consequence, uncertainty, and evidence burden. Extend only where a material requirement is missing. Build a bespoke method only when there is evidence that mature approaches cannot satisfy a necessary property.

That foundation is why this kit emphasizes provenance, source hierarchy, claim/evidence separation, contradiction and falsification, explicit assumptions, uncertainty, reversible experiments, sensitivity analysis, decision traceability, and proportional rigor rather than treating an LLM's confidence as evidence.

This is intentionally a **general research framework**, not a claim of complete methodology coverage for every academic or regulated discipline. Deeper domain-specific standards reconciliation remains planned before a 1.0 release, particularly for high-assurance research.

## The research chain

Important conclusions should be traceable backward:

```text
CONCLUSION
    ↓
CLAIM
    ↓
ARGUMENT
    ↓
EVIDENCE
    ↓
SOURCE
    ↓
SOURCE VERSION / DATE / SNAPSHOT
```

Contradictory evidence belongs on the same claim record.

## Evidence is not authority

This kit deliberately separates:

```text
Research evidence
    ↓
Candidate interpretation
    ↓
Recommendation
    ↓
Accepted decision
```

Research can support a decision. It does not silently become the decision.

## Method selection

Before inventing a new methodology, framework, scoring system, or experiment, use:

**ADOPT → PROFILE → EXTEND → BUILD**

1. **ADOPT** a mature research method or standard when it already fits.
2. **PROFILE** it to the actual research question and risk.
3. **EXTEND** only where a material requirement is not covered.
4. **BUILD** a bespoke method only when there is evidence that mature approaches cannot satisfy a necessary property.

## Research rigor profiles

- **EXPLORATORY** — learning, orientation, brainstorming, and low-consequence investigation.
- **EVIDENCE-BASED** — reports, technical/business decisions, serious synthesis, and claims that need traceability.
- **HIGH ASSURANCE** — consequential domains such as medicine, law, public policy, safety, regulated work, formal scientific review, or other decisions where being wrong could cause major harm.

Profiles change the evidence burden. They are not certificates.

## Download and use it

Current distributions are controlled by the proprietary license in `LICENSE`. Do not copy, redistribute, adapt, or commercialize the current version unless you have written authorization.

Authorized users should follow [`INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md`](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md).

## Current release and development state

**Last declared release: v0.2.0 — Proprietary Baseline**

Current development state: **unreleased post-v0.2.0 hardening**. A new release/version has not been declared.

v0.2.0 preserved the research methodology while changing the active distribution model from the historical CC BY 4.0 public preview to a proprietary, all-rights-reserved baseline. Current hardening adds parent/derivative contracts, machine-readable invariants/components, qualification-domain separation, and executable/hybrid methodology eval infrastructure without changing the historical v0.2.0 meaning.

A deeper standards-reconciliation pass remains planned before a 1.0 release, particularly for domain-specific formal research and high-assurance use.

## Quick start

1. Read `OPEN_THIS_FIRST.md`.
2. Choose a rigor profile.
3. Define the question before searching.
4. Register sources before treating them as evidence.
5. Extract evidence separately from interpretation.
6. Build claims from evidence.
7. Search for contradiction and falsification.
8. Record uncertainty.
9. Keep recommendation separate from accepted decision.
10. Audit the final report.

## License

Copyright © 2026 Kyle Gannon. All Rights Reserved.

Current v0.2.0+ distributions are proprietary. No public license is granted except as expressly stated in a separate written authorization or agreement and subject to rights necessarily arising under applicable law or hosting-platform terms.

Historical v0.1.0 copies distributed under CC BY 4.0 remain governed by that historical grant. See `LICENSE_HISTORY.md`.

## Contributions

Substantive contributions are not accepted as project-owned intellectual property without an appropriate signed contributor, employment, contractor, or IP-assignment agreement. See `CONTRIBUTING.md` and `LEGAL/CONTRIBUTOR_POLICY.md`.
