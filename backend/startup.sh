#!/bin/bash

# Coinage Backend Startup Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=development

# Initialize database
echo "Initializing database..."
flask db upgrade

# Prompt for admin user creation
read -p "Do you want to create an admin user? (y/n): " create_admin

if [[ "$create_admin" == "y" || "$create_admin" == "Y" ]]; then
    read -p "Enter admin username: " admin_username
    read -p "Enter admin email: " admin_email
    read -sp "Enter admin password: " admin_password
    
    python3 create_admin.py "$admin_username" "$admin_email" "$admin_password"
fi

# Start the Flask development server
echo "Starting Coinage Backend..."
flask run
