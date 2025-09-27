# Debug Agent System

A sophisticated AI-powered debugging agent built with LangGraph that automatically analyzes, fixes, and validates code issues using a multi-agent workflow.

## 🚀 Features

- **Automated Bug Detection**: Intelligent analysis of error messages and stack traces
- **Code Generation**: AI-powered fix suggestions and implementations
- **Test Execution**: Deterministic test running with comprehensive validation
- **Multi-Agent Workflow**: Coordinated programmer, executor, critic, and summarizer agents
- **Observability**: Optional Langfuse integration for workflow tracing
- **Deterministic Execution**: Consistent and reproducible test results

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/debug-agent
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv debug_agent_env
   source debug_agent_env/bin/activate  # On Windows: debug_agent_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

## ⚙️ Configuration

### Required Environment Variables

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_actual_openai_api_key

# Langfuse Configuration (Optional)
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE_HOST=http://localhost:3000

# LangSmith Configuration (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=debug-agent

# Debug Agent Configuration
DEBUG_AGENT_MAX_ITERATIONS=5
DEBUG_AGENT_TIMEOUT=300
```

### API Key Setup

1. **OpenAI API Key** (Required):
   - Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
   - Create a new API key
   - Replace `your_actual_openai_api_key` in `.env`

2. **Langfuse** (Optional - for observability):
   - Set up local Langfuse instance or use cloud version
   - Get your secret and public keys
   - Update the Langfuse configuration in `.env`

## 🚀 Usage

### Quick Start

```bash
# Activate environment
source debug_agent_env/bin/activate

# Run the debug agent
python graph.py
```

### Using the One-Click Script

```bash
# Make script executable
chmod +x run_debug_agent.sh

# Run the debug agent
./run_debug_agent.sh
```

### Programmatic Usage

```python
from graph import DebugAgent

# Initialize the debug agent
agent = DebugAgent()

# Define a bug report
bug_report = {
    "description": "Function returns None instead of expected value",
    "error_message": "AssertionError: Expected 42, got None",
    "code_snippet": '''
def calculate_answer():
    # Missing return statement
    result = 6 * 7
''',
    "test_case": '''
def test_calculate_answer():
    assert calculate_answer() == 42
'''
}

# Run the debug session
result = agent.debug(bug_report)

print(f"Success: {result['success']}")
print(f"Summary: {result['summary']}")
```

## 🏗️ Architecture

### Core Components

1. **DeterministicExecutor** (`executor_tool.py`):
   - Handles code execution and test running
   - Provides consistent, reproducible results
   - Manages execution history and validation

2. **DebugAgent** (`graph.py`):
   - Orchestrates the multi-agent workflow
   - Manages state transitions and decision logic
   - Integrates with observability platforms

### Workflow Nodes

1. **Programmer Node**: Analyzes bugs and generates fixes
2. **Executor Node**: Runs tests and validates solutions
3. **Critic Node**: Evaluates results and suggests improvements
4. **Summarizer Node**: Provides final analysis and recommendations

### State Management

The system uses a typed state dictionary to track:
- Bug reports and descriptions
- Generated code and fixes
- Test results and execution history
- Iteration counts and success metrics

## 🧪 Testing

### Run Individual Components

```bash
# Test the executor tool
python executor_tool.py

# Test the complete workflow
python graph.py
```

### Example Test Cases

The system includes built-in test cases that demonstrate:
- Successful bug fixes
- Failed execution scenarios
- Edge cases and error handling

## 🔧 Troubleshooting

### Common Issues

1. **API Key Errors**:
   ```
   Error: Incorrect API key provided
   ```
   - Verify your OpenAI API key in `.env`
   - Ensure the key has sufficient credits

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'langgraph'
   ```
   - Activate the virtual environment
   - Install missing dependencies: `pip install -r requirements.txt`

3. **Environment Variable Issues**:
   ```
   ValueError: embedded null byte
   ```
   - Recreate the `.env` file
   - Ensure no hidden characters or encoding issues

### Debug Mode

Enable verbose logging by setting:
```env
DEBUG_AGENT_VERBOSE=true
```

## 📊 Observability

### Langfuse Integration

When properly configured, the system provides:
- Workflow execution traces
- Performance metrics
- Error tracking and analysis
- Cost monitoring

### LangSmith Integration

Optional integration for:
- Advanced debugging
- Prompt optimization
- Performance analytics

## 🔒 Security

- API keys are externalized in environment variables
- No sensitive data is logged or stored
- Execution is sandboxed within the virtual environment

## 📈 Performance

- **Average execution time**: 30-60 seconds per bug report
- **Success rate**: Depends on bug complexity and code quality
- **Resource usage**: Minimal CPU and memory footprint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the example usage
3. Examine the test cases for reference implementations

---

**Note**: This system requires valid API keys to function. The example keys in `.env` are placeholders and must be replaced with actual credentials.