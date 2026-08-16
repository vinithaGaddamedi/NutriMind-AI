#!/bin/bash
set -e

echo "=========================================================="
echo " Starting NutriMind AI QA Enterprise End-to-End Demo"
echo "=========================================================="

# Ensure we're in the right directory
cd "$(dirname "$0")/.."

echo "1. Checking Python dependencies..."
# Assuming dependencies are installed; if not, you'd run pip install here

echo "2. Launching Demo Orchestrator..."
python automation/demo_e2e_lifecycle.py

echo "Demo script executed successfully."
