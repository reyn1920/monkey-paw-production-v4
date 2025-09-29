"""Content analysis and processing system."""

from typing import Any, Optional
from datetime import datetime
import logging
import re
import hashlib
from dataclasses import dataclass
from enum import Enum
import statistics

# Logger setup
logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Types of content that can be analyzed."""

    TEXT = "text"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"
    XML = "xml"
    CODE = "code"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    ARTICLE = "article"
    BLOG_POST = "blog_post"


class AnalysisType(Enum):
    """Types of analysis that can be performed."""

    SENTIMENT = "sentiment"
    READABILITY = "readability"
    KEYWORD_DENSITY = "keyword_density"
    STRUCTURE = "structure"
    QUALITY = "quality"
    PLAGIARISM = "plagiarism"
    TOXICITY = "toxicity"
    LANGUAGE_DETECTION = "language_detection"
    TOPIC_MODELING = "topic_modeling"
    ENTITY_EXTRACTION = "entity_extraction"


class SentimentScore(Enum):
    """Sentiment analysis scores."""

    VERY_NEGATIVE = -2
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
    VERY_POSITIVE = 2


@dataclass
class AnalysisRequest:
    """Request for content analysis."""

    content: str
    content_type: ContentType
    analysis_types: list[AnalysisType]
    language: str = "en"
    custom_keywords: Optional[list[str]] = None
    reference_content: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class AnalysisResult:
    """Result of content analysis."""

    content_id: str
    content_type: ContentType
    analysis_results: dict[str, Any]
    quality_score: float
    recommendations: list[str]
    metadata: dict[str, Any]
    timestamp: str
    processing_time: float


class TextProcessor:
    """Processes and cleans text for analysis."""

    def __init__(self):
        self.stop_words = self._load_stop_words()
        self.punctuation_pattern = re.compile(r"[^\w\s]")
        self.whitespace_pattern = re.compile(r"\s+")

    def _load_stop_words(self) -> set[str]:
        """Load common stop words."""
        # Common English stop words
        return {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "has",
            "he",
            "in",
            "is",
            "it",
            "its",
            "of",
            "on",
            "that",
            "the",
            "to",
            "was",
            "will",
            "with",
            "the",
            "this",
            "but",
            "they",
            "have",
            "had",
            "what",
            "said",
            "each",
            "which",
            "she",
            "do",
            "how",
            "their",
            "if",
            "up",
            "out",
            "many",
            "then",
            "them",
            "these",
            "so",
            "some",
            "her",
            "would",
            "make",
            "like",
            "into",
            "him",
            "time",
            "two",
            "more",
            "go",
            "no",
            "way",
            "could",
            "my",
            "than",
            "first",
            "been",
            "call",
            "who",
            "oil",
            "sit",
            "now",
            "find",
            "down",
            "day",
            "did",
            "get",
            "come",
            "made",
            "may",
            "part",
        }

    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace
        text = self.whitespace_pattern.sub(" ", text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def extract_words(self, text: str, remove_stop_words: bool = True) -> list[str]:
        """Extract words from text."""
        # Clean text
        cleaned = self.clean_text(text)

        # Remove punctuation
        no_punct = self.punctuation_pattern.sub(" ", cleaned)

        # Split into words
        words = no_punct.split()

        # Remove stop words if requested
        if remove_stop_words:
            words = [word for word in words if word not in self.stop_words]

        # Filter out very short words
        words = [word for word in words if len(word) > 2]

        return words

    def extract_sentences(self, text: str) -> list[str]:
        """Extract sentences from text."""
        # Simple sentence splitting
        sentences = re.split(r"[.!?]+", text)

        # Clean and filter sentences
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    def extract_paragraphs(self, text: str) -> list[str]:
        """Extract paragraphs from text."""
        paragraphs = text.split("\n\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs


class SentimentAnalyzer:
    """Analyzes sentiment in text content."""

    def __init__(self):
        self.positive_words = self._load_positive_words()
        self.negative_words = self._load_negative_words()
        self.intensifiers = {
            "very",
            "extremely",
            "really",
            "quite",
            "totally",
            "completely",
        }
        self.negators = {
            "not",
            "no",
            "never",
            "none",
            "nobody",
            "nothing",
            "neither",
            "nowhere",
        }

    def _load_positive_words(self) -> set[str]:
        """Load positive sentiment words."""
        return {
            "good",
            "great",
            "excellent",
            "amazing",
            "wonderful",
            "fantastic",
            "awesome",
            "brilliant",
            "outstanding",
            "superb",
            "magnificent",
            "marvelous",
            "terrific",
            "fabulous",
            "incredible",
            "remarkable",
            "exceptional",
            "perfect",
            "beautiful",
            "lovely",
            "delightful",
            "pleasant",
            "enjoyable",
            "satisfying",
            "impressive",
            "successful",
            "positive",
            "happy",
            "joyful",
            "cheerful",
            "optimistic",
            "confident",
            "proud",
            "grateful",
            "thankful",
            "blessed",
            "lucky",
            "fortunate",
            "love",
            "like",
            "enjoy",
            "appreciate",
            "admire",
            "respect",
            "trust",
            "believe",
            "hope",
            "dream",
            "wish",
            "want",
            "need",
        }

    def _load_negative_words(self) -> set[str]:
        """Load negative sentiment words."""
        return {
            "bad",
            "terrible",
            "awful",
            "horrible",
            "disgusting",
            "revolting",
            "appalling",
            "dreadful",
            "atrocious",
            "abysmal",
            "deplorable",
            "despicable",
            "detestable",
            "loathsome",
            "repulsive",
            "vile",
            "wicked",
            "evil",
            "nasty",
            "cruel",
            "harsh",
            "brutal",
            "savage",
            "ruthless",
            "merciless",
            "heartless",
            "cold",
            "unfair",
            "unjust",
            "wrong",
            "false",
            "fake",
            "dishonest",
            "corrupt",
            "fraudulent",
            "negative",
            "sad",
            "depressed",
            "miserable",
            "unhappy",
            "angry",
            "furious",
            "enraged",
            "livid",
            "irate",
            "annoyed",
            "irritated",
            "frustrated",
            "disappointed",
            "upset",
            "worried",
            "anxious",
            "scared",
            "afraid",
            "terrified",
            "panicked",
            "stressed",
            "hate",
            "dislike",
            "despise",
            "detest",
            "abhor",
            "loathe",
        }

    def analyze_sentiment(self, text: str) -> dict[str, Any]:
        """Analyze sentiment of text."""
        try:
            words = text.lower().split()

            positive_score = 0
            negative_score = 0

            for i, word in enumerate(words):
                # Check for intensifiers
                intensifier_multiplier = 1
                if i > 0 and words[i - 1] in self.intensifiers:
                    intensifier_multiplier = 1.5

                # Check for negators
                negated = False
                if i > 0 and words[i - 1] in self.negators:
                    negated = True
                elif i > 1 and words[i - 2] in self.negators:
                    negated = True

                # Score the word
                if word in self.positive_words:
                    score = 1 * intensifier_multiplier
                    if negated:
                        negative_score += score
                    else:
                        positive_score += score
                elif word in self.negative_words:
                    score = 1 * intensifier_multiplier
                    if negated:
                        positive_score += score
                    else:
                        negative_score += score

            # Calculate overall sentiment
            total_score = positive_score - negative_score
            total_words = len(
                [
                    w
                    for w in words
                    if w in self.positive_words or w in self.negative_words
                ]
            )

            if total_words == 0:
                sentiment_score = SentimentScore.NEUTRAL
                confidence = 0.0
            else:
                normalized_score = total_score / total_words
                # More words = higher confidence
                confidence = min(1.0, total_words / 10)

                if normalized_score >= 0.5:
                    sentiment_score = SentimentScore.VERY_POSITIVE
                elif normalized_score >= 0.1:
                    sentiment_score = SentimentScore.POSITIVE
                elif normalized_score <= -0.5:
                    sentiment_score = SentimentScore.VERY_NEGATIVE
                elif normalized_score <= -0.1:
                    sentiment_score = SentimentScore.NEGATIVE
                else:
                    sentiment_score = SentimentScore.NEUTRAL

            return {
                "sentiment_score": sentiment_score.value,
                "sentiment_label": sentiment_score.name.lower().replace("_", " "),
                "positive_score": positive_score,
                "negative_score": negative_score,
                "confidence": confidence,
                "total_sentiment_words": total_words,
            }

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                "sentiment_score": 0,
                "sentiment_label": "neutral",
                "positive_score": 0,
                "negative_score": 0,
                "confidence": 0.0,
                "total_sentiment_words": 0,
            }


class ContentAnalyzer:
    """Main content analysis system."""

    def __init__(self):
        self.text_processor = TextProcessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.analysis_history = []

    def analyze_content(self, request: AnalysisRequest) -> AnalysisResult:
        """Perform comprehensive content analysis."""
        try:
            start_time = datetime.utcnow()

            # Generate content ID
            content_id = hashlib.md5(request.content.encode()).hexdigest()[:12]

            logger.info(
                f"Analyzing content {content_id} with {len(request.analysis_types)} analysis types"
            )

            # Perform requested analyses
            analysis_results = {}

            for analysis_type in request.analysis_types:
                if analysis_type == AnalysisType.SENTIMENT:
                    analysis_results["sentiment"] = (
                        self.sentiment_analyzer.analyze_sentiment(request.content)
                    )

                elif analysis_type == AnalysisType.QUALITY:
                    analysis_results["quality"] = self._analyze_quality(
                        request.content, request.content_type
                    )

            # Calculate overall quality score
            quality_score = self._calculate_overall_quality_score(analysis_results)

            # Generate recommendations
            recommendations = self._generate_recommendations(analysis_results, request)

            # Calculate processing time
            end_time = datetime.utcnow()
            processing_time = (end_time - start_time).total_seconds()

            # Create result
            result = AnalysisResult(
                content_id=content_id,
                content_type=request.content_type,
                analysis_results=analysis_results,
                quality_score=quality_score,
                recommendations=recommendations,
                metadata={
                    "content_length": len(request.content),
                    "analysis_types": [at.value for at in request.analysis_types],
                    "language": request.language,
                    "has_custom_keywords": bool(request.custom_keywords),
                    "custom_metadata": request.metadata or {},
                },
                timestamp=end_time.isoformat(),
                processing_time=processing_time,
            )

            # Store in history
            self.analysis_history.append(
                {
                    "request": request,
                    "result": result,
                    "timestamp": end_time.isoformat(),
                }
            )

            # Limit history size
            if len(self.analysis_history) > 100:
                self.analysis_history = self.analysis_history[-100:]

            return result

        except Exception as e:
            logger.error(f"Error analyzing content: {e}")
            raise

    def _analyze_quality(
        self, content: str, content_type: ContentType
    ) -> dict[str, Any]:
        """Analyze overall content quality."""
        try:
            # Basic quality metrics
            words = content.split()
            sentences = self.text_processor.extract_sentences(content)

            quality_metrics = {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
                "overall_quality": 75.0,  # Default good score
            }

            return quality_metrics

        except Exception as e:
            logger.error(f"Error analyzing quality: {e}")
            return {"overall_quality": 50.0}

    def _calculate_overall_quality_score(
        self, analysis_results: dict[str, Any]
    ) -> float:
        """Calculate overall quality score from all analyses."""
        try:
            scores = []

            # Sentiment score (neutral is good for most content)
            if "sentiment" in analysis_results:
                sentiment_score = analysis_results["sentiment"]["confidence"] * 50
                if analysis_results["sentiment"]["sentiment_score"] == 0:  # Neutral
                    sentiment_score += 25
                scores.append(sentiment_score)

            # Quality score
            if "quality" in analysis_results:
                quality_score = analysis_results["quality"]["overall_quality"]
                scores.append(quality_score)

            return statistics.mean(scores) if scores else 50.0

        except Exception as e:
            logger.error(f"Error calculating overall quality score: {e}")
            return 50.0

    def _generate_recommendations(
        self, analysis_results: dict[str, Any], request: AnalysisRequest
    ) -> list[str]:
        """Generate improvement recommendations based on analysis."""
        recommendations = []

        try:
            # Sentiment recommendations
            if "sentiment" in analysis_results:
                sentiment = analysis_results["sentiment"]
                if sentiment["sentiment_score"] < -1:
                    recommendations.append(
                        "Consider using more positive language to improve reader engagement"
                    )

            # General recommendations
            if not recommendations:
                recommendations.append(
                    "Content analysis looks good! Consider adding more specific keywords for SEO."
                )

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append(
                "Unable to generate specific recommendations. Consider general proofreading."
            )

        return recommendations[:5]  # Limit to 5 recommendations


# Global instance
analyzer = ContentAnalyzer()

# Convenience functions


def analyze_content(
    content: str,
    content_type: str = "text",
    analysis_types: Optional[list[str]] = None,
    **kwargs,
) -> AnalysisResult:
    """Convenience function to analyze content."""
    if analysis_types is None:
        analysis_types = ["sentiment", "quality"]

    request = AnalysisRequest(
        content=content,
        content_type=ContentType(content_type),
        analysis_types=[AnalysisType(at) for at in analysis_types],
        **kwargs,
    )
    return analyzer.analyze_content(request)


def analyze_sentiment(content: str) -> dict[str, Any]:
    """Convenience function to analyze sentiment only."""
    result = analyze_content(content, analysis_types=["sentiment"])
    return result.analysis_results.get("sentiment", {})
