# India Research Corps (IRC) Workflow Automation System

This repository contains the workflow models, multi-agent Python scripts, and database configurations that automate student onboarding, progress auditing, and funding metrics tracking for the **India Research Corps (IRC)** program at **WELL Labs, Bangalore**.

---

## 🗺️ Documentation Index

To make this workspace fully self-contained and accessible to developers and AI agents alike, our documentation is structured into the following detailed guides:

1.  **[System & Architecture Overview](docs/ARCHITECTURAL_OVERVIEW.md)**
    *   Learn about the orchestrator-specialist topology, component directories, and our model-agnostic LLM router.
2.  **[Academic Metrics & Rubrics Specification](docs/ACADEMIC_METRICS_SPEC.md)**
    *   Examine the evaluation criteria for the Core Academic Triad (Methodology, Triangulation, Writing Clarity), the Sponsor Alignment Index (SAI), and proportional grading rules.
3.  **[Operational Edge-Case Playbook](docs/EDGE_CASE_PLAYBOOK.md)**
    *   Read the detailed rules and parameters governing the 16 custom workflow systems (inception gate fails, missing transcripts, due date cascades, and database pruning).
4.  **[Operations & Databases Manual](docs/OPERATIONS_MANUAL.md)**
    *   Get step-by-step setup guides, SQLite portability data, Airtable database schemas, and manual CLI troubleshooting procedures.
5.  **[Trigger Board & Semantic Intent Guide](docs/TRIGGER_BOARD_GUIDE.md)**
    *   Find trigger keywords, natural phrasing examples, and custom agent rules.
6.  **[Induction Modules Curriculum Reference](docs/INDUCTION_MODULES_REFERENCE.md)**
    *   Review core scientific tenets, conceptual model variables, and methodologies taught to students.
7.  **[AI Agent Onboarding Guide](AGENT_ONBOARDING.md)**
    *   The bootstrap specification file designed specifically for incoming AI coding agents to set up the repository automatically.
8.  **[GitHub Sharing & Workspace Onboarding Guide](docs/SHARING_GUIDE.md)**
    *   Instructions on how to share the private repository, use link-sharing workarounds, and configure native MCP connectors.




---

## ⚡ Quick Start

### 1. Initialize the Workspace
Run the automated diagnostic and setup script:
```bash
python setup_workspace.py
```

### 2. Start the Local n8n Server
Start the local server pointing to the localized configuration folder:
```powershell
$env:N8N_USER_FOLDER=".n8n"; .\node_modules\.bin\n8n start
```

### 3. Verify Local CLI Agents
Test the document auditor manually:
```powershell
$env:PYTHONPATH="."
python irc_agent.py --action audit-doc --student "Rahul" --student-report-file "docs/temp/test_student_report.txt" --baseline-report-file "docs/temp/test_student_report.txt" --degree-level "MSc" --duration-months 8
```

---

## 🧠 Graphify Code Graph
The **`graphify-out/`** directory contains the pre-rendered code graph database. Incoming agents will query this directory to map dependencies, import relationships, and logic boundaries instantly.

To update the graph database after modifications:
```bash
graphify update .
```
