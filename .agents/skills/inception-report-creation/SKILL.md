---
name: inception-report-creation
description: Use whenever the user gives a research question, topic, or assignment title (e.g. from an IRC/WISER-style client-question table) and wants a full inception report drafted from it — for research fellows, program associates, or similar training programs at WELL Labs. Trigger on "create an inception report", "draft an inception report for this question", "write up this assignment", "generate an inception report for [research question]", or any request to turn a bare research question + client/theme into a structured project write-up. Builds the report by identifying the discipline and conceptual model (same method as inception-report-review), then an argument-mode literature framing, a concrete study design, a month-by-month work plan, and a draft data-collection instrument — closing with a plain-language summary and ELI5/80-20 framing. Use together with inception-report-review's rigor standards so the generated report would survive that same audit.
---

# Inception Report Creation

Generates a full inception report from a bare research question — the inverse of `inception-report-review`. Same underlying principles (discipline identification, conceptual model rigor, argument-mode literature review), applied to construct a report that would pass that review, not critique one that already exists.

## Input

The user will typically give some subset of:
- A research question or topic (required — ask if missing)
- Client / commissioning body (e.g. ACIWRM)
- Application (what the study feeds into)
- Theme (e.g. Institutions & Governance, Agricultural Systems & Water Productivity)
- Project site, duration, or team size (optional)

If client, site, or duration are missing, don't block on them — make a reasonable assumption grounded in the question and WELL Labs' typical portfolio (Karnataka/watershed program geographies, 6–8 month inception-to-fieldwork window), state the assumption explicitly at the top of the output, and proceed. Only ask a clarifying question if the research question itself is too vague to identify a discipline or unit of analysis (e.g. "study water in Karnataka" — ask what phenomenon or outcome it's about).

## Workflow

### Step 1: Identify the discipline and unit of analysis
Load `references/discipline_identification.md`. From the question's phenomenon, implied variables, and likely data sources, name the discipline(s) this report will be built under (e.g. "institutional economics of collective action", "agricultural remote sensing / hydrology"). This choice governs every later step — the conceptual model, the kind of literature cited, and the study design all follow from it.

### Step 2: Build the conceptual model
Load `references/conceptual_model_construction.md`. Turn the bare question into an explicit IV/DV/mediator/moderator/control structure with a stated hypothesized relationship — never leave this implicit the way a first-draft researcher would.

### Step 3: Construct the literature framing
Load `references/lit_review_construction.md`. Build an argument-mode framing (not a summary list): identify the dominant existing framework(s) for this question, state a specific gap this study fills, and name real, well-known anchor papers/frameworks where you can — never fabricate a citation or attribute false specifics; if unsure a source is real, describe the type of source needed instead of inventing one.

### Step 4: Design the study
Load `references/study_design_construction.md`. Produce a concrete study design: sampling frame and size with reasoning, identification/recruitment method, respondent or data-source list tied to the conceptual model's variables, and (for biophysical/remote-sensing questions) the data sources and validation approach instead of a respondent list.

### Step 5: Build the work plan
Load `references/work_plan_construction.md`. Produce a month-by-month activity/milestone table sized to the stated or assumed project duration.

### Step 6: Draft the data-collection instrument
Load `references/instrument_drafting.md`. Draft a short annex instrument (survey/interview guide, or data-extraction protocol for quantitative/remote-sensing work) with items that map directly to the conceptual model's variables — every question or extracted variable should trace back to something named in Step 2.

### Step 7: Assemble the report
Load `references/report_template.md` for section order and headers — this is WELL Labs' actual inception report format, not the academic review template. Fill every header; don't leave placeholder text.

### Step 8: Close with plain-language framing
Load `references/eli5_8020_framing.md`. Before or after the full report (see Output order below), give:
1. A first-principles, jargon-free restatement of what the study is actually trying to find out.
2. The 80/20 call: which single design choice (conceptual model link, sampling logic, or data source) is most load-bearing for the whole study's credibility — the one thing worth getting right above all else.

## Output order
1. **Plain-language summary** (2-4 sentences, no jargon) — what this study is trying to find out and why, in the terms a non-technical stakeholder would use.
2. **ELI5 + 80/20 framing** — the first-principles restatement and the single highest-leverage design choice, per Step 8.
3. **Full inception report**, structured per `references/report_template.md`.

Output in chat only — no file unless the user asks for one. Keep the full report scannable: short paragraphs, bullet lists for study design and work plan, a real markdown table for the work plan's month-by-activity grid.

## Consistency check before finalizing
Before presenting, re-read your own draft and check: does the study design in Step 4 actually test the relationship named in Step 2? Does the instrument in Step 6 actually collect the variables named in Step 2? Does the literature framing in Step 3 actually justify the specific method chosen in Step 4 (not just the topic)? A report that's internally inconsistent across these steps is exactly what `inception-report-review` would flag first — fix it before showing the user.
