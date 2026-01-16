#!/bin/bash

# ============= Python CI/CD Project Setup Script =============
# Automated setup for the complete project environment
# Sets up virtual environment, installs dependencies, and verifies setup

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# ============= HELPER FUNCTIONS =============

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_step() {
    echo -e "${BLUE}→ $1${NC}"
}

# ============= PRE-FLIGHT CHECKS =============

print_header "Pre-Flight Checks"

# Check Python installation
print_step "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.9+"
    exit 1
fi
python_version=$(python3 --version | awk '{print $2}')
print_success "Python $python_version found"

# Check Git installation
print_step "Checking Git installation..."
if ! command -v git &> /dev/null; then
    print_warning "Git is not installed. Some features may not work."
else
    print_success "Git found"
fi

# ============= DIRECTORY STRUCTURE =============

# print_header "Creating Directory Structure"

# print_step "Creating app directory..."
# mkdir -p app
# print_success "app/ directory ready"

# print_step "Creating tests directory..."
# mkdir -p tests
# print_success "tests/ directory ready"

# print_step "Creating .github/workflows directory..."
# mkdir -p .github/workflows
# print_success ".github/workflows/ directory ready"

# ============= VIRTUAL ENVIRONMENT =============

print_header "Setting Up Virtual Environment"

if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    print_step "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

print_step "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# ============= DEPENDENCY INSTALLATION =============

print_header "Installing Dependencies"

print_step "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

if [ -f "requirements.txt" ]; then
    print_step "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt > /dev/null 2>&1
    print_success "Dependencies installed"
else
    print_warning "requirements.txt not found. Skipping dependency installation."
fi

# ============= GIT SETUP =============

print_header "Git Configuration"

if command -v git &> /dev/null; then
    if [ -d ".git" ]; then
        print_warning "Git repository already initialized. Skipping."
    else
        print_step "Initializing Git repository..."
        git init > /dev/null 2>&1
        print_success "Git repository initialized"
    fi
    
    if [ -f ".gitignore" ]; then
        print_success ".gitignore found and configured"
    fi
else
    print_warning "Git not found. Skipping Git setup."
fi

# ============= VERIFICATION =============

print_header "Verifying Installation"

# Check Python
print_step "Verifying Python..."
python --version
print_success "Python verified"

# Check pip packages
print_step "Verifying installed packages..."
pip list | grep -E "Flask|pytest|requests" > /dev/null 2>&1
print_success "Key packages installed"

# Check directory structure
print_step "Verifying directory structure..."
if [ -d "app" ] && [ -d "tests" ] && [ -d ".github/workflows" ]; then
    print_success "Directory structure verified"
else
    print_error "Directory structure incomplete!"
    exit 1
fi

# Check files
print_step "Checking for required files..."
required_files=("app/__init__.py" "tests/__init__.py" "Dockerfile" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file found"
    else
        print_warning "$file not found (will be created separately)"
    fi
done

# ============= SUMMARY =============

print_header "Setup Complete!"

echo ""
print_success "Project setup completed successfully!"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Activate environment: ${YELLOW}source venv/bin/activate${NC}"
echo "2. Run tests: ${YELLOW}pytest tests/ -v${NC}"
echo "3. Start app: ${YELLOW}python -m flask run${NC}"
echo "4. Visit: ${YELLOW}http://localhost:5000${NC}"
echo ""
print_success "Ready to start learning! 🚀"
echo ""
