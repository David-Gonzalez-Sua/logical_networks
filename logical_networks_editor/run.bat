@echo off
call conda run -p "%~dp0.venv" python "%~dp0app\main.py"