@echo off
rem Windows, inside this topic folder (or Mixed set folder, e.g. 00_Mixed\M01):
rem   judge     judge the whole topic (double-click works too)
rem   judge 5   judge problem 5 only        (PowerShell: .\judge 5)
setlocal
cd /d "%~dp0"
rem Judge\ is in the package root: ..\Judge from a topic folder, ..\..\Judge from a Mixed set (00_Mixed\M01)
set "JUDGE=..\Judge\judge.py"
if not exist "%JUDGE%" if exist "..\..\Judge\judge.py" set "JUDGE=..\..\Judge\judge.py"
where py >nul 2>nul
if errorlevel 1 (
  python "%JUDGE%" %1
) else (
  py -3 "%JUDGE%" %1
)
if "%~1"=="" pause
