# Your first research project: can one switch power eight cameras?

> **Fictional teaching example.** Every product, source, quotation, revision, and equipment specification below was invented for this exercise. These are not verified product documents or installation advice. No purchase, installation, or project decision has been approved.

This example follows all 12 files in the [research project template](../02_RESEARCH_KNOWLEDGE_TEMPLATE/10_RESEARCH_QUESTION.md). Copy each numbered section into its matching file when practicing. Field names match the templates. The short source extracts included here are the complete source material for this exercise.

**PoE** means *Power over Ethernet*: supplying electrical power through an Ethernet network cable. A **watt (W)** measures power. A switch's **combined power budget** is the total power available across the relevant ports; its number of ports is a separate limit.

The lesson is to check whether evidence supports a precise claim, preserve uncertainty, and keep a recommendation separate from an accepted decision.

## 1. Research question

File: [10_RESEARCH_QUESTION.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/10_RESEARCH_QUESTION.md)

**Primary question:** Can the fictional MX-8 switch guarantee power for eight fictional MC-10 cameras operating simultaneously at their stated maximum power requirement?

**Why it matters:** Selecting equipment by port count alone could leave the required operating condition unsupported.

**Decision or output this research may inform:** Whether to retain this proposed switch-and-camera configuration for further investigation.

**What would count as a useful answer:** A traceable power-budget comparison, the assumptions needed to make it, and a clear list of issues that the comparison cannot settle.

## 2. Scope and definitions

File: [20_SCOPE_AND_DEFINITIONS.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/20_SCOPE_AND_DEFINITIONS.md)

**Population/system:** One MX-8 switch and eight identical MC-10 cameras.

**Time period:** Only the fixed fictional document revisions reproduced below; no claim about current products.

**Geography/context:** A hypothetical installation exercise with no jurisdiction or physical site specified.

**Key definitions:** *Simultaneous maximum* means all eight cameras demand their stated maximum at the same time. *Guarantee* here means the documented budget covers that condition under the exercise assumptions; it does not mean an independent performance certification. A *source* is a document examined; *evidence* is the relevant information extracted from it; a *claim* is a statement evaluated using that evidence.

**Included:** Port count, the combined power budget, camera maximum demand, basic arithmetic, and the competing assertions in the supplied material.

**Excluded:** Product selection, prices, actual power measurements, electrical installation, network throughput, startup behavior, standards compatibility, and cable losses.

**Known boundary conditions:** For the arithmetic exercise, assume that 60 W available and 10 W required use comparable power accounting. The documents do not establish that assumption for a real installation. Compatibility, vendor budgeting rules, and losses require separate verification.

## 3. Method and profile

File: [30_METHOD_AND_PROFILE.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/30_METHOD_AND_PROFILE.md)

**Rigor profile:** EVIDENCE-BASED, applied to an illustrative documented comparison. This selection does not certify installation suitability.

**Adopted method/standard:** Structured comparison of the supplied specification statements, with source registration, exact extraction, claim assessment, contradiction recording, and reproducible arithmetic. No engineering standard or certification procedure is claimed.

**Profiled changes:** Use a fixed fictional source set instead of searching for actual equipment documentation. Keep the research stages visible even though the arithmetic is small.

**Extensions:** Include a misleading reseller statement and a copied version to practice assessing source dependence.

**Bespoke elements and justification:** Treat the two power figures as comparable so the lesson isolates the distinction between port count and aggregate power demand.

**Falsification plan:** Check for a revised switch budget, an applicable exception, different maximum camera requirements, or incompatible power accounting. Any of these could change the comparison. Investigate a suggested lower-power operating mode separately; it would change the operating condition rather than disprove the calculation for simultaneous maximum demand.

**Reproducibility plan:** Preserve source IDs, revisions, locations, and extracts below. Recompute eight × 10 W = 80 W; compare with 60 W. Another reader should reach the same conditional conclusion from the same material.

## 4. Source criteria

File: [40_SOURCE_CRITERIA.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/40_SOURCE_CRITERIA.md)

**Preferred source types:** Model-specific manufacturer specifications with explicit numerical limits.

