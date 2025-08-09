@echo off
echo Starting Lag Switch with Administrator privileges...
echo.
echo This will open a User Account Control (UAC) prompt.
echo Please click "Yes" to allow the program to run.
echo.
pause
cd /d "%~dp0dist"
LagSwitch.exe
pause
