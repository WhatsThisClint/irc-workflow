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

## 2. API Key Configuration & Environment Inheritance
To run the Gemini model queries, the Python sub-agents require access to `GEMINI_API_KEY`.
*   **Zero-Input Key Inheritance**: Since you (the agent) are running inside a shell that is already authenticated, **you must start the n8n server using your own command execution tool** (e.g. `run_command` or similar). 
*   **Why this works**: By starting the n8n background task directly from your agentic environment, the spawned n8n process (and any command-line sub-processes it triggers daily) will **inherit your shell's environment variables** (including `GEMINI_API_KEY` or other authorization tokens). This completely eliminates the need for the user to manually configure or type API keys.

---

## 3. Starting the Local n8n Server
The project runs on an isolated local n8n instance. All credentials, custom nodes, and databases are saved directly in the workspace under the `.n8n/` folder.

You must launch n8n as a background task directly from your agent session:
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
