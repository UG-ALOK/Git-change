# =====================================================================
# TOOL: CLONE REPO & README UPDATE TOOL (CODEBERG / GITEA / GITHUB)
# =====================================================================

import os
import sys
import time
import threading
import base64
import hashlib
import requests
from colorama import Fore, Style, init

init(autoreset=True)

EXT_DIR = "/sdcard/Download"
if not os.path.exists(EXT_DIR):
    EXT_DIR = os.path.expanduser("~")

USER_DB = os.path.join(EXT_DIR, "users_db.txt")
T_FILE = os.path.join(EXT_DIR, "token.txt")
active_token = None

# Custom Color Palette
C_GOLD = Fore.YELLOW + Style.BRIGHT
C_GREEN = Fore.GREEN + Style.BRIGHT
C_RED = Fore.RED + Style.BRIGHT
C_CYAN = Fore.CYAN + Style.BRIGHT
C_WHITE = Fore.WHITE + Style.BRIGHT
C_MAGENTA = Fore.MAGENTA + Style.BRIGHT
C_BLUE = Fore.BLUE + Style.BRIGHT


def show_banner():
    print(C_MAGENTA + """
    ███████╗██╗      ██████╗ ███╗   ██╗███████╗
    ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝
    ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  
    ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  
    ╚███████╗███████╗╚██████╔╝██║ ╚████║███████╗
    ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    """ + C_CYAN + "      [ CODEBERG / GITEA REPO UPDATE TOOL ]      " + Style.RESET_ALL)


def token_timer():
    global active_token
    while True:
        time.sleep(60)
        if active_token is not None:
            active_token = None
            print(C_CYAN + "\n[i] Token auto-cleared from memory." + Style.RESET_ALL)


threading.Thread(target=token_timer, daemon=True).start()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    print(C_CYAN + "\n--- REGISTER NEW ACCOUNT ---" + Style.RESET_ALL)
    username = input(C_GOLD + "[?] Enter Username: " + Style.RESET_ALL).strip()
    password = input(C_GOLD + "[?] Enter Password: " + Style.RESET_ALL).strip()
    
    if not username or not password:
        print(C_RED + "[-] Username and password cannot be empty!" + Style.RESET_ALL)
        return False
        
    users = {}
    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f:
                for line in f:
                    if ":" in line:
                        u, p = line.strip().split(":", 1)
                        users[u] = p
        except:
            pass
            
    if username in users:
        print(C_RED + "[-] User already exists!" + Style.RESET_ALL)
        return False
        
    users[username] = hash_password(password)
    try:
        with open(USER_DB, "w") as f:
            for u, p in users.items():
                f.write(f"{u}:{p}\n")
        print(C_GREEN + "[+] Registration successful!" + Style.RESET_ALL)
        return True
    except:
        print(C_RED + "[-] Failed to save user data!" + Style.RESET_ALL)
        return False


def login_user():
    print(C_CYAN + "\n--- LOGIN TO SYSTEM ---" + Style.RESET_ALL)
    attempts = 3
    while attempts > 0:
        username = input(C_GOLD + "[?] Username: " + Style.RESET_ALL).strip()
        password = input(C_GOLD + "[?] Password: " + Style.RESET_ALL).strip()
        
        if not os.path.exists(USER_DB):
            print(C_RED + "[-] No registered users found. Please register first." + Style.RESET_ALL)
            return False
            
        try:
            with open(USER_DB, "r") as f:
                for line in f:
                    if ":" in line:
                        u, p = line.strip().split(":", 1)
                        if u == username and p == hash_password(password):
                            print(C_GREEN + "[+] Login successful!" + Style.RESET_ALL)
                            return True
        except:
            pass
            
        attempts -= 1
        if attempts > 0:
            print(C_RED + f"[-] Invalid credentials! Attempts left: {attempts}" + Style.RESET_ALL)
        else:
            print(C_RED + "[-] Maximum attempts reached. Login failed!" + Style.RESET_ALL)
            
    return False


def api_request(method, url, **kwargs):
    for _ in range(5):
        try:
            return requests.request(method, url, timeout=15, **kwargs)
        except:
            time.sleep(3)
    return None


def check_token(t_in):
    res = api_request("GET", "https://codeberg.org/api/v1/user", headers={"Authorization": f"token {t_in}"})
    if res and res.status_code == 200:
        return True, res.json().get("username", "Unknown"), "Codeberg"

    res = api_request("GET", "https://gitea.com/api/v1/user", headers={"Authorization": f"token {t_in}"})
    if res and res.status_code == 200:
        return True, res.json().get("username", "Unknown"), "Gitea"

    res = api_request("GET", "https://api.github.com/user", headers={"Authorization": f"Bearer {t_in}", "Accept": "application/vnd.github+json"})
    if res and res.status_code == 200:
        return True, res.json().get("login", "Unknown"), "GitHub"

    res = api_request("GET", "https://gitlab.com/api/v4/user", headers={"Private-Token": t_in})
    if res and res.status_code == 200:
        return True, res.json().get("username", "Unknown"), "GitLab"

    return False, "", None


