@echo off
title SilentRoot - Advanced Minecraft Account Checker
echo Starting SilentRoot...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the SilentRoot script
python "silentmain.py"

REM Keep window open if there's an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Script encountered an error (Exit code: %ERRORLEVEL%)
    echo Press any key to exit...
    pause >nul
)