**Minimum recency requirements:** Exact exercise revisions only. In a real project, check that documents apply to the equipment and revision being evaluated.

**Primary-source requirements:** Trace power limits to the fictional manufacturers' documents, rather than accepting a reseller's interpretation as equivalent evidence.

**Inclusion criteria:** The source identifies the relevant model and provides a locatable statement that bears on the question. Keep rejected sources in the register for review.

**Exclusion criteria:** Exclude unsupported assertions and copied assertions from the evidence used to establish equipment capability. Record why they fail; disagreement alone is not an exclusion reason.

**Conflict-of-interest checks:** Manufacturer and reseller documents have commercial interests. Prefer explicit specifications for the narrow specification claim; manufacturer status alone is not proof of measured performance.

**Correction/retraction checks:** No correction notices are included in this invented dataset. No real-world correction search was performed. A real project would check superseding documents and record the result.

## 5. Source register and supplied extracts

File: [50_SOURCE_REGISTER.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/50_SOURCE_REGISTER.md)

**All entries and extracts in this section are fictional.** “Original?” refers only to their assigned relationship within the exercise.

| ID | Source | Type | Date/version | Original? | Status | Notes |
|---|---|---|---|---|---|---|
| SRC-01 | Example Equipment Co., MX-8 manual | Manufacturer specification | Fictional revision 1 | Yes, within exercise | Included | Page 4, §2.1, Power overview. |
| SRC-02 | Example Camera Co., MC-10 data sheet | Manufacturer specification | Fictional revision 2 | Yes, within exercise | Included | Page 1, table 2, Power. |
| SRC-03 | Example Reseller, MX-8 listing | Sales assertion | Fictional snapshot A | Original assertion | Rejected for capability claim | “Camera bundle” paragraph; no measurement, calculation, or applicable exception supplied. |
| SRC-04 | Example Equipment Blog, bundle repost | Repetition | Fictional snapshot B | No; copies SRC-03 | Duplicate; no independent support | “Recommended bundle” paragraph credits SRC-03. |

**SRC-01 — page 4, §2.1:** “MX-8: eight PoE output ports. Total PoE power budget: 60 W.”

**SRC-02 — page 1, table 2:** “MC-10 maximum power requirement per camera: 10 W.”

**SRC-03 — Camera bundle:** “The MX-8 has eight PoE ports, so it can power eight MC-10 cameras simultaneously at their full stated maximum.”

**SRC-04 — Recommended bundle:** “The MX-8 has eight PoE ports, so it can power eight MC-10 cameras simultaneously at their full stated maximum. Source: Example Reseller.”

SRC-03 is rejected as support for capability because it substitutes port count for a power calculation and supplies no evidence overcoming the conflicting figures. SRC-04 repeats that same assertion. Two pages here do not provide two independent findings.

## 6. Evidence ledger

File: [60_EVIDENCE_LEDGER.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/60_EVIDENCE_LEDGER.md)

Evidence direction below is relative to CLM-01 in the next section. Extraction confidence describes whether we copied the supplied text accurately; it does not authenticate fictional documents.

| Field | EVD-01 | EVD-02 | EVD-03 |
|---|---|---|---|
| Evidence ID | EVD-01 | EVD-02 | EVD-03 |
| Source ID | SRC-01 | SRC-02 | SRC-03 |
| Exact proposition/finding | MX-8 has eight PoE output ports and a total 60 W PoE power budget. | MC-10 has a maximum power requirement of 10 W per camera. | Reseller asserts eight ports permit eight MC-10 cameras at simultaneous full stated maximum. |
| Location in source | Page 4, §2.1. | Page 1, table 2. | Camera bundle paragraph. |
| Context/population/conditions | One MX-8; combined budget. | One MC-10; stated maximum, not measured typical use. | Proposed eight-camera bundle at maximum. |
| Method/design | Stated manufacturer specification. | Stated manufacturer specification. | Sales assertion; no calculation or test supplied. |
| Limitations | No budgeting basis, compatibility details, or measurements supplied. | No budgeting basis, power-saving mode, or measurements supplied. | Port-count argument omits combined power demand. |
| Direction: supporting / contradicting / neutral | Supporting. | Supporting. | Contradicting assertion; rejected as reliable capability evidence. |
| Verification status | Checked against the complete fictional extract. | Checked against the complete fictional extract. | Wording verified against extract; capability claim fails comparison. |
| Confidence in extraction | High for the supplied text. | High for the supplied text. | High for what the reseller says; not for its truth. |

