# 🚀 Clone Repo Update Tool

An advanced, secure, and professional command-line utility designed to manage, fix, and update repository references (such as old usernames to new usernames) seamlessly across multiple Git hosting platforms including GitHub, GitLab, Gitea, and Codeberg.

---

## ✨ Features
* Multi-Platform Support: Works with GitHub, GitLab, Gitea, and Codeberg API.
* Batch Processing: Update 10+ repositories simultaneously with a single click.
* Local & Remote Fixes: Automatically patches local .git/config files and remote README.md files.
* Secure Token Handling: Automatic session clearing and persistent token management.
* Easy Shortcut Command: Run the tool instantly using just CLON (No python command required).

---

## 🛠 Installation & Setup

You can install the tool easily by running our automated installer script. Open your terminal and run:
```bash
git clone https://github.com/UG-ALOK/Git-change.git
```
```bash
cd Git-change
```
```bash
bash install.sh
```
Run
```bash
python3 main.py
```
---

## 🔑 How to Generate & Use Access Tokens

To interact with remote repositories via API, the tool requires a personal access token. Below is the complete guide on how to generate tokens for different platforms:

### 1. GitHub Personal Access Token (PAT)
1. Go to your GitHub account settings: Settings > Developer settings > Personal access tokens.
2. Choose Fine-grained tokens (recommended) or Tokens (classic).
3. If using Classic, make sure to check the following scopes:
   - repo (Full control of private repositories)
   - workflow (Update GitHub Action workflows if needed)
4. Click Generate token and copy it.

### 2. GitLab Personal Access Token
1. Go to GitLab User Settings > Access Tokens.
2. Give your token a name and select the expiration date.
3. Under scopes, select:
   - api (Complete access to the API)
   - read_repository / write_repository
4. Click Create personal access token and copy the string.

### 3. Gitea / Codeberg Token
1. Navigate to Settings > Applications > Manage Access Tokens.
2. Click Generate Token, provide a token name, and check repository permissions (repo).
3. Click Generate Token and save it safely.

---

## 💡 Usage Guide

1. Launch the tool simply by typing:
   CLON
2. Authentication: Register a local account or log in securely.
3. Token Setup: The tool will prompt for your API Token (it will be saved securely to token.txt for future sessions).
4. Select Repository Option: Choose an individual repository from the list or select the batch option (4) to process all repositories at once.
5. Enter Usernames: 
   - Old Username: Enter your previous username or link string to replace.
   - New Username: Enter your new updated username.
6. The tool will automatically update all remote readmes and local configurations!

---

## 🛡️ Security & Privacy
* Tokens are stored locally on your device (token.txt) and are never shared with any third-party servers.
* Built-in background auto-clear timer protects tokens from unauthorized access.

---


## ⚠️ Disclaimer
* This tool is for personal and educational use only. The developer takes **no liability or responsibility** if any cookie, token, or session data is stolen or compromised. Especially if the stolen cookie or token contains high administrative permissions, the user is solely responsible. If your cookies or session are compromised, make sure to delete or revoke them immediately from your account settings (admin panel). Use this tool at your own risk.

---
This tool is optimized by default for **Codeberg**, but it features built-in multi-platform support. By providing an access token from any supported platform (**Codeberg, Gitea, GitHub, or GitLab**), you can automatically update your repository's `README.md` file and clone links with your new username.

