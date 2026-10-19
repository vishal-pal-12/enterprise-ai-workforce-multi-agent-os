@echo off
title Enterprise AI Workforce - Service Launcher
echo =====================================================================
echo    Enterprise AI Workforce - Multi-Agent Operating System
echo =====================================================================
echo.
echo [1/3] Clearing any existing processes on ports 8000 and 8501...
powershell -Command "Get-NetTCPConnection -LocalPort 8000, 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"

echo [2/3] Launching FastAPI Backend on port 8000...
start "Enterprise OS - FastAPI Backend" cmd /k "title FastAPI Backend && cd /d %~dp0 && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak >nul

echo [3/3] Launching Streamlit Web Console on port 8501...
start "Enterprise OS - Streamlit UI" cmd /k "title Streamlit UI && cd /d %~dp0 && python -m streamlit run app/ui/streamlit_app.py --server.port 8501"

timeout /t 3 /nobreak >nul
echo.
echo Opening browser at http://localhost:8501 ...
start http://localhost:8501

echo.
echo =====================================================================
echo Services are now active!
echo Backend:   http://127.0.0.1:8000 (Docs: http://127.0.0.1:8000/docs)
echo Frontend:  http://localhost:8501
echo =====================================================================