def get_repos(token, p_form):
    repos = []
    try:
        if p_form in ["Gitea", "Codeberg"]:
            b_url = "https://gitea.com" if p_form == "Gitea" else "https://codeberg.org"
            h = {"Authorization": f"token {token}"}
            res = api_request("GET", f"{b_url}/api/v1/user/repos?limit=100", headers=h)
            if res and res.status_code == 200:
                for r in res.json():
                    repos.append({"name": r.get("name"), "full_name": r.get("full_name"), "clone_url": r.get("clone_url")})
        elif p_form == "GitHub":
            h = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
            res = api_request("GET", "https://api.github.com/user/repos?per_page=100", headers=h)
            if res and res.status_code == 200:
                for r in res.json():
                    repos.append({"name": r.get("name"), "full_name": r.get("full_name"), "clone_url": r.get("clone_url")})
    except:
        pass
    return repos


def update_readme_and_clone_links(token, p_form, repo, old_u, new_u):
    try:
        if p_form in ["Gitea", "Codeberg"]:
            b_url = "https://gitea.com" if p_form == "Gitea" else "https://codeberg.org"
            h = {"Authorization": f"token {token}", "Accept": "application/json"}
            url = f"{b_url}/api/v1/repos/{repo}/contents/README.md"
            res = api_request("GET", url, headers=h)
            if not res or res.status_code != 200:
                return False
            data = res.json()
            text = base64.b64decode(data.get("content", "")).decode('utf-8', errors='ignore')
            
            if old_u in text:
                new_text = text.replace(old_u, new_u)
                payload = {
                    "branch": "main",
                    "content": base64.b64encode(new_text.encode('utf-8')).decode('utf-8'),
                    "message": f"Update clone links & username from {old_u} to {new_u}",
                    "sha": data.get("sha")
                }
                put = api_request("PUT", url, headers=h, json=payload)
                return put and put.status_code in [200, 201]
    except:
        pass
    return False


def fix_local(path, old_u, new_u):
    exts = ('.md', '.txt', '.py', '.sh', '.json', '.yml', '.yaml')
    for root, dirs, files in os.walk(path):
        if '.git' in dirs:
            cfg = os.path.join(root, '.git', 'config')
            if os.path.exists(cfg):
                try:
                    with open(cfg, 'r', encoding='utf-8', errors='ignore') as f:
                        c = f.read()
                    if old_u in c:
                        with open(cfg, 'w', encoding='utf-8') as f:
                            f.write(c.replace(old_u, new_u))
                except:
                    pass
            dirs.remove('.git')
        for file in files:
            if file.endswith(exts):
                f_path = os.path.join(root, file)
                try:
                    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
                        c = f.read()
                    if old_u in c:
                        with open(f_path, 'w', encoding='utf-8') as f:
                            f.write(c.replace(old_u, new_u))
                except:
                    pass


def get_token():
    global active_token
    if active_token:
        return active_token

    t_in = ""
    if os.path.exists(T_FILE):
        try:
            with open(T_FILE, "r") as f:
                t_in = f.read().strip()
        except:
            pass

    if not t_in:
        t_in = input(C_GOLD + "[?] token.txt not found. Enter Codeberg Token: " + Style.RESET_ALL).strip()
        if not t_in:
            print(C_RED + "Failed" + Style.RESET_ALL)
            return None
        try:
            with open(T_FILE, "w") as f:
                f.write(t_in)
        except:
            pass

    active_token = t_in
    return active_token


def run_fixer():
    token = get_token()
    if not token:
        return

    valid, user, p_form = check_token(token)
    if not valid:
        print(C_RED + "Invalid Token!" + Style.RESET_ALL)
        if os.path.exists(T_FILE):
            os.remove(T_FILE)
        return

    print(C_GREEN + f"[✔] Connected to {p_form} as user: {user}" + Style.RESET_ALL)
    repos = get_repos(token, p_form)
    if not repos:
        print(C_RED + "No Repos Found!" + Style.RESET_ALL)
        return

    print(C_GOLD + f"\n[+] Found {len(repos)} repositories on {p_form}." + Style.RESET_ALL)
    print(C_GOLD + "\n" + "="*45)
    for i, r in enumerate(repos, 1):
        print(C_GOLD + f" [{i}] " + C_WHITE + f"{r['name']} -> Clone: {r.get('clone_url', 'N/A')}" + Style.RESET_ALL)
    print(C_GOLD + f" [{len(repos)+1}] " + C_WHITE + "Process All Repos (Batch Update)" + Style.RESET_ALL)
    print(C_GOLD + "="*45 + Style.RESET_ALL)

    choice = input(C_GOLD + "[?] Select Option: " + Style.RESET_ALL).strip()
    old_u = input(C_GOLD + "[?] Old Username: " + Style.RESET_ALL).strip()
    new_u = input(C_GOLD + "[?] New Username: " + Style.RESET_ALL).strip()

    if not old_u or not new_u:
        print(C_RED + "Invalid Input!" + Style.RESET_ALL)
        return

    print(C_GOLD + "[*] Updating git clone commands & README references..." + Style.RESET_ALL)

    batch_opt = str(len(repos) + 1)
    if choice == batch_opt:
        success_count = 0
        for r in repos:
            if update_readme_and_clone_links(token, p_form, r['full_name'], old_u, new_u):
                success_count += 1
        fix_local(".", old_u, new_u)
        print(C_GREEN + f"[+] Batch processing completed! Successfully updated {success_count} repositories." + Style.RESET_ALL)
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(repos):
                repo = repos[idx]
                success = update_readme_and_clone_links(token, p_form, repo['full_name'], old_u, new_u)
                fix_local(".", old_u, new_u)
                if success:
                    print(C_GREEN + "[+] Git clone commands & README update successful!" + Style.RESET_ALL)
                else:
                    print(C_RED + "[-] Update failed or no matching pattern found." + Style.RESET_ALL)
            else:
                print(C_RED + "[-] Invalid Choice!" + Style.RESET_ALL)
        except:
            print(C_RED + "[-] Error executing process!" + Style.RESET_ALL)


