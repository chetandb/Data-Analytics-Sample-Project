#!/bin/bash

# Define variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
ENV_FILE=".env"
FLASK_APP="app.py"

# Step 1: Create and activate a virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Step 2: Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r $REQUIREMENTS_FILE

# Step 3: Set up environment variables
if [ ! -f $ENV_FILE ]; then
  echo "Creating .env file..."
  echo "SECRET_KEY=$(openssl rand -base64 32)" > $ENV_FILE
  echo "MAIL_SERVER=smtp.example.com" >> $ENV_FILE
  echo "MAIL_PORT=587" >> $ENV_FILE
  echo "MAIL_USERNAME=your_email@example.com" >> $ENV_FILE
  echo "MAIL_PASSWORD=your_email_password" >> $ENV_FILE
  echo "Ensure to update the .env file with the correct values."
else
  echo ".env file already exists."
fi

# Step 4: Initialize the database
echo "Initializing the database..."
python -c "
from app import db
db.create_all()
"

# Step 5: Run the Flask application
echo "Running the Flask application..."
flask run

echo "Build script completed."
