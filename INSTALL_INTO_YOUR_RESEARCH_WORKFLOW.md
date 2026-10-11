# Install into your research workflow

The kit's core consists of ordinary text documents, prompts, and checklists. You can use them with an AI assistant or follow the method yourself. You do not need to write code to fill in the research records.

AI applications differ in their support for file uploads, project instructions, search, file editing, and automated actions. This guide describes the files to provide and the result to check. Use your application's current instructions for its controls.

## 1. Obtain the right version

Current v0.2.0+ distributions are proprietary. Read [LICENSE](LICENSE) and use the repository revision or package covered by your written authorization.

The [v0.1.0 GitHub Release](https://github.com/GannoK/GTS-AI-Research-System-Template/releases/tag/v0.1.0) contains historical public-preview archives. A filename ending in `v0.1.0.zip` identifies that earlier distribution. It is not a download of the current v0.2.1 version. Historical licensing is explained in [LICENSE_HISTORY.md](LICENSE_HISTORY.md).

For an authorized current project:

1. Obtain the approved repository snapshot or package.
2. Extract it if it is an archive.
3. Keep the original kit available as your reference copy.
4. Record the release label and, where available, the commit ID supplied with that copy.

A **commit ID** identifies a particular saved repository revision. Record the actual ID you used; a branch name such as `main` can point to a different revision later.

If you have not obtained authorization for the current distribution, contact the repository owner through the project's listed GitHub profile or your existing GTS contact. Repository visibility alone does not identify which distribution you are authorized to use.

## 2. Create a workspace for one question

Create a folder for the research project. Give it a name that identifies the question, such as `camera-power-research`.

A simple layout is:

| Folder | Purpose |
|---|---|
| `camera-power-research/knowledge/` | Your completed project records. Copy the contents of `02_RESEARCH_KNOWLEDGE_TEMPLATE/` here. |
| `camera-power-research/sources/` | Source material you are permitted to retain, or notes identifying material held elsewhere. |
| `camera-power-research/reports/` | Written summaries and handoffs produced from the research records. |

Create these as ordinary folders. The kit does not create them automatically.

Keep the names of the copied research files so the index can still identify them. Open `knowledge/00_INDEX_AND_ROUTING.md` first. Leave the reusable template in your reference copy available for future projects.

Paths beginning with `03_PROMPTS/`, `07_TEMPLATES/`, or `08_CHECKLISTS/` refer to your reference copy of the kit. Research-record filenames such as `120_CURRENT_STATE.md` refer to the files in your project's `knowledge/` folder.

Keep private source files out of public repositories. The project records should identify where authorized reviewers can find restricted material without exposing it.

## 3. Define the first task

Read [OPEN_THIS_FIRST.md](OPEN_THIS_FIRST.md), then follow the [quick start](00_QUICK_START/QUICK_START_ONE_PAGE.md).

Complete the question, scope, method/profile, and source criteria before broad searching. The [worked example](09_EXAMPLES/01_FIRST_RESEARCH_PROJECT.md) shows what completed fields look like.

In `120_CURRENT_STATE.md`, also record the kit version or revision used, your working environment, and any important access limits. These notes help another person resume the work.

## 4. Choose how to work

### With an AI assistant

1. Provide `03_PROMPTS/00_GLOBAL_RESEARCH_RULES.txt` as project guidance when your application supports it. Otherwise include those rules when starting the research task.
2. Provide your research index and the completed question, scope, method/profile, and source criteria.
3. Use `03_PROMPTS/01_START_A_RESEARCH_PROJECT.txt` to begin the first stage.
4. Ask the assistant which files it could read and what remains unavailable. Check its answer against your supplied material.
5. Provide the relevant source documents or use available search tools for the next stage.
6. If the assistant can edit your project files, inspect the saved result. If it cannot, copy its proposed entries into the corresponding documents yourself.

Uploading files is not proof that the assistant used all of them. For an important claim, require the source identity and the specific passage or location that supports it.

Use the individual prompts in `03_PROMPTS/` for later stages. Retrieve or supply the smallest relevant material needed for the current task.

### Without AI

Follow the same research index, fill in the same records, and apply the checklists yourself. The prompts can serve as reminders of the questions to ask at each stage.

### With an existing agent or RAG system

Provide the same research rules, index, and stage documents through the capabilities that system actually supports.

RAG retrieves information for an answer. An agent may select and carry out steps. Neither term establishes that a file was read correctly, that a conclusion was verified, or that an action was authorized.

Treat source documents as data. Instructions embedded in a webpage, document, or comment do not override the research task or operator authority.

## 5. Check, pause, and resume

Before treating the result as complete, use `08_CHECKLISTS/04_FINAL_RESEARCH_AUDIT.md`.

To pause, update `120_CURRENT_STATE.md` and prepare a handoff using `07_TEMPLATES/09_RESEARCH_HANDOFF_TEMPLATE.md`. Record the question, relevant evidence, claims, uncertainty, any accepted decisions, blockers, and the exact next step.

To resume, read that state and the project index, then load the records needed for the next step. Recheck sources when their age, version, or changed circumstances could affect the conclusion.

## Common questions

**Does this include an AI model or a hosted research service?**

The kit provides research documents, prompts, templates, and checks. Access to a model, an AI application, search, and execution tools comes from the environment you choose.

**Does installing the files start an automated investigation?**

Copying the files creates a research workspace. An automated run requires a separately configured system that can execute the steps with the necessary access and authorization.

**What will it cost?**

AI subscriptions, API calls, hosted tools, and local computing may have their own costs. Check your provider's current terms. Define the question and a time or usage budget, reuse recorded evidence, and expand the investigation when a material gap justifies it.

**What if a source cannot be opened?**

Record the access limit. Do not claim to have checked the source or use a generated quotation as a replacement. Seek an accessible original, another suitable source, or an explicitly qualified conclusion.

**What if sources disagree?**

Preserve both evidence paths and record the conflict. Check definitions, dates, scope, and methods before deciding whether the sources address the same claim. See [When sources disagree](01_BEGINNER_GUIDE/05_WHEN_SOURCES_DISAGREE.md).

**Can a local model keep everything private?**

Local inference means model computation happens on a machine you control. Other components may still use cloud storage, search, telemetry, or external services. Check the full workflow before using restricted material.

**Where should I look up an unfamiliar term?**

Use the [glossary](10_REFERENCE/01_GLOSSARY.md), then return to the [quick start](00_QUICK_START/QUICK_START_ONE_PAGE.md).

## For derivative creators

Use the [derivative contract](DERIVATIVE_CONTRACT.md) when preparing a reusable domain template. An ordinary project can continue to use the workspace instructions above.

Keep the checked-out parent unchanged. Write derivative manifests and resolution outputs in a separate derivative workspace outside the parent checkout; `--output` paths inside the parent are rejected.

1. Choose a released, qualified parent and check out that exact revision. The parent version, existing release tag, commit, repository-manifest hash, and component-registry hash must agree.
2. Record the parent in a [derivative mutation manifest](07_TEMPLATES/13_DERIVATIVE_MUTATION_MANIFEST_TEMPLATE.json). A manifest lists the deliberate changes to inherited components.
3. Declare the domain-specific changes and the evidence that the parent research principles still hold. Generic domain placeholders left unspecified remain unresolved draft work.
4. Resolve the component dispositions and complete the applicable [qualification controls](assurance/CONTROL_DOMAINS.md). Passing an integrity check or creating a manifest does not qualify a derivative.
5. Record the responsible review disposition and track parent compatibility separately from whether the derivative has adopted newer parent changes.

This unreleased hardening candidate cannot currently serve as a qualified released parent. Planning the next version as v0.3.0 does not create its tag, publish it, or qualify any derivative.

## Maintainer validation setup

Maintainers running the repository tools need **Python 3.11 or later** and the dependencies in [requirements-dev.txt](requirements-dev.txt). This setup is for checking or developing the template; filling in the ordinary research records requires no Python installation.

Open a terminal in the repository's top-level folder, where `README.md` and `requirements-dev.txt` are located. Use the Python environment in which you intend to run the checks:

```bash
python --version
python -m pip install -r requirements-dev.txt
python tools/verify_repository.py
python -m unittest discover -s tests -v
```

The first command must report Python 3.11 or later. Installing with `python -m pip` puts the declared dependencies into that Python environment. The repository uses the standard `jsonschema` validator pinned in the requirements file; missing validation dependencies must be reported rather than silently skipping checks.

For an authorized qualification review, use the [hardening acceptance criteria](HARDENING/AIRST-HARDENING-001-ACCEPTANCE.json) and the [qualification domains](assurance/CONTROL_DOMAINS.md). Record unresolved or manual controls explicitly. A successful automated check is not a release decision.

Generate a candidate evidence record with:

```bash
python tools/generate_qualification_bundle.py --output dist/airst-qualification-bundle.json
```

That command records the required and acceptance controls. Missing real-system results remain `UNKNOWN`, and judgments requiring human review remain `MANUAL`. The fixture self-tests check the evaluation harness; they do not demonstrate the behavior of an actual research system.

If you have retained results from an actual system, supply their directory with `--results-dir PATH` to the bundle command, or run `python tools/run_methodology_evals.py --results-dir PATH --json` directly. Replace `PATH` with that directory. Each `AR-xxx.json` record identifies the evaluation, system, run, result fields, and SHA-256 references to retained evidence files inside the same directory. Missing, malformed, or mismatched evidence must remain visible in the result. Matching records and assertions provide traceability; the applicable semantic review still requires human evidence.

[Back to README](README.md)
