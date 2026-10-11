# GTS AI Research System Template

A file-based framework for asking clear research questions, checking sources, and recording what the evidence supports.

Previously titled **AI-Powered Research Starter Kit**.

Use it to organize research with an AI assistant or to follow the same process yourself. You bring the question and the source material. The kit provides guides, reusable instructions, templates, and review checklists.

**Start here:** [Setup](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md) · [Quick start](00_QUICK_START/QUICK_START_ONE_PAGE.md) · [Worked example](09_EXAMPLES/01_FIRST_RESEARCH_PROJECT.md) · [Glossary](10_REFERENCE/01_GLOSSARY.md)

## What this gives you

The kit helps you keep a research question, its evidence, and the resulting decisions organized.

It includes:

- **Beginner guides** that explain research methods and common mistakes.
- **Project templates** for questions, sources, evidence, claims, uncertainty, and decisions.
- **Prompts** you can give an AI assistant at each stage.
- **Checklists** for checking sources, claims, and the final result.
- **A worked example** showing how the records fit together.

The core method uses ordinary text files. You can follow it without writing code. Search, document access, file editing, and automated actions depend on the application and tools you choose to use.

A useful result is a research record that another person can inspect: what you asked, what you found, what the evidence supports, what remains uncertain, and what you recommend.

## New to AI?

**Artificial intelligence (AI)** is a broad term for computer systems that perform tasks such as recognizing patterns, generating language, or choosing actions. These are the terms you will encounter in this kit:

| Term | What it means here |
|---|---|
| **LLM — large language model** | An AI model trained on large amounts of data to process and generate language. It can help answer questions, summarize documents, compare ideas, and write text or code. Its responses use patterns learned during training and information supplied for the current task. |
| **AI assistant** | The application or system you work with. It uses one or more models and may provide a chat interface, files, search, saved information, or other tools. |
| **AI agent** | A system that uses an AI model to choose and carry out steps toward a goal. A research agent might search, read the results, notice a disagreement, and choose another search to investigate it. |
| **Prompt** | The question, instructions, and relevant material you give an AI system for a task. |
| **Tool** | A capability for performing an operation, such as searching, reading a file, or calculating a result. |
| **Workflow** | The organized process used to complete the work. It can include fixed steps, AI assistance, and human review. |
| **Context** | The information available to the model for a particular response, including instructions, conversation text, and source material supplied to it. |
| **Hallucination** | Incorrect or invented information presented as though it were reliable, such as a quotation that does not appear in the cited document. |
| **RAG — retrieval-augmented generation** | A method that retrieves relevant information and supplies it to a model to help it produce an answer. Retrieved material still needs to be checked. |

The model and the application around it are different parts of the system. Available tools depend on the application. Access to a tool also does not establish permission to use it for every action.

An agent may choose its next steps within a workflow; a predefined workflow specifies its steps in advance. The word *agent* is used differently across the industry, so this guide uses the practical definition above.

