# India Research Corps (IRC) Student Tracking & Onboarding System

This repository contains the production-ready workflow models, local AI agent configurations, and operational schemas to automate student onboarding, progress auditing, and funding metrics calculation for the **India Research Corps (IRC)** program at **WELL Labs, Bangalore**.

---

## 1. Operational Context & Rationale

### The India Research Corps (IRC) Program
The IRC program brings together postgraduate and doctoral students from home universities and matches them with sponsoring **Client/Partner Agencies** to solve critical environmental water problems (socio-hydrology). 

Because the program is scaling rapidly, the Coordinator needs automated, real-time insights to answer:
1.  *Are the students' methodologies scientifically rigorous and actually answering the sponsor's problem?*
2.  *Are mentors providing high-quality, substantive engagement, or are they ghosting?*
3.  *Where are the bottleneck delay points in the curriculum?*
4.  *How do we quantitatively prove student capability growth and research value to secure future program funding?*

To solve this, this system integrates **n8n** locally with a **multi-agent Python system** powered by **Gemini 3.5 Flash** to manage the entire cohort cycle.

---

## 2. Detailed Edge-Case & Operational Logic Rules

The system implements 16 specific rules to handle real-world operational challenges:

1.  **Unique Workspace Folder Naming**: Student folders are named `[S.No] - [Student Name] - IRC Workspace` (e.g., `003 - Rahul Dev - IRC Workspace`). Using the Master Sheet Serial Number guarantees uniqueness and prevents collisions if two students share common names.
2.  **Inception Gate Rejection (Fail State)**: If a student's `Inception Gate Status` is marked `Fail` by the coordinator:
    *   The student's Asana board section is archived immediately to keep the active dashboard clean.
    *   Google Drive permissions are revoked for the student and mentor, shifting folders to **Read-Only** to preserve audit trails.
    *   A draft rejection email is saved in Gmail Drafts for coordinator review.
3.  **Missing Meeting Transcripts**: The system cross-references Google Calendar past events against uploaded files in the student's `Transcripts` folder. If a sync occurred but no Granola AI transcript is uploaded within **48 hours**, it alerts the dashboard and emails the student.
4.  **Calendar Sync Filter**: Scans active Google Calendar event status, ignoring cancelled, declined, or rescheduled slots to prevent false alerts for delayed meetings.
5.  **Transcript Format Validation**: The system accepts only `.txt` and `.md` plain text files for meeting transcripts. If a student drops a `.docx` or `.pdf` file, it emails them requesting a text re-export.
6.  **Google Doc Edit Conflicts**: The document audit runs daily at **2:00 AM** when students are inactive. If the doc link is deleted or invalid, it flags a "Doc Missing" warning on the Dashboard.
7.  **Mentor Comment Retrieval**: Queries both active and resolved comments from the Docs API, ensuring a complete historical record of mentor feedback.
8.  **Asana Due Date Cascades**: If a student or mentor shifts a due date in Asana, the monitor logs the delay in Airtable and automatically shifts all dependent future tasks by the same delta.
9.  **Cumulative Delay Escalations**: If a student's total task delay exceeds **14 days**, an immediate Gmail escalation alert is sent to the coordinator.
10. **Proportional Academic Rigor**: The AI baseline generator and report auditor adjust evaluations proportionally:
    *   *Degree Level*: BSc (focus on basic field feasibility), MSc (requires robust data triangulation), PhD (demands theoretical novelty and publication depth).
    *   *Cohort Duration*: 6 months (prioritizes rapid field checks) vs. 10 months (demands exhaustive reporting).
11. **Asana Board Clutter Prevention**: The transcript parser extracts action items, creating separate Asana tasks only for substantive milestones. Minor notes are combined inside a single "Sync Notes" task description.
12. **Gate Transition De-duplication**: The daily monitor reads the active transition status in Airtable prior to execution. If a transition (Pass/Fail) has already been processed, it is skipped. This prevents duplicate sync invites or double-archiving.
13. **Gantt Chart Parsing Fallback**: If a student's personal Gantt Chart is unreadable or deleted, the workflow falls back to calculating the project phase based on elapsed calendar time from the `Cohort Start Date` and raises a warning.
14. **Daily Admin Report Delivery**: At **8:00 AM** every morning, n8n sends a consolidated HTML report to your Gmail inbox summarizing all active audits, newly parsed transcript tasks, and active red flags.
15. **Database Size Pruning & CSV Archiving**: At the end of each cohort cycle (once the graduation and exit transitions complete), the workflow exports all related record sheets, snapshot histories, and mentor audits from Airtable to a backup CSV file placed in your restricted Google Drive Admin folder, then clears those rows in Airtable to maintain free plan tier limits.
16. **Weekly Director Digest**: At **5:00 PM** every Friday, the workflow compiles and delivers a cohort-level executive summary of average student competency triad score changes, phase-level bottlenecks, and active red flags to the coordinator's Gmail, facilitating a quick review session before subsequent cohort scheduling.

