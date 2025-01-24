# Coinage Platform Environment Configuration

# Database Configuration
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_NAME = "coinage_platform"
$env:DB_USER = "coinage_admin"
$env:DB_PASSWORD = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString()))

# Security Configuration
$env:JWT_SECRET = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString()))
$env:ENCRYPTION_KEY = [System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))

# MLflow Configuration
$env:MLFLOW_TRACKING_URI = "file:///mlflow-tracking"

# Logging Configuration
$env:LOG_LEVEL = "INFO"

# Email Configuration for Beta Testing
$env:SMTP_SERVER = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SENDER_EMAIL = "beta@coinage.com"

# Validate and Display Environment Variables
Write-Host " Environment Variables Set Successfully" -ForegroundColor Green
Write-Host "Database Host: $env:DB_HOST" -ForegroundColor Cyan
Write-Host "Database Name: $env:DB_NAME" -ForegroundColor Cyan
Write-Host "MLflow Tracking URI: $env:MLFLOW_TRACKING_URI" -ForegroundColor Cyan

# Optional: Persist environment variables
[Environment]::SetEnvironmentVariable("DB_HOST", $env:DB_HOST, [EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable("DB_NAME", $env:DB_NAME, [EnvironmentVariableTarget]::User)
