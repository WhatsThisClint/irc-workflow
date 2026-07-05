# IRC Agent Trigger Board

This document maps simple verbal triggers you can type in your AI agent's chat interface (such as Antigravity, Claude Code, or Cursor) to the automatic execution of the workflow scripts.

---

## 🗺️ Verbal Trigger Mappings

When you resume your session, simply copy-paste or type one of the following prompts into your agent's chat:

| Goal / Action | Type this in Agent Chat (Verbal Triggers) | What the Agent Will Do |
|---|---|---|
| **Master Morning Sync (Do Everything)** | `run morning checks`, `do everything`, or `morning sync` | Checks all student statuses, detects new students, updates phases, and runs all academic/sponsor audits to output an executive cohort dashboard |
| **Onboard a New Student** | `onboard student [Name]` or `/onboard [Name]` | Prompts for research details and executes `generate-baseline` |
| **Scan Student Progress** | `run daily monitor` or `check student updates` | Runs Gantt calculations and document audits for all active students |
| **Audit a Student Report** | `audit report for [Name]` or `/audit [Name]` | Locates the student's report and baseline to execute `audit-doc` |
| **Parse a Meeting Transcript** | `parse transcript [File]` or `/transcript [File]` | Reads the meeting notes and syncs extracted tasks to Asana |
| **Check Sponsor Alignment** | `check alignment for [Name]` | Compares student research directly against their sponsor's problem statement |
| **Compile Weekly Report** | `generate weekly digest` or `/weekly-digest` | Queries Airtable metrics logs and compiles the Weekly Director Digest |
| **Run Diagnostic Checks** | `verify setup` or `/diagnose` | Executes the workspace environment and n8n verification checks |


---

## ⚡ Examples of Interactions

### Example 1: Onboarding
*   **You**: `onboard student Priya Sen`
*   **Agent**: *"Priya Sen detected. Let me pull her details from the Master Sheet to generate the expert baseline report..."* (Agent runs `onboarding_agent.py`)

### Example 2: Daily Check
*   **You**: `check student updates`
*   **Agent**: *"I will scan the Google Sheets and check document revisions. Starting the document audits..."* (Agent runs the daily monitor commands)