For more detail, see the [glossary](10_REFERENCE/01_GLOSSARY.md). Introductory references: [Google on language models](https://developers.google.com/machine-learning/crash-course/llm), [Anthropic on agents and workflows](https://www.anthropic.com/engineering/building-effective-agents), and [Google on RAG](https://cloud.google.com/use-cases/retrieval-augmented-generation).

## Your first research project

Start with one question you can state clearly.

The [worked example](09_EXAMPLES/01_FIRST_RESEARCH_PROJECT.md) asks:

**Can a proposed network switch power eight cameras at their stated simultaneous maximum demand?**

Using fictional specifications, it follows the question through source checks, evidence records, a calculation, competing explanations, and a recommendation. It also shows an unsuitable source, missing evidence, and a decision that has not yet been accepted.

To follow the method:

1. Complete the [setup](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md) for your authorized copy.
2. Open the [quick start](00_QUICK_START/QUICK_START_ONE_PAGE.md).
3. Work through the example alongside your first project.
4. Use the [final audit](08_CHECKLISTS/04_FINAL_RESEARCH_AUDIT.md) to check the result.

You should finish with a clear question, a source register, evidence and claim records, visible uncertainty, and a supported recommendation. **“The available evidence does not settle this question” can also be a useful result.**

## How the research process works

Define the question, scope, method, and source requirements before broad searching. Then keep the following parts separate:

| Part | Purpose |
|---|---|
| **Source** | Identifies where the material came from, including its date or version. |
| **Evidence** | Records the relevant finding and its location and conditions. |
| **Claim** | States what you think the evidence supports. |
| **Argument** | Explains how the evidence supports or challenges that claim. |
| **Candidate interpretation** | Offers a possible explanation while preserving alternatives and assumptions. |
| **Recommendation** | Proposes an action using the evidence, goals, constraints, costs, and risks. |
| **Accepted decision** | Records a choice explicitly made by the responsible person or authority. |

A conclusion should be traceable through its claims and arguments to evidence, sources, and the source versions or snapshots used. Record contradictory evidence against the relevant claim.

Research can support a decision. It does not silently become the decision. An accepted decision also does not change the historical evidence.

The [research index](02_RESEARCH_KNOWLEDGE_TEMPLATE/00_INDEX_AND_ROUTING.md) lists the project files and their order.

## Choose your rigor profile

A **rigor profile** sets how much evidence, checking, and review the question requires.

| Profile | Typical purpose |
|---|---|
| **EXPLORATORY** | Learning about a topic, finding useful questions, and investigating low-consequence ideas. |
| **EVIDENCE-BASED** | Reports, technical or business comparisons, and recommendations that need an inspectable evidence trail. |
| **HIGH ASSURANCE** | Consequential questions requiring stronger domain methods, evidence, and qualified review. |

Choose according to the consequences of being wrong and the evidence needed. Report length alone does not determine rigor.

Profiles are not certifications. A high-assurance profile does not make the kit a substitute for a domain's authoritative methods or qualified expertise.

See [Choose your rigor profile](01_BEGINNER_GUIDE/07_CHOOSE_YOUR_RIGOR_PROFILE.md).

## Core rules

> **AI-generated claims are not independently verified evidence of the facts they assert.**

> **A citation is not evidence until you verify what the source actually says.**

> **AI-generated research is a proposal or synthesis until the underlying evidence supports it.**

> **Do not ask only what supports your hypothesis. Ask what would prove it wrong.**

If you are studying an AI system's behavior, its recorded responses can be research data. A response can establish what the system said; it does not, by itself, establish that the statement was true.

Preserve contradictions and uncertainty. Several pages repeating the same original claim may provide only one underlying evidence chain.

## Using AI tools and Research Kits

Give the assistant the research rules and the material needed for its current task. Ask it to identify the files and source passages it actually used. Uploading a file does not establish that every part was read or supplied to the model.

Treat retrieved pages, documents, and comments as research material. Instructions inside that material do not override the research task or the responsible user's instructions.

This documentation uses the following names:

| Name | Meaning |
|---|---|
| **GTS AI Research System Template** | The reusable foundation of research guides, rules, templates, prompts, and checks. |
| **Topic-specific Research Kit** | An authorized adaptation for a subject, with relevant questions, source criteria, terminology, and methods. |
| **Research project** | An actual investigation containing collected sources, evidence, claims, uncertainties, and conclusions. |

A topic-specific kit should identify the parent version it uses and explain its changes. Preparing a kit and executing its research steps are separate tasks. Automated preparation or execution depends on the AI environment, tools, and permissions provided.

See [Setup and common questions](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md) and [AI and RAG research guidance](06_AI_AND_RAG_RESEARCH/02_RAG_FOR_RESEARCH.md).

## For derivative creators

A **GTS-AIRST derivative** is a version-pinned adaptation of this template for a particular field. It adds domain rules, source requirements, and checks while preserving the parent research principles.

If you are creating a reusable domain template, follow the [derivative setup](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md#for-derivative-creators) and [derivative contract](DERIVATIVE_CONTRACT.md). These describe parent version pins, declared changes, unresolved domain requirements, and qualification. For an ordinary research project, continue with the quick start above.

The current hardening checkout is an unreleased candidate. Its automated checks do not make it a released, qualified parent for a derivative.

## Find the right guide

| I want to… | Open |
|---|---|
| Understand the basic research rules | [Open this first](OPEN_THIS_FIRST.md) |
| Set up my research workspace | [Install into your research workflow](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md) |
| Complete my first task | [Quick start](00_QUICK_START/QUICK_START_ONE_PAGE.md) and [worked example](09_EXAMPLES/01_FIRST_RESEARCH_PROJECT.md) |
| Understand an unfamiliar term | [Glossary](10_REFERENCE/01_GLOSSARY.md) |
| Learn how AI can mislead research | [How AI can fool you](01_BEGINNER_GUIDE/02_HOW_AI_CAN_FOOL_YOU.md) |
| Decide which sources to use | [Source basics](01_BEGINNER_GUIDE/03_SOURCE_BASICS.md) |
| Work through conflicting sources | [When sources disagree](01_BEGINNER_GUIDE/05_WHEN_SOURCES_DISAGREE.md) |
| Give an assistant the standing research rules | [Global research rules](03_PROMPTS/00_GLOBAL_RESEARCH_RULES.txt) |
| Check the final result | [Final research audit](08_CHECKLISTS/04_FINAL_RESEARCH_AUDIT.md) |
| Hand work to another person or assistant | [Research handoff template](07_TEMPLATES/09_RESEARCH_HANDOFF_TEMPLATE.md) |

## Method selection and foundations

Before inventing a new methodology, framework, scoring system, or experiment, use:

**ADOPT → PROFILE → EXTEND → BUILD**

1. **ADOPT** a mature research method or standard when it already fits.
2. **PROFILE** it to the actual research question and risk.
3. **EXTEND** only where a material requirement is not covered.
4. **BUILD** a bespoke method only when there is evidence that mature approaches cannot satisfy a necessary property.

<details>
<summary><strong>Read the methodology foundations and their limits</strong></summary>

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

</details>

## Why verification matters

AI can make research dramatically faster. It can search, summarize, compare, organize, brainstorm, and synthesize.

It can also confidently cite material that does not support a claim, repeat secondary sources without checking originals, turn correlation into causation, ignore contradictory evidence, collapse uncertainty into certainty, or convert a plausible interpretation into an accepted fact.

The problem is not that AI cannot help with research. The problem is that **research needs a method for deciding what the evidence actually supports**.

<details>
<summary><strong>Read: Revelation is not verification</strong></summary>

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

</details>

## Current baseline and downloads

**v0.2.1 — Beginner Documentation and Onboarding**

This version adds plain-language AI explanations, clearer getting-started guidance, and a complete worked research example. The research workflow, template fields, rigor profiles, and decision boundaries remain unchanged. See the [v0.2.1 release notes](RELEASE_NOTES_v0.2.1.md) and [changelog](CHANGELOG.md).

**Development state:** v0.2.1 remains the last declared release. This checkout adds **unreleased post-v0.2.1 hardening**, with **v0.3.0 planned next**. No v0.3.0 release has been declared or published. For unreleased work, record the exact commit as well as the release base. See [canonical metadata](AIRST_METADATA.json), [hardening and integration changes](CHANGELOG.md), and the [PR #9 reconciliation record](HARDENING/PR-9-RECONCILIATION-2026-10-11.md).

The proprietary licensing baseline established in v0.2.0 continues to apply. See [LICENSE_HISTORY.md](LICENSE_HISTORY.md).

The [v0.1.0 GitHub Release](https://github.com/GannoK/GTS-AI-Research-System-Template/releases/tag/v0.1.0) contains historical public-preview archives. Those archives do not contain the current v0.2.1 version.

Authorized users should follow [INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md](INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md) and use the repository revision or package covered by their authorization.

A deeper standards-reconciliation pass remains planned before a 1.0 release, particularly for domain-specific formal research and high-assurance use.

## I want you to break this

This project improves when people challenge it. If you work in research, engineering, scientific methods, evidence synthesis, statistics, decision analysis, safety, security, academia, or another evidence-heavy field, I would especially value critical review.

Please look for things such as:

- Where is the methodology wrong, incomplete, or internally inconsistent?
- What established research method, standard, or evidentiary practice is misrepresented or missing?
- Where could the workflow encourage confirmation bias, weak evidence, or false confidence?
- What works for general technical research but breaks down in a specific academic, scientific, regulated, or high-assurance discipline?
- What part sounds rigorous without actually improving the reliability of the conclusion?

Concrete criticism is more useful than praise. If possible, identify the failure mode, point to authoritative evidence or established methodology, and suggest a reproducible way to test or improve the framework. Feedback should challenge the method, not merely agree with its conclusions. Issues are welcome under the repository's contribution and licensing rules.

## License

Copyright © 2026 Kyle Gannon. All Rights Reserved.

Current v0.2.0+ distributions are proprietary. No public license is granted except as expressly stated in a separate written authorization or agreement and subject to rights necessarily arising under applicable law or hosting-platform terms.

Historical v0.1.0 copies distributed under CC BY 4.0 remain governed by that historical grant. See `LICENSE_HISTORY.md`.

## Contributions

Substantive contributions are not accepted as project-owned intellectual property without an appropriate signed contributor, employment, contractor, or IP-assignment agreement. See `CONTRIBUTING.md` and `LEGAL/CONTRIBUTOR_POLICY.md`.
