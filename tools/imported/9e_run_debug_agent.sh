#!/bin/bash

# Debug Agent One-Click Runner
# This script sets up and runs the AI-powered debug agent system

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[DEBUG AGENT]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main execution function
main() {
    print_status "🚀 Starting Debug Agent System..."
    
    # Check Python installation
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
        exit 1
    fi
    
    # Check if we're in the right directory
    if [[ ! -f "graph.py" ]] || [[ ! -f "executor_tool.py" ]]; then
        print_error "Debug agent files not found. Please run this script from the debug agent directory."
        exit 1
    fi
    
    # Check if virtual environment exists
    if [[ ! -d "debug_agent_env" ]]; then
        print_warning "Virtual environment not found. Creating debug_agent_env..."
        python3 -m venv debug_agent_env
        print_success "Virtual environment created."
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source debug_agent_env/bin/activate
    
    # Check if requirements.txt exists and install dependencies
    if [[ -f "requirements.txt" ]]; then
        print_status "Installing/updating dependencies..."
        pip install -q -r requirements.txt
        print_success "Dependencies installed."
    else
        print_warning "requirements.txt not found. Installing core dependencies..."
        pip install -q openai langchain langgraph langfuse python-dotenv
        print_success "Core dependencies installed."
    fi
    
    # Check if .env file exists
    if [[ ! -f ".env" ]]; then
        print_warning ".env file not found. Creating from template..."
        if [[ -f ".env.example" ]]; then
            cp .env.example .env
            print_warning "Please edit .env file with your actual API keys before running again."
            print_status "Opening .env file for editing..."
            ${EDITOR:-nano} .env
        else
            print_error ".env file and .env.example not found. Please create .env with required API keys."
            exit 1
        fi
    fi
    
    # Validate OpenAI API key
    if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
        print_warning "Default OpenAI API key detected in .env file."
        print_warning "Please update .env with your actual OpenAI API key."
        read -p "Do you want to edit .env now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        else
            print_error "Cannot proceed without valid API key. Exiting."
            exit 1
        fi
    fi
    
    # Run the debug agent
    print_status "🔍 Launching Debug Agent..."
    echo
    python graph.py
    
    # Check exit status
    if [[ $? -eq 0 ]]; then
        print_success "✅ Debug Agent completed successfully!"
    else
        print_error "❌ Debug Agent encountered an error."
        exit 1
    fi
}

# Function to show help
show_help() {
    echo "Debug Agent One-Click Runner"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -t, --test     Run executor tool tests only"
    echo "  -s, --setup    Setup environment only (don't run)"
    echo "  -c, --clean    Clean virtual environment and reinstall"
    echo
    echo "Examples:"
    echo "  $0              # Run the debug agent"
    echo "  $0 --test       # Run tests only"
    echo "  $0 --setup      # Setup environment only"
    echo "  $0 --clean      # Clean and reinstall environment"
}

# Function to run tests only
run_tests() {
    print_status "🧪 Running executor tool tests..."
    source debug_agent_env/bin/activate
    python executor_tool.py
}

# Function to setup environment only
setup_only() {
    print_status "🛠️ Setting up environment..."
    
    if [[ -d "debug_agent_env" ]]; then
        print_status "Virtual environment already exists."
    else
        print_status "Creating virtual environment..."
        python3 -m venv debug_agent_env
    fi
    
    source debug_agent_env/bin/activate
    
    if [[ -f "requirements.txt" ]]; then
        pip install -q -r requirements.txt
    else
        pip install -q openai langchain langgraph langfuse python-dotenv
    fi
    
    print_success "Environment setup complete!"
    print_status "Don't forget to configure your .env file with actual API keys."
}

# Function to clean environment
clean_environment() {
    print_status "🧹 Cleaning environment..."
    
    if [[ -d "debug_agent_env" ]]; then
        rm -rf debug_agent_env
        print_success "Virtual environment removed."
    fi
    
    setup_only
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -t|--test)
        run_tests
        exit 0
        ;;
    -s|--setup)
        setup_only
        exit 0
        ;;
    -c|--clean)
        clean_environment
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac