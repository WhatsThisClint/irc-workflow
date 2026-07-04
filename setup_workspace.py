import os
import sys
import subprocess
import shutil

def log(msg):
    print(f"[SETUP] {msg}")

def check_command(cmd):
    return shutil.which(cmd) is not None

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
        return res.returncode == 0, res.stdout, res.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    log("Starting automated IRC workspace setup and diagnostics...")

    # 1. Check Python Version
    python_ver = sys.version.split()[0]
    log(f"Detected Python version: {python_ver}")
    
    # 2. Check Node and NPM
    if not check_command("node"):
        log("ERROR: 'node' (Node.js) is not installed or not on the PATH.")
        sys.exit(1)
    if not check_command("npm"):
        log("ERROR: 'npm' is not installed or not on the PATH.")
        sys.exit(1)
        
    node_ok, node_out, _ = run_cmd("node --version")
    npm_ok, npm_out, _ = run_cmd("npm --version")
    log(f"Detected Node: {node_out.strip()} | NPM: {npm_out.strip()}")

    # 3. Install NPM dependencies (n8n local installation)
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    node_modules_path = os.path.join(workspace_dir, "node_modules")
    
    if not os.path.exists(node_modules_path):
        log("npm dependencies not found. Installing local n8n and project modules...")
        install_ok, _, install_err = run_cmd("npm install", cwd=workspace_dir)
        if not install_ok:
            log(f"ERROR: npm install failed: {install_err}")
            sys.exit(1)
        log("Successfully installed npm dependencies.")
    else:
        log("Local node_modules already exists. Skipping installation.")

    # 4. Verify Local .n8n Configuration Folder
    n8n_folder = os.path.join(workspace_dir, ".n8n")
    if not os.path.exists(n8n_folder):
        log("Creating isolated local .n8n configuration directory...")
        os.makedirs(n8n_folder, exist_ok=True)
    else:
        log("Isolated .n8n directory found.")

    # 5. Check for GEMINI_API_KEY environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        log("WARNING: 'GEMINI_API_KEY' environment variable is NOT set in this shell.")
        log("--> Incoming agents must ask the user to configure the GEMINI_API_KEY before running the workflows.")
    else:
        log("Verified: 'GEMINI_API_KEY' is active in the environment.")

    # 6. Verify Critical Code Files Integrity
    critical_files = [
        "irc_agent.py",
        "agents/onboarding_agent.py",
        "agents/academic_auditor.py",
        "agents/mentor_auditor.py",
        "agents/transcript_parser.py",
        "agents/coordinator_agent.py",
        "agents/alignment_agent.py",
        "n8n/workflows/irc_master_workflow.json",
        "README.md",
        "CLAUDE.md"
    ]
    
    missing_files = []
    for f_path in critical_files:
        abs_f = os.path.join(workspace_dir, f_path)
        if not os.path.exists(abs_f):
            missing_files.append(f_path)
            
    if missing_files:
        log(f"ERROR: Critical files are missing from the workspace: {', '.join(missing_files)}")
        sys.exit(1)
    else:
        log("All critical workflow files and sub-agents verified successfully.")

    log("\n[SUCCESS] Setup complete! The workspace is fully ready for AI execution.")
    log("To launch the local n8n instance, run:")
    log("  Windows Powershell: $env:N8N_USER_FOLDER=\".n8n\"; .\\node_modules\\.bin\\n8n start")
    log("  Mac/Linux Terminal: N8N_USER_FOLDER=\".n8n\" ./node_modules/.bin/n8n start")

if __name__ == "__main__":
    main()
