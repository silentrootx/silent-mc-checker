@echo off
title SilentRoot Setup - Installing Requirements
echo ================================================
echo           SilentRoot Setup Script
echo ================================================
echo.
echo Installing Python requirements for SilentRoot...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Version:
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip is not available!
    echo Attempting to install pip...
    python -m ensurepip --upgrade
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install pip. Please reinstall Python.
        pause
        exit /b 1
    )
)

echo Installing requirements from requirements.txt...
echo.
python -m pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo         Setup completed successfully!
    echo ================================================
    echo.
    echo SilentRoot is ready to use.
    echo You can now run "run.bat" to start the application.
    echo.
) else (
    echo.
    echo ================================================
    echo            Setup failed!
    echo ================================================
    echo.
    echo There was an error installing the requirements.
    echo Please check the error messages above.
    echo.
)

echo Press any key to exit...
pause >nul
