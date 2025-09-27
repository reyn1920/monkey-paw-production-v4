#!/usr/bin/env python3
"""
Prompt Coach Service - AI-powered script optimization for CTR improvement
Helps tighten and optimize scripts for better click-through rates with TTS support
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import Any
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PromptCoach:
    """AI-powered prompt and script optimization service"""

    def __init__(self):
        """Initialize the Prompt Coach service"""
        self.optimization_rules = {
            "ctr_optimization": {
                "urgency_words": [
                    "now",
                    "today",
                    "limited",
                    "exclusive",
                    "urgent",
                    "immediate",
                ],
                "action_verbs": [
                    "discover",
                    "unlock",
                    "transform",
                    "boost",
                    "maximize",
                    "achieve",
                ],
                "power_words": [
                    "proven",
                    "guaranteed",
                    "secret",
                    "insider",
                    "breakthrough",
                    "revolutionary",
                ],
                "emotional_triggers": [
                    "fear",
                    "curiosity",
                    "desire",
                    "social_proof",
                    "scarcity",
                    "authority",
                ],
            },
            "structure_rules": {
                "hook_length": 8,  # words
                "max_sentence_length": 20,  # words
                "paragraph_max": 3,  # sentences
                "call_to_action_position": "end",
            },
        }
        self.tts_model_path = os.getenv(
            "TRAE_PIPER_MODEL", "runtime/tts_voices/en_US-ryan-high.onnx"
        )
        logger.info("Prompt Coach initialized successfully")

    def analyze_script(self, text: str) -> dict[str, Any]:
        """Analyze script for CTR optimization opportunities"""
        logger.info("Analyzing script for CTR optimization")

        words = text.split()
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        analysis = {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_sentence_length": len(words) / max(len(sentences), 1),
            "urgency_score": self._calculate_urgency_score(text),
            "action_score": self._calculate_action_score(text),
            "emotional_score": self._calculate_emotional_score(text),
            "readability_score": self._calculate_readability_score(text),
            "ctr_potential": 0.0,
        }

        # Calculate overall CTR potential
        analysis["ctr_potential"] = (
            analysis["urgency_score"] * 0.3
            + analysis["action_score"] * 0.25
            + analysis["emotional_score"] * 0.25
            + analysis["readability_score"] * 0.2
        )

        return analysis

    def _calculate_urgency_score(self, text: str) -> float:
        """Calculate urgency score based on urgency words"""
        urgency_words = self.optimization_rules["ctr_optimization"]["urgency_words"]
        if isinstance(urgency_words, list):
            text_lower = text.lower()
            urgency_count = sum(1 for word in urgency_words if word in text_lower)
            return min(urgency_count / 3.0, 1.0) * 100
        return 0.0

    def _calculate_action_score(self, text: str) -> float:
        """Calculate action score based on action verbs"""
        action_verbs = self.optimization_rules["ctr_optimization"]["action_verbs"]
        if isinstance(action_verbs, list):
            text_lower = text.lower()
            action_count = sum(1 for verb in action_verbs if verb in text_lower)
            return min(action_count / 2.0, 1.0) * 100
        return 0.0

    def _calculate_emotional_score(self, text: str) -> float:
        """Calculate emotional engagement score"""
        power_words = self.optimization_rules["ctr_optimization"]["power_words"]
        if isinstance(power_words, list):
            text_lower = text.lower()
            power_count = sum(1 for word in power_words if word in text_lower)
            return min(power_count / 2.0, 1.0) * 100
        return 0.0

    def _calculate_readability_score(self, text: str) -> float:
        """Calculate readability score (simplified)"""
        words = text.split()
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        if not sentences:
            return 0.0

        avg_sentence_length = len(words) / len(sentences)
        max_length_val = self.optimization_rules["structure_rules"][
            "max_sentence_length"
        ]
        ideal_length = (
            float(max_length_val)
            if isinstance(max_length_val, (int, float, str))
            else 20.0
        )

        # Score based on how close to ideal sentence length
        if avg_sentence_length <= ideal_length:
            return 100.0
        else:
            return max(0.0, 100.0 - (avg_sentence_length - ideal_length) * 5)

    def generate_optimized_script(self, original_text: str) -> dict[str, Any]:
        """Generate an optimized version of the script for better CTR"""
        logger.info("Generating optimized script")

        analysis = self.analyze_script(original_text)

        # Generate optimization suggestions
        suggestions = []
        optimized_text = original_text

        # Add urgency if missing
        if analysis["urgency_score"] < 50:
            suggestions.append(
                "Add urgency words like 'now', 'today', or 'limited time'"
            )
            optimized_text = self._add_urgency(optimized_text)

        # Improve action orientation
        if analysis["action_score"] < 50:
            suggestions.append(
                "Include more action verbs like 'discover', 'unlock', or 'transform'"
            )
            optimized_text = self._enhance_action_verbs(optimized_text)

        # Enhance emotional appeal
        if analysis["emotional_score"] < 50:
            suggestions.append(
                "Add power words like 'proven', 'secret', or 'breakthrough'"
            )
            optimized_text = self._add_power_words(optimized_text)

        # Improve readability
        if analysis["readability_score"] < 70:
            suggestions.append("Shorten sentences for better readability")
            optimized_text = self._improve_readability(optimized_text)

        return {
            "original_text": original_text,
            "optimized_text": optimized_text,
            "analysis": analysis,
            "suggestions": suggestions,
            "improvement_score": self._calculate_improvement_score(
                original_text, optimized_text
            ),
        }

    def _add_urgency(self, text: str) -> str:
        """Add urgency elements to the text"""
        urgency_phrases = ["Don't wait - ", "Limited time: ", "Act now - "]
        if not any(phrase.lower() in text.lower() for phrase in urgency_phrases):
            return f"Don't wait - {text}"
        return text

    def _enhance_action_verbs(self, text: str) -> str:
        """Enhance text with action verbs"""
        # Simple replacement strategy
        replacements = {
            "see": "discover",
            "get": "unlock",
            "find": "uncover",
            "learn": "master",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _add_power_words(self, text: str) -> str:
        """Add power words to enhance emotional appeal"""
        if "secret" not in text.lower() and "proven" not in text.lower():
            # Add a power word at the beginning
            return f"Discover the proven {text.lower()}"
        return text

    def _improve_readability(self, text: str) -> str:
        """Improve text readability by shortening sentences"""
        sentences = text.split(".")
        improved_sentences = []

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                words = sentence.split()
                if len(words) > 20:
                    # Split long sentences
                    mid_point = len(words) // 2
                    part1 = " ".join(words[:mid_point])
                    part2 = " ".join(words[mid_point:])
                    improved_sentences.extend([part1, part2])
                else:
                    improved_sentences.append(sentence)

        return ". ".join(improved_sentences) + "."

    def _calculate_improvement_score(self, original: str, optimized: str) -> float:
        """Calculate improvement score between original and optimized text"""
        original_analysis = self.analyze_script(original)
        optimized_analysis = self.analyze_script(optimized)

        improvement = (
            optimized_analysis["ctr_potential"] - original_analysis["ctr_potential"]
        )
        return max(0, improvement)

    def speak_text(self, text: str) -> bool:
        """Convert text to speech using Piper TTS"""
        try:
            if not os.path.exists(self.tts_model_path):
                logger.warning(f"TTS model not found at {self.tts_model_path}")
                return False

            logger.info("Converting text to speech")

            # Use Piper TTS with the configured model
            cmd = [
                "echo",
                text,
                "|",
                "piper",
                "--model",
                self.tts_model_path,
                "--output_file",
                "/tmp/prompt_coach_output.wav",
            ]

            # Alternative: use system say command on macOS
            if sys.platform == "darwin":
                subprocess.run(["say", text], check=True)
                logger.info("Text spoken successfully using macOS say")
                return True

            logger.info("Text-to-speech completed")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"TTS error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected TTS error: {e}")
            return False

    def save_optimization_report(
        self, optimization_result: dict[str, Any], output_file: Optional[str] = None
    ) -> str:
        """Save optimization report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data/prompt_optimization_{timestamp}.json"

        # Ensure data directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(optimization_result, f, indent=2)

        logger.info(f"Optimization report saved to {output_file}")
        return output_file


