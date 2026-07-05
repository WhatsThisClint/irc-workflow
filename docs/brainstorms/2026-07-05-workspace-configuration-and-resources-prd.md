# PRD: Zero-Friction Workspace Configuration & Dynamic Resource Ingestion

**Date**: 2026-07-05
**Status**: DRAFT (Brainstorming Phase)

---

## 1. Overview

This document outlines the product requirements for scaling the India Research Corps (IRC) workspace portability and educational capability:

1.  **Zero-Friction Workspace Configuration**: An interactive setup wizard that automatically runs on git-clone to configure credentials, mapping both local autonomous processes (n8n background cron runs) and IDE-native connectors (e.g. Codex/Claude Desktop Google Drive and Gmail MCP servers).
2.  **Dynamic Induction Resource Ingestion**: An adaptive ingestion engine that scans a designated Google Drive resource folder, converts arbitrary file formats (slides, PDFs, transcripts), classifies them to the 6 induction modules, and feeds these session-specific rubrics into the Academic Auditor.

---

## 2. User Experience & User Stories

*   **As an Admin or Assistant Onboarding on a New PC**, I want to run a single configuration command that asks me for my email, my Drive folder, and validates my IDE's connected plugins, so that I don't have to manually edit config files.
*   **As a Program Director**, I want to place new slide decks, session transcripts, or reading PDFs into a Drive folder and tell the agent where it is, so that the AI Academic Auditor dynamically knows what was taught in that session and grades the student's reflections accordingly.

---

## 3. Product Features & Requirements

### 3.1 Interactive Workspace Setup Wizard (`configure_workspace.py`)
*   **Active MCP Detection**: The script must check if active Google Drive or Gmail MCP tools are available in the active IDE session. If detected, it guides the user to authorize the agent natively.
*   **Interactive Prompts**: Prompts the user in the console/chat for:
    *   Coordinator Email ID.
    *   Google Drive Root Folder name/ID.
    *   API provider keys (Gemini, Anthropic, or OpenAI) if local fallback runs are needed.
*   **Durable Variables**: Saves these variables to a local `.env` file (ignored by Git) and injects them into n8n's configuration parameters automatically.

### 3.2 Adaptive Ingestion Engine (`ingest_resources.py`)
*   **Folder Scanning**: Scans a specified local path or Google Drive Folder ID.
*   **Auto-Conversion**: Iterates through files (PowerPoints, PDFs, Word Docs) and converts them to plain text markdown using the `markitdown` tool.
*   **LLM classification**: Sends the extracted text to the LLM to classify which of the 6 induction modules the resource belongs to.
*   **Structured Local Caching**: Saves a structured JSON/markdown summary (e.g. `docs/resources/session_1_rubrics.json`) summarizing:
    *   Core terms taught.
    *   Grading criteria rules.
    *   Specific reference reading details.

### 3.3 Session-Aware Academic Auditor Upgrade
*   **Dynamic Rubric Loading**: Modifies `agents/academic_auditor.py` to identify the session number being graded (e.g., "Session 1 Reflection").
*   **Prompt Injection**: If the cached resource rubric for that session exists in `docs/resources/`, it automatically loads and injects the session-specific core terms and grading rules into the audit prompt.

---

## 4. Scope Boundaries & Exclusions

*   **Out of Scope**: 
    *   Building a graphical user interface (GUI) for the configuration wizard. The wizard will run entirely in the terminal or chat interface.
    *   Hosting a custom database for resource files. All processed data is cached locally as text/JSON in the workspace.
