# ==============================================================================
# ApisLM Backend PyInstaller Compiler
# ==============================================================================
# This script compiles the entire FastAPI Python backend into a single .exe
# so it can run autonomously on any Windows machine without requiring Python.
# ==============================================================================

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🛠️ Compiling FastAPI Backend to Standalone Executable" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Set-Location -Path "ApisLM_Local_Backend"

Write-Host "`n[1/3] Installing PyInstaller..." -ForegroundColor Yellow
# Using cmd /c to bypass potential execution policy issues
cmd /c pip install pyinstaller uvicorn fastapi sqlalchemy

Write-Host "`n[2/3] Freezing Python Scripts into .exe..." -ForegroundColor Yellow
# We compile main_api.py into a single executable (--onefile)
# We include uvicorn explicitly so it can bundle the ASGI server
cmd /c pyinstaller --name "ApisLM_Gateway" --onefile --hidden-import uvicorn main_api.py

Write-Host "`n[3/3] Build Complete!" -ForegroundColor Green
Write-Host "The production binary is located at: ApisLM_Local_Backend/dist/ApisLM_Gateway.exe" -ForegroundColor Green
Write-Host "You can now run this .exe on any Windows machine without installing Python." -ForegroundColor Cyan

Set-Location -Path ".."
