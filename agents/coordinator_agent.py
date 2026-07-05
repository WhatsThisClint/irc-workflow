import sys
import json
import argparse
from datetime import datetime
from agents.llm_client import call_llm

def log_debug(msg):
    print(f"[DEBUG] [CoordinatorAgent] {msg}", file=sys.stderr)


def extract_coordinator_feedback(cheat_sheet_text):
    lines = cheat_sheet_text.split("\n")
    feedback_lines = []
    capture = False
    for line in lines:
        if "## coordinator feedback" in line.lower() or "## coordinator corrections" in line.lower():
            capture = True
            continue
        if capture:
            if line.startswith("#"):
                break
            feedback_lines.append(line)
            
    feedback = "\n".join(feedback_lines).strip()
    return feedback

def calculate_phase(gantt_json_file, cohort_start_date_str, duration_months):
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

def compile_cheat_sheet(student_name, critique, mentor_score, mentor_critique, reflection_questions, feedback_memory, methodology_score, triangulation_score, clarity_score, alignment_index, alignment_critique):
    questions_md = "\n".join([f"*   {q}" for q in reflection_questions])
    
    cheat_sheet = f"""# IRC Admin Cheat Sheet: {student_name}
**Generated on**: {datetime.now().strftime("%Y-%m-%d")}
**Previous AI Memory Active**: {"Yes" if feedback_memory else "No"}

## 1. Technical Gap Critique (Student Report vs. Baseline)
{critique}

## 2. Core Academic Competency Ratings
*   **Scientific Methodology**: {methodology_score}/10
*   **Data Triangulation**: {triangulation_score}/10
*   **Academic Writing Clarity**: {clarity_score}/10

## 3. Sponsor Alignment Index
*   **Alignment Score**: {alignment_index}%
*   **Critique**: {alignment_critique}

## 4. Mentor Engagement Assessment
*   **Mentor Score**: {mentor_score}/10
*   **Mentor Evaluation**: {mentor_critique}

## 5. Recommended Meeting Reflection Questions
{questions_md}

## 6. Coordinator Feedback/Corrections
*Write your corrections and feedback here. The AI will absorb them to customize the next audit.*
{feedback_memory if feedback_memory else ""}
"""
    return cheat_sheet

def draft_nudge_email(student_name, critique, mentor_score):
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

