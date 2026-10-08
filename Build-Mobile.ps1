# ==============================================================================
# ApisLM Mobile Edge (Android APK) Build Script
# ==============================================================================
# This orchestrates the Expo Application Services (EAS) CLI to compile
# the React Native app into a production Android APK.
# ==============================================================================

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "📱 Compiling Mobile Edge App (Android APK)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

Set-Location -Path "ApisLM_Mobile_Edge"

Write-Host "`n[1/3] Installing EAS CLI globally..." -ForegroundColor Yellow
cmd /c npm install -g eas-cli

Write-Host "`n[2/3] Authenticating & Configuring Build..." -ForegroundColor Yellow
Write-Host "Note: You will need an Expo account to build on their free cloud tier." -ForegroundColor DarkGray
Write-Host "If you want to build locally without an account, use: eas build --platform android --local" -ForegroundColor DarkGray

Write-Host "`n[3/3] Initiating Production Android Build..." -ForegroundColor Yellow
# Using the local flag so it builds on the machine without needing an Expo cloud account
cmd /c eas build --platform android --profile production --local

Write-Host "`n✅ Build Process Complete!" -ForegroundColor Green
Write-Host "The generated .apk file can now be transferred via USB to your field tablets." -ForegroundColor Cyan

Set-Location -Path ".."
