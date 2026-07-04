import os
import sys
import json
import argparse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] [CoordinatorAgent] {msg}", file=sys.stderr)

def extract_coordinator_feedback(cheat_sheet_text):
    """
    Parses feedback written under the ## Coordinator Feedback/Corrections section.
    """
    lines = cheat_sheet_text.split("\n")
    feedback_lines = []
    capture = False
    for line in lines:
        if "## coordinator feedback" in line.lower() or "## coordinator corrections" in line.lower():
            capture = True
            continue
        if capture:
            # Stop if we hit another header
            if line.startswith("#"):
                break
            feedback_lines.append(line)
            
    feedback = "\n".join(feedback_lines).strip()
    return feedback

def calculate_phase(gantt_json_file, cohort_start_date_str, duration_months):
    """
    Calculates current project phase using Gantt dates or elapsed calendar time.
    """
    today = datetime.now()
    gantt_data = None
    if gantt_json_file and os.path.exists(gantt_json_file):
        try:
            with open(gantt_json_file, "r", encoding="utf-8") as f:
                gantt_data = json.load(f)
        except Exception as e:
            log_debug(f"Gantt file parse error: {str(e)}")
            
    if gantt_data:
        try:
            for row in gantt_data:
                task = row.get("task_name", "")
                start_str = row.get("start_date") or row.get("start")
                end_str = row.get("end_date") or row.get("end")
                if start_str and end_str:
                    start_dt = datetime.strptime(start_str.split("T")[0], "%Y-%m-%d")
                    end_dt = datetime.strptime(end_str.split("T")[0], "%Y-%m-%d")
                    if start_dt <= today <= end_dt:
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
        except Exception as e:
            log_debug(f"Error parsing Gantt rows: {str(e)}")
            
    # Fallback elapsed calendar time
    try:
        start_date = datetime.strptime(cohort_start_date_str.split("T")[0], "%Y-%m-%d")
        delta_months = (today.year - start_date.year) * 12 + today.month - start_date.month
        
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

def compile_cheat_sheet(student_name, critique, mentor_score, mentor_critique, reflection_questions, feedback_memory):
    """
    Compiles the final markdown structure for the Admin Cheat Sheet.
    """
    questions_md = "\n".join([f"*   {q}" for q in reflection_questions])
    
    cheat_sheet = f"""# IRC Admin Cheat Sheet: {student_name}
**Generated on**: {datetime.now().strftime("%Y-%m-%d")}
**Previous AI Memory Active**: {"Yes" if feedback_memory else "No"}

## 1. Technical Gap Critique (Student Report vs. Baseline)
{critique}

## 2. Mentor Engagement Assessment
*   **Mentor Score**: {mentor_score}/10
*   **Mentor Evaluation**: {mentor_critique}

## 3. Recommended Meeting Reflection Questions
{questions_md}

## 4. Coordinator Feedback/Corrections
*Write your corrections and feedback here. The AI will absorb them to customize the next audit.*
{feedback_memory if feedback_memory else ""}
"""
    return cheat_sheet

def draft_nudge_email(student_name, critique, mentor_score):
    """
    Drafts a personalized follow-up nudge email based on audit findings.
    """
    if mentor_score <= 4:
        subject = f"IRC Progress Sync: Let's get aligned, {student_name}"
        body = f"""Hi {student_name},

I was reviewing the version history of your Inception Report Google Doc, and noticed we haven't seen much activity or feedback from your mentor recently. 

It is crucial that we refine the research methodologies as we prepare for the inception gate. Are you or your mentor facing any roadblocks? Let's check in during our weekly sync tomorrow.

Best,
Coordinator"""
    else:
        subject = f"IRC Inception Report Progress Update - {student_name}"
        body = f"""Hi {student_name},

Great job progressing the latest draft. I noticed some technical gaps regarding the data parameters compared to our expert baseline research.

Please take a look at the methodology section before our weekly meeting so we can discuss and address these points together.

Best,
Coordinator"""

    return {"subject": subject, "body": body}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRC Coordinator Agent")
    parser.add_argument("--action", required=True, choices=["calculate-phase", "extract-feedback", "compile-report"])
    parser.add_argument("--gantt-file", help="Path to Gantt Chart JSON")
    parser.add_argument("--cohort-start-date", help="Cohort start date")
    parser.add_argument("--duration-months", type=int, default=6, help="Cohort duration")
    parser.add_argument("--cheat-sheet-file", help="Path to previous cheat sheet text file")
    parser.add_argument("--memory-file", help="Path to write/read memory JSON")
    
    # Arguments for compiling the final report
    parser.add_argument("--student", help="Student name")
    parser.add_argument("--academic-critique-file", help="Path to academic auditor JSON output")
    parser.add_argument("--mentor-critique-file", help="Path to mentor auditor JSON output")
    
    args = parser.parse_args()
    
    if args.action == "calculate-phase":
        output = calculate_phase(args.gantt_file, args.cohort_start_date, args.duration_months)
        print(output)
        
    elif args.action == "extract-feedback":
        if not args.cheat_sheet_file or not args.memory_file:
            print(json.dumps({"error": "Missing parameters for extract-feedback."}))
            sys.exit(1)
        try:
            with open(args.cheat_sheet_file, "r", encoding="utf-8") as f:
                content = f.read()
            feedback = extract_coordinator_feedback(content)
            
            # Save to memory file
            memory_data = {"feedback": feedback}
            with open(args.memory_file, "w", encoding="utf-8") as f:
                json.dump(memory_data, f, indent=2)
            log_debug(f"Extracted and saved feedback memory to {args.memory_file}")
            print(json.dumps({"success": True, "feedback": feedback}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
            
    elif args.action == "compile-report":
        if not args.student or not args.academic-critique-file or not args.mentor-critique-file:
            # argparse parses dashes, so academic-critique-file maps to args.academic_critique_file
            # but wait, let's look at python's namespace replacement: dashes become underscores
            pass
        
        # Safe namespace parsing for argparse dashes
        academic_file = getattr(args, "academic_critique_file", None)
        mentor_file = getattr(args, "mentor_critique_file", None)
        
        try:
            with open(academic_file, "r", encoding="utf-8") as f:
                academic_data = json.load(f)
            with open(mentor_file, "r", encoding="utf-8") as f:
                mentor_data = json.load(f)
                
            feedback_memory = ""
            if args.memory_file and os.path.exists(args.memory_file):
                with open(args.memory_file, "r", encoding="utf-8") as f:
                    memory_data = json.load(f)
                    feedback_memory = memory_data.get("feedback", "")
            
            critique = academic_data.get("critique", "")
            reflection_questions = academic_data.get("reflection_questions", [])
            mentor_score = mentor_data.get("mentor_score", 5)
            mentor_critique = mentor_data.get("mentor_critique", "")
            
            cheat_sheet = compile_cheat_sheet(
                args.student, 
                critique, 
                mentor_score, 
                mentor_critique, 
                reflection_questions, 
                feedback_memory
            )
            
            nudge = draft_nudge_email(args.student, critique, mentor_score)
            
            output_report = {
                "cheat_sheet": cheat_sheet,
                "nudge_subject": nudge["subject"],
                "nudge_body": nudge["body"]
            }
            print(json.dumps(output_report))
        except Exception as e:
            print(json.dumps({"error": f"Failed to compile report: {str(e)}"}))
            sys.exit(1)
