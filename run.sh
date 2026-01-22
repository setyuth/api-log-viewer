#!/bin/bash

# API Log Viewer - Quick Start Script
# This script helps you quickly set up and run the log viewer

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  API Log Viewer - Quick Start${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check for log file argument
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}No log file specified. Using example file.${NC}"

    # Check if example files exist
    if [ ! -f "examples/sample_json.log" ]; then
        echo -e "${RED}Example files not found. Please provide a log file path.${NC}"
        echo -e "${YELLOW}Usage: ./run.sh <path-to-log-file>${NC}"
        exit 1
    fi

    LOG_FILE="examples/sample_json.log"
    echo -e "${GREEN}Using: $LOG_FILE${NC}"
else
    LOG_FILE="$1"

    # Check if file exists
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${RED}Error: File not found: $LOG_FILE${NC}"
        exit 1
    fi

    echo -e "${GREEN}Using: $LOG_FILE${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Starting API Log Viewer...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Run the application
python3 main.py "$LOG_FILE"

# Deactivate virtual environment on exit
deactivate