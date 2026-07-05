# Operational Edge Case Playbook

This document details the operational logic, trigger conditions, and parameters behind the 16 specialized rules implemented in the IRC Workflow system to handle real-world operational edge cases.

---

## 1. Onboarding & Drive Structure Rules

### Rule 1: Unique Workspace Folder Naming
*   **Trigger**: Onboarding flow initiation.
*   **Logic**: Drive folders are prefixed with the student's Master Sheet Serial Number: `[S.No] - [Student Name] - IRC Workspace` (e.g., `002 - Priya Sen - IRC Workspace`).
*   **Rationale**: Prevents name collision errors in Google Drive searches when multiple students share common names.

### Rule 2: Inception Gate Rejection (Fail Transition)
*   **Trigger**: `Inception Gate Status` in the Master Sheet changes to `Fail`.
*   **Logic**:
    *   **Asana Board**: Locates the student's board section and archives it immediately to prevent dashboard clutter.
    *   **Google Drive**: Changes the student and mentor shared folder permissions to **Read-Only** (retaining full access for the Coordinator Admin).
    *   **Gmail**: Drafts and saves an exit/rejection email in the Coordinator's Gmail Drafts folder.
*   **Rationale**: Retains the historical evidence and student contributions as an unalterable audit trail while freeing up coordinator resources.

---

## 2. Calendar, Transcript, & Meeting Rules

### Rule 3: Missing Meeting Transcripts
*   **Trigger**: Run daily. Cross-references completed Google Calendar events with files inside the student's `Transcripts` Drive folder.
*   **Logic**: If an event has passed but no transcript file (`.txt`/`.md`) is uploaded within **48 hours**, n8n logs a warning on the dashboard and sends a polite reminder email to the student.
*   **Rationale**: Ensures that transcripts (from Granola AI or manual notes) are captured immediately while the meeting context is fresh.

### Rule 4: Calendar Sync Filter
*   **Trigger**: Daily calendar scanner.
*   **Logic**: Queries Calendar events but filters out status updates marked as `cancelled`, `declined`, or `rescheduled`.
*   **Rationale**: Prevents generating false warnings for meetings that were postponed or declined.

### Rule 5: Transcript Format Validation
*   **Trigger**: Transcript uploader event.
*   **Logic**: Validates file extension. If the student uploads a `.docx`, `.pdf`, or audio file, n8n sends an automated email requesting a re-export in plain text (`.txt` or `.md`).
*   **Rationale**: The Python parser requires clean plain text to avoid PDF/Docx formatting parsing errors.

---

## 3. Document Auditing & Feedback Memory Rules

### Rule 6: Google Doc Edit Conflicts
*   **Trigger**: Daily document auditor run at **2:00 AM**.
*   **Logic**: The audit runs when students are offline. If the document URL is unreachable or deleted, the system flags a "Doc Missing" alert on the dashboard.
*   **Rationale**: Avoids overwrite conflicts and ensures the agent evaluates stabilized drafts.

### Rule 7: Mentor Comment Retrieval
*   **Trigger**: Daily monitor comment check.
*   **Logic**: Queries the Google Docs API for both `active` and `resolved` comment threads.
*   **Rationale**: Provides a complete view of mentor-student engagement history, ensuring resolved feedback is factored into the mentor responsiveness score.

### Rule 8: Coordinator Persistent Memory Consolidation
*   **Trigger**: Sub-agent auditor initialization.
*   **Logic**: If the accumulated coordinator corrections in `memory.json` exceed **1500 characters**, the agent invokes Gemini/Claude/OpenAI to compress and summarize the history into a concise list of rules (`consolidated_rules`).
*   **Rationale**: Avoids context limit overflows and token waste by keeping the prompts focused on active guidelines.

---

## 4. Timeline, Scheduling, & Escalation Rules

### Rule 9: Asana Due Date Cascades
*   **Trigger**: A due date is changed on an active task in Asana.
*   **Logic**: Logs the delay delta in Airtable and automatically pushes the due dates of all dependent future tasks forward by the same number of days.
*   **Rationale**: Maintains timeline alignment and reflects realistic graduation/completion dates automatically.

### Rule 10: Cumulative Delay Escalations
*   **Trigger**: Delay tracking scanner.
*   **Logic**: If the accumulated delays across a student's tasks exceed **14 days**, the system bypasses standard warnings and sends an immediate Gmail escalation alert to the Coordinator.
*   **Rationale**: Prompts immediate human intervention before the project slips beyond recovery.

### Rule 11: Gantt Chart Parsing Fallback
*   **Trigger**: Gantt parsing action.
*   **Logic**: If the student's customized Gantt spreadsheet is deleted or corrupted, the system falls back to calculating the project phase based on elapsed calendar time from the `Cohort Start Date` and raises a warning.
*   **Rationale**: Prevents workflow execution failures and ensures continuous monitoring.

### Rule 12: Asana Board Clutter Prevention
*   **Trigger**: Transcript parse execution.
*   **Logic**: The agent filters out minor conversational topics, creating separate Asana tasks only for major deliverables, while listing minor notes in the sync task's description.
*   **Rationale**: Keeps the task board clean and actionable.

### Rule 13: Transition De-duplication
*   **Trigger**: Student status monitor.
*   **Logic**: Queries the student's status flag in Airtable before running onboarding or exit commands. If the status matches the current transition, it is skipped.
*   **Rationale**: Prevents duplicate calendar invites or multiple email drafts.

---

## 5. Reporting & Archive Rules

### Rule 14: Daily Admin Summary Email
*   **Trigger**: Every morning at **8:00 AM**.
*   **Logic**: Compiles all daily audit scores, red flags, and extracted action items, and sends a single, consolidated HTML email digest to the Coordinator's Gmail.
*   **Rationale**: Provides the Coordinator with a quick review list at the start of the workday.

### Rule 15: Database Size Pruning & CSV Archiving
*   **Trigger**: Student graduation or exit transition complete.
*   **Logic**: Exports the student's records from Airtable into a CSV file saved in the secure Google Drive Admin folder, then deletes the active rows in Airtable.
*   **Rationale**: Adheres to free-tier storage limits while preserving full historical records.

### Rule 16: Weekly Director Digest
*   **Trigger**: Every Friday at **5:00 PM**.
*   **Logic**: Aggregates all daily metrics logged to Airtable over the past 7 days and compiles a cohort-level executive markdown report detailing success velocity, competency growth trajectory, and sponsor alignment.
*   **Rationale**: Facilitates immediate leadership reviews and provides metrics to include in funding updates.
