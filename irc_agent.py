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
    cmd = [sys.executable, script_path] + args_list
    log_debug(f"Executing: {' '.join(cmd)}")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env)
    if result.returncode != 0:
        log_debug(f"Sub-agent failed: {result.stderr}")
        raise RuntimeError(f"Sub-agent failed: {result.stderr}")
    return result.stdout


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IRC AI Workflow Agent Router")
    parser.add_argument("--action", required=True, choices=["generate-baseline", "audit-doc", "parse-transcript", "calculate-phase", "check-alignment", "compile-weekly-digest", "ingest-resources"])
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
    parser.add_argument("--sponsor-problem", help="Sponsor's problem statement for alignment check")
    parser.add_argument("--weekly-metrics-file", help="Path to weekly metrics JSON file")
    parser.add_argument("--resources-dir", help="Path to resources directory for ingestion")
    
    args = parser.parse_args()
    log_debug(f"Routing action: {args.action}")
    
    onboarding_script = "agents/onboarding_agent.py"
    academic_script = "agents/academic_auditor.py"
    mentor_script = "agents/mentor_auditor.py"
    transcript_script = "agents/transcript_parser.py"
    coordinator_script = "agents/coordinator_agent.py"
    alignment_script = "agents/alignment_agent.py"
    
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
            
    elif args.action == "check-alignment":
        try:
            output = run_agent_script(alignment_script, [
                args.student_report_file, args.sponsor_problem
            ])
            print(output)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
            
    elif args.action == "compile-weekly-digest":
        try:
            output = run_agent_script(coordinator_script, [
                "--action", "compile-weekly-digest",
                "--weekly-metrics-file", args.weekly_metrics_file
            ])
            print(output)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
            
    elif args.action == "ingest-resources":
        try:
            ingest_script = "agents/ingest_resources.py"
            output = run_agent_script(ingest_script, [args.resources_dir])
            print(output)
        except Exception as e:
            print(json.dumps({"status": "failed", "error": str(e)}))
            sys.exit(1)
            
    elif args.action == "audit-doc":
        try:
            dir_name = os.path.dirname(args.student_report_file) if args.student_report_file else "."
            student_name = args.student if args.student else "Student"
            memory_file = os.path.join(dir_name, f"memory.json")
            cheat_sheet_file = os.path.join(dir_name, f"cheat_sheet.md")
            
            if not os.path.exists(cheat_sheet_file) and args.student_report_file:
                try:
                    with open(cheat_sheet_file, "w", encoding="utf-8") as f:
                        f.write(f"# IRC Admin Cheat Sheet: {student_name}\n\n## Coordinator Feedback/Corrections\n")
                except Exception:
                    pass
                    
            if os.path.exists(cheat_sheet_file):
                try:
                    run_agent_script(coordinator_script, [
                        "--action", "extract-feedback",
                        "--cheat-sheet-file", cheat_sheet_file,
                        "--memory-file", memory_file
                    ])
                except Exception as e:
                    log_debug(f"Memory extraction warning: {e}")
                    
            # 1. Spawn Academic Auditor
            academic_output_file = os.path.join(dir_name, "academic_temp.json")
            academic_json = run_agent_script(academic_script, [
                args.student_report_file,
                args.baseline_report_file,
                args.degree_level,
                str(args.duration_months),
                memory_file
            ])
            with open(academic_output_file, "w", encoding="utf-8") as f:
                f.write(academic_json)
                
            # 2. Spawn Mentor Auditor
            mentor_output_file = os.path.join(dir_name, "mentor_temp.json")
            mentor_json = run_agent_script(mentor_script, [
                args.student_report_file,
                args.student_report_file
            ])
            with open(mentor_output_file, "w", encoding="utf-8") as f:
                f.write(mentor_json)
                
            # 3. Optional: Spawn Sponsor Alignment Agent (only if problem statement is passed)
            alignment_output_file = os.path.join(dir_name, "alignment_temp.json")
            if args.sponsor_problem:
                try:
                    alignment_json = run_agent_script(alignment_script, [
                        args.student_report_file,
                        args.sponsor_problem
                    ])
                    with open(alignment_output_file, "w", encoding="utf-8") as f:
                        f.write(alignment_json)
                except Exception as e:
                    log_debug(f"Sponsor Alignment check failed: {e}")
                    
            # 4. Spawn Coordinator Agent to compile final report
            compile_args = [
                "--action", "compile-report",
                "--student", student_name,
                "--academic-critique-file", academic_output_file,
                "--mentor-critique-file", mentor_output_file,
                "--memory-file", memory_file
            ]
            if os.path.exists(alignment_output_file):
                compile_args.extend(["--alignment-critique-file", alignment_output_file])
                
            report_json = run_agent_script(coordinator_script, compile_args)
            
            # Clean up temp files
            for temp_file in [academic_output_file, mentor_output_file, alignment_output_file]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
            print(report_json)
        except Exception as e:
            # Fallback cleanup
            for temp_file in ["academic_temp.json", "mentor_temp.json", "alignment_temp.json"]:
                p = os.path.join(dir_name if 'dir_name' in locals() else ".", temp_file)
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except:
                        pass
            print(json.dumps({
                "status": "failed",
                "error": str(e),
                "cheat_sheet": f"ERROR: Failed to perform audit: {str(e)}",
                "scientific_methodology": 5,
                "data_triangulation": 5,
                "academic_writing_clarity": 5,
                "sponsor_alignment_index": 50,
                "mentor_score": 5,
                "nudge_subject": "IRC Progress Sync Alert",
                "nudge_body": "Could not compile nudge due to an internal execution error."
            }))
            sys.exit(1)

