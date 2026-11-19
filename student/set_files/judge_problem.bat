@echo off
rem Windows, inside this problem folder:
rem   judge     judge this problem (double-click works too)        (PowerShell: .\judge)
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python "..\..\Judge\judge.py"
) else (
  py -3 "..\..\Judge\judge.py"
)
pause
