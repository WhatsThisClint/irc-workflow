# CLAUDE.md (IRC Workflow Memory Bank)

This file contains the persistent architectural context, commands, design decisions, and edge-case resolution rules for the India Research Corps (IRC) Workflow Automation system. Read this first when resuming work in this workspace on any machine.

---

## 1. Project Overview
The IRC Workflow Automation coordinates environment-science student onboarding, dynamic milestone calculations, Google Doc edits, and Granola AI transcript audits for WELL Labs, Bangalore. It uses **n8n** locally for execution and a local Python agent (**Gemini 3.5 Flash**) for AI logic.

---

## 2. Porting & Copy-Pasting to Another PC
To migrate this entire system to another PC:
1. **Copy the Folder**: Simply copy the entire `IRC Workflow/` folder to the target machine.
2. **What is Transferred**:
   - **Workflows & Configurations**: All n8n workflow models and connections.
   - **Local n8n User Data**: Because we run n8n pointing to `.n8n` in this workspace, all your imported workflows, custom nodes, credentials, and settings are saved inside `IRC Workflow/.n8n` and transfer *intact*.
   - **Local AI Agent**: `irc_agent.py` and the test scripts.
3. **Setup on New PC**:
   - Install Python 3.10+.
   - Set the system environment variable: `GEMINI_API_KEY` to your Google AI Studio API key.
   - Run the startup command to launch n8n.

---

## 3. Development Commands

### Starting n8n Server (Local)
Always run n8n pointing to the local `.n8n` directory to keep settings self-contained:
```powershell
$env:N8N_USER_FOLDER="f:\Antigravity\IRC Workflow\.n8n"; .\node_modules\.bin\n8n start
```

### Running the Python AI Agent
The Python script `irc_agent.py` is invoked by n8n to execute Gemini 3.5 Flash queries. You can test it locally via shell:
```bash
# Generate Baseline Report
python irc_agent.py --action generate-baseline --student "Rahul" --question "Rainfall patterns" --problem "Borewell extraction rates rising" --degree-level "MSc" --duration-months 8

# Audit Student Document
python irc_agent.py --action audit-doc --student-report-file "path/to/student_doc.txt" --baseline-report-file "path/to/baseline.txt" --degree-level "PhD" --duration-months 10

# Parse Granola AI Transcript
python irc_agent.py --action parse-transcript --transcript-file "path/to/transcript.txt"

# Calculate Project Phase
python irc_agent.py --action calculate-phase --cohort-start-date "2026-07-01" --duration-months 8 --gantt-file "path/to/gantt.json"
```

---

## 4. Folder & File Structure
```
f:/Antigravity/IRC Workflow
 ├── n8n/
 │    └── workflows/
 │         └── irc_master_workflow.json (Consolidated Onboarding + Monitor branches)
 ├── .n8n/                               (Self-contained n8n database & credentials)
 ├── docs/
 │    └── brainstorms/
 │         └── 2026-07-04-irc-workflow-scaling-requirements.md
 ├── irc_agent.py                        (Local Gemini 3.5 Flash python agent)
 ├── test_workflow_mock.py               (Local math/dates validator)
 ├── README.md                           (Master sheet schemas & folder permissions)
 └── CLAUDE.md                           (This context preservation file)
```

---

## 5. Key Design Decisions & Resolved Edge Cases

* **Google Drive Prefixing**: Workspace folders are named `[S.No] - [Student Name] - IRC Workspace` to prevent folder collisions if two students share the same name.
* **Exit on Gate Failure**: If `Inception Gate Status` is marked as `Fail`, the workflow archives their Asana section, limits Drive folders to **Read-Only** access for student/mentor (retaining admin access), and drafts an exit email in your Gmail Drafts.
* **Proportional Grading Criteria**: The AI baseline generator and report auditor adjust their expectations based on **both** the Degree Level (BSc: basic feasibility; MSc: data triangulation; PhD: mathematical modeling/novelty) and Program Duration (6 vs. 10 months).
* **Missing Transcript Nudges**: The workflow cross-references Google Calendar past sync events with files inside the `Transcripts` folder. If a meeting occurred but no Granola AI transcript is uploaded within 48 hours, it flags the dashboard and emails a reminder to the student.
* **Reschedules & Cancellations**: Checks the active calendar event status, avoiding false alerts for meetings that were postponed or declined.
* **Asana Due Date Cascades**: If a due date is shifted in Asana, the monitor shifts subsequent dependent tasks dynamically and logs the delay slippage to Airtable.
* **Cumulative Delay Escalation**: If a student accumulates more than 14 days of total task delay, an immediate Gmail alert is sent to your inbox.
* **Transcript Clean Tasking**: Filters out minor chatter, creating separate Asana tasks only for major milestones, while summarizing minor notes inside a single description.
* **Transition De-duplication**: The workflow queries the active state in Airtable before running Pass/Fail actions, preventing duplicate sync invites or double-archiving.
