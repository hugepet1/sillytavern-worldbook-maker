@echo off
chcp 65001 >nul
cd /d "%~dp0"
title SillyTavern Worldbook Maker
echo Installing deps if needed...
python -m pip install -r requirements.txt -q
echo.
echo Starting...
python app.py
if errorlevel 1 pause
