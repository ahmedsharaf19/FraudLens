#!/usr/bin/env bash
set -e

# Simple start script for Unix-like systems
# - creates a virtual environment in .venv if not present
# - activates it for the script's session
# - installs requirements and runs the main console app

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

# Activate the venv for this script
# (use `source .venv/bin/activate` to activate interactively)
source .venv/bin/activate

pip install -r requirements.txt

python main.py
