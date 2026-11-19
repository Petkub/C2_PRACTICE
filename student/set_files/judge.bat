@echo off
rem Windows, inside this topic folder:
rem   judge     judge the whole topic (double-click works too)
rem   judge 5   judge problem 5 only        (PowerShell: .\judge 5)
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python "..\Judge\judge.py" %1
) else (
  py -3 "..\Judge\judge.py" %1
)
if "%~1"=="" pause