---

## 3. Funding & Impact Metrics Framework

To provide compelling proof of impact for future funding proposals, the system automatically aggregates and visualizes three key dimensions:

### 3.1 Student Competency Growth Index
For every audit, the AI Academic Auditor rates the student's document on the **Core Academic Triad** on a scale of 1-10:
*   **Scientific Methodology**: Rationale and execution feasibility.
*   **Data Triangulation**: Comparison of primary measurements with secondary literature.
*   **Academic Writing Clarity**: Structure, formatting, and logical flow.
*   *KPI*: Logs the trajectory and calculates the delta/growth slope from Month 1 to Final Thesis.

### 3.2 Sponsor Alignment Index
An AI Partner Engagement Lead compares the student's research against the sponsor's original problem statement, outputting an **Alignment Index (1-100%)** and critique. This is run at:
*   **Month 1 Inception Gate**: To catch and correct research drift early.
*   **Final Thesis Submission**: To prove direct real-world alignment and value to the sponsor.

### 3.3 Cohort Success Velocity
Tracks total delay days categorized by cohort phase (Induction, Fieldwork, Thesis) and compares current averages against historical cohort baselines to display process maturity.

---

## 4. Master Google Sheet Schema

| Column Letter | Header Name | Type | Description / Options |
|---|---|---|---|
| **A** | `S.No` | Text / Number | Auto-incrementing Serial Number |
| **B** | `Student Name` | Text | First and Last name of the student |
| **C** | `College` | Text | Home university or college of the student |
| **D** | `Degree Level` | Text | `BSc` / `MSc` / `PhD` |
| **E** | `Research Question` | Text | The specific research question assigned to the student |
| **F** | `Client / Partner Agency` | Text | The agency/organization sponsoring or requiring the research |
| **G** | `Problem Statement` | Text | Background on the problem the student is trying to solve |
| **H** | `Interview Date` | Date | `YYYY-MM-DD` |
| **I** | `Enrollment Date` | Date | `YYYY-MM-DD` |
| **J** | `Inception Cohort Start Date` | Date | `YYYY-MM-DD` |
| **K** | `Inception Cohort End Date` | Date | Calculated: Start Date + 1 month (`YYYY-MM-DD`) |
| **L** | `Inception Presentation Date` | Date | `YYYY-MM-DD` (Date of pass/fail gate) |
| **M** | `Inception Gate Status` | Text | `Pass` / `Fail` / `Pending` |
| **N** | `Total Duration` | Number | Total duration in months (e.g. `6`, `8`, `10`) |
| **O** | `Fieldwork Timing Context` | Text | `Pre-monsoon` / `Post-monsoon` / `Both` |
| **P** | `Google Drive Shared Folder Link` | Link | Auto-filled by onboarding workflow |
| **Q** | `Google Drive Admin Folder Link` | Link | Auto-filled by onboarding workflow |
| **R** | `Reflection Google Doc Link` | Link | Auto-filled by onboarding workflow |
| **S** | `Current Project Phase` | Text | Auto-filled by daily monitor: `Induction`, `Fieldwork`, `Thesis Drafting`, `Completed` |

---

## 5. Google Drive Folder & Permission Hierarchy

```
[Student Root Folder] (Admin-only access)
 ├── [Admin Only] (Admin-only access)
 │    ├── Sample Inception Report (AI-generated expert reference)
 │    ├── Admin Cheat Sheet (AI-updated pre-meeting guide)
 │    └── memory.json (AI persistent feedback memory)
 ├── [Transcripts] (Admin-only access)
 │    └── Meeting Transcripts (imported from Granola AI)
 └── [Shared Space] (Shared with Student & Mentor)
      ├── [Student Name] - Inception Report (Google Doc copy of template)
      ├── [Student Name] - Gantt Chart (Spreadsheet for timeline customizations)
      └── [Reading Materials] (Shortcut or copy of reading files)
```

---

## 6. How to Import the n8n Master Workflow

1. Open your n8n workspace (typically `http://localhost:5678`).
2. Click **Workflows** -> **Add Workflow** -> **Import from File**.
3. Select the consolidated master workflow file:
   *   **`n8n/workflows/irc_master_workflow.json`**
4. Set up the credentials in n8n for:
   *   **Google Sheets**, **Google Drive**, **Google Docs**, **Google Calendar**, **Gmail**, and **Asana**.
5. Fill in the global variables in n8n settings for the template document IDs and parent folder IDs.

---

## 7. Graphify Database

The **`graphify-out/`** folder contains the dedicated knowledge graph built for the `IRC Workflow` codebase, mapping the relationship between scripts, agents, and configurations.
*   Incoming AI agents can read the files inside `graphify-out/` (`graph.json`, `GRAPH_REPORT.md`) to instantly bootstrap their understanding of the workspace structure, classes, and logic.
*   To update the graph after editing code or documentation, run:
    ```bash
    graphify update .
    ```
