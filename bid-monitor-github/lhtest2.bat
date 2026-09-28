@echo off
chcp 65001 >nul
cd /d "%~dp0"
py lhtest2.py
echo.
pause
