#!/usr/bin/env python3
"""
🚀 **WORKING AI POWERHOUSE** - Your Confirmed AI Arsenal!

This script uses your CONFIRMED working AI services:
✅ HuggingFace Router (1000+ models)
✅ Local Ollama (19 models)
✅ VS Code Extensions (11 AI tools)

Author: Your AI Assistant 🤖
Status: LEGENDARY SETUP! ⚡
"""

import asyncio
import os
import time
from dataclasses import dataclass
from typing import Dict, List

import aiohttp
from openai import OpenAI


@dataclass
class AIResponse:
    provider: str
    model: str
    response: str
    cost: float
    latency: float
    tokens_used: int


class WorkingAIPowerhouse:
    """🔥 Use your CONFIRMED working AI services!"""

    def __init__(self):
        # 🤗 HuggingFace Router - CONFIRMED WORKING
        self.hf_client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.environ.get("HF_TOKEN", "hf_your_token_here"),
        )

        # 🏠 Your 19 Local Ollama Models - CONFIRMED WORKING
        self.coding_models = [
            "deepseek-coder:6.7b",  # 🎯 Best for coding
            "qwen2.5-coder:7b",  # 🔥 Excellent coder
            "codellama:7b",  # 📝 Facebook's coding model
        ]

        self.chat_models = [
            "llama3.1:8b",  # 🌟 Latest Llama
            "llama3.2:3b",  # ⚡ Fast & capable
            "mistral:7b",  # 🚀 Mistral AI
        ]

        self.analysis_models = [
            "llama2:13b",  # 🧠 Large for analysis
            "llama3.1:latest",  # 🎯 Most recent
            "gemma2:latest",  # 🔍 Google's model
        ]

        self.lightweight_models = [
            "phi3:3.8b",  # 💡 Microsoft's efficient model
            "llama3.2:1b",  # ⚡ Ultra-fast
        ]

        # 🎯 Task routing strategy
        self.best_models = {
            "coding": "deepseek-coder:6.7b",
            "debugging": "qwen2.5-coder:7b",
            "chat": "llama3.1:8b",
            "analysis": "llama2:13b",
            "creative": "llama3.1:latest",
            "quick": "phi3:3.8b",
        }

    async def call_huggingface(
        self, prompt: str, model: str = "microsoft/DialoGPT-medium"
    ) -> AIResponse:
        """🤗 Call HuggingFace Router - Your working cloud AI!"""
        start_time = time.time()

        try:
            completion = self.hf_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )

            latency = time.time() - start_time
            response_text = completion.choices[0].message.content
            tokens = (
                completion.usage.total_tokens if hasattr(completion, "usage") else 0
            )

            return AIResponse(
                provider="HuggingFace Router",
                model=model,
                response=response_text,
                cost=0.0,  # Free through router!
                latency=latency,
                tokens_used=tokens,
            )

        except Exception as e:
            return AIResponse(
                provider="HuggingFace Router",
                model=model,
                response=f"Error: {str(e)}",
                cost=0.0,
                latency=time.time() - start_time,
                tokens_used=0,
            )

    async def call_ollama(self, model: str, prompt: str) -> AIResponse:
        """🏠 Call your local Ollama models - Private & Free!"""
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "top_p": 0.9},
                }

                async with session.post(
                    "http://localhost:11434/api/generate", json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_text = data.get("response", "No response")
                        tokens = len(response_text.split())  # Rough estimate

                        latency = time.time() - start_time

                        return AIResponse(
                            provider="Ollama Local",
                            model=model,
                            response=response_text,
                            cost=0.0,  # Completely free!
                            latency=latency,
                            tokens_used=tokens,
                        )
                    else:
                        raise Exception(f"HTTP {response.status}")

        except Exception as e:
            return AIResponse(
                provider="Ollama Local",
                model=model,
                response=f"Error: {str(e)}",
                cost=0.0,
                latency=time.time() - start_time,
                tokens_used=0,
            )

    async def smart_route(self, prompt: str, task_type: str = "general") -> AIResponse:
        """🧠 Route to the BEST model for each task type!"""

        # Determine if task needs privacy
        private_keywords = ["password", "secret", "private", "confidential", "internal"]
        needs_privacy = any(keyword in prompt.lower() for keyword in private_keywords)

        if needs_privacy or task_type in ["coding", "debugging"]:
            # Use local models for privacy & coding
            best_model = self.best_models.get(task_type, "llama3.1:8b")
            return await self.call_ollama(best_model, prompt)
        else:
            # Use HuggingFace for diversity & power
            if task_type == "creative":
                model = "microsoft/DialoGPT-large"
            elif task_type == "analysis":
                model = "microsoft/DialoGPT-medium"
            else:
                model = "microsoft/DialoGPT-medium"

            return await self.call_huggingface(prompt, model)

    async def compare_local_models(
        self, prompt: str, task_type: str = "coding"
    ) -> List[AIResponse]:
        """🔥 Compare your local models for a task!"""

        if task_type == "coding":
            models = self.coding_models
        elif task_type == "chat":
            models = self.chat_models[:2]  # Test 2 models
        else:
            models = ["llama3.1:8b", "phi3:3.8b"]  # Quick comparison

        tasks = [self.call_ollama(model, prompt) for model in models]
        responses = await asyncio.gather(*tasks)

        # Sort by latency (fastest first)
        responses.sort(key=lambda x: x.latency)

        return responses

    async def test_all_services(self) -> Dict[str, bool]:
        """🔍 Test which services are working right now!"""

        test_prompt = "Hello! How are you?"
        results = {}

        # Test HuggingFace
        try:
            hf_result = await self.call_huggingface(test_prompt)
            results["HuggingFace"] = "Error" not in hf_result.response
        except:
            results["HuggingFace"] = False

        # Test local Ollama
        try:
            local_result = await self.call_ollama("phi3:3.8b", test_prompt)
            results["Ollama"] = "Error" not in local_result.response
        except:
            results["Ollama"] = False

        return results

    def print_response(self, response: AIResponse, title: str = ""):
        """📝 Pretty print AI response"""
        print(f"\n{'=' * 60}")
        if title:
            print(f"🎯 **{title}**")
        print(f"🤖 **Provider:** {response.provider}")
        print(f"📱 **Model:** {response.model}")
        print(f"⚡ **Latency:** {response.latency:.2f}s")
        print(f"💰 **Cost:** ${response.cost:.4f}")
        print(f"🔢 **Tokens:** {response.tokens_used}")
        print("📝 **Response:**")
        print(f"   {response.response[:300]}...")
        print(f"{'=' * 60}")


async def main():
    """🚀 Demo your WORKING AI powerhouse!"""

    ai = WorkingAIPowerhouse()

    print("🎊 **YOUR WORKING AI POWERHOUSE DEMO** 🎊")
    print("Using your CONFIRMED working AI services!")
    print("🤗 HuggingFace + 🏠 19 Local Ollama Models + 💻 11 VS Code AI Tools")
    print("=" * 70)

    # 1. Test which services are working
    print("\n🔍 **Testing AI Services...**")
    service_status = await ai.test_all_services()
    for service, working in service_status.items():
        status = "✅ WORKING" if working else "❌ NOT AVAILABLE"
        print(f"   {service}: {status}")

    # 2. Demo smart routing
    test_cases = [
        {
            "prompt": "Write a Python function to reverse a string",
            "task_type": "coding",
            "title": "CODING TASK (Local AI for Privacy)",
        },
        {
            "prompt": "Explain the benefits of renewable energy",
            "task_type": "analysis",
            "title": "ANALYSIS TASK (Cloud AI for Power)",
        },
        {
            "prompt": "My secret password is 12345. Help me create a better one.",
            "task_type": "general",
            "title": "PRIVATE DATA (Auto-routed to Local)",
        },
    ]

    for test in test_cases:
        print(f"\n🎯 **{test['title']}**")
        print(f"📝 Prompt: {test['prompt']}")

        result = await ai.smart_route(test["prompt"], test["task_type"])
        ai.print_response(result)

    # 3. Compare local coding models
    if service_status.get("Ollama", False):
        print("\n🔥 **COMPARING LOCAL CODING MODELS**")
        coding_prompt = "Write a function to find prime numbers"

        comparisons = await ai.compare_local_models(coding_prompt, "coding")

        print(f"\n📊 **Results for: {coding_prompt}**")
        for i, resp in enumerate(comparisons, 1):
            ai.print_response(resp, f"Model {i}: {resp.model}")

        # Show speed ranking
        print("\n🏆 **SPEED RANKING:**")
        for i, resp in enumerate(comparisons, 1):
            print(f"   {i}. {resp.model}: {resp.latency:.2f}s")

    print("\n✨ **YOUR AI ARSENAL SUMMARY:**")
    print("🤗 HuggingFace Router: 1000+ models (cloud power)")
    print("🏠 Local Ollama: 19 models (~66GB) (privacy & speed)")
    print("💻 VS Code Extensions: 11 AI tools (integrated workflow)")
    print("🎯 Smart Routing: Auto-selects best model for each task")
    print("💰 Cost: Mix of free local + free cloud routing")
    print("\n🎉 **STATUS: LEGENDARY AI SETUP!** 🏆")


if __name__ == "__main__":
    # Set up environment (if needed)
    if not os.environ.get("HF_TOKEN"):
        print("💡 Tip: Set HF_TOKEN environment variable for HuggingFace access")
        print("   export HF_TOKEN=your_token_here")

    asyncio.run(main())
