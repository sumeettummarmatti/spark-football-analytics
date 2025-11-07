#!/bin/bash

echo "🚀 SPARK Football Analytics - Setup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+ first.${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js version:$(node --version)${NC}"
echo -e "${GREEN}✅ Python version:$(python3 --version)${NC}"
echo ""

# Install Frontend Dependencies
echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
cd frontend
if npm install; then
    echo -e "${GREEN}✅ Frontend dependencies installed successfully!${NC}"
else
    echo -e "${RED}❌ Failed to install frontend dependencies${NC}"
    exit 1
fi
cd ..

# Install Backend Dependencies
echo ""
echo -e "${YELLOW}📦 Installing backend dependencies...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if pip install --upgrade pip && pip install -r requirements.txt; then
    echo -e "${GREEN}✅ Backend dependencies installed successfully!${NC}"
else
    echo -e "${RED}❌ Failed to install backend dependencies${NC}"
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}✨ Setup completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Start database: docker-compose up -d postgres"
echo "2. Start backend: cd backend && source venv/bin/activate && python -m uvicorn src.main:app --reload"
echo "3. Start frontend: cd frontend && npm run dev"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"

