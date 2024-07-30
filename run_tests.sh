#!/bin/bash

# Ensure the database is running
docker-compose up -d db

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install or update dependencies
pip install -r dev-requirements.txt

# Set the Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the tests
pytest tests/

# Deactivate the virtual environment
deactivate

# Optional: Bring down the database after tests
# docker-compose down