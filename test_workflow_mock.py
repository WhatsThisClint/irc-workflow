"""
IRC Student Workflow Mock & Verification Runner
This script simulates the dynamic calculations and AI prompt engineering used in the n8n workflows.
It serves as a dry-run tool to verify logic before deploying on n8n.
"""

from datetime import datetime, timedelta
import json

def calculate_milestones(cohort_start_str, duration_months):
    """
    Simulates the dynamic milestone calculations based on Cohort Start Date and Duration.
    """
    start_date = datetime.strptime(cohort_start_str, "%Y-%m-%d")
    
    # 1. Induction Phase (1 month / 30 days)
    induction_end = start_date + timedelta(days=30)
    sessions = []
    for i in range(1, 7):
        # Spaced out every 5 days
        due_date = start_date + timedelta(days=i * 5)
        sessions.append({
            "task": f"Session {i} Reflection",
            "due_date": due_date.strftime("%Y-%m-%d")
        })
        
    # 2. Fieldwork Phase
    fieldwork_start = induction_end + timedelta(days=7) # Starts 1 week after induction
    fieldwork_duration_months = max(1, duration_months - 2) # Total minus induction and final
    fieldwork_end = fieldwork_start + timedelta(days=fieldwork_duration_months * 30)
    
    # 3. Mid-Term Review
    midpoint_months = duration_months / 2
    midterm_date = start_date + timedelta(days=int(midpoint_months * 30))
    
    # 4. Final Thesis Submission
    final_submission_date = start_date + timedelta(days=duration_months * 30)
    
    return {
        "Induction Start": start_date.strftime("%Y-%m-%d"),
        "Induction End (Inception Presentation Gate)": induction_end.strftime("%Y-%m-%d"),
        "Induction Sessions": sessions,
        "Fieldwork Phase": {
            "Start": fieldwork_start.strftime("%Y-%m-%d"),
            "End": fieldwork_end.strftime("%Y-%m-%d")
        },
        "Mid-Term Review": midterm_date.strftime("%Y-%m-%d"),
        "Final Submission": final_submission_date.strftime("%Y-%m-%d")
    }

def print_mock_prompt_templates(student_name, research_question, problem_statement, transcript_text=None):
    """
    Displays the formatted prompts sent to AI nodes for validation.
    """
    print("\n" + "="*50)
    print("AI PROMPT TEMPLATES & CONFIGURATION")
    print("="*50)
    
    # 1. Expert Sample Report Generator Prompt
    sample_prompt = f"""
[SYSTEM PROMPT - ROLE: Domain Expert socio-hydrologist / socio-economist at WELL Labs, Bangalore]
You are a senior environmental researcher at WELL Labs.
Your task is to generate a comprehensive, professional Sample Inception Report template for the research question: '{research_question}'
and problem statement: '{problem_statement}'.
This report is meant for the program coordinator (Admin) to use as an evaluation benchmark. Do not address the student directly.

Structure your output into:
1. Literature Review Scope (Key papers, legal frameworks, and socio-economic datasets needed)
2. Detailed Methodology (Field surveys, water pinch analysis, community mapping, or hydrological monitoring tools)
3. Data Requirements List (Primary and secondary data variables, frequency, and source types)
4. Fieldwork Risk Matrix (Monsoon dependency, safety, community trust barriers, and data reliability limits)
"""
    print("\n--- 1. Sample Inception Report Prompt (Onboarding) ---")
    print(sample_prompt.strip())
    
    # 2. Mentor Evaluation and Reflection Prep
    review_prompt = f"""
[SYSTEM PROMPT - ROLE: Academic Advisor / Program Director]
Compare the Student's Reflection Document against the Sample Inception Report.
Identify technical gaps in the student's methodology, data collection plan, or literature context.

Additionally, analyze the Mentor's comments in the document:
- Count the frequency and depth of their comments.
- Check if they are providing superficial advice (e.g., 'looks good', 'fix formatting') vs. substantive critique (e.g., 're-evaluate sample size', 'check pre-monsoon baseline').
- Assign a Mentor Engagement Score (1-10) with reasoning.

Output a critique summary and 3 high-leverage reflection questions to ask BOTH the student and mentor during the next sync call.
"""
    print("\n--- 2. Student Doc Review & Mentor Engagement Audit Prompt ---")
    print(review_prompt.strip())

    # 3. Transcript Action Item Parser
    if transcript_text:
        transcript_prompt = f"""
[SYSTEM PROMPT - ROLE: Operations Analyst]
Read the following meeting transcript:
"{transcript_text}"

Extract all action items discussed during the meeting. Categorize each action item under one of:
- STUDENT
- MENTOR
- COORDINATOR

For each task, extract:
- Task Name
- Detailed Description
- Due Date (if mentioned, otherwise set to 'Null')

Format the output strictly as a JSON array of objects:
{{
  "tasks": [
    {{"assignee": "STUDENT", "task_name": "Create pre-monsoon survey", "details": "Draft a questionnaire with 15 household questions", "due_date": "2026-07-15"}},
    ...
  ]
}}
"""
        print("\n--- 3. Transcript Action Item Parser Prompt ---")
        print(transcript_prompt.strip())

if __name__ == "__main__":
    # Test 1: Dynamic Timeline Calculations
    print("="*50)
    print("TESTING DYNAMIC TIMELINE CALCULATION")
    print("="*50)
    
    # Simulate a 6-month cohort
    timeline_6m = calculate_milestones("2026-07-01", 6)
    print(f"\nTimeline for 6-Month Cohort (Start: 2026-07-01):")
    print(json.dumps(timeline_6m, indent=2))
    
    # Simulate an 8-month cohort
    timeline_8m = calculate_milestones("2026-07-01", 8)
    print(f"\nTimeline for 8-Month Cohort (Start: 2026-07-01):")
    print(json.dumps(timeline_8m, indent=2))

    # Test 2: Display prompts
    sample_transcript = "Mentor: Let's make sure the student collects groundwater samples from at least 15 wells by the end of next week. Student: Yes, I will create the sampling protocol by Friday and share it. Coordinator: Excellent, I will review and print the protocols once they are ready."
    print_mock_prompt_templates(
        student_name="Ananya Sharma",
        research_question="Evaluating the impact of community-managed irrigation user groups on groundwater recharge rates in rural Karawang.",
        problem_statement="Over-extraction of borewells for paddy fields has caused severe water table depletion. We want to check if community cooperatives manage aquifer recharge more effectively than direct state administration.",
        transcript_text=sample_transcript
    )
