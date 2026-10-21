#!/usr/bin/env bash
# One-command setup: a virtual environment, the dependencies and a .env file to fill in.
set -e
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
echo "Done. Add your ANTHROPIC_API_KEY to .env, then run: . .venv/bin/activate && streamlit run main.py"
