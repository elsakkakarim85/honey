# ==============================================================================
# ApisLM Production Cluster Orchestration
# ==============================================================================
# This script spins up the entire Zero-Cost ecosystem using Docker Compose.
# It boots the FastAPI Backend, Qdrant Vector DB, and Next.js Web UI in detached mode.
# ==============================================================================

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🌐 Booting ApisLM Production Cluster (Docker)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Write-Host "`n[1/2] Verifying Docker Installation..." -ForegroundColor Yellow
$dockerCheck = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCheck) {
    Write-Host "❌ Docker is not installed or not in PATH! Please install Docker Desktop." -ForegroundColor Red
    Exit
}

Write-Host "`n[2/2] Rebuilding and Launching Containers (Detached)..." -ForegroundColor Yellow
cmd /c docker-compose up -d --build

Write-Host "`n✅ Production Cluster is LIVE!" -ForegroundColor Green
Write-Host "--------------------------------------------------" -ForegroundColor DarkGray
Write-Host "-> Command Center (Next.js): http://localhost:3000" -ForegroundColor Cyan
Write-Host "-> AI API Gateway (FastAPI): http://localhost:8000" -ForegroundColor Cyan
Write-Host "-> Vector Database (Qdrant): http://localhost:6333" -ForegroundColor Cyan
Write-Host "--------------------------------------------------" -ForegroundColor DarkGray
Write-Host "`nTo stop the cluster, run: docker-compose down" -ForegroundColor Yellow