SRC-04 adds no independent evidence item because its dependence on SRC-03 is explicit. Its existence and duplicate status remain visible in the source register.

## 7. Claims ledger

File: [70_CLAIMS_LEDGER.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/70_CLAIMS_LEDGER.md)

### CLM-01: simultaneous maximum demand exceeds the budget

**Claim ID:** CLM-01.

**Exact claim wording:** Assuming comparable power accounting, eight MC-10 cameras at their stated simultaneous maximum require 80 W, exceeding the MX-8's stated 60 W combined budget by 20 W. The selected switch therefore cannot guarantee powering all eight at that maximum.

**Supporting evidence IDs:** EVD-01 and EVD-02.

**Contradicting evidence IDs:** EVD-03 records an opposing assertion, rejected for the reasons documented above. SRC-04 repeats it without independent support.

**Argument connecting evidence to claim:** Eight × 10 W = 80 W. Available budget is 60 W. The difference is 80 W − 60 W = 20 W. Eight ports establish connection count; they do not increase the stated combined budget.

**Assumptions:** All eight cameras demand maximum power simultaneously; requirements add; available and required figures use comparable accounting; the documents apply to the proposed models.

**Residual uncertainty:** Real compatibility, accounting basis, losses, operating measurements, and the behavior of any lower-power mode remain unverified.

**Evidence sufficiency: insufficient / provisional / supported / strongly supported:** Supported within the fictional dataset and stated assumptions. This is not real-world product validation.

**Stronger wording that is NOT justified:** “Eight cameras cannot run under any condition,” “the installation is unsafe,” or “this identifies the correct replacement switch.”

### CLM-02: a power-saving mode could make this configuration sufficient

**Claim ID:** CLM-02.

**Exact claim wording:** The proposed eight cameras can meet the installation's needs using an available power-saving mode within the 60 W combined budget.

**Supporting evidence IDs:** None. This is an unproven competing hypothesis introduced for investigation.

**Contradicting evidence IDs:** None directly. EVD-02 specifies maximum demand; it does not establish whether a lower-power mode exists or meets the user's needs.

**Argument connecting evidence to claim:** No supported argument yet. Lower consumption could change the comparison, but possibility does not establish an available, adequate configuration.

**Assumptions:** Such a mode exists, remains within budget under relevant conditions, and preserves required camera functions.

**Residual uncertainty:** Every assumption above requires evidence.

**Evidence sufficiency: insufficient / provisional / supported / strongly supported:** Insufficient.

**Stronger wording that is NOT justified:** “Enable power saving and the problem is solved.”

## 8. Conflicts and uncertainties

File: [80_CONFLICTS_AND_UNCERTAINTIES.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/80_CONFLICTS_AND_UNCERTAINTIES.md)

| ID | Issue | State | Resolution or evidence needed next |
|---|---|---|---|
| UNC-01 | Reseller assertion conflicts with the numerical specification comparison. | Resolved within exercise | Retain the assertion and reject its capability inference using EVD-01, EVD-02, and CLM-01. |
| UNC-02 | Repost might appear to corroborate the reseller. | Resolved within exercise | SRC-04 explicitly derives from SRC-03; record dependence. |
| UNC-03 | Power-saving mode might support a different operating condition. | Open | Model-specific documentation and evidence that required functions and demand limits are satisfied. |
| UNC-04 | Comparable power accounting is assumed. | Open outside exercise | Verify actual vendor power basis and any relevant losses. |
| UNC-05 | Physical installation suitability is unknown. | Outside scope | Verify actual standards compatibility, startup behavior, site requirements, and other installation constraints separately. |

Resolved conflicts remain recorded. An unanswered question stays unanswered until adequate evidence arrives.

