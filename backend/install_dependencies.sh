#!/bin/bash
# Install backend Python dependencies

echo "Installing backend Python dependencies..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend dependencies installed successfully!"
echo "To activate the virtual environment, run: source venv/bin/activate"

