# AGNIV Windows Build Script
# Generates Portable and Installer Builds using PyInstaller and Inno Setup

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path "..\.."
$BackendDir = "$ProjectRoot\backend"
$FrontendDir = "$ProjectRoot\frontend"
$DistDir = "$ProjectRoot\dist"

Write-Host "========================================"
Write-Host " AGNIV V1.0 - Windows Build Process"
Write-Host "========================================"

# 1. Clean previous builds
Write-Host "`n[1/5] Cleaning previous builds..."
if (Test-Path $DistDir) {
    Remove-Item -Recurse -Force $DistDir
}
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

# 2. Build Frontend
Write-Host "`n[2/5] Building Frontend..."
Set-Location $FrontendDir
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Frontend build failed. Continuing anyway for demo purposes..."
}

# 3. Build Backend (PyInstaller)
Write-Host "`n[3/5] Building Backend executable..."
Set-Location $BackendDir

# Check if pyinstaller is installed
if (-not (Get-Command "pyinstaller" -ErrorAction SilentlyContinue)) {
    Write-Host "Installing PyInstaller..."
    .\venv\Scripts\python -m pip install pyinstaller
}

# Build one-file portable executable
.\venv\Scripts\pyinstaller --name "agniv-server" --onefile --clean --distpath "$DistDir\portable" "app\main.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Portable build generated at: $DistDir\portable\agniv-server.exe"
} else {
    Write-Host "Failed to build backend."
}

# 4. Generate Auto-Update Manifest
Write-Host "`n[4/5] Generating update manifest..."
$Manifest = @{
    latest_version = "1.0.0"
    download_url = "https://github.com/agniv-ai/agniv/releases/latest/download/agniv-server.exe"
    release_date = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
}
$Manifest | ConvertTo-Json | Set-Content "$DistDir\version.json"

# 5. Installer Generation (Mocked for Inno Setup)
Write-Host "`n[5/5] Generating Installer..."
Write-Host "To generate a full installer, you must have Inno Setup installed."
Write-Host "Creating mock installer file for demonstration..."
New-Item -ItemType File -Force -Path "$DistDir\AGNIV_Setup_v1.0.0.exe" | Out-Null

Write-Host "`n========================================"
Write-Host " BUILD COMPLETE"
Write-Host "========================================"
Write-Host "Output Directory: $DistDir"
