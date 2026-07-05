# ELI5 + Accountability Questions — Method

This closing section turns the technical audit into something a program manager can actually use in a conversation with the technical staff who own the work. It is not a dumbed-down repeat of the analysis — it's a different artifact with a different job: giving the PM leverage in a real conversation.

## 1. Apply the 80/20 principle
Look across every gap surfaced in the Scientific Rigor Audit, Conceptual Model, Lit Review, and Coherence sections. Identify the one gap (rarely more than two) that:
- most of the other gaps are symptoms or downstream consequences of, or
- would most change the study's credibility/usefulness if fixed.

State this explicitly and rank it above everything else — don't present a flat list of equally-weighted issues. A PM with limited time and technical depth needs to know where to spend their one hard conversation.

Example judgment call: if a study has no ground-truth validation AND has arbitrary thresholds AND has an inconsistent index choice, the validation gap is usually the 80% issue — the thresholds and index choice are only knowable to be a problem *because* there's no validation step to check them against. Fixing validation would surface (and likely help fix) the others; fixing the others without validation wouldn't fix the core problem.

## 2. Apply first principles
In 1-2 plain sentences, state what the study is fundamentally trying to establish, with all method-specific jargon stripped out. Ask: if you removed every technical term (NDVI, hexagon, CV, regression), what is the actual real-world question being answered? This framing should be recognizable to someone with zero domain background.

## 3. Write the ELI5 explanation
- Short sentences. No jargon without immediately explaining it in one clause.
- Use one concrete, everyday analogy per major gap — something physical and familiar (a thermometer never checked against a known temperature, a lock tested only by looking at it rather than trying a key, a recipe scaled up without ever tasting it).
- Explain *why* the gap matters in terms of real-world consequence (what wrong conclusion could result), not just "this violates validity."
- Keep secondary gaps brief — one or two sentences each — so the top gap gets the weight it deserves.

## 4. Generate accountability questions
Group by gap, most important gap first. For each question:
- **Plain-language, PM-askable**: the PM should be able to ask it without needing to understand the underlying method themselves.
- **Answerable by the technical owner in plain terms**: if a technical person can't explain their answer without deflecting into jargon, that itself is diagnostic — note this framing for the PM ("if the answer isn't clear and concrete, that's worth flagging").
- **Specific enough to catch a non-answer**: avoid questions that can be answered with a vague "yes, we considered that." Prefer questions that require a concrete artifact or number in response (e.g. "how many known-source fields did we validate against, and what was the accuracy?" rather than "did we validate this?").
- **Owner-appropriate**: these questions are for whoever is technically accountable for that piece of the work — usually the report's lead researcher/analyst, but note if a question should go to a specific specialist (e.g. GIS lead vs. field data lead) if the report makes that division of labor visible.

## Output shape
1. 80/20 framing (1-2 sentences naming the priority gap)
2. First-principles restatement (1-2 sentences)
3. ELI5 explanation (short paragraphs, one analogy per major gap, weighted toward the top gap)
4. Grouped, ranked accountability question list
