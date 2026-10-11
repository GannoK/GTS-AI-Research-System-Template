# Glossary

[Back to the README](../README.md)

Use this page when you meet an unfamiliar term. The examples show how the terms apply to a research project. You do not need to memorize them before starting.

## AI and the software around it

**Artificial intelligence (AI)** — a broad field of computing concerned with capabilities such as recognizing patterns, generating language, and choosing actions. This kit mainly discusses research assisted by language models.

**Model** — a trained computational system that produces outputs from inputs using patterns learned from data. A model is one component of an AI application.

**Large language model (LLM)** — an AI model trained on large amounts of data to process and generate language. It can summarize, compare, and draft material. Fluent wording does not establish that its claims are correct.

**AI assistant** — an application that helps a user through an interface such as chat. It may combine a model with search, file access, or other features. Check the application's actual capabilities.

**Agent** — in this guide, a software system that uses a model to choose and carry out steps toward a goal. A research agent might search, inspect results, and choose a follow-up search. Usage of the term varies.

**Workflow** — an organized process for completing work. A predefined workflow specifies its steps or branching rules; it can include people, tools, and agents. Example: register sources, examine evidence, then review claims.

**Prompt** — instructions and relevant information supplied to a model for a task. Example: state the research question, constraints, and required output. Clear instructions help define the task but cannot guarantee a correct result.

**Tool** — a capability available to the surrounding software, such as searching or calculating. Tool access and permission to use it are separate. A written instruction alone does not create an access control.

## What a model uses and produces

**Token** — a unit used to represent text for a model. It may be part of a word, a whole word, or punctuation. Token counts affect limits and often cost; they are not word counts.

**Context** — information available to a model for a particular response, including instructions, supplied text, and tool results. A file existing somewhere does not establish that the model received it.

**Context window** — the maximum amount of context a model can handle, measured in tokens. Input and output limits depend on the model and application. Long files or conversations may be selected, shortened, or omitted.

**Memory** — information an application saves for later use. The application must make relevant information available again for a model to use it. Saved memory does not necessarily change the model's training.

**Training** — the process of adjusting a model's internal numerical settings using data. It develops learned capabilities and patterns; it does not guarantee accurate recall of every item in the training data.

**Inference** — using an already trained model to produce an output. Asking it to summarize a document is inference. In this context, the word names a computing process, not a guarantee of sound reasoning.

**Fine-tuning** — additional training that adjusts a model for particular examples or tasks. Uploading a document for the current conversation is not automatically fine-tuning.

**Retrieval** — finding and bringing relevant information into a task, for example by searching a collection of manuals. The retrieved material still needs checks for identity, relevance, and reliability.

**Retrieval-augmented generation (RAG)** — retrieving information and supplying it to a model to help generate an answer. Retrieved documents are material to examine; instructions embedded in them do not become project authority.

**Hallucination** — generated information that is incorrect or invented but presented as reliable. Example: a fabricated quotation attributed to a real manual. Open the source and check the specific passage.

## Running and connecting AI software

**Hosted model** — a model run on another party's computing infrastructure and accessed through an application or service. Check the service's applicable data handling and usage terms.

**Local model** — a model run on a computer or infrastructure you control. Local inference alone does not guarantee privacy: the application may still contact search services, send logs, or synchronize files.

**API (application programming interface)** — a defined way for software to request operations from other software. A research application might use an API to retrieve records. Available operations depend on the service and granted access.

**Integration** — a connection that lets systems exchange information or perform operations together. Connecting a document service is an integration; its access permissions determine which documents the research application can read.

## Research and evidence

**Claim** — a statement that may be true or false and requires appropriate support.

Example: “This switch can power all eight proposed cameras.”

**Evidence** — information relevant to evaluating a claim.

Example: the specified power budget and the cameras' maximum power requirements.

**Source** — where information or evidence originated.

Example: a manufacturer's manual for the exact equipment model.

**Argument** — the reasoning that connects evidence to a claim.

Example: compare the combined camera requirement with the switch's stated power budget.

