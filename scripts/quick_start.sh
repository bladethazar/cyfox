#!/bin/bash
# Quick start script for Cyfox

set -e

echo "🚀 Starting Cyfox..."

# Check if running on Raspberry Pi
if [ -d "/sys/class/gpio" ]; then
    echo "✓ Raspberry Pi detected"
else
    echo "⚠ Running in simulation mode (not on Raspberry Pi)"
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check dependencies
echo "Checking dependencies..."
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Check config
if [ ! -f "config/config.yaml" ]; then
    echo "⚠ Config file not found, using defaults"
fi

# Run Cyfox
echo "Starting Cyfox..."
python3 -m src.main

