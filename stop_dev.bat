@echo off
title Stop Enterprise Services
echo Stopping all processes running on port 8000 and 8501...
powershell -Command "Get-NetTCPConnection -LocalPort 8000, 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue; Write-Host 'Stopped process' $_.OwningProcess 'on port' $_.LocalPort }"
echo Done! Ports 8000 and 8501 are free.
pause
