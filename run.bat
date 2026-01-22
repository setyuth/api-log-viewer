@echo off
REM API Log Viewer - Windows Quick Start Script

echo ========================================
echo   API Log Viewer - Quick Start
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Check for log file argument
if "%~1"=="" (
    echo No log file specified. Using example file.

    if not exist "examples\sample_json.log" (
        echo [ERROR] Example files not found. Please provide a log file path.
        echo Usage: run.bat ^<path-to-log-file^>
        pause
        exit /b 1
    )

    set LOG_FILE=examples\sample_json.log
    echo Using: %LOG_FILE%
) else (
    set LOG_FILE=%~1

    if not exist "%LOG_FILE%" (
        echo [ERROR] File not found: %LOG_FILE%
        pause
        exit /b 1
    )

    echo Using: %LOG_FILE%
)

echo.
echo ========================================
echo   Starting API Log Viewer...
echo ========================================
echo.

REM Run the application
python main.py "%LOG_FILE%"

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause