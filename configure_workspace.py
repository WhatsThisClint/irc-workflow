import os
import sys

def log(msg):
    print(f"[SETUP WIZARD] {msg}")

def check_mcp_plugins():
    log("Scanning for IDE-native MCP plugins...")
    
    # Check if running within common AI coding terminals (Claude Code, VSCode, etc.)
    agent_env_vars = ["CLAUDE_DEVICES", "VSCODE_PID", "AGY_CLI", "ANTIGRAVITY_APP_DATA"]
    is_agent_environment = any(var in os.environ for var in agent_env_vars)
    
    print("\n--- IDE MCP CONNECTOR STATUS ---")
    if is_agent_environment:
        print("[INFO] Active AI Agent environment detected.")
    else:
        print("[INFO] Standard local shell environment detected.")
        
    print("\nTo leverage agent-native connectors in Codex or Claude Desktop, make sure you configure:")
    print("1. Google Drive MCP Server (provides 'google_drive' tools)")
    print("2. Gmail MCP Server (provides 'gmail' tools)")
    print("---------------------------------\n")

def get_input(prompt, default=""):
    try:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(1)

def main():
    if "--silent" in sys.argv or os.environ.get("DEBIAN_FRONTEND") == "noninteractive":
        log("Silent mode. Skipping interactive setup.")
        return

    log("Welcome to the India Research Corps (IRC) Workspace Configuration Wizard.")
    check_mcp_plugins()
    
    # Load existing .env if present to present defaults
    env_vars = {}
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    env_vars[k.strip()] = v.strip()
                    
    print("Let's configure your workspace variables.\n")
    
    email = get_input("Enter Coordinator Email ID", env_vars.get("COORDINATOR_EMAIL", "coordinator@welllabs.org"))
    drive_root = get_input("Enter Google Drive Root Folder ID or Path", env_vars.get("DRIVE_ROOT_FOLDER", "IRC_Root_Folder"))
    
    # API configuration
    provider = get_input("Select LLM Provider (gemini/anthropic/openai)", env_vars.get("LLM_PROVIDER", "gemini")).lower()
    
    gemini_key = env_vars.get("GEMINI_API_KEY", "")
    anthropic_key = env_vars.get("ANTHROPIC_API_KEY", "")
    openai_key = env_vars.get("OPENAI_API_KEY", "")
    
    if provider == "gemini":
        gemini_key = get_input("Enter GEMINI_API_KEY", gemini_key)
    elif provider == "anthropic":
        anthropic_key = get_input("Enter ANTHROPIC_API_KEY", anthropic_key)
    elif provider == "openai":
        openai_key = get_input("Enter OPENAI_API_KEY", openai_key)
        
    # Write .env file
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("# IRC Workspace Local Environment Variables\n")
        f.write(f"COORDINATOR_EMAIL={email}\n")
        f.write(f"DRIVE_ROOT_FOLDER={drive_root}\n")
        f.write(f"LLM_PROVIDER={provider}\n")
        if gemini_key:
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
        if anthropic_key:
            f.write(f"ANTHROPIC_API_KEY={anthropic_key}\n")
        if openai_key:
            f.write(f"OPENAI_API_KEY={openai_key}\n")
            
    log(f"Successfully configured local workspace credentials in {env_path}")
    print("\nSetup complete! You can run 'python setup_workspace.py' to run full diagnostics.")

if __name__ == "__main__":
    main()
