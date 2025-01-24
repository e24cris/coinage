#!/usr/bin/env pwsh

# Coinage Development Environment Setup Script

# Ensure script runs with admin privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "Please run this script as Administrator"
    exit 1
}

# Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Check Python installation
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python is not installed. Please install Python 3.9+ first."
    exit 1
}
Write-Host "Detected Python Version: $pythonVersion" -ForegroundColor Green

# Create virtual environment
python -m venv coinage_env
.\coinage_env\Scripts\Activate.ps1

# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Configure environment variables
Copy-Item -Path ".env.example" -Destination ".env"

# Initialize database
flask db upgrade

# Run initial security audit
python backend/security_audit.py

# Train initial ML model
python backend/ml/investment_prediction_model.py

# Start development services
docker-compose -f docker-compose.dev.yml up -d

Write-Host "Coinage development environment setup complete!" -ForegroundColor Green
