#!/bin/bash

# Colors
C_GREEN="\033[1;32m"
C_RED="\033[1;31m"
C_CYAN="\033[1;36m"
C_RESET="\033[0m"

echo -e "${C_CYAN}[*] Installing Clone Repo Update Tool...${C_RESET}"

# Update & install python, git if needed
pkg update -y && pkg install python git -y 2>/dev/null || sudo apt update && sudo apt install python3 python3-pip git -y 2>/dev/null

# Install required python modules
echo -e "${C_CYAN}[*] Installing required python libraries (requests, colorama)...${C_RESET}"
pip install requests colorama

# Make script executable
chmod +x main.py

echo -e "${C_GREEN}[✔] Installation completed successfully!${C_RESET}"
echo -e "${C_CYAN}[i] Now you can run the tool directly using: python3 main.py${C_RESET}"
