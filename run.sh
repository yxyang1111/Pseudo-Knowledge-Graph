#!/bin/bash

# Check if Neo4j configuration is set
if [ ! -f config/config.py ]; then
    echo "Neo4j configuration file not found. Please ensure config/config.py exists and is correctly set."
    exit 1
fi

# Install required Python packages
echo "Installing required packages..."
pip install -r requirements.txt

# Check if data directory exists
if [ ! -d "./data" ]; then
    echo "Data directory not found. Please ensure your data is placed in ./data."
    exit 1
fi

# Build the Pseudo-Knowledge Graph
echo "Building the Pseudo-Knowledge Graph..."
python builder/pkg_create_text.py

# Retrieve information using all methods
echo "Retrieving all information..."
python retriever/get_all_information.py user_query

echo "Run process completed successfully."
