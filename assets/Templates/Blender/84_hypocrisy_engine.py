"""Hypocrisy detection and analysis engine."""

from typing import Any, Optional
from datetime import datetime
import logging
import re

# Logger setup
logger = logging.getLogger(__name__)


class HypocrisyAnalyzer:
    """Analyzes text for potential hypocrisy patterns."""

    def __init__(self):
        self.contradiction_patterns = [
            # Basic contradiction patterns
            (r"never\s+\w+", r"always\s+\w+"),
            (r"I\s+don't\s+\w+", r"I\s+\w+"),
            (r"we\s+should\s+not\s+\w+", r"we\s+must\s+\w+"),
            (r"against\s+\w+", r"support\s+\w+"),
            (r"oppose\s+\w+", r"endorse\s+\w+"),
        ]

        self.temporal_indicators = [
            "yesterday",
            "today",
            "tomorrow",
            "last week",
            "next week",
            "previously",
            "now",
            "currently",
            "before",
            "after",
            "in the past",
            "going forward",
            "historically",
        ]

    def analyze_text(
        self, text: str, context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Analyze text for hypocrisy patterns."""
        try:
            if not text or not isinstance(text, str):
                return self._create_empty_result("Invalid input text")

            # Clean and normalize text
            normalized_text = self._normalize_text(text)

            # Perform various analyses
            contradiction_analysis = self._detect_contradictions(normalized_text)
            temporal_analysis = self._analyze_temporal_inconsistencies(normalized_text)
            sentiment_analysis = self._analyze_sentiment_shifts(normalized_text)

            # Calculate overall hypocrisy score
            hypocrisy_score = self._calculate_hypocrisy_score(
                contradiction_analysis, temporal_analysis, sentiment_analysis
            )

            result = {
                "timestamp": datetime.utcnow().isoformat(),
                "text_length": len(text),
                "hypocrisy_score": hypocrisy_score,
                "analysis": {
                    "contradictions": contradiction_analysis,
                    "temporal_inconsistencies": temporal_analysis,
                    "sentiment_shifts": sentiment_analysis,
                },
                "summary": self._generate_summary(
                    hypocrisy_score, contradiction_analysis, temporal_analysis
                ),
                "context": context or {},
            }

            return result

        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return self._create_error_result(str(e))

    def _normalize_text(self, text: str) -> str:
        """Normalize text for analysis."""
        # Convert to lowercase
        normalized = text.lower()

        # Remove extra whitespace
        normalized = re.sub(r"\s+", " ", normalized)

        # Remove special characters but keep punctuation
        normalized = re.sub(r"[^\w\s.,!?;:-]", "", normalized)

        return normalized.strip()

    def _detect_contradictions(self, text: str) -> dict[str, Any]:
        """Detect contradictory statements in text."""
        contradictions = []

        try:
            # Split text into sentences
            sentences = re.split(r"[.!?]+", text)

            # Check for contradiction patterns
            for i, sentence1 in enumerate(sentences):
                for j, sentence2 in enumerate(sentences[i + 1 :], i + 1):
                    contradiction = self._check_sentence_contradiction(
                        sentence1, sentence2
                    )
                    if contradiction:
                        contradictions.append(
                            {
                                "sentence1": sentence1.strip(),
                                "sentence2": sentence2.strip(),
                                "type": contradiction["type"],
                                "confidence": contradiction["confidence"],
                                "positions": [i, j],
                            }
                        )

            return {
                "found": len(contradictions) > 0,
                "count": len(contradictions),
                "contradictions": contradictions[:5],  # Limit to top 5
                "severity": self._assess_contradiction_severity(contradictions),
            }

        except Exception as e:
            logger.error(f"Error detecting contradictions: {e}")
            return {"found": False, "count": 0, "contradictions": [], "error": str(e)}

    def _check_sentence_contradiction(
        self, sentence1: str, sentence2: str
    ) -> Optional[dict[str, Any]]:
        """Check if two sentences contradict each other."""
        try:
            # Check for direct negation patterns
            if self._contains_negation_pair(sentence1, sentence2):
                return {"type": "direct_negation", "confidence": 0.8}

            # Check for opposite sentiment words
            if self._contains_opposite_sentiments(sentence1, sentence2):
                return {"type": "sentiment_opposition", "confidence": 0.6}

            # Check for contradiction patterns
            for pattern1, pattern2 in self.contradiction_patterns:
                if re.search(pattern1, sentence1) and re.search(pattern2, sentence2):
                    return {"type": "pattern_contradiction", "confidence": 0.7}

            return None

        except Exception:
            return None

    def _contains_negation_pair(self, sentence1: str, sentence2: str) -> bool:
        """Check if sentences contain negation pairs."""
        negation_words = ["not", "never", "no", "don't", "won't", "can't", "shouldn't"]
        affirmation_words = ["always", "yes", "do", "will", "can", "should", "must"]

        # Simple heuristic: check for negation in one and affirmation in
        # another
        has_negation_1 = any(word in sentence1 for word in negation_words)
        has_affirmation_2 = any(word in sentence2 for word in affirmation_words)

        has_negation_2 = any(word in sentence2 for word in negation_words)
        has_affirmation_1 = any(word in sentence1 for word in affirmation_words)

        return (has_negation_1 and has_affirmation_2) or (
            has_negation_2 and has_affirmation_1
        )

    def _contains_opposite_sentiments(self, sentence1: str, sentence2: str) -> bool:
        """Check for opposite sentiment words."""
        positive_words = [
            "good",
            "great",
            "excellent",
            "love",
            "support",
            "agree",
            "favor",
        ]
        negative_words = [
            "bad",
            "terrible",
            "awful",
            "hate",
            "oppose",
            "disagree",
            "against",
        ]

        has_positive_1 = any(word in sentence1 for word in positive_words)
        has_negative_2 = any(word in sentence2 for word in negative_words)

        has_negative_1 = any(word in sentence1 for word in negative_words)
        has_positive_2 = any(word in sentence2 for word in positive_words)

        return (has_positive_1 and has_negative_2) or (
            has_negative_1 and has_positive_2
        )

    def _assess_contradiction_severity(
        self, contradictions: list[dict[str, Any]]
    ) -> str:
        """Assess the severity of contradictions found."""
        if not contradictions:
            return "none"

        high_confidence_count = sum(
            1 for c in contradictions if c.get("confidence", 0) > 0.7
        )

        if high_confidence_count >= 3:
            return "severe"
        elif high_confidence_count >= 1:
            return "moderate"
        elif len(contradictions) >= 2:
            return "mild"
        else:
            return "minimal"

    def _analyze_temporal_inconsistencies(self, text: str) -> dict[str, Any]:
        """Analyze temporal inconsistencies in statements."""
        try:
            temporal_markers = []

            # Find temporal indicators
            for indicator in self.temporal_indicators:
                matches = list(
                    re.finditer(
                        rf"\b{re.escape(indicator)}\b",
                        text,
                        re.IGNORECASE,
                    )
                )
                for match in matches:
                    temporal_markers.append(
                        {
                            "indicator": indicator,
                            "position": match.start(),
                            "context": text[
                                max(0, match.start() - 20) : match.end() + 20
                            ],
                        }
                    )

            # Analyze for inconsistencies
            inconsistencies = self._find_temporal_inconsistencies(
                temporal_markers, text
            )

            return {
                "found": len(inconsistencies) > 0,
                "count": len(inconsistencies),
                "temporal_markers": len(temporal_markers),
                "inconsistencies": inconsistencies[:3],  # Limit to top 3
                "severity": (
                    "high"
                    if len(inconsistencies) > 2
                    else "low" if inconsistencies else "none"
                ),
            }

        except Exception as e:
            logger.error(f"Error analyzing temporal inconsistencies: {e}")
            return {"found": False, "count": 0, "error": str(e)}

    def _find_temporal_inconsistencies(
        self, markers: list[dict[str, Any]], text: str
    ) -> list[dict[str, Any]]:
        """Find temporal inconsistencies in the text."""
        inconsistencies = []

        # Simple heuristic: look for conflicting temporal references
        past_indicators = [
            "yesterday",
            "previously",
            "before",
            "in the past",
            "historically",
        ]
        present_indicators = ["today", "now", "currently"]
        future_indicators = ["tomorrow", "next week", "going forward"]

        has_past = any(marker["indicator"] in past_indicators for marker in markers)
        has_present = any(
            marker["indicator"] in present_indicators for marker in markers
        )
        has_future = any(marker["indicator"] in future_indicators for marker in markers)

        if has_past and has_present and has_future:
            inconsistencies.append(
                {
                    "type": "mixed_temporal_references",
                    "description": "Text contains conflicting temporal references",
                    "confidence": 0.6,
                }
            )

        return inconsistencies

    def _analyze_sentiment_shifts(self, text: str) -> dict[str, Any]:
        """Analyze sentiment shifts that might indicate hypocrisy."""
        try:
            sentences = re.split(r"[.!?]+", text)
            sentiment_scores = []

            for sentence in sentences:
                if sentence.strip():
                    score = self._calculate_sentence_sentiment(sentence)
                    sentiment_scores.append(score)

            # Calculate sentiment variance
            if len(sentiment_scores) > 1:
                mean_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                variance = sum(
                    (score - mean_sentiment) ** 2 for score in sentiment_scores
                ) / len(sentiment_scores)

                return {
                    "found": variance > 0.5,  # Threshold for significant shifts
                    "variance": round(variance, 3),
                    "mean_sentiment": round(mean_sentiment, 3),
                    "sentence_count": len(sentiment_scores),
                    "severity": (
                        "high"
                        if variance > 1.0
                        else "moderate" if variance > 0.5 else "low"
                    ),
                }
            else:
                return {
                    "found": False,
                    "variance": 0.0,
                    "sentence_count": len(sentiment_scores),
                }

        except Exception as e:
            logger.error(f"Error analyzing sentiment shifts: {e}")
            return {"found": False, "error": str(e)}

    def _calculate_sentence_sentiment(self, sentence: str) -> float:
        """Calculate basic sentiment score for a sentence."""
        positive_words = [
            "good",
            "great",
            "excellent",
            "amazing",
            "wonderful",
            "love",
            "like",
            "support",
            "agree",
            "positive",
        ]
        negative_words = [
            "bad",
            "terrible",
            "awful",
            "horrible",
            "hate",
            "dislike",
            "oppose",
            "disagree",
            "negative",
        ]

        words = sentence.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        if positive_count + negative_count == 0:
            return 0.0

        return (positive_count - negative_count) / len(words)

    def _calculate_hypocrisy_score(
        self,
        contradictions: dict[str, Any],
        temporal: dict[str, Any],
        sentiment: dict[str, Any],
    ) -> float:
        """Calculate overall hypocrisy score."""
        try:
            score = 0.0

            # Contradiction score (0-40 points)
            if contradictions.get("found"):
                contradiction_weight = {
                    "severe": 40,
                    "moderate": 25,
                    "mild": 15,
                    "minimal": 5,
                }
                score += contradiction_weight.get(
                    contradictions.get("severity", "minimal"), 0
                )

            # Temporal inconsistency score (0-30 points)
            if temporal.get("found"):
                temporal_weight = {"high": 30, "moderate": 20, "low": 10}
                score += temporal_weight.get(temporal.get("severity", "low"), 0)

            # Sentiment shift score (0-30 points)
            if sentiment.get("found"):
                sentiment_weight = {"high": 30, "moderate": 20, "low": 10}
                score += sentiment_weight.get(sentiment.get("severity", "low"), 0)

            # Normalize to 0-100 scale
            return min(100.0, score)

        except Exception as e:
            logger.error(f"Error calculating hypocrisy score: {e}")
            return 0.0

    def _generate_summary(
        self, score: float, contradictions: dict[str, Any], temporal: dict[str, Any]
    ) -> str:
        """Generate a human-readable summary of the analysis."""
        try:
            if score < 20:
                level = "Low"
                description = "The text shows minimal signs of hypocrisy or contradictory statements."
            elif score < 50:
                level = "Moderate"
                description = "The text contains some contradictory elements that may indicate inconsistency."
            elif score < 80:
                level = "High"
                description = "The text shows significant contradictions and inconsistent statements."
            else:
                level = "Very High"
                description = "The text contains severe contradictions and highly inconsistent messaging."

            details = []
            if contradictions.get("found"):
                details.append(f"{contradictions['count']} contradiction(s) detected")
            if temporal.get("found"):
                details.append(f"{temporal['count']} temporal inconsistency(ies) found")

            summary = f"{level} hypocrisy level (score: {
                score:.1f}/100). {description}"
            if details:
                summary += f" Specific issues: {', '.join(details)}."

            return summary

        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Analysis completed with score: {score:.1f}/100"

    def _create_empty_result(self, reason: str) -> dict[str, Any]:
        """Create an empty result with reason."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "hypocrisy_score": 0.0,
            "analysis": {
                "contradictions": {"found": False, "count": 0},
                "temporal_inconsistencies": {"found": False, "count": 0},
                "sentiment_shifts": {"found": False},
            },
            "summary": f"No analysis performed: {reason}",
            "error": reason,
        }

    def _create_error_result(self, error: str) -> dict[str, Any]:
        """Create an error result."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "hypocrisy_score": 0.0,
            "analysis": {},
            "summary": "Analysis failed due to error",
            "error": error,
        }


# Main engine class


class HypocrisyEngine:
    """Main hypocrisy detection engine."""

    def __init__(self):
        self.analyzer = HypocrisyAnalyzer()
        self.cache = {}  # Simple in-memory cache

    def analyze(
        self, text: str, context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Analyze text for hypocrisy patterns."""
        try:
            # Create cache key
            cache_key = hash(text + str(context or {}))

            # Check cache
            if cache_key in self.cache:
                logger.info("Returning cached hypocrisy analysis")
                return self.cache[cache_key]

            # Perform analysis
            result = self.analyzer.analyze_text(text, context)

            # Cache result (limit cache size)
            if len(self.cache) < 100:
                self.cache[cache_key] = result

            return result

        except Exception as e:
            logger.error(f"Hypocrisy engine error: {e}")
            return self.analyzer._create_error_result(str(e))

    def batch_analyze(
        self, texts: list[str], context: Optional[dict[str, Any]] = None
    ) -> list[dict[str, Any]]:
        """Analyze multiple texts for hypocrisy patterns."""
        results = []

        for i, text in enumerate(texts):
            try:
                text_context = context.copy() if context else {}
                text_context["batch_index"] = i

                result = self.analyze(text, text_context)
                results.append(result)

            except Exception as e:
                logger.error(f"Error analyzing text {i}: {e}")
                results.append(self.analyzer._create_error_result(str(e)))

        return results

    def get_stats(self) -> dict[str, Any]:
        """Get engine statistics."""
        return {
            "cache_size": len(self.cache),
            "engine_status": "active",
            "analyzer_type": "HypocrisyAnalyzer",
            "timestamp": datetime.utcnow().isoformat(),
        }

    def clear_cache(self) -> None:
        """Clear the analysis cache."""
        self.cache.clear()
        logger.info("Hypocrisy engine cache cleared")


# Global engine instance
engine = HypocrisyEngine()

# Convenience functions


def analyze_hypocrisy(
    text: str, context: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """Convenience function to analyze text for hypocrisy."""
    return engine.analyze(text, context)


def batch_analyze_hypocrisy(
    texts: list[str], context: Optional[dict[str, Any]] = None
) -> list[dict[str, Any]]:
    """Convenience function to batch analyze texts for hypocrisy."""
    return engine.batch_analyze(texts, context)
