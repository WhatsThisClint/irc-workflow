---
name: inception-report-review
description: Use whenever the user asks to (a) recommend which discipline/methodology fits a research question before an inception report is written, or (b) review/audit a completed research inception report, proposal, or research design document — for research fellows, program associates, or similar training programs (e.g. IRC, WISER). Trigger on "review this inception report", "which discipline fits this", "critique the conceptual model", "check the methodology", "is this peer-review ready", or any upload with literature review/conceptual framework/methodology sections. Applies a scientific-rigor audit (objectivity, validity, reliability, transparency, replicability), a conceptual-model check (IV/DV/mediator/moderator/control, theoretical justification), a lit-review critique (argument vs. summary), a discipline-appropriate lens (social science vs. natural science/hydrology), and closes with an ELI5/80-20 summary plus accountability questions for the technical owner.
---

# Inception Report Review

A two-mode skill for programs that train researchers (e.g. WELL Labs' IRC program): first helping pick the right disciplinary lens for a research question, then rigorously auditing the inception report once written.

## Mode Selection

Read the user's request and any attached files first, then pick a mode:

- **Mode A — Discipline/Methodology Recommendation**: user has a research question/topic but no report yet, and wants to know which discipline, theoretical tradition, or methodological family fits.
- **Mode B — Inception Report Review**: a report/document already exists (uploaded or pasted) with sections resembling a literature review, conceptual framework, and/or methodology.
- Both may apply in one conversation (recommend first, review later) — treat them as sequential, not mutually exclusive.

If a file is referenced but not visible in context, check `/mnt/user-data/uploads` before proceeding — don't assume it's missing.

---

## Mode A: Discipline / Methodology Recommendation

Given a research question or topic:

1. Identify the core phenomenon being studied (behavioral, institutional, biophysical, socio-technical, etc.) and name the 2-4 disciplines that plausibly claim it (e.g. institutional economics vs. political ecology vs. hydrology vs. behavioral science).
2. For each candidate discipline, state: its core theoretical lens, the kind of variables/data it would foreground, its typical methods, and a 1-line tradeoff (what it illuminates vs. what it misses).
3. Recommend one primary discipline (or a stated hybrid) with an explicit justification tied to the research question's actual dependent variable/outcome of interest — not just topic-matching.
4. Name which discipline(s) will govern the eventual report review and, per `references/disciplinary_lenses.md`'s method, what that discipline's characteristic rigor standards and reviewer concerns look like — so the researcher knows what standard they'll be held to later. Don't limit this to a preset pair of lenses; derive it from the recommended discipline itself.
5. Suggest 2-4 anchor papers or frameworks per recommended discipline if you can identify well-known, real ones — never fabricate citations.

Keep this mode concise — it's a scoping conversation, not the full audit.

---

## Mode B: Inception Report Review

This is the core, detailed mode. Load `references/scientific_tenets.md`, `references/conceptual_model_review.md`, and `references/lit_review_critique.md` before writing the review — they contain the specific diagnostic questions to apply. Load `references/disciplinary_lenses.md` for the *method* of identifying and constructing a disciplinary lens — it is not a fixed menu to pick from. The report's actual discipline(s) must be identified from its content each time (see Step 2, point 5) — never default to a pre-set pair of lenses.

### Step 1: Read the whole report first
Don't critique section-by-section in isolation. Read fully, then assess cross-section coherence — e.g. does the methodology actually answer the question the conceptual model poses; does the lit review's stated gap match the hypotheses tested.

### Step 2: Run the five-part analysis

Produce findings under these headings, in this order:

1. **Scientific Rigor Audit** — assess each tenet from `references/scientific_tenets.md`: Objectivity, Validity, Reliability, Transparency, Replicability. For each: verdict (strong/adequate/weak/absent), the specific evidence in the report supporting that verdict, and what's missing.

2. **Conceptual Model Analysis** — using `references/conceptual_model_review.md`: extract (or note the absence of) the theoretical constructs, and classify variables as independent/dependent/moderating/mediating/control. Map the hypothesized relationships explicitly (even as a simple text diagram, e.g. "IV1 → mediated by M1 → DV1, moderated by Mod1"). Check whether each construct/relationship is justified by cited literature or theory, or is asserted without grounding.

3. **Literature Review as Argument** — using `references/lit_review_critique.md`: determine whether the lit review is summary-mode ("Paper A found X, Paper B found Y...") or argument-mode (using the literature to stake out a position and justify a specific choice). Check for engagement with opposing/competing theoretical frameworks — not just supportive citations. Note whether citations are real, specific, and correctly used (never assume a citation is fabricated without checking, but flag vague/unverifiable ones).

4. **Coherence, Assumptions & Anticipated Critique** — identify: unstated assumptions load-bearing to the argument; hypotheses that could plausibly fail in the field and whether the report acknowledges this; counterfactual explanations for expected findings that aren't ruled out; and the most likely points of critique a peer reviewer or advisor in that discipline would raise (methodological, theoretical, or feasibility-based) — note explicitly whether the report anticipates and addresses these or is silent on them.

5. **Disciplinary Lens Check** — using the method in `references/disciplinary_lenses.md`: first identify, from the report's own content (subject matter, constructs, methods, journals/frameworks it cites), which actual discipline(s) or sub-fields the work belongs to — don't assume it's social science or hydrology by default, and don't force-fit it into a pre-set category. Name the discipline(s) explicitly (e.g. "agricultural remote sensing / hydrological engineering", "institutional economics", "epidemiology", "behavioral development economics"), state why, then construct the reviewer persona and concerns that discipline's own practitioners would actually raise — its characteristic rigor standards, common failure modes, and the theoretical debates active in that field. If the work spans more than one discipline, identify each and flag the integration point between them as its own risk area.

### Step 3: Summarize
Close the main analysis (not the whole output — Step 4 follows this) with:
- **Peer-review readiness verdict**: would this argument, as currently built, survive a peer review or advisor review in its discipline? Be direct, not diplomatic-to-a-fault.
- **What the literature review actually accomplished** and whether it's sufficient for the argument being made.
- **Top 3-5 gaps**, ranked by how load-bearing they are to the overall argument (a weak conceptual model justification is usually more load-bearing than a missing citation).
- **For each gap, a concrete fix**: a specific real paper/framework to read, a design change (e.g. "add a control variable for X"), or a scoping/feasibility tradeoff to make explicit — never just "needs more literature" without naming what kind.

### Step 4: ELI5 + Accountability Questions (always include, after the summary)
This closing section is for the program manager, not the researcher — it's what they'll use in a real conversation with the technical staff responsible for the report's rigor. Load `references/eli5_accountability.md` for the full method. In brief:

1. **80/20 cut**: from all the gaps identified in Steps 2-3, identify the single gap (or at most 2-3) that most other issues are downstream of or symptomatic of — the one that, if fixed, would most change the study's credibility. Say so explicitly ("everything else is secondary to this").
2. **First principles**: restate, in one or two plain sentences, what the study is fundamentally trying to establish — strip away jargon and method-specific terms.
3. **ELI5 explanation**: explain the top gap(s) using short sentences and a concrete everyday analogy (e.g. an uncalibrated thermometer, a lock with no key to test it against) — not a diluted restatement of the technical section, an actually simple one.
4. **Accountability questions**: produce a question list for the technical owner(s) (the researcher/analyst responsible for the report), grouped by gap, ordered by priority (validation/highest-leverage gap first). Each question should be:
   - Answerable in plain terms by someone who actually did the technical work — if they can't answer it plainly, that itself is a signal.
   - Phrased so a non-technical PM can ask it without needing to understand the underlying method.
   - Specific enough that a vague or deflecting answer is easy to spot.

### Output format
Give the full analysis in chat, structured with the headings above (Steps 2-3) followed by the ELI5 + Accountability Questions section (Step 4) — no filler preamble, straight into the findings. Then also produce a Word document version (use the **docx** skill) mirroring the same structure including the closing ELI5 + questions section, saved to `/mnt/user-data/outputs`, for the user to share internally. Use `references/report_template.md` as the section order/template for the docx.

### Tone
This output is a working tool for a program manager coaching researchers, not a rejection letter. Be rigorous and unsparing about the analysis itself, but frame gaps as coachable and specific enough for the PM to sit down with the researcher and work through them.
