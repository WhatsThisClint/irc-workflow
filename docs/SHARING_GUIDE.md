# GitHub Sharing & Workspace Onboarding Guide

This document explains how to share this private repository with collaborators, how to use link-sharing workarounds (since GitHub does not natively support "unlisted link sharing"), and how incoming collaborators can initialize the workspace.

---

## 1. How GitHub Permissions Work

On GitHub, a repository has only two primary visibility levels:
1.  **Public**: Searchable, indexable, and visible to everyone. Anyone can clone or download it.
2.  **Private**: Invisible to the public, not searchable. Only explicitly invited collaborators can clone or download it.

GitHub **does not natively support unlisted links** (where anyone with the link can clone/download without an invitation or account). To achieve this, use one of the workarounds below.

---

## 2. Options for Link-Based Sharing

### Option A: Share a Google Drive ZIP Link (Recommended for "Anyone with the Link")
If you want to give people a simple link to download the codebase without managing GitHub accounts:
1. Compress the repository folder into a ZIP file (e.g., `irc-workflow.zip`).
2. Upload the ZIP file to your Google Drive.
3. Right-click the file in Google Drive, select **Share**, and set the permission to **"Anyone with the link can view/download"**.
4. Send the link to your collaborators. They can download it and extract it to start working immediately.

### Option B: Invite Collaborators (Secure GitHub standard)
If you want to keep the repository private and secure on GitHub but allow specific people to clone it:
1. Go to the repository home page on GitHub: [https://github.com/WhatsThisClint/irc-workflow](https://github.com/WhatsThisClint/irc-workflow).
2. Click on the **Settings** tab.
3. In the left-hand menu, click **Collaborators**.
4. Click **Add people**, search for their GitHub username or email, and invite them.
5. Once they accept, they can clone the private repository directly using `git clone`.

### Option C: Obfuscated Public Repository (Security through Obscurity)
If you must allow direct `git clone` using a link without inviting users, you can change the repository to **Public** but name it with a randomized string:
1. Go to **Settings** -> **Danger Zone** -> **Change repository visibility** -> **Make public**.
2. Go to the top of **Settings**, and rename the repository to something random (e.g., `irc-workflow-x9a2b7f3d`).
3. *Note: While it won't be easily guessable, it will technically still be public, listed on your profile, and searchable on GitHub.*

---

## 3. Onboarding Steps for Collaborators

Once a collaborator clones the repository or extracts the ZIP file, they must run the initialization checks:

### Step 3.1: Run Workspace Diagnostics & Setup
Run the automated setup script in their terminal:
```bash
python setup_workspace.py
```
This script will:
* Verify Python, Node.js, and NPM environments.
* Install local `n8n` server and node dependencies.
* Validate all workflow file paths.
* Launch the **Interactive Configuration Wizard** (`configure_workspace.py`) to set up `.env` credentials.

### Step 3.2: Configure IDE MCP Connectors (Codex / Claude Desktop)
To enable Gmail and Google Drive capabilities:
1. Add the MCP server configurations to the Claude Desktop config file:
   ```json
   {
     "mcpServers": {
       "google-drive": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-gdrive"]
       },
       "gmail": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-gmail"]
       }
     }
   }
   ```
2. Restart Claude Desktop and log in to authorize access.
