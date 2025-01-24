# Coinage Platform Dependency Installation

# Ensure running with administrative privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as an Administrator!"
    break
}

# Set execution policy
Set-ExecutionPolicy RemoteSigned -Force

# Check and install Python if not present
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Installing Python..." -ForegroundColor Yellow
    winget install Python.Python.3.9
}

# Upgrade pip
python -m pip install --upgrade pip

# Create virtual environment
python -m venv coinage_env
.\coinage_env\Scripts\Activate.ps1

# Install core dependencies
pip install --upgrade pip setuptools wheel

# Install project-specific dependencies
$dependencies = @(
    "flask",
    "sqlalchemy",
    "scikit-learn",
    "mlflow",
    "prometheus_client",
    "redis",
    "celery",
    "pandas",
    "numpy",
    "joblib",
    "psycopg2-binary",
    "python-jose[cryptography]"
)

foreach ($package in $dependencies) {
    Write-Host "Installing $package..." -ForegroundColor Cyan
    pip install $package
}

# Verify installations
Write-Host "`n🔍 Dependency Installation Check:" -ForegroundColor Green
pip list

# Optional: Create requirements.txt
pip freeze > requirements.txt

Write-Host "`n✅ Coinage Platform Dependencies Installed Successfully!" -ForegroundColor Green
