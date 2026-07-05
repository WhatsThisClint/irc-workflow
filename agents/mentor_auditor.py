import sys
import json
from agents.llm_client import call_llm

def log_debug(msg):
    print(f"[DEBUG] [MentorAuditor] {msg}", file=sys.stderr)

def audit_mentor(comments_text, student_report_text):
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
    log_debug("Calling LLM client for mentor audit...")
    return call_llm(prompt, json_mode=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing parameters"}))
        sys.exit(1)
        
    comments_file = sys.argv[1]
    student_file = sys.argv[2]
    
    try:
        with open(comments_file, "r", encoding="utf-8") as f:
            comments_text = f.read()
        with open(student_file, "r", encoding="utf-8") as f:
            student_text = f.read()
            
        output_str = audit_mentor(comments_text, student_text)
        res = json.loads(output_str)
        res["status"] = "success"
        res["error"] = None
        print(json.dumps(res))
    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e), "mentor_score": 5, "mentor_critique": f"Mentor Auditor failed: {str(e)}"}))
        sys.exit(1)


