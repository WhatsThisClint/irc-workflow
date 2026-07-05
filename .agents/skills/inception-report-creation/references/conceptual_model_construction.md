# Conceptual Model Construction

Turn the bare research question into an explicit model — never leave it as a one-line question. This is the single most common gap `inception-report-review` flags in real reports, so build it in from the start.

## Step 1: Extract or assign the core constructs
Name the abstract ideas the question is really about, even if the question doesn't use these words. E.g. "why do farmers in Maharashtra pay a cess but Karnataka's don't" is really about *institutional design of cost-recovery mechanisms* and *compliance/willingness to pay*, not just "cess."

## Step 2: Classify variables
- **Independent variable (IV)**: the presumed driver (e.g. state-level institutional/legal design of cess collection).
- **Dependent variable (DV)**: the outcome of interest (e.g. cess payment/compliance rate, or WUC management quality).
- **Mediating variable**: the mechanism connecting IV to DV (e.g. perceived legitimacy of the WUC, transparency of fund use).
- **Moderating variable**: what changes the strength of the IV→DV link without being on the causal path (e.g. crop type/irrigation dependency, distance from head-reach).
- **Control variable**: what must be held constant or accounted for (e.g. farm size, canal command position, pre-existing local governance capacity).

For biophysical/remote-sensing questions, the same structure still applies but the "variables" are measured/derived quantities: e.g. IV = irrigation source (canal vs. well), DV = crop water status (NDVI signature), controls = crop type, sowing date, soil type.

## Step 3: State the hypothesized relationship explicitly
Write it as a simple text relationship map, not prose:
```
IV: Government funding modality for WUCs (direct vs. cess-dependent)
 → mediated by: Financial autonomy / discretionary budget control (M)
 → DV: WUC management quality (infrastructure maintenance, meeting regularity, fund utilization)
 → moderated by: Years since WUC formation, canal command position (Mod)
 → controls: WUC size, crop mix, prior institutional capacity
```

## Step 4: Ground every link in theory or name it as an assumption
For each arrow in the model, either cite a real theoretical tradition/study that predicts it (this becomes input to Step 3 of the main workflow — the lit review) or explicitly label it as a working assumption to be tested, not asserted as fact. A generated report should never present an ungrounded link as if it were established.

## Step 5: Watch for the common failure modes proactively
Since this report is being built rather than audited, deliberately avoid the gaps `inception-report-review` looks for:
- Don't assert only a direct IV→DV effect if the likely literature suggests mediation — model the mediator explicitly.
- Don't ignore plausible confounders (e.g. wealthier WUCs may both receive direct funding *and* have better pre-existing management capacity — flag this as a control/identification concern in Step 4 of the main workflow, not just a limitation footnote).
- Don't assume directionality without considering reverse causality (e.g. well-managed WUCs may be selected for direct funding, rather than funding causing good management) — name this explicitly and note how the study design (Step 4) will address or at least acknowledge it.
