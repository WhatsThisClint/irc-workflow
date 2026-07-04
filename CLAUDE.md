# CLAUDE.md (IRC Workflow Memory Bank)

This file contains the persistent architectural context, commands, design decisions, and edge-case resolution rules for the India Research Corps (IRC) Workflow Automation system. Read this first when resuming work in this workspace on any machine.

---

## 1. Project & Academic Context
The India Research Corps (IRC) matches university students with partner agencies to solve applied socio-hydrological problems in environmental water systems (WELL Labs, Bangalore). 
*   **Scale Challenge**: As student and mentor volume expands, tracking research quality, timeline delays, and mentor feedback becomes a bottleneck for the Coordinator.
*   **Solution**: A local **n8n** master workflow orchestrating Google Workspace, Asana, and Airtable, delegating AI analysis to a local **multi-agent Python system** querying **Gemini 3.5 Flash**.

---

## 2. Portability & Agent Onboarding
To migrate this entire system to another PC:
1.  **Copy the Folder**: Simply copy/clone the `IRC Workflow/` folder to the target machine.
2.  **Isolated n8n Data**: The local n8n server is configured to write to `IRC Workflow/.n8n/`. This ensures all credentials, tokens, custom nodes, and workflow configurations sync and transfer intact.
3.  **Agent Setup**: When a new coding agent opens this workspace, it should read **`AGENT_ONBOARDING.md`** and run the setup script:
    ```bash
    python setup_workspace.py
    ```

---

## 3. Development & Execution Commands

### Starting n8n Local Server
Always point n8n to the local `.n8n/` folder:
```powershell
# Windows Powershell
$env:N8N_USER_FOLDER="f:\Antigravity\IRC Workflow\.n8n"; .\node_modules\.bin\n8n start

# Mac/Linux Terminal
N8N_USER_FOLDER="./.n8n" ./node_modules/.bin/n8n start
```

### Direct Python Agent Commands
The main entry point CLI router `irc_agent.py` delegates actions to specialized sub-agents:

```bash
# A. Generate Baseline Inception Report (Onboarding Path)
# Calls agents/onboarding_agent.py
python irc_agent.py --action generate-baseline --student "Rahul" --question "Rainfall patterns" --problem "Borewell extraction rates rising" --degree-level "MSc" --duration-months 8

# B. Audit Student Inception Report & Comments (Monitoring Path)
# Calls agents/academic_auditor.py, agents/mentor_auditor.py, and optionally agents/alignment_agent.py
python irc_agent.py --action audit-doc --student "Rahul" --student-report-file "path/to/report.txt" --baseline-report-file "path/to/baseline.txt" --degree-level "PhD" --duration-months 10 --sponsor-problem "Sponsor's problem statement..."

# C. Calculate Current Project Phase (Monitoring Path)
# Calls agents/coordinator_agent.py
python irc_agent.py --action calculate-phase --cohort-start-date "2026-07-01" --duration-months 8 --gantt-file "path/to/gantt.json"

# D. Parse Granola AI Meeting Transcript (Transcript Path)
# Calls agents/transcript_parser.py
python irc_agent.py --action parse-transcript --transcript-file "path/to/transcript.txt"

# E. Sponsor Alignment Check (Alignment Path)
# Calls agents/alignment_agent.py
python irc_agent.py --action check-alignment --student-report-file "path/to/report.txt" --sponsor-problem "Sponsor's problem statement..."

# F. Compile Weekly Director Digest (Digest Path)
# Calls agents/coordinator_agent.py
python irc_agent.py --action compile-weekly-digest --weekly-metrics-file "path/to/metrics_snapshots.json"
```

---

## 4. Multi-Agent Specialist Architecture

*   **[irc_agent.py](file:///f:/Antigravity/IRC%20Workflow/irc_agent.py)**: CLI Router. Maintains backward compatibility with n8n execute command nodes, orchestrates and parses intermediate JSON files, and prints output.
*   **[onboarding_agent.py](file:///f:/Antigravity/IRC%20Workflow/agents/onboarding_agent.py)**: Formulates the baseline inception report based on degree level and program duration.
*   **[academic_auditor.py](file:///f:/Antigravity/IRC%20Workflow/agents/academic_auditor.py)**: Audits progress compared to the baseline, checks coordinator feedback, and scores the **Core Academic Triad** (Scientific Methodology, Data Triangulation, Academic Writing Clarity) from 1 to 10.
*   **[mentor_auditor.py](file:///f:/Antigravity/IRC%20Workflow/agents/mentor_auditor.py)**: Scores mentor comment quality (substantive vs. superficial) and responsiveness from 1 to 10.
*   **[alignment_agent.py](file:///f:/Antigravity/IRC%20Workflow/agents/alignment_agent.py)**: Compares research files against the sponsor's problem statement to output the **Sponsor Alignment Index (1-100%)**.
*   **[transcript_parser.py](file:///f:/Antigravity/IRC%20Workflow/agents/transcript_parser.py)**: Extracts substantive action items from meeting conversations, preventing task board clutter.
*   **[coordinator_agent.py](file:///f:/Antigravity/IRC%20Workflow/agents/coordinator_agent.py)**: Manages coordinator memory files, calculates milestones, compiles final cheat sheets, drafts Gmail nudges, and generates the Weekly Director Digest.

---

## 5. Folder & File Structure
```
f:/Antigravity/IRC Workflow
 ├── n8n/
 │    └── workflows/
 │         └── irc_master_workflow.json (Consolidated Onboarding + Monitor + Digest branches)
 ├── .n8n/                               (Self-contained local n8n credentials database)
 ├── agents/                             (Specialized multi-agent system package)
 │    ├── academic_auditor.py
 │    ├── alignment_agent.py
 │    ├── coordinator_agent.py
 │    ├── mentor_auditor.py
 │    ├── onboarding_agent.py
 │    └── transcript_parser.py
 ├── docs/
 │    └── brainstorms/
 │         └── 2026-07-04-irc-workflow-scaling-requirements.md
 ├── graphify-out/                       (Dedicated project code-graph database for agents)
 ├── irc_agent.py                        (Main CLI router agent)
 ├── setup_workspace.py                  (Automated setup script)
 ├── AGENT_ONBOARDING.md                 (AI onboarding instructions)
 ├── README.md                           (Master sheet schemas & operational logic details)
 └── CLAUDE.md                           (This context file)
```

---

## 6. Key Design Decisions & Rationale

*   **Google Drive Unique Names**: Folder naming: `[S.No] - [Student Name] - IRC Workspace` (e.g. `002 - Rahul Dev - IRC Workspace`). Prevents file reference errors when multiple students share common names.
*   **Failed Gate revokes permissions**: Revoking edit access (leaving Read-Only) when a student fails the Inception Gate prevents undocumented changes or document deletion after exit.
*   **Human-In-The-Loop Feedback**: The coordinator writes edits inside the `Admin Cheat Sheet` under `## Coordinator Feedback/Corrections`. The daily monitor extracts this text and saves it to a portable `memory.json` inside the student's Google Drive `Admin Only` folder. The Academic Auditor reads this JSON on subsequent runs to align future critiques.
*   **Weekly Director Digest**: Every Friday at 5:00 PM, n8n queries Airtable metrics snapshot logs from the past week, compiles them, and emails a Markdown dashboard report to the director, showing cohort velocity and competency growth trajectories.
*   **Graphify Integration Whitelist**: The `graphify-out/` directory is whitelisted in Git. When cloned, incoming agents query the local graph database (`graph.json`, `GRAPH_REPORT.md`) to map file relations and logic boundaries instantly.
