# Conceptual Model Review

## What to extract from the report
1. **Theoretical constructs** — the abstract ideas being invoked (e.g. "financial autonomy", "civic participation", "institutional trust", "hydrological connectivity"). List them explicitly even if the report doesn't.
2. **Variables** — for each construct, what is the operationalized variable(s)? Classify each as:
   - **Independent variable (IV)**: what's manipulated or presumed to drive change
   - **Dependent variable (DV)**: the outcome of interest
   - **Mediating variable**: sits on the causal path between IV and DV, explaining *how/why* the effect occurs
   - **Moderating variable**: changes the *strength or direction* of the IV→DV relationship without being on the causal path
   - **Control variable**: held constant/accounted for to rule out confounding
3. **Hypothesized relationships** — draw them out explicitly, even as simple text arrows: `IV → DV`, `IV → M → DV`, `IV × Moderator → DV`. If the report doesn't specify a mechanism (just "X leads to Y"), flag that mediation is asserted, not modeled.

## Common gaps to check for
- **No explicit conceptual model at all** — relationships are implied in prose but never diagrammed or listed. This is a common and significant gap; flag it directly, and note that program teams should require an explicit conceptual model diagram before fieldwork.
- **Missing moderators/mediators** — a report that only claims direct IV→DV effects should be checked against the literature it cites: does that literature actually support a direct effect, or does it suggest the real mechanism runs through a mediator the report hasn't modeled?
- **Uncontrolled confounders** — variables correlated with both IV and DV that aren't accounted for (e.g. baseline wealth affecting both program participation and the outcome).
- **Construct-variable mismatch** — the named construct is broader/narrower than what's actually measured (see Validity in scientific_tenets.md).
- **Directionality assumed, not tested** — especially in cross-sectional/qualitative designs, check whether reverse causality or bidirectionality is acknowledged (e.g. does financial autonomy drive civic participation, or does prior civic engagement select women into the fee-for-service program in the first place?).

## Justification check
For every construct and relationship in the model, ask: **is this grounded in cited theory/literature, or asserted?**
- Grounded: the report cites a specific theoretical framework or empirical study that predicts this relationship, and explains why it applies to this context.
- Asserted: the relationship is stated as if self-evident, with no theoretical anchor.
Flag every asserted (ungrounded) link in the model — these are the primary target for "why is this the right way to model this?" pushback in a peer review.

## Output format for this section
Prefer a simple structured list or ASCII-style relationship map, e.g.:

```
IV: Access to fee-for-service ASP training
 → mediates through: Perceived financial autonomy (M)
 → DV: Participation in Water User Cooperative Societies
 → moderated by: Household bargaining position (Mod) [not addressed in report — gap]
 → controls needed: prior civic engagement, land ownership, caste/community [partially addressed]
```
