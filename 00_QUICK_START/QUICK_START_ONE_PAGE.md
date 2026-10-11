# Quick start: your first research project

Use this guide with an authorized copy of the kit. If your workspace is not ready, follow [setup](../INSTALL_INTO_YOUR_RESEARCH_WORKFLOW.md) first. Keep the [worked example](../09_EXAMPLES/01_FIRST_RESEARCH_PROJECT.md) open beside your project. Look up unfamiliar words in the [glossary](../10_REFERENCE/01_GLOSSARY.md).

## 1. Open your project files

If you have not already created your project during setup, copy the contents of [02_RESEARCH_KNOWLEDGE_TEMPLATE](../02_RESEARCH_KNOWLEDGE_TEMPLATE/) into your project's `knowledge/` folder. For an existing project, open its current `knowledge/` folder and preserve the completed files. Open `00_INDEX_AND_ROUTING.md`, which lists the records you will use.

The template is a set of documents. Copying it does not start an automated research run.

## 2. Define the task before searching

Open these four files in your project and complete their fields:

| File | Write |
|---|---|
| `10_RESEARCH_QUESTION.md` | The exact question, why it matters, the decision or output it may inform, and what a useful answer would establish. |
| `20_SCOPE_AND_DEFINITIONS.md` | The system or population, relevant period and setting, key definitions, inclusions, exclusions, and boundary conditions. |
| `30_METHOD_AND_PROFILE.md` | The rigor profile, the established method you will use, and what evidence would challenge your conclusion. |
| `40_SOURCE_CRITERIA.md` | Which sources qualify, how current they need to be, and why you would reject a source. |

For the example, the question concerns eight specified cameras at their simultaneous maximum power demand. That scope is more precise than asking whether a switch is “good.”

Use the simplest established method that fits: **ADOPT → PROFILE → EXTEND → BUILD**. The [profile guide](../01_BEGINNER_GUIDE/07_CHOOSE_YOUR_RIGOR_PROFILE.md) explains the three rigor levels.

## 3. Give your assistant its starting material

If you are using an AI assistant, provide:

- [Global research rules](../03_PROMPTS/00_GLOBAL_RESEARCH_RULES.txt).
- Your project index and the four completed files above.
- [Start a research project](../03_PROMPTS/01_START_A_RESEARCH_PROJECT.txt) as the stage prompt.

Tell it which question to work on. Ask it to identify the files it could actually read and to report missing material. If you are working without AI, use the same documents as your plan.

## 4. Collect sources and extract evidence

Record where and how you searched using the [search log template](../07_TEMPLATES/02_SEARCH_LOG_TEMPLATE.md).

Register each source in `50_SOURCE_REGISTER.md`. Record its identity, date or version, and status. Include rejected sources and explain the reason.

In `60_EVIDENCE_LEDGER.md`, record relevant findings with their source IDs, exact locations, conditions, and limitations. Check the original material. A generated quotation or search snippet is not a substitute for that check.

## 5. Build and challenge the claims

In `70_CLAIMS_LEDGER.md`, connect each claim to supporting and contradicting evidence. Explain the reasoning, assumptions, and remaining uncertainty.

In `80_CONFLICTS_AND_UNCERTAINTIES.md`, record disagreements, gaps, and alternative explanations. Search for evidence that could show your current conclusion is wrong. Keep a record of how any conflict was resolved.

## 6. Separate the conclusion from the decision

Record possible explanations in `90_CANDIDATE_INTERPRETATIONS.md` and proposed actions in `100_RECOMMENDATIONS.md`.

Only put an actual, explicitly accepted choice in `110_ACCEPTED_DECISIONS.md`. If none has been made, write **“No accepted decision recorded.”**

## 7. Check the result and leave a clear next step

Use the [final audit](../08_CHECKLISTS/04_FINAL_RESEARCH_AUDIT.md). Check that important claims trace to source passages, the passages support the wording, and contradictions and limits remain visible.

Update `120_CURRENT_STATE.md` with the strongest supported conclusion, unresolved questions, the next bounded step, and any blocker. Use the [handoff template](../07_TEMPLATES/09_RESEARCH_HANDOFF_TEMPLATE.md) when another person or assistant will continue.

**Done for this scope** means the required checks are complete and the remaining uncertainty is explicit. A result may be inconclusive. Do not mark a check complete simply because the assistant says it passed.

[Back to README](../README.md)
