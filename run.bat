@echo off
setlocal enabledelayedexpansion

title VLM-IDP Research -- Full-Stack System (Port 8896)
cd /d "%~dp0"

echo ========================================================================
echo   VLM-IDP RESEARCH -- INTELLIGENT DOCUMENT PROCESSING UNDER DEGRADATION
echo   Phases 0-14 IEEE Framework -- Physical CUDA 12.6 Inference & 3D Showcase
echo ========================================================================
echo.

:: 1. Detect Python Environment (Prefer Phase 14 CUDA Virtualenv)
if exist "%~dp0.venv_phase14\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv_phase14\Scripts\python.exe"
    echo [INFO] Active Environment: .venv_phase14 (NVIDIA CUDA 12.6 Enabled)
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    echo [INFO] Active Environment: .venv
) else (
    set "PYTHON_EXE=python"
    echo [INFO] Active Environment: System PATH Python
)

echo [INFO] Python Executable: !PYTHON_EXE!
echo.

:: 2. Check Python version
"!PYTHON_EXE!" --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found! Please check your environment setup.
    pause
    exit /b 1
)

:: 3. Launch Default Web Browser to localhost:8896 after 1.5 seconds delay in background
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8896"

echo ========================================================================
echo   SYSTEM LAUNCHING ON http://localhost:8896
echo   * Interactive 3D Showcase:  http://localhost:8896/
echo   * Real-Time Health API:     http://localhost:8896/api/health
echo   * Empirical Metrics API:    http://localhost:8896/api/metrics
echo   * Pipeline Inference API:   http://localhost:8896/api/pipeline/infer
echo ========================================================================
echo.
echo [SERVER] Starting unified HTTP backend and UI engine on port 8896...
echo [SERVER] Press Ctrl+C in this terminal to stop the server at any time.
echo.

:: 4. Start Server on Port 8896
"!PYTHON_EXE!" src\server.py --port 8896 --host 0.0.0.0

if errorlevel 1 (
    echo.
    echo [ERROR] Server terminated with an error code.
    pause
)
