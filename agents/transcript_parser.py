import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] [TranscriptParser] {msg}", file=sys.stderr)

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

def parse_transcript(transcript_text, api_key):
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
    log_debug("Calling Gemini 3.5 Flash for transcript parse...")
    return call_gemini(prompt, api_key)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing parameters"}))
        sys.exit(1)
        
    api_key = os.environ.get("GEMINI_API_KEY")
    transcript_file = sys.argv[1]
    
    try:
        with open(transcript_file, "r", encoding="utf-8") as f:
            transcript_text = f.read()
            
        output = parse_transcript(transcript_text, api_key)
        print(output)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
