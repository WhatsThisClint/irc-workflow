import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] [AlignmentAgent] {msg}", file=sys.stderr)

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

def check_alignment(student_text, problem_statement, api_key):
    prompt = f"""
You are a Partner Engagement Lead evaluating environmental research alignment.
Below are the reference documents:

1. Sponsor / Partner Agency's Problem Statement:
"{problem_statement}"

2. Student's Current Inception Report or Thesis Draft:
"{student_text}"

Evaluate how directly the student's research methodologies, data parameters, and field work address the sponsor's stated problem. Identify any gaps where the student's work drifts into purely theoretical concepts that do not solve the sponsor's real-world needs.

Output the result strictly as a valid JSON object matching this schema:
{{
  "sponsor_alignment_index": 85, // Integer from 1 to 100 indicating percentage alignment
  "alignment_critique": "A detailed explanation of how well the research matches the problem statement, highlighting any drift or gaps."
}}
"""
    log_debug("Calling Gemini 3.5 Flash for sponsor alignment check...")
    return call_gemini(prompt, api_key)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing parameters. Required: [student_report_file] [problem_statement]"}))
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
    student_file = sys.argv[1]
    problem_statement = sys.argv[2]
    
    try:
        with open(student_file, "r", encoding="utf-8") as f:
            student_text = f.read()
            
        output = check_alignment(student_text, problem_statement, api_key)
        print(output)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
