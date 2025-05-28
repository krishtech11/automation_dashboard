#!/bin/bash
# Shell script to set up the development environment on Linux/macOS

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}Found ${PYTHON_VERSION}${NC}"

# Check if Node.js is installed
if ! command_exists node; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 14 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}Node.js version: $(node --version)${NC}"

# Check if npm is installed
if ! command_exists npm; then
    echo -e "${RED}npm is not installed. Please install npm.${NC}"
    exit 1
fi

echo -e "${GREEN}npm version: $(npm --version)${NC}"

# Check if Tesseract OCR is installed
if ! command_exists tesseract; then
    echo -e "${YELLOW}Tesseract OCR is not installed. Document automation will not work without it.${NC}"
    echo -e "On Ubuntu/Debian: sudo apt install tesseract-ocr"
    echo -e "On macOS: brew install tesseract"
    echo -e "On Fedora: sudo dnf install tesseract"
else
    echo -e "${GREEN}Tesseract OCR is installed: $(tesseract --version | head -n 1)${NC}"
fi

# Set up backend
echo -e "\n${GREEN}Setting up backend...${NC}"
cd backend

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Created virtual environment${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install Python dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}Installed Python dependencies${NC}"

# Set up frontend
echo -e "\n${GREEN}Setting up frontend...${NC}"
cd ../frontend

# Install Node.js dependencies
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install Node.js dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}Installed Node.js dependencies${NC}"

# Return to project root
cd ..

# Make start script executable
chmod +x start_servers.sh

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "To start the application, run: ${GREEN}./start_servers.sh${NC}"
echo -e "Backend will be available at: ${GREEN}http://localhost:8000${NC}"
echo -e "Frontend will be available at: ${GREEN}http://localhost:3000${NC}"