def main():
    show_banner()
    
    while True:
        print(C_CYAN + "+---------------------------------------------+" + Style.RESET_ALL)
        print(C_CYAN + "|               AUTHENTICATION                |" + Style.RESET_ALL)
        print(C_CYAN + "+---------------------------------------------+" + Style.RESET_ALL)
        print(C_CYAN + "| " + C_GREEN + "1." + C_WHITE + " Register Account                           " + C_CYAN + "|" + Style.RESET_ALL)
        print(C_CYAN + "| " + C_GREEN + "2." + C_WHITE + " Login                                      " + C_CYAN + "|" + Style.RESET_ALL)
        print(C_CYAN + "| " + C_GREEN + "3." + C_WHITE + " Exit                                       " + C_CYAN + "|" + Style.RESET_ALL)
        print(C_CYAN + "+---------------------------------------------+" + Style.RESET_ALL)
        
        auth_opt = input(C_GREEN + "[?] Option: " + Style.RESET_ALL).strip()
        if auth_opt == "1":
            register_user()
        elif auth_opt == "2":
            if login_user():
                break
        elif auth_opt == "3":
            sys.exit(0)
        else:
            print(C_RED + "[-] Invalid option!" + Style.RESET_ALL)

    while True:
        exists = os.path.exists(T_FILE)
        
        print(C_CYAN + "+---------------------------------------------+" + Style.RESET_ALL)
        print(C_CYAN + "|                   MAIN MENU                 |" + Style.RESET_ALL)
        print(C_CYAN + "+---------------------------------------------+" + Style.RESET_ALL)
        
        if not exists:
            print(C_CYAN + "| " + C_GREEN + "1." + C_WHITE + " Input Codeberg Token                       " + C_CYAN + "|" + Style.RESET_ALL)
            print(C_CYAN + "| " + C_GREEN + "2." + C_WHITE + " Run Repo & Clone Link Fixer                " + C_CYAN + "|" + Style.RESET_ALL)
            print(C_CYAN + "| " + C_GREEN + "3." + C_WHITE + " Exit                                       " + C_CYAN + "|" + Style.RESET_ALL)
        else:
            print(C_CYAN + "| " + C_GREEN + "1." + C_WHITE + " Run Repo & Clone Link Fixer                " + C_CYAN + "|" + Style.RESET_ALL)
            print(C_CYAN + "| " + C_GREEN + "2." + C_WHITE + " Delete Token File                          " + C_CYAN + "|" + Style.RESET_ALL)
            print(C_CYAN + "| " + C_GREEN + "3." + C_WHITE + " Exit                                       " + C_CYAN + "|" + Style.RESET_ALL)
            
        print(C_CYAN + "+---------------------------------------------+" + Style.RESET_ALL)
        print(C_CYAN + "| " + C_BLUE + "Dev: RAJ-Alok | Platform: Codeberg" + C_CYAN + "           |" + Style.RESET_ALL)
        print(C_CYAN + "+---------------------------------------------+" + Style.RESET_ALL)
        
        opt = input(C_GREEN + "[?] Option: " + Style.RESET_ALL).strip()
        
        if not exists:
            if opt == "1":
                get_token()
            elif opt == "2":
                run_fixer()
            elif opt == "3":
                sys.exit(0)
        else:
            if opt == "1":
                run_fixer()
            elif opt == "2":
                global active_token
                active_token = None
                if os.path.exists(T_FILE):
                    os.remove(T_FILE)
                    print(C_GREEN + "Token Deleted!" + Style.RESET_ALL)
                time.sleep(1)
            elif opt == "3":
                sys.exit(0)

if __name__ == "__main__":
    main()
