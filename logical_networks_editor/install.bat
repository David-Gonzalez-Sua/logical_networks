@echo off
SET ENV_PATH=%~dp0.venv

echo Creating conda environment at %ENV_PATH%...
call conda create -p "%ENV_PATH%" python=3.12 -y

echo Installing Clingo...
call conda run -p "%ENV_PATH%" conda install -c potassco clingo -y

echo Installing Python dependencies...
call conda run -p "%ENV_PATH%" pip install dearpygui

echo Done. Run run.bat to start the application.