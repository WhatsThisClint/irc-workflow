import os
import sys
import json
import argparse
import subprocess

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def log_debug(msg):
    print(f"[DEBUG] [Router] {msg}", file=sys.stderr)

def run_agent_script(script_path, args_list):
    """
    Executes a sub-agent python script and returns its stdout.
    """
    cmd = [sys.executable, script_path] + args_list
    log_debug(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        log_debug(f"Sub-agent failed: {result.stderr}")
        raise RuntimeError(f"Sub-agent failed: {result.stderr}")
    return result.stdout

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRC AI Workflow Agent Router")
    parser.add_argument("--action", required=True, choices=["generate-baseline", "audit-doc", "parse-transcript", "calculate-phase"])
    parser.add_argument("--student", help="Student name")
    parser.add_argument("--question", help="Research question")
    parser.add_argument("--problem", help="Problem statement")
    parser.add_argument("--degree-level", default="MSc", help="BSc / MSc / PhD")
    parser.add_argument("--duration-months", type=int, default=6, help="6 / 8 / 10 months")
    parser.add_argument("--student-report-file", help="Path to student's report text file")
    parser.add_argument("--baseline-report-file", help="Path to baseline report text file")
    parser.add_argument("--transcript-file", help="Path to transcript text file")
    parser.add_argument("--gantt-file", help="Path to Gantt Chart JSON file")
    parser.add_argument("--cohort-start-date", help="Cohort start date YYYY-MM-DD")
    
    args = parser.parse_args()
    log_debug(f"Routing action: {args.action}")
    
    # Set paths to specialized agents
    onboarding_script = "agents/onboarding_agent.py"
    academic_script = "agents/academic_auditor.py"
    mentor_script = "agents/mentor_auditor.py"
    transcript_script = "agents/transcript_parser.py"
    coordinator_script = "agents/coordinator_agent.py"
    
    if args.action == "generate-baseline":
        try:
            output = run_agent_script(onboarding_script, [
                args.student, args.question, args.problem, args.degree_level, str(args.duration_months)
            ])
            print(output)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
            
    elif args.action == "calculate-phase":
        try:
            output = run_agent_script(coordinator_script, [
                "--action", "calculate-phase",
                "--cohort-start-date", args.cohort_start_date,
                "--duration-months", str(args.duration_months),
                "--gantt-file", args.gantt_file if args.gantt_file else ""
            ])
            print(output)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
            
    elif args.action == "parse-transcript":
        try:
            output = run_agent_script(transcript_script, [args.transcript_file])
            print(output)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
            
    elif args.action == "audit-doc":
        # Multi-Agent Coordination Loop:
        # 1. First, check if there is an existing Cheat Sheet to extract coordinator feedback memory.
        #    If student_report_file exists, we search in its directory for S.No prefixed cheat sheets.
        dir_name = os.path.dirname(args.student_report_file) if args.student_report_file else "."
        # Define files
        student_name = args.student if args.student else "Student"
        memory_file = os.path.join(dir_name, f"memory.json")
        cheat_sheet_file = os.path.join(dir_name, f"cheat_sheet.md")
        
        # Write mock files if they don't exist to prevent crashes during dry runs
        if not os.path.exists(cheat_sheet_file) and args.student_report_file:
            try:
                with open(cheat_sheet_file, "w", encoding="utf-8") as f:
                    f.write(f"# IRC Admin Cheat Sheet: {student_name}\n\n## Coordinator Feedback/Corrections\n")
            except Exception:
                pass
                
        # 2. Extract feedback and save to memory.json
        if os.path.exists(cheat_sheet_file):
            try:
                run_agent_script(coordinator_script, [
                    "--action", "extract-feedback",
                    "--cheat-sheet-file", cheat_sheet_file,
                    "--memory-file", memory_file
                ])
            except Exception as e:
                log_debug(f"Memory extraction warning: {e}")
                
        # 3. Spawn Academic Auditor
        academic_output_file = os.path.join(dir_name, "academic_temp.json")
        try:
            academic_json = run_agent_script(academic_script, [
                args.student_report_file,
                args.baseline_report_file,
                args.degree_level,
                str(args.duration_months),
                memory_file
            ])
            with open(academic_output_file, "w", encoding="utf-8") as f:
                f.write(academic_json)
        except Exception as e:
            print(json.dumps({"error": f"Academic Auditor failed: {str(e)}"}))
            sys.exit(1)
            
        # 4. Spawn Mentor Auditor
        mentor_output_file = os.path.join(dir_name, "mentor_temp.json")
        try:
            # We pass the student report file as both comments and text for this fallback
            mentor_json = run_agent_script(mentor_script, [
                args.student_report_file,
                args.student_report_file
            ])
            with open(mentor_output_file, "w", encoding="utf-8") as f:
                f.write(mentor_json)
        except Exception as e:
            print(json.dumps({"error": f"Mentor Auditor failed: {str(e)}"}))
            sys.exit(1)
            
        # 5. Spawn Coordinator Agent to compile final report
        try:
            report_json = run_agent_script(coordinator_script, [
                "--action", "compile-report",
                "--student", student_name,
                "--academic-critique-file", academic_output_file,
                "--mentor-critique-file", mentor_output_file,
                "--memory-file", memory_file
            ])
            
            # Clean up temp files
            for temp_file in [academic_output_file, mentor_output_file]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
            # Output final json for n8n to digest
            print(report_json)
        except Exception as e:
            print(json.dumps({"error": f"Coordinator compilation failed: {str(e)}"}))
            sys.exit(1)
