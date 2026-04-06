#!/usr/bin/env pwsh
# Iceland Trip 2026 - Travel Assistant Loop Launcher
# Runs Claude Code in /loop mode to execute tasks from loop-tasks.md

$ErrorActionPreference = 'Stop'
$tripDir = "C:\Users\Nick\Dropbox\Iceland Trip 2026"

Set-Location $tripDir

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host " Iceland Trip 2026 - Travel Assistant Loop" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Working dir : $tripDir" -ForegroundColor Gray
Write-Host "Tasks file  : loop-tasks.md" -ForegroundColor Gray
Write-Host "Message board: loop.html (loop-log.json)" -ForegroundColor Gray
Write-Host ""
Write-Host "Interval: 2 hours (edit this script to change)" -ForegroundColor Yellow
Write-Host "Stop: Ctrl+C or close this window" -ForegroundColor Yellow
Write-Host ""

# Check MCP status so user knows if Chrome DevTools is available
Write-Host "Checking MCP servers..." -ForegroundColor Gray
claude mcp list
Write-Host ""

Write-Host "Starting Claude in loop mode..." -ForegroundColor Green
Write-Host ""

# The prompt that will run each iteration
$loopPrompt = "Read loop-tasks.md and execute all tasks listed there in order. Post results to the message board via loop_log.py. Be proactive about suggestions and warnings. Commit and push any data file changes with 'Auto:' prefix."

claude --dangerously-skip-permissions "/loop 2h $loopPrompt"
