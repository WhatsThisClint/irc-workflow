# IRC Comprehensive Workflow & Node Reference Manual

This manual provides an exhaustive, node-by-node reference of the India Research Corps (IRC) workspace topology. It maps how all database fields, diagnostics scripts, specialist agents, syllabus rubrics, and academic rules link together to automate the cohort tracking system.

---

## 1. The Database Schema (Airtable / Google Sheets)
The data storage layer consists of three linked database tables that represent the state and progress history of the cohort.

```
[Students Table] 
    | (1-to-Many Link)
    v
[Competency Logs Table] <---> [Daily Snapshots Table] (Trend Analysis)
```

### 1.1 The `Students` Table (The Master Registry)
*   **Student (Primary Key)**: The student's full name. Acts as the primary foreign key linking audits and snapshots.
*   **S.No**: Master sheet serial identifier used to index students sequentially.
*   **Degree Level**: Single-select (`BSc` / `MSc` / `PhD`). Instructs the AI Academic Auditor on what level of scientific complexity and literature depth to grade against.
*   **Current Project Phase**: Single-line text updated dynamically by `coordinator_agent.py` (`Induction`, `Fieldwork`, `Thesis Writing`, or `Completed`).
*   **Problem Statement**: Long text of the partner sponsor's research parameters. Used by `alignment_agent.py` to compile the Sponsor Alignment Index.
*   **Drive Shared Folder Link**: The URL to the student's shared workspace.
*   **Reflection Doc Link**: The URL to the student's active weekly reflection document or inception report.
*   **Status**: Single-select (`Active` / `Graduated` / `Failed`).

### 1.2 The `Competency Logs` Table (The Grade Ledger)
Every time a document audit runs, the system appends a new record to this table:
*   **Audit ID**: Autonumber primary key.
*   **Student**: Name linked to the `Students` table.
*   **Date**: Timestamp of when the sub-agents executed.
*   **Scientific Methodology**: Numerical score (1-10) tracking question clarity, falsifiability of hypotheses, and research logic.
*   **Data Triangulation**: Numerical score (1-10) tracking survey sample size validity, remote-sensing data crosschecks, and bias mitigations.
*   **Academic Writing Clarity**: Numerical score (1-10) assessing prose style, argument-mode literature reviews, and structural layout.
*   **Sponsor Alignment Index (SAI)**: Percentage score (1-100%) tracking how well the student's methodology answers the sponsor's problem.
*   **Mentor Score**: Numerical score (1-10) grading the substantiveness of the academic advisor's doc comments.

### 1.3 The `Daily Snapshots / Metrics` Table (The Velocity Tracker)
*   **Snapshot ID**: Autonumber primary key.
*   **Student**: Name identifier.
*   **Phase**: Active research phase.
*   **Delay Days**: Cumulative number of days the student has lagged on reflection uploads or Gantt milestones. used by n8n to trigger escalations.

---

## 2. Setup, Diagnostics, & Configuration Wizard
This layer handles first-time installation, local variable initialization, and IDE integrations.

```
[setup_workspace.py] ---> Launches ---> [configure_workspace.py]
                                                |
                                                v
                                        Creates [.env] 
                                        & Configures MCP Plugins
```

*   **`setup_workspace.py`**:
    *   *Python Version Check*: Ensures Python 3.x is active.
    *   *NPM/Node Diagnostics*: Verifies local node environment and installs `n8n` dependencies to the local `.n8n/` workspace folder.
    *   *Critical File Audit*: Scans for missing specialist python scripts.
    *   *Global Tool Installation*: Validates that Graphify CLI (`graphify`) and Ponytail CLI (`ponytail`) are globally active.
    *   *Launcher*: Automatically spawns `configure_workspace.py` if no local `.env` is found.
*   **`configure_workspace.py`**:
    *   *MCP Plugin Detection*: Scans for active Model Context Protocol (MCP) servers (Google Drive / Gmail) inside Codex or Claude Desktop. Guides the user to authorize browser permission dialogs.
    *   *Interactive Prompts*: Collects email settings, Drive folder paths, and preferred API keys (Gemini, Anthropic, or OpenAI).
    *   *`.env` Builder*: Writes variables into a localized `.env` file inherited by background n8n runs.

---

## 3. The CLI Router & LLM client Layer

```
[n8n / CLI Command] 
       |
       v
[irc_agent.py Router] 
       | (Checks PYTHONPATH, sets env, spawns subprocess)
       v
[Specialist Python Agent] 
       |
       v
[llm_client.py Wrapper] ---> [send_request_with_retry] ---> API Providers
```

