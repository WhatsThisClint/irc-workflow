# AI Agent Workspace Onboarding Guide

Welcome, Agent! You have been spawned to manage, scale, or edit the India Research Corps (IRC) student tracking and workflow automation system. Follow the steps below to initialize and verify the workspace.

---

## 1. Automated Setup & Diagnostics
Your first task is to execute the automated setup script. This script validates Node.js/NPM, ensures Python is configured, installs local `n8n` dependencies, and verifies the integrity of the specialized sub-agents.

Run this command in the shell:
```bash
python setup_workspace.py
```

---

## 2. API Key Configuration
The local Python sub-agents call the Gemini API directly via standard Python libraries.
*   **Prerequisite**: Ensure the `GEMINI_API_KEY` environment variable is loaded in your shell context.
*   **Action**: If the key is missing, ask the user to provide it and set it in the active terminal environment:
    *   **Windows PowerShell**: `$env:GEMINI_API_KEY="your-key-here"`
    *   **Mac/Linux Terminal**: `export GEMINI_API_KEY="your-key-here"`

---

## 3. Starting the Local n8n Server
The project runs on an isolated local n8n instance. All credentials, custom nodes, and databases are saved directly in the workspace under the `.n8n/` folder.

To start n8n as a background task, execute:
*   **Windows PowerShell**:
    ```powershell
    $env:N8N_USER_FOLDER="f:\Antigravity\IRC Workflow\.n8n"; .\node_modules\.bin\n8n start
    ```
*   **Mac/Linux Terminal**:
    ```bash
    N8N_USER_FOLDER="./.n8n" ./node_modules/.bin/n8n start
    ```

---

## 4. Key Workflows & Agent Architecture
*   **Master n8n Workflow**: The consolidated canvas configuration is located at `n8n/workflows/irc_master_workflow.json`.
*   **CLI Router**: All n8n Execute Command nodes call the main CLI router `irc_agent.py`.
*   **Specialist Sub-Agents**: The router delegates commands to the files under the `agents/` folder:
    *   `onboarding_agent.py`: Generates the expert baseline reports.
    *   `academic_auditor.py`: Audits student document revisions against the baseline.
    *   `mentor_auditor.py`: Analyzes active/resolved comments to audit mentor responsiveness.
    *   `transcript_parser.py`: Extracts actionable tasks from transcripts.
    *   `alignment_agent.py`: Scores report alignment against the sponsor's problem statement.
    *   `coordinator_agent.py`: Aggregates audit outputs and compiles the Weekly Director Digest.

---

## 5. Next Steps Checklist for Incoming Agents
1.  [ ] Run `python setup_workspace.py` and verify all checks pass.
2.  [ ] Check if the n8n port `5678` is listening. If not, launch n8n as a background task.
3.  [ ] Scan the `CLAUDE.md` and `README.md` files to understand sheet schemas, Airtable log columns, and edge cases.
4.  [ ] Present a summary of the current environment status to the user and ask for their next instruction.
