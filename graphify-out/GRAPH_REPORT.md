# Graph Report - IRC Workflow  (2026-07-05)

## Corpus Check
- 18 files · ~11,646 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 209 nodes · 224 edges · 46 communities (14 shown, 32 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7e47efb9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]

## God Nodes (most connected - your core abstractions)
1. `connections` - 36 edges
2. `call_llm()` - 12 edges
3. `CLAUDE.md (IRC Workflow Memory Bank)` - 12 edges
4. `India Research Corps (IRC) Student Tracking & Onboarding System` - 8 edges
5. `AI Agent Workspace Onboarding Guide` - 7 edges
6. `India Research Corps Strategy` - 7 edges
7. `Agent-Native Architecture Audit: IRC Workflow` - 5 edges
8. `2. Core Principles Scorecard` - 5 edges
9. `Requirements: IRC Workflow Scaling & Performance Tracking` - 5 edges
10. `2. Metric Specifications & Tracking Logic` - 5 edges

## Surprising Connections (you probably didn't know these)
- `generate_weekly_digest()` --calls--> `call_llm()`  [EXTRACTED]
  agents/coordinator_agent.py → agents/llm_client.py
- `audit_document()` --calls--> `call_llm()`  [EXTRACTED]
  agents/academic_auditor.py → agents/llm_client.py
- `check_alignment()` --calls--> `call_llm()`  [EXTRACTED]
  agents/alignment_agent.py → agents/llm_client.py
- `audit_mentor()` --calls--> `call_llm()`  [EXTRACTED]
  agents/mentor_auditor.py → agents/llm_client.py
- `generate_baseline()` --calls--> `call_llm()`  [EXTRACTED]
  agents/onboarding_agent.py → agents/llm_client.py

## Import Cycles
- None detected.

## Communities (46 total, 32 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.17
Nodes (11): 1. Objectives & Focus Areas, 2.1 Student Progress Tracking, 2.2 Mentor Engagement Audit, 2.3 Cohort & Operational KPI Definitions, 2.4 Funding & Impact Metrics (For Pitching & Scaling), 2. Metric Specifications & Tracking Logic, 3.1 Google Sheets Dashboard Tab, 3.2 Airtable Logging Schema (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (16): 1. Project & Academic Context, 1. Project Overview, 2. Portability & Agent Onboarding, 2. Porting & Copy-Pasting to Another PC, 3. Development Commands, 3. Development & Execution Commands, 4. Folder & File Structure, 4. Multi-Agent Specialist Architecture (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.22
Nodes (8): description, devDependencies, n8n, main, name, scripts, start, version

### Community 3 - "Community 3"
Cohesion: 0.36
Nodes (4): calculate_phase(), call_gemini(), generate_weekly_digest(), log_debug()

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (7): 1. Automated Setup & Diagnostics, 2. API Key Configuration, 2. API Key Configuration & Environment Inheritance, 3. Starting the Local n8n Server, 4. Key Workflows & Agent Architecture, 5. Next Steps Checklist for Incoming Agents, AI Agent Workspace Onboarding Guide

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (9): main, main, main, connections, AI Dynamic Phase Calculator, AI Expert Report Generator, AI Weekly Digest Generator, Create Session 1 Task (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (17): 1. Master Google Sheet Schema, 1. Operational Context & Rationale, 2. Detailed Edge-Case & Operational Logic Rules, 2. Google Drive Folder & Permission Hierarchy, 3.1 Student Competency Growth Index, 3.2 Sponsor Alignment Index, 3.3 Cohort Success Velocity, 3. Asana Cohort Board Structure (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (5): calculate_milestones(), print_mock_prompt_templates(), IRC Student Workflow Mock & Verification Runner This script simulates the dynami, Simulates the dynamic milestone calculations based on Cohort Start Date and Dura, Displays the formatted prompts sent to AI nodes for validation.

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (5): active, name, nodes, settings, executionTimeout

### Community 9 - "Community 9"
Cohesion: 0.70
Nodes (4): check_command(), log(), main(), run_cmd()

### Community 10 - "Community 10"
Cohesion: 0.20
Nodes (14): audit_document(), call_gemini(), log_debug(), call_gemini(), check_alignment(), log_debug(), call_llm(), log_debug() (+6 more)

### Community 11 - "Community 11"
Cohesion: 0.17
Nodes (11): 1. Executive Summary, 2.1 Parity (Score: 8/10), 2.2 Granularity & Primitives (Score: 9/10), 2.3 Composability & Emergent Capability (Score: 9/10), 2.4 Accumulated Context / Memory (Score: 10/10), 2. Core Principles Scorecard, 3.1 The Shared Workspace Pattern, 3.2 Cardinal Sin Prevention Check (+3 more)

### Community 14 - "Community 14"
Cohesion: 0.83
Nodes (3): call_gemini(), log_debug(), parse_transcript()

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (10): Cohort Dashboard & Reporting, Daily Monitor & Auditing, India Research Corps Strategy, Key metrics, Marketing, Onboarding Automation, Our approach, Target problem (+2 more)

## Knowledge Gaps
- **101 isolated node(s):** `name`, `nodes`, `main`, `main`, `main` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `connections` connect `Community 5` to `Community 8`, `Community 12`, `Community 13`, `Community 16`, `Community 17`, `Community 19`, `Community 20`, `Community 21`, `Community 22`, `Community 23`, `Community 25`, `Community 26`, `Community 27`, `Community 28`, `Community 29`, `Community 31`, `Community 32`, `Community 33`, `Community 34`, `Community 35`, `Community 36`, `Community 37`, `Community 38`, `Community 39`, `Community 40`, `Community 41`, `Community 42`, `Community 43`, `Community 44`, `Community 45`, `Community 46`, `Community 47`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `call_llm()` connect `Community 10` to `Community 3`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **What connects `name`, `nodes`, `main` to the rest of the system?**
  _104 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `Community 6` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._