import json
import os

onboarding_path = "n8n/workflows/irc_student_onboarding.json"
monitor_path = "n8n/workflows/irc_daily_deadline_monitor.json"

# 1. Update Onboarding Workflow
if os.path.exists(onboarding_path):
    with open(onboarding_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for node in data.get("nodes", []):
        # Prefix main folder with serial number
        if node.get("name") == "Create Student Main Folder":
            node["parameters"]["name"] = "={{ $json[\"S.No\"] }} - {{ $json[\"Student Name\"] }} - IRC Workspace"
            
        # Replace OpenAI Report Generator with Execute Command node
        if node.get("name") == "AI Expert Report Generator":
            node["type"] = "n8n-nodes-base.executeCommand"
            node["typeVersion"] = 1
            node["parameters"] = {
                "command": 'python "f:/Antigravity/IRC Workflow/irc_agent.py" --action generate-baseline --student "{{ $node[\\"Filter Unprocessed\\"].json[\\"Student Name\\"] }}" --question "{{ $node[\\"Filter Unprocessed\\"].json[\\"Research Question\\"] }}" --problem "{{ $node[\\"Filter Unprocessed\\"].json[\\"Problem Statement\\"] }}" --degree-level "{{ $node[\"Filter Unprocessed\"].json[\"Degree Level\"] }}" --duration-months "{{ $node[\"Filter Unprocessed\"].json[\"Total Duration\"] }}"'
            }
            
        # Update Create Sample Doc in Drive content parameter to fetch from stdout
        if node.get("name") == "Create Sample Doc in Drive":
            node["parameters"]["content"] = "={{ $json[\"stdout\"] }}"
            
    with open(onboarding_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Updated onboarding workflow successfully.")

# 2. Update Monitor Workflow
if os.path.exists(monitor_path):
    with open(monitor_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # We will introduce a Code node to parse the JSON array after executing parse-transcript
    # We locate the connections to redirect: List New Transcripts -> AI Transcript Task Extractor -> Sync Action Items to Asana
    # And we'll change AI Dynamic Phase Calculator to Execute Command
    new_nodes = []
    for node in data.get("nodes", []):
        # Replace AI Dynamic Phase Calculator with Execute Command
        if node.get("name") == "AI Dynamic Phase Calculator":
            node["type"] = "n8n-nodes-base.executeCommand"
            node["typeVersion"] = 1
            node["parameters"] = {
                "command": 'python "f:/Antigravity/IRC Workflow/irc_agent.py" --action calculate-phase --cohort-start-date "{{ $node[\\"Filter Active Students\\"].json[\\"Inception Cohort Start Date\\"] }}" --duration-months "{{ $node[\\"Filter Active Students\\"].json[\\"Total Duration\\"] }}"'
            }
            
        # Replace Update Phase in Master Sheet input content from stdout
        if node.get("name") == "Update Phase in Master Sheet":
            node["parameters"]["columns"]["Current Project Phase"] = "={{ $json[\"stdout\"].trim() }}"
            
        # Replace AI Transcript Task Extractor with Execute Command
        if node.get("name") == "AI Transcript Task Extractor":
            node["type"] = "n8n-nodes-base.executeCommand"
            node["typeVersion"] = 1
            node["parameters"] = {
                "command": 'python "f:/Antigravity/IRC Workflow/irc_agent.py" --action parse-transcript --transcript-file "{{ $json[\"path\"] }}"'
            }
            
        new_nodes.append(node)
        
    # Inject intermediate code node to parse stdout from parse-transcript
    # Let's check if the parse code node already exists or add it
    code_node = {
        "parameters": {
            "jsCode": "return JSON.parse($input.item.json.stdout).tasks;"
        },
        "id": "code-node-parse-tasks-json",
        "name": "Parse Transcript Tasks JSON",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [2250, 300]
    }
    new_nodes.append(code_node)
    
    # Adjust connections for the new Parse node:
    # Old: AI Transcript Task Extractor -> Sync Action Items to Asana
    # New: AI Transcript Task Extractor -> Parse Transcript Tasks JSON -> Sync Action Items to Asana
    connections = data.get("connections", {})
    if "AI Transcript Task Extractor" in connections:
        connections["AI Transcript Task Extractor"] = {
            "main": [
                [
                    {
                        "node": "Parse Transcript Tasks JSON",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    connections["Parse Transcript Tasks JSON"] = {
        "main": [
            [
                {
                    "node": "Sync Action Items to Asana",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }
    
    data["nodes"] = new_nodes
    data["connections"] = connections
    
    with open(monitor_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Updated daily monitor workflow successfully.")
