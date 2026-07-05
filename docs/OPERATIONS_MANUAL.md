# System Operations & Databases Manual

This document provides setup instructions, database schema layouts, and troubleshooting guidelines for the India Research Corps (IRC) system.

---

## 1. Developer Setup & Portability

### 1.1 Local n8n Portability
All local configurations, custom credentials, variables, and workflows are saved directly inside the workspace under the **`.n8n/`** folder.
*   **Copy-and-Paste Ready**: Copying or git-cloning the workspace folder onto another PC preserves your n8n settings.
*   **Command Execution**: n8n must be launched from the workspace root so it writes database entries to the localized directory:
    ```powershell
    $env:N8N_USER_FOLDER="f:\Antigravity\IRC Workflow\.n8n"; .\node_modules\.bin\n8n start
    ```

### 1.2 Zero-Touch Agent Diagnostics
Incoming AI agents (or developers) can run the setup script to check Node/NPM dependencies and verify script directories:
```bash
python setup_workspace.py
```

---

## 2. Airtable Database Layout

Set up your Airtable Base with the following three tables to log metric histories and feed the dashboard panels:

### Table A: `Students`
Tracks active student status and Drive directory links.
*   **Student** (Single Line Text) - Primary Key: Name of the student.
*   **S.No** (Number): Master sheet serial identifier.
*   **Degree Level** (Single Select): `BSc` / `MSc` / `PhD`.
*   **Current Project Phase** (Single Line Text): Induction, Fieldwork, Thesis, or Completed.
*   **Problem Statement** (Long Text): Sponsoring partner's problem text.
*   **Drive Shared Folder Link** (URL).
*   **Drive Admin Folder Link** (URL).
*   **Reflection Doc Link** (URL).
*   **Status** (Single Select): `Active` / `Graduated` / `Failed`.

### Table B: `Competency Logs`
Logs the progress audits compiled by the academic and alignment sub-agents.
*   **Audit ID** (Autonumber) - Primary Key.
*   **Student** (Single Line Text / Link to Students): Name of the audited student.
*   **Date** (Created Time): Time of audit execution.
*   **Scientific Methodology** (Number): Score from 1 to 10.
*   **Data Triangulation** (Number): Score from 1 to 10.
*   **Academic Writing Clarity** (Number): Score from 1 to 10.
*   **Sponsor Alignment Index** (Number): Score from 1% to 100%.
*   **Mentor Score** (Number): Score from 1 to 10.

### Table C: `Daily Snapshots / Metrics Table`
Logs daily snapshots to compute delay trends and cohort metrics.
*   **Snapshot ID** (Autonumber) - Primary Key.
*   **Student** (Single Line Text): Student name.
*   **Phase** (Single Line Text): Current project phase.
*   **Delay Days** (Number): Number of task delay days.
*   **Scientific Methodology** (Number): Current methodology score.
*   **Data Triangulation** (Number): Current triangulation score.
*   **Academic Writing Clarity** (Number): Current clarity score.
*   **Sponsor Alignment Index** (Number): Current alignment score.
*   **Timestamp** (Created Time).

---

## 3. Manual Run & Troubleshooting Commands

If a workflow fails in n8n, you can run the sub-agents directly from your terminal to isolate errors.

### 3.1 Run Document Audit Manually
```bash
# Formulate the Python path and execute the CLI agent router
$env:PYTHONPATH="f:\Antigravity\IRC Workflow"
python irc_agent.py --action audit-doc --student "Rahul" --student-report-file "docs/temp/test_student_report.txt" --baseline-report-file "docs/temp/test_student_report.txt" --degree-level "MSc" --duration-months 8 --sponsor-problem "Sponsor problem statement here..."
```

### 3.2 Run Weekly Digest Manually
```bash
# Save a test JSON containing daily snapshots and run the digest compiler
python irc_agent.py --action compile-weekly-digest --weekly-metrics-file "docs/temp/test_weekly_metrics.json"
```

### 3.3 Diagnostics
*   **ModuleNotFoundError**: Ensure the `PYTHONPATH` system environment variable includes the workspace root.
*   **Model Query Error**: Verify `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, or `OPENAI_API_KEY` is exported in the active shell.
*   **n8n Database Locked**: Close any other local n8n terminal sessions before launching the start script.
