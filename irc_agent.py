import os
import sys
import json
import urllib.request
import argparse
from datetime import datetime

# Force UTF-8 encoding for stdout/stderr to prevent CP1252 console crashes on Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] {msg}", file=sys.stderr)

def call_gemini(prompt, response_mime_type="text/plain"):
    """
    Direct HTTPS call to the Gemini API using Python's standard library.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        log_debug("Error: GEMINI_API_KEY not found.")
        print(json.dumps({"error": "GEMINI_API_KEY environment variable not found."}))
        sys.exit(1)
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "responseMimeType": response_mime_type
        }
    }
    
    log_debug(f"Sending request to Gemini API (URL: {url})...")
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode("utf-8"), 
            headers=headers, 
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            log_debug("Request sent. Reading response...")
            res_data = json.loads(response.read().decode("utf-8"))
            log_debug("Response decoded successfully.")
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        log_debug(f"Error occurred: {str(e)}")
        print(json.dumps({"error": f"Failed to connect to Gemini API: {str(e)}"}))
        sys.exit(1)

def generate_baseline(student_name, question, problem, degree_level, duration_months):
    """
    Generates a full, domain-expert baseline Inception Report tailored to degree level and duration.
    """
    prompt = f"""
You are a senior socio-hydrology and water systems expert at WELL Labs, Bangalore.
Your task is to conduct deep research and write a highly thorough, professional, baseline Inception Report for a Master's thesis student named '{student_name}'.
The research question is: '{question}'
The problem statement is: '{problem}'

This Inception Report serves as the baseline technical reference for the program coordinator. It must be written from the perspective of an expert doing the actual work, detailing the exact methodologies, frameworks, data parameters, and risk mitigations.

ADJUST THE COHORT RIGOR ACCORDING TO:
1. Degree Level: {degree_level}
   - BSc: Focus on basic field feasibility, simple surveys, direct physical measurements, and a clear, descriptive approach.
   - MSc: Require robust data triangulation (primary and secondary comparison), statistical analyses, and structured socio-economic interviews.
   - PhD: Require high theoretical novelty, advanced mathematical or system dynamics modeling, extensive literature review, and academic publication readiness.
2. Program Duration: {duration_months} months
   - Adjust the complexity of the data collection and literature review proportionally. A longer program (10 months) requires deeper research and longer observation cycles; a shorter program (6 months) must prioritize rapid execution and immediate fieldwork tasks.

Follow the exact template structure below:

# Inception Report: {question}
**Prepared by**: AI Research Advisor (WELL Labs)
**Student**: {student_name} (Degree: {degree_level}, Duration: {duration_months} Months)
**Date**: {datetime_now()}

## 1. Context & Literature Review Scope
- Provide a robust background on this problem within India's socio-hydrological context.
- Identify the key academic literatures, legal acts/policies, and historical datasets required.

## 2. Research Conceptual Model
- Detail the core system variables (natural, social, and economic).
- Outline how these variables interact (e.g. extraction rates vs. agricultural crop choices vs. groundwater table).

## 3. Data Collection Methodology
- Define the exact field methods (e.g. household interviews, borewell monitoring, crop mapping).
- Specify sample sizes, target demographics, and geographic selection criteria.
- Create a Data Requirements Matrix: list variables, frequency, and source type (primary/secondary).

## 4. Fieldwork Timeline & Seasonal Considerations
- Outline the fieldwork plan.
- Explicitly detail monsoon dependencies (pre-monsoon baseline vs. post-monsoon readings) and how it affects the timetable.

## 5. Potential Constraints & Risk Mitigation
- Identify community trust barriers, seasonal accessibility limits, and data reliability risks.
- Propose mitigation strategies for each.
"""
    return call_gemini(prompt)

def audit_doc(student_report_text, baseline_report_text, degree_level, duration_months):
    """
    Compares the student's active report against the AI baseline, and audits the mentor's feedback.
    """
    prompt = f"""
You are an Academic Director auditing a student's thesis progress.
Below are two documents:
1. The AI-generated Baseline Inception Report (benchmark standards):
{baseline_report_text}