def generate_weekly_digest(weekly_data_json):
    prompt = f"""
You are the Academic and Operations Director at WELL Labs, Bangalore.
Review the following aggregated weekly snapshot data for the current India Research Corps (IRC) student cohort:
{weekly_data_json}

Write a comprehensive, professional, executive Weekly Director Digest report. This report is designed for presentation to funding partners and directors to prove operational scalability and student capability growth.

Follow this exact structure:

# IRC Weekly Director Digest: Cohort Executive Review
**Week ending**: {datetime.now().strftime("%Y-%m-%d")}

## 1. Executive Summary
Provide a high-level summary (3-4 sentences) of overall cohort health, highlighting scaling successes and critical blockers.

## 2. Cohort Timeline & Success Velocity
*   Analyze the average delays by phase (Induction vs. Fieldwork vs. Thesis).
*   Compare these delays to the historical cohort baselines. Highlight any reduction in average delay days showing process maturity.

## 3. Student Competency Growth Trajectory
*   Report on the average scores for the Core Academic Triad (Scientific Methodology, Data Triangulation, Writing Clarity).
*   Quantify the competency gains/slopes from early drafts to current drafts.

## 4. Sponsor & Partner Agency Alignment
*   Review the average Sponsor Alignment Index scores across the cohort.
*   Detail how well the active projects are answering sponsors' real-world water problems.

## 5. Critical Escalations & Operations Warnings
*   List any active student red flags (lagging edits) or unresponsive mentors.
*   Recommend immediate interventions for the upcoming week.
"""
    log_debug("Calling LLM client for weekly digest generation...")
    return call_llm(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRC Coordinator Agent")
    parser.add_argument("--action", required=True, choices=["calculate-phase", "extract-feedback", "compile-report", "compile-weekly-digest"])
    parser.add_argument("--gantt-file", help="Path to Gantt Chart JSON")
    parser.add_argument("--cohort-start-date", help="Cohort start date")
    parser.add_argument("--duration-months", type=int, default=6, help="Cohort duration")
    parser.add_argument("--cheat-sheet-file", help="Path to previous cheat sheet text file")
    parser.add_argument("--memory-file", help="Path to write/read memory JSON")
    parser.add_argument("--weekly-metrics-file", help="Path to weekly metrics JSON file")
    
    # Arguments for compiling the final report
    parser.add_argument("--student", help="Student name")
    parser.add_argument("--academic-critique-file", help="Path to academic auditor JSON output")
    parser.add_argument("--mentor-critique-file", help="Path to mentor auditor JSON output")
    parser.add_argument("--alignment-critique-file", help="Path to alignment agent JSON output")
    
    args = parser.parse_args()
    
    if args.action == "calculate-phase":
        output = calculate_phase(args.gantt_file, args.cohort_start_date, args.duration_months)
        print(output)
        
    elif args.action == "extract-feedback":
        if not args.cheat_sheet_file or not args.memory_file:
            print(json.dumps({"status": "failed", "error": "Missing parameters for extract-feedback."}))
            sys.exit(1)
        try:
            with open(args.cheat_sheet_file, "r", encoding="utf-8") as f:
                content = f.read()
            feedback = extract_coordinator_feedback(content)
            
            history = []
            consolidated_rules = ""
            if os.path.exists(args.memory_file):
                try:
                    with open(args.memory_file, "r", encoding="utf-8") as f:
                        memory_data = json.load(f)
                        if "history" in memory_data:
                            history = memory_data.get("history", [])
                            consolidated_rules = memory_data.get("consolidated_rules", "")
                        elif "feedback" in memory_data:
                            old_feedback = memory_data.get("feedback", "")
                            if old_feedback:
                                history = [old_feedback]
                                consolidated_rules = old_feedback
                except Exception as e:
                    log_debug(f"Warning: Failed to load existing memory file: {e}")
            
            if feedback and (not history or history[-1] != feedback):
                history.append(feedback)
                log_debug(f"New feedback appended. History length: {len(history)}")
                
                total_len = sum(len(h) for h in history)
                if total_len > 1500:
                    log_debug(f"Feedback history exceeds 1500 characters. Compressing...")
                    history_str = "\n---\n".join(history)
                    prompt = f"""
You are the Coordinator Agent.
The Coordinator user has provided several rounds of corrections and feedback over successive student report iterations.
Here is the accumulated feedback history for this student:
{history_str}

Consolidate this list into a clean, concise, non-overlapping, bulleted list of rules and principles that the AI Auditor must check in the student's work. Eliminate duplicates and resolve any contradictions in favor of the latest feedback.
Output only the consolidated list. Do not include introductory or concluding remarks.
"""
                    try:
                        consolidated_rules = call_llm(prompt)
                        log_debug("Successfully compressed memory history.")
                    except Exception as e:
                        log_debug(f"Warning: Memory compression query failed: {e}. Falling back to raw concatenation.")
                        consolidated_rules = "\n\n".join(history)
                else:
                    consolidated_rules = "\n\n".join(history)
            elif not feedback and history:
                pass
            elif feedback:
                if not consolidated_rules:
                    consolidated_rules = feedback
                    
            memory_data = {
                "history": history,
                "consolidated_rules": consolidated_rules
            }
            with open(args.memory_file, "w", encoding="utf-8") as f:
                json.dump(memory_data, f, indent=2)
            log_debug(f"Extracted and saved feedback memory to {args.memory_file}")
            print(json.dumps({"status": "success", "error": None, "feedback": feedback, "consolidated_rules": consolidated_rules}))
        except Exception as e:
            print(json.dumps({"status": "failed", "error": str(e)}))
            sys.exit(1)

            
    elif args.action == "compile-report":
        academic_file = getattr(args, "academic_critique_file", None)
        mentor_file = getattr(args, "mentor_critique_file", None)
        alignment_file = getattr(args, "alignment_critique_file", None)
        
        try:
            with open(academic_file, "r", encoding="utf-8") as f:
                academic_data = json.load(f)
            with open(mentor_file, "r", encoding="utf-8") as f:
                mentor_data = json.load(f)
                
            alignment_index = 100
            alignment_critique = "Not checked (outside gate)."
            if alignment_file and os.path.exists(alignment_file):
                with open(alignment_file, "r", encoding="utf-8") as f:
                    alignment_data = json.load(f)
                    alignment_index = alignment_data.get("sponsor_alignment_index", 100)
                    alignment_critique = alignment_data.get("alignment_critique", "")
            
            feedback_memory = ""
            if args.memory_file and os.path.exists(args.memory_file):
                with open(args.memory_file, "r", encoding="utf-8") as f:
                    memory_data = json.load(f)
                    feedback_memory = memory_data.get("consolidated_rules") or memory_data.get("feedback", "")
            
            critique = academic_data.get("critique", "")
            reflection_questions = academic_data.get("reflection_questions", [])
            
            competency_scores = academic_data.get("competency_scores", {})
            methodology_score = competency_scores.get("scientific_methodology", 5)
            triangulation_score = competency_scores.get("data_triangulation", 5)
            clarity_score = competency_scores.get("academic_writing_clarity", 5)
            
            mentor_score = mentor_data.get("mentor_score", 5)
            mentor_critique = mentor_data.get("mentor_critique", "")
            
            cheat_sheet = compile_cheat_sheet(
                args.student, 
                critique, 
                mentor_score, 
                mentor_critique, 
                reflection_questions, 
                feedback_memory,
                methodology_score,
                triangulation_score,
                clarity_score,
                alignment_index,
                alignment_critique
            )
            
            nudge = draft_nudge_email(args.student, critique, mentor_score)
            
            output_report = {
                "status": "success",
                "error": None,
                "cheat_sheet": cheat_sheet,
                "scientific_methodology": methodology_score,
                "data_triangulation": triangulation_score,
                "academic_writing_clarity": clarity_score,
                "sponsor_alignment_index": alignment_index,
                "mentor_score": mentor_score,
                "nudge_subject": nudge["subject"],
                "nudge_body": nudge["body"]
            }
            print(json.dumps(output_report))
        except Exception as e:
            print(json.dumps({"status": "failed", "error": f"Failed to compile report: {str(e)}"}))
            sys.exit(1)
            
    elif args.action == "compile-weekly-digest":
        if not args.weekly_metrics_file:
            print(json.dumps({"status": "failed", "error": "Missing --weekly-metrics-file parameter."}))
            sys.exit(1)
        try:
            with open(args.weekly_metrics_file, "r", encoding="utf-8") as f:
                weekly_data = f.read()
            digest = generate_weekly_digest(weekly_data)
            print(digest)
        except Exception as e:
            print(f"ERROR: Failed to compile weekly digest: {str(e)}")
            sys.exit(1)


