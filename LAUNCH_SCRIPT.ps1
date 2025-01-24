# Coinage Platform Launch Script

# Check and guide execution policy
function Test-ExecutionPolicy {
    $currentPolicy = Get-ExecutionPolicy

    if ($currentPolicy -eq 'Restricted') {
        Write-Host "`n❌ PowerShell Execution Policy is Restricted" -ForegroundColor Red
        Write-Host "`nTo run this script, you need to adjust the execution policy:" -ForegroundColor Yellow
        Write-Host "1. Open PowerShell as Administrator" -ForegroundColor Cyan
        Write-Host "2. Run the following command:" -ForegroundColor Cyan
        Write-Host "   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" -ForegroundColor Green
        Write-Host "`nThis allows running local scripts that you trust." -ForegroundColor Yellow
        return $false
    }
    return $true
}

# Execution policy check
if (-not (Test-ExecutionPolicy)) {
    exit 1
}

# Ensure running with administrative privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as an Administrator!"
    Write-Host "`nTo run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click PowerShell" -ForegroundColor Cyan
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor Cyan
    exit 1
}

# Set strict error handling
$ErrorActionPreference = 'Stop'

# Load environment variables
. .\set_env_vars.ps1

# Activate virtual environment
.\coinage_env\Scripts\Activate.ps1

# Pre-launch checks
Write-Host "🔍 Performing Pre-Launch System Checks" -ForegroundColor Cyan

# Check Python version
$pythonVersion = python --version
Write-Host "Detected Python Version: $pythonVersion" -ForegroundColor Cyan

if ($pythonVersion -notmatch "Python 3.9") {
    Write-Error "Incompatible Python version. Required: Python 3.9+. Detected: $pythonVersion" -ForegroundColor Red
    Write-Host "Please install Python 3.9 or later and update your system PATH." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Python version check passed" -ForegroundColor Green

# Check required dependencies
$requiredPackages = @(
    "flask", "sqlalchemy", "scikit-learn", 
    "mlflow", "prometheus_client", "redis", "celery"
)

foreach ($package in $requiredPackages) {
    pip show $package | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Missing package: $package"
        exit 1
    }
}

# Launch Platform
Write-Host "`n🚀 Launching Coinage Platform" -ForegroundColor Green

try {
    # Run launch orchestrator
    python LAUNCH_ORCHESTRATOR.py

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 Coinage Platform Launch Successful!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Platform Launch Failed" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "`n❌ Critical Launch Error: $_" -ForegroundColor Red
    exit 1
}

# Optional: Open monitoring dashboard
if (Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe") {
    Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "http://localhost:8000"
} elseif (Test-Path "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") {
    Start-Process -FilePath "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -ArgumentList "http://localhost:8000"
} else {
    Write-Host "Could not find Chrome. Opening default browser." -ForegroundColor Yellow
    Start-Process "http://localhost:8000"
}
