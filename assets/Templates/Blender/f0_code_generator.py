# trae_ai/agents/code_generator.py
import logging
from typing import Optional
import os


class CodeGenerator:
    """
    A powerful code-writing agent that can generate code based on prompts.
    This agent is designed to work with TDD workflows and generate minimal
    code fixes to make failing tests pass.
    """

    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.logger = logging.getLogger(__name__)

        if not self.api_key:
            self.logger.warning("No OpenAI API key found. Using mock responses.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            try:
                import openai

                openai.api_key = self.api_key
                self.openai = openai
            except ImportError:
                self.logger.warning(
                    "OpenAI package not installed. Using mock responses."
                )
                self.mock_mode = True

    def implement_from_prompt(self, prompt: str) -> str:
        """
        Generate code based on a given prompt.

        Args:
            prompt: The prompt describing what code to generate

        Returns:
            Generated code as a string
        """
        if self.mock_mode:
            return self._generate_mock_response(prompt)

        try:
            response = self.openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python developer specializing in Test-Driven Development. Generate minimal, clean code that fixes the specific issue described.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.1,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            return self._generate_mock_response(prompt)

    def _generate_mock_response(self, prompt: str) -> str:
        """Generate a mock response when API is not available."""
        if "ServiceRegistry" in prompt and "register" in prompt:
            return """
class ServiceRegistry:
    def __init__(self):
        self.services = {}
    
    def register(self, name: str, service: Any) -> None:
        \"\"\"Register a service with the given name.\"\"\"
        self.services[name] = service
    
    def get(self, name: str) -> Any:
        \"\"\"Get a registered service by name.\"\"\"
        return self.services.get(name)
"""

        elif "missing method" in prompt.lower():
            return """
def missing_method(self, *args, **kwargs):
    \"\"\"Placeholder method implementation.\"\"\"
    pass
"""

        else:
            return """
# Generated code fix
# This is a mock response - implement the actual fix based on the test failure
pass
"""

    def generate_test_code(self, description: str) -> str:
        """
        Generate test code based on a description.

        Args:
            description: Description of what the test should do

        Returns:
            Generated test code as a string
        """
        prompt = f"""
        Generate a pytest test case for the following requirement:
        {description}
        
        The test should follow TDD principles and be minimal but comprehensive.
        """

        return self.implement_from_prompt(prompt)
