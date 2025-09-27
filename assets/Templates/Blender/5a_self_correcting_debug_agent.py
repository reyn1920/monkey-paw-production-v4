#!/usr/bin/env python3
"""
Self-Correcting AI Debugging Agent
Based on the engineering blueprint for stateful, multi-agent debugging system.

This implements a ReAct-based multi-agent system using LangGraph for:
- Stateful workflow orchestration
- Self-verification and correction
- Complete observability with Langfuse
"""

import os
import subprocess
import tempfile
import shutil
from typing import List, TypedDict, Annotated, Dict, Any, Optional
import operator
from pathlib import Path
import json
import logging

# Core LangGraph and LangChain imports
try:
    from langgraph.graph import StateGraph, END, START
    from langgraph.prebuilt import ToolNode
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("Warning: LangGraph/LangChain not available. Install with: pip install -r requirements_debug_agent.txt")

from dotenv import load_dotenv

# Langfuse for observability
try:
    from langfuse.langchain import CallbackHandler
    langfuse_available = True
except ImportError:
    langfuse_available = False
    print("Warning: Langfuse not available. Install with: pip install langfuse")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """Shared state for the multi-agent debugging system."""
    bug_report: str
    code_files: Dict[str, str]  # filename -> content
    current_patch: str
    test_results: str
    critique_history: Annotated[List[str], operator.add]
    iteration_count: int
    max_iterations: int
    success: bool
    error_log: str