*   **`irc_agent.py`**: 
    *   Serves as the main routing gateway.
    *   Enforces paths by dynamically prepending the workspace root to the `PYTHONPATH` system environment variable, avoiding `ModuleNotFoundError` inside spawned subprocesses.
    *   Catches global errors and wraps script failure messages in a standardized completion JSON envelope (`{"status": "failed", "error": "details"}`) for n8n.
*   **`agents/llm_client.py`**:
    *   *Central Route Handler*: Coordinates calls to Gemini, Claude, or OpenAI.
    *   *JSON Mode Enforcement*: Ensures models return strictly parsable JSON objects.
    *   *`send_request_with_retry` Handler*: Implements a rate-limit retry loop using exponential backoff (e.g. 3s, 6s, 12s delay triggers) to bypass `HTTP Error 429: Too Many Requests` during rapid batch runs.

---

## 4. Specialist Sub-Agent Nodes (The Brains)

### 4.1 `onboarding_agent.py` (Baseline Generator)
*   **Input**: Student Name, Research Question, Degree Level, Cohort Duration (months).
*   **Logic**: Uses prompt templates defining *Proportional Rigor* to write the initial inception baseline. BSc baselines focus on fieldwork feasibility; MSc baselines focus on methodological rigor; PhD baselines require modeling complexity and novelty.
*   **Output**: Clean baseline text report.

### 4.2 `academic_auditor.py` (Progress Auditor)
*   **Input**: Student report file, baseline file, degree level, duration, memory file.
*   **Logic**:
    1.  *Session Detection*: Scans filename and content snippet (using regex) to detect the active induction session (Session 1 to 6).
    2.  *Rubric Injection*: Reads `docs/resources/session_rubrics.json` to load dynamic syllabus expectations for the active session, merging them into the prompt.
    3.  *Memory Integration*: Reads coordinator memory guidelines from `memory.json` to enforce historical corrections.
*   **Output**: Competency scores, detailed critique, and 3-4 weekly sync questions.

### 4.3 `mentor_auditor.py` (Feedback Evaluator)
*   **Input**: Student report Google Doc comments log.
*   **Logic**: Analyzes active and resolved comment text. Flags superficial mentor approvals and scores feedback substantiveness (1-10).
*   **Output**: Substantiveness score and feedback critique.

### 4.4 `alignment_agent.py` (Sponsor Alignment Analyst)
*   **Input**: Student report file, sponsor problem statement.
*   **Logic**: Evaluates whether the student's field methods actively resolve the sponsor's requirements, compiling the Sponsor Alignment Index (1-100%).
*   **Output**: Alignment Index score and critique.

### 4.5 `transcript_parser.py` (Meeting distiller)
*   **Input**: Raw meeting transcript text.
*   **Logic**: Filters conversational filler and extracts concrete action items.
*   **Output**: JSON list of structured tasks.

### 4.6 `coordinator_agent.py` (State & memory Manager)
*   **Extract Feedback Mode**: Reads the `Admin Cheat Sheet` document, parses coordinator remarks, and appends them to `memory.json` (compressing logs if they exceed 1,500 characters).
*   **Digest Compile Mode**: Reads weekly snapshot metrics and renders the formatted Weekly Director Digest.

### 4.7 `ingest_resources.py` (Syllabus Ingestor)
*   **Input**: Path to course folder.
*   **Logic**: Processes PPTX, PDF, and DOCX files via `markitdown` text conversion, classifies them to the 6 induction modules using LLM classification, and saves core concepts and grading expectations to `session_rubrics.json`.

---

## 5. Academic Rules & Syllabus Curriculum

### 5.1 The 6 Induction Modules (`docs/resources/session_rubrics.json`)
*   **Module 1 (Scientific Method)**: Formulating falsifiable research questions and hypothesis testing frameworks.
*   **Module 2 (Conceptual Model)**: Variables classification (Independent, Dependent, Mediators, Moderating controls).
*   **Module 3 (Research Scope)**: Boundary definitions and 80/20 design choices.
*   **Module 4 (Methodology)**: Selecting biophysical vs. socio-hydrological methods.
*   **Module 5 (Data Collection)**: Sampling design and survey biases.
*   **Module 6 (Data Analysis)**: Remote sensing, spatial statistics, and reporting structures.

### 5.2 Scientific Rigor Tenets (`docs/INDUCTION_MODULES_REFERENCE.md`)
*   **Objectivity**: Eliminating bias in data reporting.
*   **Validity**: Checking if survey questions measure what they claim to.
*   **Reliability**: Consistency of instrumentation.
*   **Transparency**: Open data sharing.
*   **Replicability**: Documenting methodology details so others can recreate the study.
