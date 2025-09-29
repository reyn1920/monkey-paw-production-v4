#!/usr/bin/env python3
"""
LangGraph Debug Agent Workflow
Implements a stateful, self-correcting debugging agent using LangGraph.
"""

import json
from typing import Dict, Any, List, TypedDict, Annotated
import operator

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# LangChain imports
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Observability imports (optional - comment out if Langfuse not available)
try:
    from langfuse.callback import CallbackHandler
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    print("⚠️ Langfuse not available - running without observability")
    LANGFUSE_AVAILABLE = False

# Local imports
from executor_tool import DeterministicExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Langfuse (optional)
if LANGFUSE_AVAILABLE:
    langfuse = Langfuse()
    langfuse_handler = CallbackHandler()
else:
    langfuse = None
    langfuse_handler = None

class AgentState(TypedDict):
    """State for the debug agent workflow."""
    messages: Annotated[List[BaseMessage], operator.add]
    bug_report: str
    current_analysis: str
    proposed_fix: str
    test_results: Dict[str, Any]
    iteration_count: int
    max_iterations: int
    is_resolved: bool
    execution_history: List[Dict[str, Any]]
    final_summary: str

class DebugAgent:
    """
    Stateful debugging agent using LangGraph workflow.
    """
    
    def __init__(self, 
                 model_name: str = "gpt-4",
                 max_iterations: int = 5,
                 temperature: float = 0.1):
        
        # Initialize components
        callbacks = [langfuse_handler] if langfuse_handler else []
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            callbacks=callbacks
        )
        self.executor = DeterministicExecutor()
        self.memory = MemorySaver()
        self.max_iterations = max_iterations
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
        
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Define the workflow
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("programmer", self._programmer_node)
        workflow.add_node("executor", self._executor_node)
        workflow.add_node("critic", self._critic_node)
        workflow.add_node("summarizer", self._summarizer_node)
        
        # Set entry point
        workflow.set_entry_point("programmer")
        
        # Add edges
        workflow.add_edge("programmer", "executor")
        workflow.add_edge("executor", "critic")
        
        # Add conditional edges from critic
        workflow.add_conditional_edges(
            "critic",
            self._should_continue,
            {
                "continue": "programmer",
                "finish": "summarizer",
                "max_iterations": "summarizer"
            }
        )
        
        workflow.add_edge("summarizer", END)
        
        # Compile with memory
        return workflow.compile(checkpointer=self.memory)
    
    def _programmer_node(self, state: AgentState) -> Dict[str, Any]:
        """Programmer node: Analyzes the bug and proposes a fix."""
        
        programmer_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Python programmer and debugger. 
            Your task is to analyze bug reports and propose precise fixes.
            
            Guidelines:
            1. Analyze the bug report thoroughly
            2. Identify the root cause
            3. Propose a specific, targeted fix
            4. Provide the exact code changes needed
            5. Explain your reasoning clearly
            
            Current iteration: {iteration_count}/{max_iterations}
            """),
            ("human", """
            Bug Report: {bug_report}
            
            Previous Analysis: {current_analysis}
            Previous Test Results: {test_results}
            
            Please provide:
            1. Updated analysis of the issue
            2. Proposed fix with exact code changes
            3. Explanation of why this fix should work
            """)
        ])
        
        # Format the prompt
        formatted_prompt = programmer_prompt.format_messages(
            iteration_count=state["iteration_count"],
            max_iterations=state["max_iterations"],
            bug_report=state["bug_report"],
            current_analysis=state.get("current_analysis", "None"),
            test_results=json.dumps(state.get("test_results", {}), indent=2)
        )
        
        # Get response from LLM
        response = self.llm.invoke(formatted_prompt)
        
        return {
            "messages": [response],
            "current_analysis": response.content,
            "proposed_fix": response.content,
            "iteration_count": state["iteration_count"]
        }
    
    def _executor_node(self, state: AgentState) -> Dict[str, Any]:
        """Executor node: Executes the proposed fix."""
        
        try:
            # Extract code from the proposed fix
            proposed_fix = state.get("proposed_fix", "")
            
            # Simple code extraction (look for code blocks)
            import re
            code_blocks = re.findall(r'```python\n(.*?)\n```', proposed_fix, re.DOTALL)
            
            if not code_blocks:
                # If no code blocks found, try to execute the entire proposed fix
                code_to_execute = proposed_fix
            else:
                # Use the first code block
                code_to_execute = code_blocks[0]
            
            # Execute the code
            result = self.executor.execute_python_code(code_to_execute)
            
            # Create response message
            if result["status"] == "success":
                response_content = f"✅ Code executed successfully!\nOutput: {result['output']}"
            else:
                response_content = f"❌ Code execution failed!\nError: {result['error']}\nExit code: {result['exit_code']}"
            
            return {
                "messages": [AIMessage(content=response_content)],
                "test_results": result,
                "execution_history": state.get("execution_history", []) + [result],
                "iteration_count": state["iteration_count"]
            }
            
        except Exception as e:
            error_msg = f"❌ Executor error: {str(e)}"
            return {
                "messages": [AIMessage(content=error_msg)],
                "test_results": {"status": "error", "error": str(e)},
                "iteration_count": state["iteration_count"]
            }
    
    def _critic_node(self, state: AgentState) -> Dict[str, Any]:
        """Critic node: Evaluates the execution results."""
        
        critic_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a critical code reviewer and tester.
            Your job is to evaluate whether a proposed fix has successfully resolved the bug.
            
            Guidelines:
            1. Analyze the execution results
            2. Determine if the bug is fixed
            3. Identify any remaining issues
            4. Decide if more iterations are needed
            """),
            ("human", """
            Original Bug Report: {bug_report}
            Proposed Fix: {proposed_fix}
            Execution Results: {test_results}
            Current Iteration: {iteration_count}/{max_iterations}
            
            Please evaluate:
            1. Is the bug fixed? (Yes/No)
            2. Are there any remaining issues?
            3. Should we continue iterating or finish?
            
            Respond with either "RESOLVED" if the bug is fixed, or "CONTINUE" if more work is needed.
            """)
        ])
        
        # Format the prompt
        formatted_prompt = critic_prompt.format_messages(
            bug_report=state["bug_report"],
            proposed_fix=state.get("proposed_fix", ""),
            test_results=json.dumps(state.get("test_results", {}), indent=2),
            iteration_count=state["iteration_count"],
            max_iterations=state["max_iterations"]
        )
        
        # Get response from LLM
        response = self.llm.invoke(formatted_prompt)
        
        # Determine if bug is resolved
        is_resolved = "RESOLVED" in response.content.upper()
        
        return {
            "messages": [response],
            "is_resolved": is_resolved,
            "iteration_count": state["iteration_count"] + 1
        }
    
    def _summarizer_node(self, state: AgentState) -> Dict[str, Any]:
        """Summarizer node: Creates final summary."""
        
        summarizer_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a technical writer creating a final summary of a debugging session.
            Provide a clear, concise summary of what was accomplished.
            """),
            ("human", """
            Bug Report: {bug_report}
            Total Iterations: {iteration_count}
            Final Status: {"RESOLVED" if state.get("is_resolved", False) else "UNRESOLVED"}
            Execution History: {execution_history}
            
            Please provide a final summary of the debugging session.
            """)
        ])
        
        # Format the prompt
        formatted_prompt = summarizer_prompt.format_messages(
            bug_report=state["bug_report"],
            iteration_count=state["iteration_count"],
            execution_history=json.dumps(state.get("execution_history", []), indent=2)
        )
        
        # Get response from LLM
        response = self.llm.invoke(formatted_prompt)
        
        return {
            "messages": [response],
            "final_summary": response.content
        }
    
    def _should_continue(self, state: AgentState) -> str:
        """Determine if the workflow should continue."""
        
        # Check if resolved
        if state.get("is_resolved", False):
            return "finish"
        
        # Check if max iterations reached
        if state["iteration_count"] >= state["max_iterations"]:
            return "max_iterations"
        
        return "continue"
    
    def debug(self, bug_report: str, thread_id: str = "debug_session") -> Dict[str, Any]:
        """
        Main entry point for debugging.
        """
        
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=bug_report)],
            "bug_report": bug_report,
            "current_analysis": "",
            "proposed_fix": "",
            "test_results": {},
            "iteration_count": 1,
            "max_iterations": self.max_iterations,
            "is_resolved": False,
            "execution_history": [],
            "final_summary": ""
        }
        
        # Run the workflow
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # Execute the workflow
            final_state = self.workflow.invoke(initial_state, config)
            
            return {
                "success": True,
                "final_state": final_state,
                "summary": final_state.get("final_summary", ""),
                "resolved": final_state.get("is_resolved", False),
                "iterations": final_state.get("iteration_count", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "summary": f"Workflow failed: {str(e)}",
                "resolved": False,
                "iterations": 0
            }

# Example usage and testing
if __name__ == "__main__":
    import traceback
    
    try:
        print("🚀 Initializing Debug Agent...")
        agent = DebugAgent()
        
        # Test bug report
        bug_report = """
        I have a Python function that's supposed to calculate the factorial of a number,
        but it's returning incorrect results for some inputs. The function is:
        
        def factorial(n):
            if n == 0:
                return 1
            return n * factorial(n - 1)
        
        When I call factorial(5), I expect 120, but I'm getting unexpected results.
        The tests are failing. Please help debug this issue.
        """
        
        print("🔍 Starting debug session...")
        result = agent.debug(bug_report)
        
        print("\n" + "="*50)
        print("DEBUG SESSION RESULTS")
        print("="*50)
        print(f"Success: {result['success']}")
        print(f"Resolved: {result['resolved']}")
        print(f"Iterations: {result['iterations']}")
        print(f"\nSummary:\n{result['summary']}")
        
        if not result['success']:
            print(f"\nError: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error running debug agent: {str(e)}")
        traceback.print_exc()