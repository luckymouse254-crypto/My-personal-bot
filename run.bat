@echo off
echo Starting @Mouselucky_bot...
echo.

REM Create venv if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Trying with py command...
        py -m venv venv
    )
)

echo Activating venv...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Trying alternative activation...
    call venv\Scripts\Activate.ps1
)

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Starting bot...
python bot.py
if errorlevel 1 (
    py bot.py
)

pause
