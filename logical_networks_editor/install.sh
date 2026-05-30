#!/bin/bash
# Install the dependencies for the project in a virtual environment.

DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Installing dependencies in $DIR/venv"
cd "$DIR" || exit 1

python3 -m venv "$DIR/venv"

source "$DIR/venv/bin/activate"

pip install dearpygui

echo "Done. Run ./run.sh to start the application."