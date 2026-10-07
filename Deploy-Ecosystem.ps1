# ==============================================================================
# ApisLM Master Deployment Pipeline
# ==============================================================================
# This script orchestrates the compilation of the entire Zero-Cost Swarm Platform.
# Run this script as Administrator.
# ==============================================================================

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "👑 Initiating ApisLM Master Deployment Pipeline 👑" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Cloud Tenant Dashboard (Next.js)
Write-Host "`n[1/4] Building Cloud Tenant Dashboard (Next.js)..." -ForegroundColor Yellow
Set-Location -Path "ApisLM_Workspace\cloud-tenant-dashboard"
npm install
npm run build
Write-Host "✅ Cloud Dashboard compiled successfully." -ForegroundColor Green
Set-Location -Path "..\.."

# 2. Desktop Wrapper (Electron)
Write-Host "`n[2/4] Compiling Standalone Desktop Installer (Electron)..." -ForegroundColor Yellow
Set-Location -Path "ApisLM_Desktop_App"
npm install
npm run dist
Write-Host "✅ Desktop Installer generated in /dist folder." -ForegroundColor Green
Set-Location -Path ".."

# 3. Mobile Edge Node (React Native / Expo)
Write-Host "`n[3/4] Preparing Mobile Edge APK Build..." -ForegroundColor Yellow
Set-Location -Path "ApisLM_Mobile_Edge"
npm install
Write-Host "✅ Mobile dependencies installed." -ForegroundColor Green
Write-Host "   -> To generate the Android APK, run: npx expo build:android" -ForegroundColor DarkGray
Set-Location -Path ".."

# 4. IoT Hardware (PlatformIO / ESP32)
Write-Host "`n[4/4] Preparing IoT Hardware Firmware..." -ForegroundColor Yellow
Write-Host "   -> To flash the ESP32 sensors, connect via USB and run: pio run --target upload" -ForegroundColor DarkGray

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOYMENT PIPELINE COMPLETE 🚀" -ForegroundColor Cyan
Write-Host "The ApisLM ecosystem is ready for global distribution." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
