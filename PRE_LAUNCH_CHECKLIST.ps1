# Coinage Platform Pre-Launch Checklist

# Ensure running with administrative privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "`n❌ Please run this script as an Administrator" -ForegroundColor Red
    Write-Host "1. Right-click PowerShell" -ForegroundColor Cyan
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor Cyan
    exit 1
}

# Function to check system readiness
function Test-SystemReadiness {
    $checks = @{
        "PowerShell Version" = { $PSVersionTable.PSVersion.Major -ge 5 }
        "Python Installation" = { Get-Command python -ErrorAction SilentlyContinue }
        "pip Installation" = { Get-Command pip -ErrorAction SilentlyContinue }
        "Git Installation" = { Get-Command git -ErrorAction SilentlyContinue }
    }

    $allChecksPassed = $true
    foreach ($check in $checks.GetEnumerator()) {
        $result = & $check.Value
        $status = if ($result) { "✅ Passed" } else { "❌ Failed" }
        Write-Host "$($check.Key): $status" -ForegroundColor $(if ($result) { "Green" } else { "Red" })
        $allChecksPassed = $allChecksPassed -and $result
    }

    return $allChecksPassed
}

# Function to install missing dependencies
function Install-MissingDependencies {
    # Check and install Python if not present
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Installing Python..." -ForegroundColor Yellow
        winget install Python.Python.3.9
    }

    # Upgrade pip
    python -m pip install --upgrade pip

    # Install required packages
    $requiredPackages = @(
        "flask", "sqlalchemy", "scikit-learn", 
        "mlflow", "prometheus_client", "redis", "celery"
    )

    foreach ($package in $requiredPackages) {
        pip install $package
    }
}

# Main pre-launch workflow
function Start-PreLaunchPreparation {
    Write-Host "`n🚀 Coinage Platform Pre-Launch Preparation" -ForegroundColor Cyan

    # Check system readiness
    $systemReady = Test-SystemReadiness

    if (-not $systemReady) {
        Write-Host "`n⚠️ Some system checks failed. Attempting to resolve..." -ForegroundColor Yellow
        Install-MissingDependencies
    }

    # Set execution policy
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

    # Set environment variables
    . .\set_env_vars.ps1

    Write-Host "`n✅ Pre-Launch Preparation Complete" -ForegroundColor Green
    Write-Host "Ready to launch Coinage Platform!" -ForegroundColor Cyan
}

# Execute pre-launch preparation
Start-PreLaunchPreparation
