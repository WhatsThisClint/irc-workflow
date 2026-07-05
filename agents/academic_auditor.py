import os
import sys
import json
from agents.llm_client import call_llm


def log_debug(msg):
    print(f"[DEBUG] [AcademicAuditor] {msg}", file=sys.stderr)

import re

def detect_session_number(student_text, file_path=""):
    filename = os.path.basename(file_path).lower()
    for m in re.finditer(r'(?:session|module|reflection)\D*([1-6])', filename):
        return int(m.group(1))
    content_snippet = student_text[:1000].lower()
    for m in re.finditer(r'(?:session|module|reflection)\D*([1-6])', content_snippet):
        return int(m.group(1))
    return None

def audit_document(student_text, baseline_text, degree_level, duration_months, memory_text, student_file=""):
    session_num = detect_session_number(student_text, student_file)
    rubrics_text = ""
    if session_num:
        workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rubrics_path = os.path.join(workspace_dir, "docs", "resources", "session_rubrics.json")
        if os.path.exists(rubrics_path):
            try:
                with open(rubrics_path, "r", encoding="utf-8") as f:
                    rubrics_data = json.load(f)
                    session_key = str(session_num)
                    if session_key in rubrics_data:
                        info = rubrics_data[session_key]
                        concepts = "\n".join(f"- {c}" for c in info.get("core_concepts", []))
                        rules = "\n".join(f"- {r}" for r in info.get("grading_rubrics", []))
                        rubrics_text = f"Module: {info.get('module_name')}\nCore Concepts expected:\n{concepts}\n\nSpecific Reflection Rubrics:\n{rules}"
                        log_debug(f"Loaded dynamic rubric expectations for Session {session_num}")
            except Exception as e:
                log_debug(f"Warning: Could not parse session rubrics cache: {e}")

    prompt = f"""
You are an Academic Director auditing a student's thesis progress.
Below are the reference files:

1. The AI-generated Baseline Inception Report (benchmark standards):
{baseline_text}

2. The Student's current Inception Report:
{student_text}

3. Coordinator's Past Corrections & Feedback Memory:
{memory_text if memory_text else "No past feedback logged."}

4. Session-Specific Rubrics (Syllabus Constraints):
{rubrics_text if rubrics_text else "No specific session rubrics loaded (using default benchmarks)."}

Analyze and compare the documents. Assess progress and identify technical gaps.
Your critique MUST incorporate and respect the Coordinator's Past Corrections (if any are present in the memory).
If session rubrics are loaded above, verify if the student has integrated those specific concepts.

EVALUATE ACCORDING TO PROPORTIONAL RIGOR:
- Degree Level: {degree_level} (BSc: basic feasibility; MSc: methodological rigor; PhD: modeling complexity and publication novelty).
- Program Duration: {duration_months} months (shorter cycles favor rapid fieldwork; longer cycles favor exhaustive literature).

Output the result strictly as a valid JSON object matching this schema:
{{
  "critique": "A detailed summary of technical gaps in the student's report compared to the baseline and your feedback memory.",
  "reflection_questions": ["A list of 3-4 specific, high-leverage reflection questions to ask the student during the weekly sync."],
  "competency_scores": {{
    "scientific_methodology": 8, // Integer score from 1 to 10
    "data_triangulation": 7, // Integer score from 1 to 10
    "academic_writing_clarity": 8 // Integer score from 1 to 10
  }}
}}
"""
    log_debug("Calling LLM client for document audit...")
    return call_llm(prompt, json_mode=True)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(json.dumps({"error": "Missing parameters"}))
        sys.exit(1)
        
    student_file = sys.argv[1]
    baseline_file = sys.argv[2]
    degree = sys.argv[3]
    duration = int(sys.argv[4])
    memory_file = sys.argv[5]
    
    try:
        with open(student_file, "r", encoding="utf-8") as f:
            student_text = f.read()
        with open(baseline_file, "r", encoding="utf-8") as f:
            baseline_text = f.read()
            
        memory_text = ""
        if memory_file and os.path.exists(memory_file):
            with open(memory_file, "r", encoding="utf-8") as f:
                memory_data = json.load(f)
                memory_text = memory_data.get("consolidated_rules") or memory_data.get("feedback", "")
                
        output_str = audit_document(student_text, baseline_text, degree, duration, memory_text, student_file)
        # Parse and inject status envelopes to make auditing robust
        res = json.loads(output_str)
        res["status"] = "success"
        res["error"] = None
        print(json.dumps(res))
    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e), "critique": f"Academic Auditor Error: {str(e)}", "reflection_questions": [], "competency_scores": {"scientific_methodology": 5, "data_triangulation": 5, "academic_writing_clarity": 5}}))
        sys.exit(1)


