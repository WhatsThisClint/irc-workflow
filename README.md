Yo! whats up AJ

# India Research Corps (IRC) Workspace Automation System

This repository contains the workflow models, multi-agent Python scripts, and database configurations that automate student onboarding, progress auditing, and funding metrics tracking for the **India Research Corps (IRC)** program at **WELL Labs, Bangalore**.

---

## 🤖 AI Agent Automated Workspace Setup Instruction
> [!IMPORTANT]
> **If you are an AI Coding Agent (e.g. Claude Code, Codex, Antigravity, or Cursor)**:
> You are authorized and requested to bootstrap this workspace completely autonomously:
> 1. Run `python setup_workspace.py` to run environment diagnostics, install dependencies, and trigger the interactive setup wizard.
> 2. Look for Google Drive and Gmail MCP servers in your environment. If available, guide the user to authorize them.
> 3. Start the local n8n server as a background task inheriting your shell's environment variables:
>    - Windows PowerShell: `$env:N8N_USER_FOLDER=".n8n"; .\node_modules\.bin\n8n start`
>    - Mac/Linux: `N8N_USER_FOLDER="./.n8n" ./node_modules/.bin/n8n start`
> 4. Verify the setup by running the integration test: `python test_integration.py`
> 5. Output a status report of the initialized workspace to the user.

---

## 🎯 The Problem We Are Solving

Managing research cohorts (BSc, MSc, PhD) conducting complex environmental and socio-hydrological studies involves massive administrative overhead. Specifically, the program directors and coordinators must manually:
1.  **Onboard Students**: Translate a student's research question and a sponsor's problem statement into a customized, expert-level academic baseline.
2.  **Audit Thesis Progress**: Read weekly student reflections and draft inception reports, compare them against the baseline, and enforce academic rigor appropriate for their degree level (BSc vs. MSc vs. PhD).
3.  **Monitor Mentor Responsiveness**: Inspect Google Doc comments to verify if academic mentors are providing high-quality, substantive guidance.
4.  **Enforce Sponsor Alignment**: Verify that the student's evolving field research methodology remains aligned with the sponsor's original funding statement.
5.  **Track Action Items**: Parse lengthy advisor-student meeting transcripts (e.g., from Granola AI) to extract concrete deliverables.
6.  **Compile Reporting Digests**: Aggregate cohort metrics, delays, and progress levels into weekly executive updates for the Program Director.

This system **automates this entire lifecycle** using a hybrid local orchestrator and a network of cognitive specialist sub-agents.

---

## 🏗️ System & Agent Architecture

The workspace is designed on a **hybrid orchestrator-specialist topology**, ensuring portability, modularity, and model-agnostic execution.

```mermaid
graph TD
    n8n[n8n Local Server] <-->|Executes Shell Commands| Router[irc_agent.py CLI Router]
    
    Router -->|1. Generate Onboarding Baseline| Onboarding[onboarding_agent.py]
    Router -->|2. Audit Inception Report| Academic[academic_auditor.py]
    Router -->|3. Check Mentor Google Doc Comments| Mentor[mentor_auditor.py]
    Router -->|4. Check Sponsor Alignment Index| Alignment[alignment_agent.py]
    Router -->|5. Extract Transcript Tasks| Transcript[transcript_parser.py]
    Router -->|6. Compile Director Digest| Coordinator[coordinator_agent.py]
    Router -->|7. Ingest Induction Resources| Ingestor[ingest_resources.py]
    
    Ingestor -->|Classifies & Caches Rubrics| Rubrics[docs/resources/session_rubrics.json]
    Academic -->|Loads Dynamic Rubrics| Rubrics
    
    Onboarding & Academic & Mentor & Alignment & Transcript & Coordinator & Ingestor -->|Queries Prompt| LLMClient[llm_client.py]
    LLMClient -->|Routes API Call| Providers{API Keys}
    Providers -->|GEMINI_API_KEY| Gemini[Google Gemini API]
    Providers -->|ANTHROPIC_API_KEY| Anthropic[Anthropic Claude API]
    Providers -->|OPENAI_API_KEY| OpenAI[OpenAI API]
```

