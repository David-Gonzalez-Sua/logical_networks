#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Installing dependencies in $DIR/.venv"

python3 -m venv "$DIR/.venv"
source "$DIR/.venv/bin/activate"
pip install dearpygui

echo "Done. Run ./run.sh to start the application."