## 9. Candidate interpretations

File: [90_CANDIDATE_INTERPRETATIONS.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/90_CANDIDATE_INTERPRETATIONS.md)

**interpretation:** The proposed configuration was assessed by port count without allowing enough combined power for its stated simultaneous maximum.

**supporting claims:** CLM-01.

**competing interpretations:** A different operating condition might be sufficient through the unproven mode in CLM-02. Alternatively, corrected specifications or different accounting could change the comparison.

**assumptions:** The exercise's selected models, maximum-demand condition, and comparable accounting apply.

**falsification conditions:** Applicable specifications establish enough available power for the same condition, or show the compared figures do not describe that condition on a comparable basis.

**confidence:** High in the arithmetic within the exercise; no established confidence in real installation performance.

## 10. Recommendations

File: [100_RECOMMENDATIONS.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/100_RECOMMENDATIONS.md)

**recommendation:** Reconsider the proposed configuration before treating the simultaneous-maximum requirement as satisfied.

**claims relied upon:** CLM-01. CLM-02 remains an investigation option, not a demonstrated solution.

**decision criteria:** Documented support for the required operating condition, compatible equipment, acceptable functionality, and the responsible person's constraints.

**alternatives:** Investigate a different power provision or a documented operating configuration that meets the actual need. No particular replacement is selected.

**risks:** Assuming typical consumption is an assured limit, overlooking losses or compatibility, or sacrificing required functionality to reduce demand.

**uncertainty:** The real installation and available alternatives have not been evaluated.

**what would change the recommendation:** Corrected applicable specifications or verified evidence that an acceptable configuration meets its requirements.

## 11. Accepted decisions

File: [110_ACCEPTED_DECISIONS.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/110_ACCEPTED_DECISIONS.md)

**No accepted decisions.** The following fields remain unfilled because no responsible person has accepted a recommendation. They are shown to prevent the analysis from being mistaken for approval.

| Field | Current entry |
|---|---|
| decision | None recorded. |
| accepted by | Not applicable. |
| date | Not applicable. |
| recommendation considered | Not recorded by a decision authority. |
| evidence/claims considered | Not recorded by a decision authority. |
| rejected alternatives | None recorded as accepted decisions. |
| review trigger | To be recorded if a decision is accepted. |

## 12. Current state

File: [120_CURRENT_STATE.md](../02_RESEARCH_KNOWLEDGE_TEMPLATE/120_CURRENT_STATE.md)

**Research status:** Fictional comparison complete; real equipment research not started.

**Last verified milestone:** Supplied extracts checked, arithmetic reproduced, and conflicting assertions assessed.

**Current strongest conclusion:** CLM-01: 80 W stated simultaneous maximum exceeds 60 W under comparable accounting; the switch cannot guarantee that condition.

**Major unresolved questions:** UNC-03 through UNC-05.

**Next bounded research step:** If pursuing an actual installation, obtain exact model documents and establish compatible, comparable power requirements before evaluating configurations.

**Blocked by:** No actual model selection, site requirements, or real evidence supplied. No block remains for completing this lesson.

## Handoff

The teaching task is complete. Preserve SRC-01 through SRC-04, EVD-01 through EVD-03, both claims, and the unresolved items. Do not convert the recommendation into an accepted decision. A future researcher should replace the fictional dataset with identified real documents and verify the accounting assumptions before carrying the conclusion into an actual equipment assessment.

## Final audit

- The research question and operating condition are explicit.
- Every source and specification is labeled fictional.
- Evidence has source IDs, exact locations, conditions, and limitations.
- CLM-01 includes supporting and opposing material plus reproducible arithmetic.
- Rejected and duplicated assertions remain traceable.
- The lower-power alternative remains unproven; it is not dismissed as impossible.
- Conclusions stay within scope, and no product recommendation or approval is invented.

**Audit result:** Complete as a worked teaching example. No finding about actual equipment suitability is established.

Continue with the [quick start](../00_QUICK_START/QUICK_START_ONE_PAGE.md) or [glossary](../10_REFERENCE/01_GLOSSARY.md).
