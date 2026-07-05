# Workspace Rules: AI Agent Trigger Mappings

This file defines the interactive behavioral rules for AI coding agents (Antigravity, Claude Code, Cursor, or Codex) operating in this workspace.

---

## 1. Verbal Prompt Interception

If the user types any of the following verbal triggers in the chat interface, you must immediately execute the corresponding shell commands on their behalf. Do not ask for further confirmation—simply identify the required arguments, run the command using your terminal tool, and present the structured result.

### 1.1 Trigger: Onboarding a Student
*   **Prompt Patterns**: `onboard student [Name]`, `start onboarding for [Name]`, `/onboard [Name]`
*   **Action**: 
    1. Check if the Master Sheet is available or ask the user for details: Research Question, Problem Statement, Degree Level (BSc/MSc/PhD), and Duration (months).
    2. Execute:
       ```bash
       python irc_agent.py --action generate-baseline --student "[Name]" --question "[Question]" --problem "[Problem]" --degree-level "[Level]" --duration-months [Duration]
       ```
    3. Display the generated baseline report.

### 1.2 Trigger: Running Student Audits
*   **Prompt Patterns**: `audit report for [Name]`, `check updates for [Name]`, `/audit [Name]`
*   **Action**:
    1. Locate the student's report and baseline text files (typically in `docs/temp/` or their Drive paths).
    2. Retrieve the sponsor's problem statement.
    3. Execute:
       ```bash
       python irc_agent.py --action audit-doc --student "[Name]" --student-report-file "[Report Path]" --baseline-report-file "[Baseline Path]" --degree-level "[Level]" --duration-months [Duration] --sponsor-problem "[Sponsor Problem]"
       ```
    4. Print the compiled audit output.

### 1.3 Trigger: Checking Sponsor Alignment
*   **Prompt Patterns**: `check alignment for [Name]`, `verify sponsor alignment for [Name]`
*   **Action**:
    1. Locate the student's report path and the sponsor's problem statement.
    2. Execute:
       ```bash
       python irc_agent.py --action check-alignment --student-report-file "[Report Path]" --sponsor-problem "[Problem Statement]"
       ```
    3. Print the Sponsor Alignment Index and critique.

### 1.4 Trigger: Compiling Weekly Digest
*   **Prompt Patterns**: `generate weekly digest`, `compile director report`, `/weekly-digest`
*   **Action**:
    1. Locate the weekly metrics snapshot file (defaults to `docs/temp/weekly_metrics.json` or query the Airtable log).
    2. Execute:
       ```bash
       python irc_agent.py --action compile-weekly-digest --weekly-metrics-file "[Metrics Path]"
       ```
    3. Print the Weekly Director Digest.

### 1.5 Trigger: Verifying Setup & Diagnostics
*   **Prompt Patterns**: `verify setup`, `run setup checks`, `/diagnose`
*   **Action**:
    1. Execute:
       ```bash
       python setup_workspace.py
       ```

### 1.6 Trigger: Master Morning Sync (Do Everything)
*   **Prompt Patterns**: `run morning checks`, `do everything`, `morning sync`, `check cohort updates`, `/morning-sync`
*   **Action**:
    1. Start the n8n background task if not running.
    2. Check the active student profiles registered in `docs/temp/` or query local logs.
    3. Run `python irc_agent.py --action audit-doc` for each student found to update metrics, check alignment, extract feedback, and update cheat sheets.
    4. Compile the overall logs and render an "Executive Cohort Dashboard" summarizing each student's current phase, delays, academic scores, and warning status.

---


## 2. Path Environment Guard
Whenever you execute any Python agent scripts:
*   **Rule**: You must set or prepend the environment variable `PYTHONPATH` to the absolute path of this workspace root (e.g. `env:PYTHONPATH="f:/Antigravity/IRC Workflow"`). This guarantees that import resolutions for `agents.*` succeed without throwing a `ModuleNotFoundError`.
