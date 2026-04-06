@echo off
REM Double-click launcher for the Iceland Trip travel assistant loop
REM Opens PowerShell, runs the loop script, keeps window open
start "Iceland Loop" powershell -NoExit -ExecutionPolicy Bypass -File "%~dp0run-loop.ps1"
