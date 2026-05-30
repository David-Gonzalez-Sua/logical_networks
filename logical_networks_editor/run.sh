#!/bin/bash
# Run the application.

cd "$(dirname "$0")" || exit 1

source venv/bin/activate

python3 app/main.py