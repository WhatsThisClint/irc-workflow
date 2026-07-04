import sys
import json
from datetime import datetime
from agents.llm_client import call_llm

def log_debug(msg):
    print(f"[DEBUG] [OnboardingAgent] {msg}", file=sys.stderr)


def generate_baseline(student_name, question, problem, degree_level, duration_months):

    prompt = f"""
You are a senior socio-hydrology and water systems expert at WELL Labs, Bangalore.
Your task is to write a highly thorough, professional, baseline Inception Report for a student named '{student_name}'.
The research question is: '{question}'
The problem statement is: '{problem}'

This Inception Report serves as the baseline technical reference. It must be written from the perspective of an expert doing the actual work, detailing the exact methodologies, frameworks, data parameters, and risk mitigations.

ADJUST THE COHORT RIGOR ACCORDING TO:
1. Degree Level: {degree_level}
   - BSc: Focus on basic field feasibility, simple surveys, direct physical measurements.
   - MSc: Require robust data triangulation (primary and secondary comparison), statistical analyses, and structured socio-economic interviews.
   - PhD: Require high theoretical novelty, advanced mathematical or system dynamics modeling, extensive literature review, and academic publication readiness.
2. Program Duration: {duration_months} months
   - Scale complexity proportionally. A longer program (10 months) requires deeper research and longer observation cycles; a shorter program (6 months) must prioritize rapid execution and immediate fieldwork tasks.

Follow the exact template structure below:

# Inception Report: {question}
**Prepared by**: AI Research Advisor (WELL Labs)
**Student**: {student_name} (Degree: {degree_level}, Duration: {duration_months} Months)
**Date**: {datetime.now().strftime("%Y-%m-%d")}

## 1. Context & Literature Review Scope
## 2. Research Conceptual Model
## 3. Data Collection Methodology
## 4. Fieldwork Timeline & Seasonal Considerations
## 5. Potential Constraints & Risk Mitigation
"""
    log_debug("Calling LLM client for baseline report...")
    return call_llm(prompt)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(json.dumps({"error": "Missing parameters"}))
        sys.exit(1)
        
    student = sys.argv[1]
    question = sys.argv[2]
    problem = sys.argv[3]
    degree = sys.argv[4]
    duration = int(sys.argv[5])
    
    try:
        report = generate_baseline(student, question, problem, degree, duration)
        print(report)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