2. The Student's current Inception Report (collaboratively written by the student and mentor):
{student_report_text}

Analyze and compare the two reports. Your job is to identify technical gaps in the student's work and evaluate the mentor's contributions.

EVALUATE ACCORDING TO PROPORTIONAL RIGOR:
- Degree Level: {degree_level} (BSc: basic field feasibility; MSc: methodological rigor; PhD: modeling complexity and publication novelty).
- Program Duration: {duration_months} months (shorter cycles favor rapid fieldwork; longer cycles favor exhaustive literature and deep monitoring).

Provide your evaluation in a JSON structure containing:
1. "critique": A detailed summary of technical gaps in the student's report compared to the baseline.
2. "mentor_score": A rating from 1 to 10 of the mentor's engagement based on active and resolved comments/edits found in the text (1 = ghosting/no feedback; 10 = deep, rigorous methodology guidance).
3. "mentor_critique": Evaluation of the mentor's input. Are they catching methodology gaps or slacking off on minor formatting?
4. "reflection_questions": A list of 3-4 specific, high-leverage reflection questions to ask BOTH the student and the mentor during the weekly meeting to test their alignment and logic.

Output the result strictly as a valid JSON object matching this schema:
{{
  "critique": "string",
  "mentor_score": 8,
  "mentor_critique": "string",
  "reflection_questions": ["string", "string", "string"]
}}
"""
    return call_gemini(prompt, response_mime_type="application/json")

def parse_transcript(transcript_text):
    """
    Parses a meeting transcript and extracts actionable tasks for Student, Mentor, and Coordinator.
    Filters out minor discussion points to prevent Asana clutter.
    """
    prompt = f"""
You are an Operations Analyst tracking thesis progress.
Read the following meeting transcript:
"{transcript_text}"

Extract all substantive, actionable action items discussed. Skip minor discussion points, administrative updates, or casual chatter.
Classify each task by assignee (STUDENT, MENTOR, or COORDINATOR).
For each task, provide:
1. "task_name": A short name (e.g., "Draft fieldwork questionnaire").
2. "details": A clear explanation of what needs to be done.
3. "due_date": The due date (formatted as YYYY-MM-DD) if mentioned or inferred relative to today, otherwise set to null.