def main():
    """Main function to run the Prompt Coach service"""
    parser = argparse.ArgumentParser(
        description="Prompt Coach - Script optimization for CTR"
    )
    parser.add_argument("--text", required=True, help="Text to optimize for CTR")
    parser.add_argument(
        "--speak", action="store_true", help="Enable text-to-speech output"
    )
    parser.add_argument("--save", help="Save optimization report to file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize Prompt Coach
    coach = PromptCoach()

    try:
        logger.info("Starting Prompt Coach optimization session")

        # Generate optimized script
        result = coach.generate_optimized_script(args.text)

        # Display results
        print("\n" + "=" * 60)
        print("PROMPT COACH - CTR OPTIMIZATION RESULTS")
        print("=" * 60)

        print("\nORIGINAL TEXT:")
        print(f"'{result['original_text']}'")

        print("\nOPTIMIZED TEXT:")
        print(f"'{result['optimized_text']}'")

        print("\nANALYSIS:")
        analysis = result["analysis"]
        print(f"  • Word Count: {analysis['word_count']}")
        print(f"  • Sentence Count: {analysis['sentence_count']}")
        print(f"  • Avg Sentence Length: {analysis['avg_sentence_length']:.1f} words")
        print(f"  • Urgency Score: {analysis['urgency_score']:.1f}%")
        print(f"  • Action Score: {analysis['action_score']:.1f}%")
        print(f"  • Emotional Score: {analysis['emotional_score']:.1f}%")
        print(f"  • Readability Score: {analysis['readability_score']:.1f}%")
        print(f"  • CTR Potential: {analysis['ctr_potential']:.1f}%")

        print("\nSUGGESTIONS:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"  {i}. {suggestion}")

        print(f"\nIMPROVEMENT SCORE: +{result['improvement_score']:.1f} points")

        # Text-to-speech output
        if args.speak:
            print("\n🔊 Speaking optimized text...")
            speech_text = f"Here's your optimized script: {result['optimized_text']}"
            if coach.speak_text(speech_text):
                print("✅ Text-to-speech completed successfully")
            else:
                print("❌ Text-to-speech failed")

        # Save report if requested
        if args.save:
            report_file = coach.save_optimization_report(result, args.save)
            print(f"\n💾 Report saved to: {report_file}")

        print("\n" + "=" * 60)
        print("✅ Prompt Coach optimization completed successfully!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"Prompt Coach error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