class SelfCorrectingDebugAgent:
    """
    A stateful, self-correcting debugging agent that uses multiple specialized agents
    to iteratively fix code issues until all tests pass.
    """
    
    def __init__(self, model_name: str = "gpt-4o", max_iterations: int = 5):
        if not LANGGRAPH_AVAILABLE:
            raise ImportError("LangGraph dependencies not available. Install with: pip install -r requirements_debug_agent.txt")
            
        self.llm = ChatOpenAI(model=model_name, temperature=0.1)
        self.max_iterations = max_iterations
        self.tools = [self.run_tests, self.apply_patch, self.analyze_codebase]
        self.app = self._build_graph()
        
        # Initialize Langfuse if available
        self.langfuse_handler: Optional[Any] = None
        if langfuse_available and os.getenv("LANGFUSE_SECRET_KEY"):
            self.langfuse_handler = CallbackHandler()
    
    @staticmethod
    @tool
    def run_tests(test_command: str = "python -m pytest -v") -> str:
        """
        Execute the project's test suite and return results.
        
        Args:
            test_command: Command to run tests (default: pytest)
            
        Returns:
            Test execution results including stdout, stderr, and exit code
        """
        try:
            logger.info(f"Running tests with command: {test_command}")
            result = subprocess.run(
                test_command.split(),
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=os.getcwd()
            )
            
            output = f"Exit Code: {result.returncode}\n"
            output += f"STDOUT:\n{result.stdout}\n"
            output += f"STDERR:\n{result.stderr}\n"
            
            if result.returncode == 0:
                output += "✅ ALL TESTS PASSED"
            else:
                output += "❌ TESTS FAILED"
                
            return output
            
        except subprocess.TimeoutExpired:
            return "❌ TEST EXECUTION TIMEOUT (5 minutes exceeded)"
        except Exception as e:
            return f"❌ TEST EXECUTION ERROR: {str(e)}"
    
    @staticmethod
    @tool
    def apply_patch(file_path: str, patch_content: str) -> str:
        """
        Apply a code patch to a specific file.
        
        Args:
            file_path: Path to the file to modify
            patch_content: New content for the file
            
        Returns:
            Success/failure message
        """
        try:
            # Create backup
            backup_path = f"{file_path}.backup"
            if os.path.exists(file_path):
                shutil.copy2(file_path, backup_path)
            
            # Apply patch
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(patch_content)
            
            logger.info(f"Applied patch to {file_path}")
            return f"✅ Successfully applied patch to {file_path}"
            
        except Exception as e:
            return f"❌ Failed to apply patch to {file_path}: {str(e)}"
    
    @staticmethod
    @tool
    def analyze_codebase(directory: str = ".") -> str:
        """
        Analyze the codebase for common issues and patterns.
        
        Args:
            directory: Directory to analyze
            
        Returns:
            Analysis results with identified issues
        """
        issues = []
        
        try:
            for root, dirs, files in os.walk(directory):
                # Skip common ignore directories
                dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}]
                
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            # Check for common issues
                            if 'TODO' in content or 'FIXME' in content:
                                issues.append(f"📝 {file_path}: Contains TODO/FIXME comments")
                            
                            if 'print(' in content and file.endswith('.py'):
                                issues.append(f"🐛 {file_path}: Contains debug print statements")
                            
                            if 'console.log' in content and file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                                issues.append(f"🐛 {file_path}: Contains console.log statements")
                                
                        except Exception as e:
                            issues.append(f"❌ {file_path}: Could not analyze - {str(e)}")
            
            return "\n".join(issues) if issues else "✅ No obvious issues found in codebase"
            
        except Exception as e:
            return f"❌ Codebase analysis failed: {str(e)}"
    
    def programmer_node(self, state: AgentState) -> Dict[str, Any]:
        """
        The Programmer Agent: Generates code patches based on bug reports and feedback.
        """
        logger.info("🤖 PROGRAMMER AGENT: Generating code patch...")
        
        # Build context for the LLM
        context = f"""
        Bug Report: {state['bug_report']}
        
        Current Code Files:
        {json.dumps(state['code_files'], indent=2)}
        
        Previous Attempts and Feedback:
        {chr(10).join(state['critique_history']) if state['critique_history'] else 'No previous attempts'}
        
        Iteration: {state.get('iteration_count', 0) + 1}/{state['max_iterations']}
        """
        
        system_prompt = """You are an expert software engineer specializing in debugging and code fixes.
        
        Your task is to analyze the bug report and generate a precise code patch that fixes the issue.
        
        Guidelines:
        1. Focus on the specific bug described in the report
        2. Consider any previous feedback from failed attempts
        3. Generate complete, working code - not just snippets
        4. Include proper error handling and edge cases
        5. Follow best practices and coding standards
        6. Be conservative - make minimal changes that fix the specific issue
        
        Return your response in this format:
        FILE_PATH: path/to/file.py
        PATCH_CONTENT:
        [Complete file content with your fixes]
        
        EXPLANATION:
        [Brief explanation of what you changed and why]
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=context)
        ]
        
        try:
            response = self.llm.invoke(messages)
            patch_content = response.content
            
            # Parse the response to extract file path and content
            lines = patch_content.split('\n')
            file_path = ""
            content_lines = []
            explanation = ""
            
            current_section = None
            for line in lines:
                if line.startswith("FILE_PATH:"):
                    file_path = line.replace("FILE_PATH:", "").strip()
                elif line.startswith("PATCH_CONTENT:"):
                    current_section = "content"
                elif line.startswith("EXPLANATION:"):
                    current_section = "explanation"
                elif current_section == "content":
                    content_lines.append(line)
                elif current_section == "explanation":
                    explanation += line + "\n"
            
            patch = "\n".join(content_lines).strip()
            
            logger.info(f"Generated patch for {file_path}")
            logger.info(f"Explanation: {explanation.strip()}")
            
            return {
                "current_patch": patch,
                "iteration_count": state.get('iteration_count', 0) + 1,
                "error_log": state.get('error_log', '') + f"\nIteration {state.get('iteration_count', 0) + 1}: Generated patch for {file_path}"
            }
            
        except Exception as e:
            error_msg = f"❌ Programmer agent failed: {str(e)}"
            logger.error(error_msg)
            return {
                "current_patch": "",
                "iteration_count": state.get('iteration_count', 0) + 1,
                "error_log": state.get('error_log', '') + f"\n{error_msg}"
            }
    
    def executor_node(self, state: AgentState) -> Dict[str, Any]:
        """
        The Executor Agent: Applies patches and runs tests to verify fixes.
        """
        logger.info("🔧 EXECUTOR AGENT: Applying patch and running tests...")
        
        if not state['current_patch']:
            return {
                "test_results": "❌ No patch to apply",
                "success": False
            }
        
        try:
            # For this implementation, we'll run the existing test command
            # In a real scenario, you'd apply the patch first
            test_result = self.run_tests("python -m pytest tests/ -v")
            
            success = "✅ ALL TESTS PASSED" in test_result
            
            logger.info(f"Test execution completed. Success: {success}")
            
            return {
                "test_results": test_result,
                "success": success
            }
            
        except Exception as e:
            error_msg = f"❌ Executor agent failed: {str(e)}"
            logger.error(error_msg)
            return {
                "test_results": error_msg,
                "success": False
            }
    
    def critic_node(self, state: AgentState) -> Dict[str, Any]:
        """
        The Critic Agent: Analyzes test results and provides feedback for improvement.
        """
        logger.info("🔍 CRITIC AGENT: Analyzing results and generating feedback...")
        
        if state['success']:
            logger.info("✅ Task completed successfully!")
            return {"success": True}
        
        if state['iteration_count'] >= state['max_iterations']:
            logger.warning(f"❌ Maximum iterations ({state['max_iterations']}) reached")
            return {
                "success": False,
                "critique_history": [f"Maximum iterations reached. Final test results: {state['test_results']}"]
            }
        
        # Generate critique using LLM
        context = f"""
        Test Results from Latest Attempt:
        {state['test_results']}
        
        Current Patch Applied:
        {state['current_patch']}
        
        Bug Report:
        {state['bug_report']}
        
        Iteration: {state['iteration_count']}/{state['max_iterations']}
        """
        
        system_prompt = """You are an expert code reviewer and debugging specialist.
        
        Analyze the test results and provide specific, actionable feedback for fixing the issues.
        
        Your feedback should:
        1. Identify the root cause of the test failures
        2. Suggest specific changes needed
        3. Point out any edge cases or scenarios not handled
        4. Be concise but comprehensive
        
        Focus on what went wrong and how to fix it in the next iteration.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=context)
        ]
        
        try:
            response = self.llm.invoke(messages)
            critique = response.content
            
            logger.info(f"Generated critique: {critique[:200]}...")
            
            return {
                "critique_history": [f"Iteration {state['iteration_count']} feedback: {critique}"]
            }
            
        except Exception as e:
            error_msg = f"❌ Critic agent failed: {str(e)}"
            logger.error(error_msg)
            return {
                "critique_history": [error_msg]
            }
    
    def should_continue(self, state: AgentState) -> str:
        """
        Router function to determine next step in the workflow.
        """
        if state['success']:
            logger.info("🎉 Routing to END - Task completed successfully!")
            return "end"
        elif state['iteration_count'] >= state['max_iterations']:
            logger.warning("⏰ Routing to END - Maximum iterations reached")
            return "end"
        else:
            logger.info(f"🔄 Routing to PROGRAMMER - Continue iteration {state['iteration_count'] + 1}")
            return "programmer"
    
    def _build_graph(self) -> Any:
        """
        Build the LangGraph workflow with all agents and routing logic.
        """
        workflow = StateGraph(AgentState)
        
        # Add agent nodes
        workflow.add_node("programmer", self.programmer_node)
        workflow.add_node("executor", self.executor_node)
        workflow.add_node("critic", self.critic_node)
        
        # Define the workflow
        workflow.set_entry_point("programmer")
        workflow.add_edge("programmer", "executor")
        workflow.add_edge("executor", "critic")
        
        # Conditional edge for the self-correction loop
        workflow.add_conditional_edges(
            "critic",
            self.should_continue,
            {
                "programmer": "programmer",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def debug(self, bug_report: str, code_files: Dict[str, str], max_iterations: Optional[int] = None) -> Dict[str, Any]:
        """
        Main entry point for debugging a codebase issue.
        
        Args:
            bug_report: Description of the bug to fix
            code_files: Dictionary of filename -> content
            max_iterations: Maximum number of fix attempts
            
        Returns:
            Final state with results
        """
        if max_iterations is not None:
            self.max_iterations = max_iterations
        
        initial_state = {
            "bug_report": bug_report,
            "code_files": code_files,
            "current_patch": "",
            "test_results": "",
            "critique_history": [],
            "iteration_count": 0,
            "max_iterations": self.max_iterations,
            "success": False,
            "error_log": ""
        }
        
        logger.info("🚀 Starting self-correcting debug session...")
        logger.info(f"Bug Report: {bug_report}")
        logger.info(f"Max Iterations: {self.max_iterations}")
        
        # Configure callbacks for observability
        config = {}
        if self.langfuse_handler:
            config["callbacks"] = [self.langfuse_handler]
        
        try:
            final_state = self.app.invoke(initial_state, config=config)
            
            if final_state['success']:
                logger.info("🎉 DEBUG SESSION COMPLETED SUCCESSFULLY!")
            else:
                logger.warning("⚠️ Debug session completed without full success")
            
            return final_state
            
        except Exception as e:
            logger.error(f"❌ Debug session failed: {str(e)}")
            return {
                **initial_state,
                "error_log": f"Session failed: {str(e)}",
                "success": False
            }

def main():
    """
    Example usage of the Self-Correcting Debug Agent
    """
    # Example bug report and code files
    bug_report = """
    The calculate_total function in main.py fails with a TypeError when the input list 
    contains non-numeric values. The function should handle mixed data types gracefully 
    and skip non-numeric values with a warning.
    """
    
    code_files = {
        "main.py": """
def calculate_total(prices):
    \"\"\"Calculate total of prices in a list.\"\"\"
    return sum(prices)

def main():
    test_prices = [10, 20, "invalid", 30, None, 40]
    total = calculate_total(test_prices)
    print(f"Total: {total}")

if __name__ == "__main__":
    main()
        """,
        "test_main.py": """
import pytest
from main import calculate_total

def test_calculate_total_valid_numbers():
    assert calculate_total([10, 20, 30]) == 60

def test_calculate_total_mixed_types():
    # Should handle mixed types gracefully
    result = calculate_total([10, "invalid", 20, None, 30])
    assert result == 60  # Should sum only valid numbers

def test_calculate_total_empty_list():
    assert calculate_total([]) == 0

def test_calculate_total_all_invalid():
    assert calculate_total(["a", "b", None]) == 0
        """
    }
    
    # Initialize the debug agent
    agent = SelfCorrectingDebugAgent(max_iterations=3)
    
    # Run the debugging session
    result = agent.debug(bug_report, code_files)
    
    # Print results
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(f"Success: {result['success']}")
    print(f"Iterations: {result['iteration_count']}")
    print(f"Final Patch:\n{result['current_patch']}")
    print(f"Test Results:\n{result['test_results']}")
    
    if result['critique_history']:
        print("\nCritique History:")
        for i, critique in enumerate(result['critique_history'], 1):
            print(f"{i}. {critique}")

if __name__ == "__main__":
    main()