**Assumption** — something the reasoning depends on but has not independently established.

Example: assuming that a manual matches the hardware revision being installed.

**Provenance** — information needed to identify where material came from and what version was used.

Record the document identity, version or date, and relevant location within it.

**Falsification** — a serious attempt to identify observations or evidence that would show a claim or interpretation is wrong.

Ask what would disprove the proposed conclusion, then look for it.

**Candidate interpretation** — a possible explanation of evidence that has not become an accepted decision.

Keep alternative explanations visible while assessing their support. Acceptance of an action does not make an interpretation true.

**Recommendation** — proposed action based on evidence plus goals, constraints, values, costs, and risk.

Example: propose equipment with sufficient documented capacity for the planned installation.

**Accepted decision** — a choice explicitly made by the responsible authority.

Record who chose what and when. An AI recommendation alone does not establish acceptance.

**Citation laundering** — repeating a claim through derivative sources without checking whether the original source supports it.

Trace repeated claims back to their origin; ten copies may still share one unsupported statement.

**Independent corroboration** — support from a separate evidence origin. Three assistants repeating the same specification do not provide three independent measurements. Identify where each answer's evidence actually originated.

## Files and records used in research

**Research brief** — a concise description of the question, purpose, scope, constraints, and expected result. It tells a person or assistant what the investigation should accomplish.

**Source register** — the record of sources considered or used. Include enough identifying information to locate the exact material again, plus its relevance and access status.

**Evidence ledger** — a structured record of what source material establishes and where it appears. Keep a quotation or observation separate from your interpretation of it.

**Claims ledger** — a record connecting claims to supporting or challenging evidence and their current status. It helps a reviewer see which conclusions still need work.

**Rigor profile** — the chosen level of research care, evidence, and review. Select it according to the question and consequences of error. A longer report is not automatically more rigorous.

**Audit** — a structured check of the research record against its requirements. Example: verify that citations support the associated claims and that unresolved contradictions remain visible. Passing a checklist cannot guarantee truth.

**Handoff** — a record that lets someone resume work. Include the current question, completed work, relevant files, unresolved issues, decisions, and exact next action. A handoff is useful even when resuming your own project.

**Traceability** — the ability to follow a conclusion back through its evidence and process. Preserve relevant sources, prompts, tool results, versions, and decisions. This supports inspection; it does not guarantee identical AI wording on a rerun.

## Repository and template vocabulary

**Repository** — a collection of project files managed together, usually with a history of changes. A GitHub repository is one way to store and share this kit.

**Git and GitHub** — Git is software that records file changes over time. GitHub is a service for hosting Git repositories and collaborating on their contents. They are separate parts of the workflow.

**Markdown** — a plain-text format for headings, lists, links, and other document structure. Files commonly end in `.md`. You can read or edit them with a text editor.

**Template** — a reusable starting structure that you copy and fill in for your own work. Empty headings and instructions are prompts to complete, not finished research.

**Topic-specific Research Kit** — an adaptation of the general template for a subject, with appropriate questions, terminology, source criteria, and methods. The name does not imply that its preparation is automated.

**Research project** — an actual investigation using the chosen structure. Its sources, evidence, claims, uncertainties, and conclusions belong to that investigation rather than to the reusable blank template.

**Version** — an identifier for a particular state of the project or document. Record versions when they matter to interpreting evidence or following instructions.

**Release** — a published, identified version of a project, sometimes accompanied by downloadable files. A version mentioned in prose does not by itself establish that a matching download exists.

**Branch** — a separate line of changes in a Git repository. A draft branch can hold proposed edits while they are reviewed. Its contents may differ from the default branch.

## Further reading

These introductions provide background for the AI terminology above. The research-record definitions describe how this kit uses those terms.

- [Google Machine Learning Crash Course: Large language models](https://developers.google.com/machine-learning/crash-course/llm)
- [Google Cloud: Retrieval-augmented generation](https://cloud.google.com/use-cases/retrieval-augmented-generation)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
