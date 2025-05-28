# PowerShell script to set up the development environment

# Check if Python is installed
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed. Please install Python 3.8 or higher from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host "Python version: $pythonVersion" -ForegroundColor Green

# Check if Node.js is installed
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Node.js is not installed. Please install Node.js 14 or higher from https://nodejs.org/" -ForegroundColor Red
    exit 1
}
Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green

# Check if npm is installed
$npmVersion = npm --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "npm is not installed. Please install npm." -ForegroundColor Red
    exit 1
}
Write-Host "npm version: $npmVersion" -ForegroundColor Green

# Check if Tesseract OCR is installed
$tesseractVersion = tesseract --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tesseract OCR is not installed. Please install it from https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    Write-Host "Note: Document automation will not work without Tesseract OCR" -ForegroundColor Yellow
} else {
    Write-Host "Tesseract OCR is installed: $tesseractVersion" -ForegroundColor Green
}

# Set up backend
Write-Host "`nSetting up backend..." -ForegroundColor Cyan
cd backend

# Create and activate virtual environment
if (-not (Test-Path -Path ".\venv")) {
    python -m venv venv
    Write-Host "Created virtual environment" -ForegroundColor Green
}

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "Installed Python dependencies" -ForegroundColor Green

# Set up frontend
Write-Host "`nSetting up frontend..." -ForegroundColor Cyan
cd ..\frontend

# Install Node.js dependencies
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Node.js dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "Installed Node.js dependencies" -ForegroundColor Green

# Return to project root
cd ..

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To start the application, run: .\start_servers.bat" -ForegroundColor Cyan
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
