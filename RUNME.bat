@echo off

set installation_error=0

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is NOT installed or not in PATH.
    echo Installing python...

    winget install -e --id Python.Python.3.13 --scope machine
) else (
    echo Python is installed -- Requirement met (make sure you have Python 3)
    python --version
)

python -m pip install nava
if %errorlevel% neq 0 (
    set installation_error=1
)

python -m pip install opencv-python
if %errorlevel% neq 0 (
    set installation_error=1
)

python -m pip install pytesseract Pillow
if %errorlevel% neq 0 (
    set installation_error=1
)

if "!installation_error!"=="1" (
    echo Installation errors and/or missing modules have prevented FRCSidewinder from working properly.
) else (
    set minmax=2.0

    setlocal
    cd /d %~dp0
    python main.py
)
pause