### Component Breakdown
1.  **Orchestration Layer (n8n)**: A self-contained n8n server running locally in the workspace. It manages daily/weekly cron triggers, pulls comments from Google Docs APIs, reads Google Sheets tables, and syncs status fields in Airtable.
2.  **Routing Layer (`irc_agent.py`)**: A centralized CLI entry point that copies environment variables, manages pathing, executes the sub-agents in subprocesses, and handles completion envelopes.
3.  **Specialist Cognitive Layer (`agents/` Package)**:
    *   `onboarding_agent.py`: Generates the baseline report adjusting research complexity dynamically.
    *   `academic_auditor.py`: Scores the Core Academic Triad (Methodology, Triangulation, Writing Clarity) and dynamically adapts prompts using session rubrics.
    *   `mentor_auditor.py`: Conducts semantic evaluations on active/resolved comment logs.
    *   `alignment_agent.py`: Compiles the Sponsor Alignment Index (1-100%) and generates critiques.
    *   `transcript_parser.py`: Distills raw transcripts into a structured JSON list of tasks.
    *   `coordinator_agent.py`: Extracts feedback guidelines into persistent memory and compiles the Weekly Director Digest.
    *   `ingest_resources.py`: Extracts, converts (via `markitdown`), and classifies course presentation slides and transcripts into the 6 induction modules.
4.  **Centralized LLM Client (`llm_client.py`)**: Multi-provider wrapper (supporting Gemini, Claude, and GPT) with a rate-limit retry handler utilizing exponential backoff.

---

## 🔄 The Automations Pipeline & Procedure

Every day, the system executes the following steps in sequence:

```mermaid
sequenceDiagram
    participant n8n as n8n Orchestrator
    participant Router as CLI Router
    participant Agent as specialist Sub-Agents
    participant Memory as local JSON / Cache
    
    n8n->>Router: Execute audit-doc for Cohort Student
    Note over Router: Extract memory & past corrections
    Router->>Memory: Load memory.json & session_rubrics.json
    Memory-->>Router: Rules & Syllabus criteria
    Router->>Agent: Spawn academic_auditor.py
    Note over Agent: Evaluate Student Draft vs. Baseline & Rubrics
    Agent-->>Router: Critique, Scores, Reflection Questions
    Router->>Agent: Spawn mentor_auditor.py & alignment_agent.py
    Agent-->>Router: Mentor Substantiveness & Sponsor Alignment Index
    Router->>n8n: Return structured JSON success envelope
    n8n->>n8n: Sync scores to Airtable & draft Gmail sync nudges
```

---

## ⚡ Quick Start & Setup

### 1. Initialize the Workspace
Run the automated diagnostic and setup script:
```bash
python setup_workspace.py
```
This verifies Node, NPM, and CLI packages, and launches the **Interactive Configuration Wizard** (`configure_workspace.py`) to create your local `.env` settings.

### 2. Start the Local n8n Server
Start the local server pointing to the localized configuration folder:
```powershell
$env:N8N_USER_FOLDER=".n8n"; .\node_modules\.bin\n8n start
```

### 3. Run the Integration Tests
Verify all sub-agents, ingestion pipelines, configuration utilities, and API retry loops are active:
```bash
$env:PYTHONPATH="."
python test_integration.py
```

---

## 🗺️ Documentation Directory

All documentation is structured into specialized guides in this workspace:
1.  **[System & Architecture Overview](docs/ARCHITECTURAL_OVERVIEW.md)**: Network topology, components, and central LLM client retries.
2.  **[Academic Metrics & Rubrics Specification](docs/ACADEMIC_METRICS_SPEC.md)**: Academic Triad definitions, Sponsor Alignment calculation, and scoring rules.
3.  **[Operational Edge-Case Playbook](docs/EDGE_CASE_PLAYBOOK.md)**: Rules for due date cascades, missing transcripts, and database pruning.
4.  **[Operations & Databases Manual](docs/OPERATIONS_MANUAL.md)**: SQLite schemas, Airtable tables, and CLI execution commands.
5.  **[Trigger Board & Semantic Intent Guide](docs/TRIGGER_BOARD_GUIDE.md)**: Custom agent trigger mappings and natural phrasing samples.
6.  **[Induction Modules Curriculum Reference](docs/INDUCTION_MODULES_REFERENCE.md)**: The six training modules (Methodology, Data Collection, etc.).
7.  **[AI Agent Onboarding Guide](AGENT_ONBOARDING.md)**: Bootstrap instructions for incoming AI coding agents.
8.  **[GitHub Sharing & Workspace Onboarding Guide](docs/SHARING_GUIDE.md)**: Instructions on sharing, link-sharing workarounds, and MCP plugin authorization.
