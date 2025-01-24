@echo off
echo Coinage Backend Startup Script

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Set environment variables
set FLASK_APP=run.py
set FLASK_ENV=development

REM Initialize database
echo Initializing database...
flask db upgrade

REM Prompt for admin user creation
set /p create_admin="Do you want to create an admin user? (y/n): "
if /i "%create_admin%"=="y" (
    set /p admin_username="Enter admin username: "
    set /p admin_email="Enter admin email: "
    set /p admin_password="Enter admin password: "
    python create_admin.py %admin_username% %admin_email% %admin_password%
)

REM Start the Flask development server
echo Starting Coinage Backend...
flask run
