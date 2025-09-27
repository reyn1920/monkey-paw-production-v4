from __future__ import annotations
import os
import httpx
from typing import List, Dict, Any

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("LLM_MODEL_NEMO9B", "nvidia/nemotron-nano-9b-v2:free")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_KEY}" if OPENROUTER_KEY else "",
    "HTTP-Referer": "https://localhost",
    "X-Title": "ONLINE_PRODUCTION",
}


async def nemo9b_chat(
    messages: List[Dict[str, str]], temperature: float = 0.2
) -> Dict[str, Any]:
    """
    Send chat messages to Nemotron-9B via OpenRouter API

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        temperature: Sampling temperature for response generation

    Returns:
        Dictionary containing the API response
    """
    payload = {"model": MODEL, "messages": messages, "temperature": temperature}
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(BASE_URL, json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json()


async def nemo9b_code_generation(prompt: str, language: str = "python") -> str:
    """
    Generate code using Nemotron-9B for specific programming language

    Args:
        prompt: Code generation prompt
        language: Target programming language

    Returns:
        Generated code as string
    """
    messages = [
        {
            "role": "system",
            "content": f"You are an expert {language} programmer. Generate clean, efficient, and well-documented code.",
        },
        {"role": "user", "content": prompt},
    ]

    response = await nemo9b_chat(messages, temperature=0.1)
    return response.get("choices", [{}])[0].get("message", {}).get("content", "")


async def nemo9b_code_review(code: str, language: str = "python") -> str:
    """
    Review code and suggest improvements using Nemotron-9B

    Args:
        code: Code to review
        language: Programming language of the code

    Returns:
        Code review and suggestions as string
    """
    messages = [
        {
            "role": "system",
            "content": f"You are an expert {language} code reviewer. Analyze the code for bugs, performance issues, security vulnerabilities, and suggest improvements.",
        },
        {
            "role": "user",
            "content": f"Please review this {language} code:\n\n```{language}\n{code}\n```",
        },
    ]

    response = await nemo9b_chat(messages, temperature=0.2)
    return response.get("choices", [{}])[0].get("message", {}).get("content", "")


async def nemo9b_debug_assistance(
    error_message: str, code_context: str, language: str = "python"
) -> str:
    """
    Get debugging assistance from Nemotron-9B

    Args:
        error_message: The error message or exception
        code_context: Relevant code context where error occurred
        language: Programming language

    Returns:
        Debugging suggestions and solutions as string
    """
    messages = [
        {
            "role": "system",
            "content": f"You are an expert {language} debugger. Help identify and fix runtime errors, exceptions, and bugs.",
        },
        {
            "role": "user",
            "content": f"I'm getting this error in my {language} code:\n\nError: {error_message}\n\nCode context:\n```{language}\n{code_context}\n```\n\nPlease help me debug and fix this issue.",
        },
    ]

    response = await nemo9b_chat(messages, temperature=0.3)
    return response.get("choices", [{}])[0].get("message", {}).get("content", "")


async def nemo9b_propose_diff(
    original_code: str, requirements: str, language: str = "python"
) -> str:
    """
    Propose code changes as a diff based on requirements

    Args:
        original_code: The original code to modify
        requirements: Description of changes needed
        language: Programming language

    Returns:
        Proposed diff or modified code as string
    """
    messages = [
        {
            "role": "system",
            "content": f"You are an expert {language} programmer. Propose specific code changes based on requirements. Show the changes clearly.",
        },
        {
            "role": "user",
            "content": f"Original {language} code:\n```{language}\n{original_code}\n```\n\nRequirements: {requirements}\n\nPlease propose the necessary changes.",
        },
    ]

    response = await nemo9b_chat(messages, temperature=0.2)
    return response.get("choices", [{}])[0].get("message", {}).get("content", "")


async def nemo9b_guided_debugging_loop(
    initial_problem: str, code: str, language: str = "python", max_iterations: int = 3
) -> List[Dict[str, str]]:
    """
    Run a guided debugging loop with iterative problem solving

    Args:
        initial_problem: Description of the initial problem
        code: The problematic code
        language: Programming language
        max_iterations: Maximum number of debugging iterations

    Returns:
        List of debugging steps and solutions
    """
    debugging_steps = []
    current_code = code
    current_problem = initial_problem

    for iteration in range(max_iterations):
        messages = [
            {
                "role": "system",
                "content": f"You are an expert {language} debugger conducting step-by-step debugging. Provide specific, actionable steps.",
            },
            {
                "role": "user",
                "content": f"Debugging iteration {iteration + 1}:\n\nProblem: {current_problem}\n\nCurrent code:\n```{language}\n{current_code}\n```\n\nProvide the next debugging step and any code modifications.",
            },
        ]

        response = await nemo9b_chat(messages, temperature=0.2)
        step_result = (
            response.get("choices", [{}])[0].get("message", {}).get("content", "")
        )

        debugging_steps.append(
            {
                "iteration": iteration + 1,
                "problem": current_problem,
                "solution": step_result,
                "code_state": current_code,
            }
        )

        # In a real implementation, you might extract updated code and problem from the response
        # For now, we'll break after getting the debugging suggestion
        break

    return debugging_steps
