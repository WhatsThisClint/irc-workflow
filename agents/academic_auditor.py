import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] [AcademicAuditor] {msg}", file=sys.stderr)

def call_gemini(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        return res_data["candidates"][0]["content"]["parts"][0]["text"]

def audit_document(student_text, baseline_text, degree_level, duration_months, memory_text, api_key):
    prompt = f"""
You are an Academic Director auditing a student's thesis progress.
Below are the reference files:

1. The AI-generated Baseline Inception Report (benchmark standards):
{baseline_text}

2. The Student's current Inception Report:
{student_text}

3. Coordinator's Past Corrections & Feedback Memory:
{memory_text if memory_text else "No past feedback logged."}

Analyze and compare the documents. Assess progress and identify technical gaps.
Your critique MUST incorporate and respect the Coordinator's Past Corrections (if any are present in the memory).

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
    log_debug("Calling Gemini 3.5 Flash for document audit...")
    return call_gemini(prompt, api_key)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(json.dumps({"error": "Missing parameters"}))
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
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
                memory_text = memory_data.get("feedback", "")
                
        output = audit_document(student_text, baseline_text, degree, duration, memory_text, api_key)
        print(output)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