Output the result strictly as a JSON object matching this schema:
{{
  "tasks": [
    {{
      "assignee": "STUDENT",
      "task_name": "string",
      "details": "string",
      "due_date": "string or null"
    }}
  ]
}}
"""
    return call_gemini(prompt, response_mime_type="application/json")

def calculate_phase(gantt_json_file, cohort_start_date_str, duration_months):
    """
    Evaluates current project phase using Gantt dates. Falls back to elapsed calendar time.
    """
    today = datetime.now()
    log_debug(f"Calculating phase. Today: {today.strftime('%Y-%m-%d')}, Cohort Start: {cohort_start_date_str}, Duration: {duration_months} Months")
    
    # Attempt to parse Gantt JSON first
    gantt_data = None
    if gantt_json_file:
        try:
            with open(gantt_json_file, "r", encoding="utf-8") as f:
                gantt_data = json.load(f)
            log_debug("Successfully loaded Gantt JSON file.")
        except Exception as e:
            log_debug(f"Gantt file parse error (will use calendar fallback): {str(e)}")
            
    # If Gantt data is available, check active phase
    if gantt_data:
        try:
            # We assume Gantt JSON represents rows of task schedules:
            # [{"task_name": "...", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}]
            # We locate the task covering today's date
            for row in gantt_data:
                task = row.get("task_name", "")
                start_str = row.get("start_date") or row.get("start")
                end_str = row.get("end_date") or row.get("end")
                if start_str and end_str:
                    start_dt = datetime.strptime(start_str.split("T")[0], "%Y-%m-%d")
                    end_dt = datetime.strptime(end_str.split("T")[0], "%Y-%m-%d")
                    if start_dt <= today <= end_dt:
                        log_debug(f"Today falls within Gantt task: '{task}'")
                        if "induction" in task.lower() or "literature" in task.lower():
                            return "Induction"
                        elif "fieldwork" in task.lower() or "data collection" in task.lower() or "survey" in task.lower():
                            return "Fieldwork"
                        elif "mid-term" in task.lower() or "review" in task.lower():
                            return "Mid-term Review"
                        elif "drafting" in task.lower() or "writing" in task.lower() or "thesis" in task.lower():
                            return "Thesis Drafting"
                        elif "complete" in task.lower() or "submit" in task.lower():
                            return "Completed"
            log_debug("No current active task found in Gantt chart rows.")
        except Exception as e:
            log_debug(f"Error parsing Gantt rows: {str(e)}")
            
    # Fallback: elapsed calendar time calculation
    try:
        start_date = datetime.strptime(cohort_start_date_str.split("T")[0], "%Y-%m-%d")
        delta_months = (today.year - start_date.year) * 12 + today.month - start_date.month
        log_debug(f"Calendar fallback: {delta_months} months elapsed since start.")
        
        if delta_months <= 1:
            return "Induction"
        elif delta_months >= duration_months:
            return "Completed"
        elif delta_months >= (duration_months - 1):
            return "Thesis Drafting"
        elif delta_months >= (duration_months // 2):
            return "Mid-term Review"
        else:
            return "Fieldwork"
    except Exception as e:
        log_debug(f"Calendar fallback error: {str(e)}")
        return "Induction"

def datetime_now():
    return datetime.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRC AI Workflow Agent")
    parser.add_argument("--action", required=True, choices=["generate-baseline", "audit-doc", "parse-transcript", "calculate-phase"])
    parser.add_argument("--student", help="Student name")
    parser.add_argument("--question", help="Research question")
    parser.add_argument("--problem", help="Problem statement")
    parser.add_argument("--degree-level", default="MSc", help="BSc / MSc / PhD")
    parser.add_argument("--duration-months", type=int, default=6, help="6 / 8 / 10 months")
    parser.add_argument("--student-report-file", help="Path to student's report text file")
    parser.add_argument("--baseline-report-file", help="Path to baseline report text file")
    parser.add_argument("--transcript-file", help="Path to transcript text file")
    parser.add_argument("--gantt-file", help="Path to Gantt Chart JSON file")
    parser.add_argument("--cohort-start-date", help="Cohort start date YYYY-MM-DD")
    
    args = parser.parse_args()
    log_debug(f"Starting action: {args.action}")
    
    if args.action == "generate-baseline":
        if not args.student or not args.question or not args.problem:
            print(json.dumps({"error": "Missing parameters for generate-baseline."}))
            sys.exit(1)
        output = generate_baseline(args.student, args.question, args.problem, args.degree_level, args.duration_months)
        print(output)
        
    elif args.action == "audit-doc":
        if not args.student_report_file or not args.baseline_report_file:
            print(json.dumps({"error": "Missing file paths for audit-doc."}))
            sys.exit(1)
        try:
            with open(args.student_report_file, "r", encoding="utf-8") as f:
                student_text = f.read()
            with open(args.baseline_report_file, "r", encoding="utf-8") as f:
                baseline_text = f.read()
            output = audit_doc(student_text, baseline_text, args.degree_level, args.duration_months)
            print(output)
        except Exception as e:
            print(json.dumps({"error": f"Failed to read files: {str(e)}"}))
            sys.exit(1)
            
    elif args.action == "parse-transcript":
        if not args.transcript_file:
            print(json.dumps({"error": "Missing transcript-file for parse-transcript."}))
            sys.exit(1)
        try:
            with open(args.transcript_file, "r", encoding="utf-8") as f:
                transcript_text = f.read()
            output = parse_transcript(transcript_text)
            print(output)
        except Exception as e:
            print(json.dumps({"error": f"Failed to read transcript file: {str(e)}"}))
            sys.exit(1)
            
    elif args.action == "calculate-phase":
        if not args.cohort_start_date:
            print(json.dumps({"error": "Missing cohort-start-date for calculate-phase."}))
            sys.exit(1)
        output = calculate_phase(args.gantt_file, args.cohort_start_date, args.duration_months)
        print(output)
