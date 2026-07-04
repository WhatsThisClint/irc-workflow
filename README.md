# IRC Student Onboarding & Progress Tracking System

This repository contains the architecture and workflow configurations to automate the student onboarding, dynamic timeline tracking, and AI-driven mentorship evaluations for the India Research Corps (IRC) initiative by WELL Labs, Bangalore.

---

## 1. Master Google Sheet Schema

Configure your Master Google Sheet with the following headers in the first row. The system reads and updates this sheet daily.

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
| **J** | `Inception Cohort Start Date` | Date | `YYYY-MM-DD` (Triggers onboarding check) |
| **K** | `Inception Cohort End Date` | Date | Calculated: Start Date + 1 month (`YYYY-MM-DD`) |
| **L** | `Inception Presentation Date` | Date | `YYYY-MM-DD` (Date of pass/fail gate) |
| **M** | `Inception Gate Status` | Text | `Pass` / `Fail` / `Pending` |
| **N** | `Total Duration` | Number | Total duration in months (e.g. `6`, `8`, `10`) |
| **O** | `Fieldwork Timing Context` | Text | `Pre-monsoon` / `Post-monsoon` / `Both` |
| **P** | `Google Drive Shared Folder Link` | Link | Auto-filled by onboarding workflow |
| **Q** | `Google Drive Admin Folder Link` | Link | Auto-filled by onboarding workflow |
| **R** | `Reflection Google Doc Link` | Link | Auto-filled by onboarding workflow |
| **S** | `Current Project Phase` | Text | Auto-filled by daily monitor: `Induction`, `Gate Evaluation`, `Fieldwork`, `Mid-term Review`, `Thesis Drafting`, `Completed` |

---

## 2. Google Drive Folder & Permission Hierarchy

The onboarding workflow automatically creates the following nested structures under your root folder:

```
[Student Root Folder] (Admin-only access)
 ├── [Admin Only] (Admin-only access)
 │    ├── Sample Inception Report (AI-generated expert reference)
 │    └── Admin Cheat Sheet (AI-updated pre-meeting guide)
 ├── [Transcripts] (Admin-only access)
 │    └── Meeting Transcripts (imported from Granola AI)
 └── [Shared Space] (Shared with Student & Mentor)
      ├── [Student Name] - Inception Report (Google Doc copy of template)
      ├── [Student Name] - Gantt Chart (Spreadsheet for timeline customizations)
      └── [Reading Materials] (Shortcut or copy of reading files)
```

---

## 3. Asana Cohort Board Structure

*   The system operates inside a single **Master Asana Project** for the current cohort.
*   **Columns/Sections**: When a student is onboarded, the workflow creates a section named after the student (e.g., `[Student Name]`).
*   **Tasks**: Under the student's section, the following standard tasks are populated:
    1.  `Session 1: Introduction & Literature Review` (Due: Start + 5 days)
    2.  `Session 2: Problem Definition` (Due: Start + 10 days)
    3.  `Session 3: Methodology Design` (Due: Start + 15 days)
    4.  `Session 4: Data Requirements` (Due: Start + 20 days)
    5.  `Session 5: Fieldwork Plan` (Due: Start + 25 days)
    6.  `Session 6: Draft Inception Report` (Due: Start + 30 days)
    7.  `Inception Presentation Gate` (Due: Cohort End Date)
    8.  `Fieldwork Data Collection` (Due: Dynamic based on Gantt Chart)
    9.  `Mid-Term Progress Review` (Due: Mid-point of Total Duration)
    10. `Final Thesis Submission` (Due: End of Total Duration)

---

## 4. How to Import the n8n Workflow

1. Open your n8n workspace (typically `http://localhost:5678`).
2. Click **Workflows** -> **Add Workflow** -> **Import from File**.
3. Select the consolidated master workflow file:
   *   `irc_master_workflow.json` (located under `n8n/workflows/`)
4. Set up the credentials in n8n for:
   *   **Google Sheets** (OAuth2 / Service Account)
   *   **Google Drive** (OAuth2 / Service Account)
   *   **Google Docs** (OAuth2 / Service Account)
   *   **Google Calendar** (OAuth2 / Service Account)
   *   **Gmail** (OAuth2 / Service Account)
   *   **Asana** (Personal Access Token or OAuth2)
5. Fill in the global variables in n8n settings (or via the environment file) for the template document IDs and parent folder IDs.

