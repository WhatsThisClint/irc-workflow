import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] [MentorAuditor] {msg}", file=sys.stderr)

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

def audit_mentor(comments_text, student_report_text, api_key):
    prompt = f"""
You are an Academic Director evaluating a thesis mentor's performance.
Below are the data sources:

1. Comments list (representing active and resolved comments pulled from the Google Doc):
{comments_text}

2. The Student's current Inception Report:
{student_report_text}

Analyze the mentor's comments. Check if their feedback is substantive (challenging methodology, correcting hydrologic math, suggesting literature) or superficial (fixing punctuation, typos, or ghosting).

Output the result strictly as a valid JSON object matching this schema:
{{
  "mentor_score": 8, // Integer score from 1 (ghosting) to 10 (high engagement)
  "mentor_critique": "A detailed explanation of the mentor's actual guidance value and responsiveness."
}}
"""
    log_debug("Calling Gemini 3.5 Flash for mentor audit...")
    return call_gemini(prompt, api_key)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing parameters"}))
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
    comments_file = sys.argv[1]
    student_file = sys.argv[2]
    
    try:
        with open(comments_file, "r", encoding="utf-8") as f:
            comments_text = f.read()
        with open(student_file, "r", encoding="utf-8") as f:
            student_text = f.read()
            
        output = audit_mentor(comments_text, student_text, api_key)
        print(output)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
