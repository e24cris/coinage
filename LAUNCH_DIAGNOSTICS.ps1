# Coinage Platform Comprehensive Diagnostics

# Logging and Error Handling
$ErrorActionPreference = 'Continue'
$global:DiagnosticLog = @()

function Write-DiagLog {
    param(
        [string]$Message, 
        [string]$Level = 'Info'
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    $global:DiagnosticLog += $logEntry
    
    switch ($Level) {
        'Error' { Write-Host $logEntry -ForegroundColor Red }
        'Warning' { Write-Host $logEntry -ForegroundColor Yellow }
        'Info' { Write-Host $logEntry -ForegroundColor Cyan }
    }
}

function Find-ChromeBrowser {
    $chromePaths = @(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    )

    $validPath = $chromePaths | Where-Object { 
        $_ -and (Test-Path -LiteralPath $_) 
    } | Select-Object -First 1

    # Ensure $null is on the left side of comparison
    return $(if ($null -eq $validPath) { $null } else { $validPath })
}

function Test-PythonEnvironment {
    $checks = @{
        "Python Installed" = $false
        "Pip Installed" = $false
        "Required Packages" = @{}
    }

    try {
        $pythonVersion = & python --version 2>&1
        $checks["Python Installed"] = $?
        Write-DiagLog "Python Version: $pythonVersion"
    }
    catch {
        Write-DiagLog "Python check failed" -Level 'Warning'
    }

    try {
        $pipVersion = & pip --version 2>&1
        $checks["Pip Installed"] = $?
        Write-DiagLog "Pip Version: $pipVersion"
    }
    catch {
        Write-DiagLog "Pip check failed" -Level 'Warning'
    }

    $requiredPackages = @(
        "flask", "sqlalchemy", "scikit-learn", 
        "mlflow", "prometheus_client", "redis", "celery"
    )

    foreach ($package in $requiredPackages) {
        try {
            $packageCheck = & pip show $package 2>$null
            $checks["Required Packages"][$package] = ($packageCheck -ne $null)
        }
        catch {
            $checks["Required Packages"][$package] = $false
        }
    }

    return $checks
}

function Get-SystemInformation {
    $osInfo = Get-CimInstance Win32_OperatingSystem
    $processorInfo = Get-CimInstance Win32_Processor | Select-Object -First 1
    $memoryInfo = Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum

    Write-Host "`n💻 System Information" -ForegroundColor Cyan
    Write-Host "  OS: $($osInfo.Caption) $($osInfo.Version)" -ForegroundColor Green
    Write-Host "  Processor: $($processorInfo.Name)" -ForegroundColor Green
    Write-Host "  Memory: $([math]::Round($memoryInfo.Sum / 1GB, 2)) GB" -ForegroundColor Green
}

function Test-CoinagePlatformReadiness {
    $systemChecks = @{
        "Chrome Browser" = $false
        "Launch Script" = $false
        "Dependencies Script" = $false
        "Virtual Environment" = $false
    }

    # Chrome Browser Check
    $chromePath = Find-ChromeBrowser
    $systemChecks["Chrome Browser"] = ($null -ne $chromePath)
    if ($chromePath) {
        Write-DiagLog "Chrome Browser found at: $chromePath"
    }

    # Script Existence Checks
    $systemChecks["Launch Script"] = Test-Path -LiteralPath ".\LAUNCH_SCRIPT.ps1"
    $systemChecks["Dependencies Script"] = Test-Path -LiteralPath ".\install_dependencies.ps1"
    $systemChecks["Virtual Environment"] = Test-Path -LiteralPath ".\coinage_env\Scripts\python.exe"

    # Python Environment Check
    $pythonEnvironment = Test-PythonEnvironment

    # Display Checks
    Write-Host "`n🚦 System Readiness Checks:" -ForegroundColor Cyan
    foreach ($check in $systemChecks.Keys) {
        $status = if ($systemChecks[$check]) { "✅ Ready" } else { "❌ Not Ready" }
        Write-Host "  $check : $status" -ForegroundColor $(if ($systemChecks[$check]) { "Green" } else { "Red" })
    }

    # Display Python Environment Details
    Write-Host "`n🐍 Python Environment:" -ForegroundColor Cyan
    foreach ($packageName in $pythonEnvironment["Required Packages"].Keys) {
        $status = if ($pythonEnvironment["Required Packages"][$packageName]) { "✅ Installed" } else { "❌ Not Installed" }
        Write-Host "  $packageName : $status" -ForegroundColor $(if ($pythonEnvironment["Required Packages"][$packageName]) { "Green" } else { "Red" })
    }

    # Overall Readiness
    $overallReadiness = $true
    foreach ($checkValue in $systemChecks.Values) {
        if (-not $checkValue) {
            $overallReadiness = $false
            break
        }
    }

    Write-Host "`n📊 Overall Platform Readiness: $( if ($overallReadiness) { '✅ READY TO LAUNCH' } else { '❌ REQUIRES ATTENTION' } )" -ForegroundColor $(if ($overallReadiness) { "Green" } else { "Red" })

    return $overallReadiness
}

function Export-DiagnosticsLog {
    $logPath = ".\coinage_diagnostics_log_$((Get-Date).ToString('yyyyMMdd_HHmmss')).txt"
    $global:DiagnosticLog | Out-File -FilePath $logPath -Encoding UTF8
    Write-Host "`n📄 Diagnostic log exported to $logPath" -ForegroundColor Green
}

# Main Execution
try {
    Get-SystemInformation
    $launchReady = Test-CoinagePlatformReadiness
    Export-DiagnosticsLog
    exit $(if ($launchReady) { 0 } else { 1 })
}
catch {
    Write-Host "Unhandled error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
