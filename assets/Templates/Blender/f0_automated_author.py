"""Automated content authoring and generation system."""

from typing import Any, Optional
from datetime import datetime
import logging
import re
import random
from dataclasses import dataclass
from enum import Enum

# Logger setup
logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Types of content that can be generated."""

    ARTICLE = "article"
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    PRODUCT_DESCRIPTION = "product_description"
    PRESS_RELEASE = "press_release"
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    CREATIVE_WRITING = "creative_writing"


class WritingStyle(Enum):
    """Writing styles for content generation."""

    FORMAL = "formal"
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    CONVERSATIONAL = "conversational"
    ACADEMIC = "academic"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    PERSUASIVE = "persuasive"


@dataclass
class ContentRequest:
    """Request for automated content generation."""

    content_type: ContentType
    topic: str
    target_audience: str
    writing_style: WritingStyle
    word_count: int = 500
    keywords: Optional[list[str]] = None
    tone: str = "neutral"
    include_sections: Optional[list[str]] = None
    exclude_topics: Optional[list[str]] = None
    additional_requirements: Optional[str] = None


@dataclass
class GeneratedContent:
    """Generated content result."""

    title: str
    content: str
    word_count: int
    content_type: ContentType
    writing_style: WritingStyle
    metadata: dict[str, Any]
    quality_score: float
    suggestions: list[str]
    timestamp: str


class ContentTemplateManager:
    """Manages content templates and structures."""

    def __init__(self):
        self.templates = self._initialize_templates()
        self.section_templates = self._initialize_section_templates()

    def _initialize_templates(self) -> dict[ContentType, dict[str, Any]]:
        """Initialize content templates."""
        return {
            ContentType.ARTICLE: {
                "structure": ["introduction", "main_content", "conclusion"],
                "min_sections": 3,
                "max_sections": 8,
                "typical_length": 800,
            },
            ContentType.BLOG_POST: {
                "structure": [
                    "hook",
                    "introduction",
                    "main_points",
                    "conclusion",
                    "call_to_action",
                ],
                "min_sections": 4,
                "max_sections": 6,
                "typical_length": 600,
            },
            ContentType.SOCIAL_MEDIA: {
                "structure": ["hook", "main_message", "hashtags"],
                "min_sections": 2,
                "max_sections": 3,
                "typical_length": 150,
            },
            ContentType.EMAIL: {
                "structure": ["subject", "greeting", "body", "closing", "signature"],
                "min_sections": 4,
                "max_sections": 5,
                "typical_length": 300,
            },
            ContentType.PRODUCT_DESCRIPTION: {
                "structure": [
                    "headline",
                    "features",
                    "benefits",
                    "specifications",
                    "call_to_action",
                ],
                "min_sections": 4,
                "max_sections": 5,
                "typical_length": 250,
            },
            ContentType.PRESS_RELEASE: {
                "structure": [
                    "headline",
                    "dateline",
                    "lead",
                    "body",
                    "boilerplate",
                    "contact",
                ],
                "min_sections": 5,
                "max_sections": 6,
                "typical_length": 400,
            },
            ContentType.TECHNICAL_DOCUMENTATION: {
                "structure": [
                    "overview",
                    "requirements",
                    "instructions",
                    "examples",
                    "troubleshooting",
                ],
                "min_sections": 4,
                "max_sections": 8,
                "typical_length": 1000,
            },
            ContentType.CREATIVE_WRITING: {
                "structure": ["opening", "development", "climax", "resolution"],
                "min_sections": 3,
                "max_sections": 6,
                "typical_length": 1200,
            },
        }

    def _initialize_section_templates(self) -> dict[str, list[str]]:
        """Initialize section templates with placeholder content."""
        return {
            "introduction": [
                "In today's rapidly evolving {topic}, understanding {key_concept} is crucial for {audience}.",
                "The importance of {topic} cannot be overstated in our modern {context}.",
                "As we delve into {topic}, it's essential to consider the impact on {stakeholders}.",
            ],
            "main_content": [
                "The primary aspects of {topic} include several key components that {audience} should understand.",
                "When examining {topic}, we must consider multiple perspectives and approaches.",
                "The implementation of {topic} requires careful consideration of various factors.",
            ],
            "conclusion": [
                "In conclusion, {topic} represents a significant opportunity for {audience} to {action}.",
                "The future of {topic} depends on how well we {implementation_strategy}.",
                "Moving forward, the key to success in {topic} lies in {success_factors}.",
            ],
            "call_to_action": [
                "Ready to get started with {topic}? Contact us today to learn more.",
                "Don't miss out on the benefits of {topic}. Take action now.",
                "Join thousands of {audience} who have already embraced {topic}.",
            ],
        }

    def get_template(self, content_type: ContentType) -> dict[str, Any]:
        """Get template for specific content type."""
        return self.templates.get(content_type, self.templates[ContentType.ARTICLE])

    def get_section_template(self, section_name: str) -> str:
        """Get a random template for a specific section."""
        templates = self.section_templates.get(
            section_name,
            [
                "This section covers important aspects of {topic} that {audience} should know."
            ],
        )
        return random.choice(templates)


class ContentGenerator:
    """Core content generation engine."""

    def __init__(self):
        self.template_manager = ContentTemplateManager()
        self.style_modifiers = self._initialize_style_modifiers()
        self.quality_checker = ContentQualityChecker()

    def _initialize_style_modifiers(self) -> dict[WritingStyle, dict[str, Any]]:
        """Initialize writing style modifiers."""
        return {
            WritingStyle.FORMAL: {
                "sentence_starters": [
                    "Furthermore,",
                    "Moreover,",
                    "Additionally,",
                    "Consequently,",
                ],
                "vocabulary_level": "advanced",
                "tone_words": ["professional", "authoritative", "comprehensive"],
            },
            WritingStyle.CASUAL: {
                "sentence_starters": ["So,", "Well,", "You know,", "Actually,"],
                "vocabulary_level": "simple",
                "tone_words": ["friendly", "approachable", "relaxed"],
            },
            WritingStyle.PROFESSIONAL: {
                "sentence_starters": [
                    "In our experience,",
                    "Research shows,",
                    "Industry experts agree,",
                ],
                "vocabulary_level": "intermediate",
                "tone_words": ["expert", "reliable", "trustworthy"],
            },
            WritingStyle.CONVERSATIONAL: {
                "sentence_starters": [
                    "Let's talk about,",
                    "Have you ever wondered,",
                    "Here's the thing,",
                ],
                "vocabulary_level": "simple",
                "tone_words": ["engaging", "personal", "direct"],
            },
            WritingStyle.ACADEMIC: {
                "sentence_starters": [
                    "Research indicates,",
                    "Studies have shown,",
                    "According to literature,",
                ],
                "vocabulary_level": "advanced",
                "tone_words": ["scholarly", "analytical", "evidence-based"],
            },
            WritingStyle.CREATIVE: {
                "sentence_starters": ["Imagine,", "Picture this,", "Once upon a time,"],
                "vocabulary_level": "varied",
                "tone_words": ["imaginative", "expressive", "artistic"],
            },
            WritingStyle.TECHNICAL: {
                "sentence_starters": [
                    "The system,",
                    "Implementation requires,",
                    "Configuration involves,",
                ],
                "vocabulary_level": "technical",
                "tone_words": ["precise", "detailed", "systematic"],
            },
            WritingStyle.PERSUASIVE: {
                "sentence_starters": [
                    "Consider this,",
                    "The benefits are clear,",
                    "Don't you agree,",
                ],
                "vocabulary_level": "intermediate",
                "tone_words": ["compelling", "convincing", "influential"],
            },
        }

    def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate content based on request."""
        try:
            logger.info(
                f"Generating {
                    request.content_type.value} content about {
                    request.topic}"
            )

            # Get template for content type
            template = self.template_manager.get_template(request.content_type)

            # Generate title
            title = self._generate_title(request)

            # Generate content sections
            content_sections = self._generate_content_sections(request, template)

            # Combine sections into full content
            full_content = self._combine_sections(content_sections, request)

            # Calculate word count
            word_count = len(full_content.split())

            # Generate metadata
            metadata = self._generate_metadata(request, word_count)

            # Check quality
            quality_score = self.quality_checker.calculate_quality_score(
                full_content, request
            )
            suggestions = self.quality_checker.generate_suggestions(
                full_content, request
            )

            return GeneratedContent(
                title=title,
                content=full_content,
                word_count=word_count,
                content_type=request.content_type,
                writing_style=request.writing_style,
                metadata=metadata,
                quality_score=quality_score,
                suggestions=suggestions,
                timestamp=datetime.utcnow().isoformat(),
            )

        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise

    def _generate_title(self, request: ContentRequest) -> str:
        """Generate title based on content type and topic."""
        title_templates = {
            ContentType.ARTICLE: [
                "Understanding {topic}: A Comprehensive Guide",
                "The Complete Guide to {topic}",
                "Everything You Need to Know About {topic}",
                "{topic}: Key Insights and Best Practices",
            ],
            ContentType.BLOG_POST: [
                "Why {topic} Matters in 2024",
                "The Ultimate Guide to {topic}",
                "How to Master {topic}: Tips and Tricks",
                "{topic}: What You Need to Know",
            ],
            ContentType.SOCIAL_MEDIA: [
                "🚀 {topic} insights you can't miss!",
                "The truth about {topic} 💡",
                "Quick {topic} tips for success ⭐",
                "{topic} made simple 📈",
            ],
            ContentType.EMAIL: [
                "Important Update About {topic}",
                "Your {topic} Questions Answered",
                "New Developments in {topic}",
                "Don't Miss Out: {topic} Insights",
            ],
            ContentType.PRODUCT_DESCRIPTION: [
                "Premium {topic} Solution",
                "Advanced {topic} Technology",
                "Professional {topic} Service",
                "Next-Generation {topic}",
            ],
            ContentType.PRESS_RELEASE: [
                "Company Announces Major {topic} Initiative",
                "Breaking: New {topic} Development",
                "Industry Leader Launches {topic} Program",
                "Revolutionary {topic} Solution Unveiled",
            ],
            ContentType.TECHNICAL_DOCUMENTATION: [
                "{topic} Implementation Guide",
                "{topic} Technical Specifications",
                "How to Configure {topic}",
                "{topic} Setup and Configuration",
            ],
            ContentType.CREATIVE_WRITING: [
                "The {topic} Chronicles",
                "A Tale of {topic}",
                "Journey Through {topic}",
                "The {topic} Adventure",
            ],
        }

        templates = title_templates.get(
            request.content_type, title_templates[ContentType.ARTICLE]
        )
        template = random.choice(templates)
        return template.format(topic=request.topic.title())

    def _generate_content_sections(
        self, request: ContentRequest, template: dict[str, Any]
    ) -> list[str]:
        """Generate content sections based on template."""
        sections = []
        structure = template["structure"]

        # Use custom sections if provided
        if request.include_sections:
            structure = request.include_sections

        for section_name in structure:
            section_content = self._generate_section_content(section_name, request)
            sections.append(section_content)

        return sections

    def _generate_section_content(
        self, section_name: str, request: ContentRequest
    ) -> str:
        """Generate content for a specific section."""
        # Get section template
        template = self.template_manager.get_section_template(section_name)

        # Fill template with request data
        content = template.format(
            topic=request.topic,
            audience=request.target_audience,
            key_concept=f"key aspects of {request.topic}",
            context=f"{request.target_audience} environment",
            stakeholders=request.target_audience,
            action="achieve their goals",
            implementation_strategy="implement best practices",
            success_factors="continuous learning and adaptation",
        )

        # Apply writing style modifications
        content = self._apply_writing_style(content, request.writing_style)

        # Expand content to meet word count requirements
        if request.word_count > 300:
            content = self._expand_content(content, request)

        return content

    def _apply_writing_style(self, content: str, style: WritingStyle) -> str:
        """Apply writing style modifications to content."""
        style_config = self.style_modifiers.get(style, {})

        # Add style-specific sentence starters
        if "sentence_starters" in style_config:
            starters = style_config["sentence_starters"]
            if random.random() < 0.3:  # 30% chance to add starter
                starter = random.choice(starters)
                content = f"{starter} {content}"

        return content

    def _expand_content(self, content: str, request: ContentRequest) -> str:
        """Expand content to meet word count requirements."""
        current_words = len(content.split())
        target_words = max(
            100, request.word_count // len(request.include_sections or ["main"])
        )

        if current_words < target_words:
            # Add additional sentences
            additional_sentences = [
                f"This approach to {request.topic} has proven effective for many {
                    request.target_audience
                }.",
                f"The benefits of implementing {
                    request.topic
                } strategies are numerous and well-documented.",
                f"Industry experts consistently recommend focusing on {
                    request.topic
                } for optimal results.",
                f"When considering {
                    request.topic
                }, it's important to evaluate all available options carefully.",
            ]

            needed_sentences = min(3, (target_words - current_words) // 15)
            for _ in range(needed_sentences):
                content += " " + random.choice(additional_sentences)

        return content

    def _combine_sections(self, sections: list[str], request: ContentRequest) -> str:
        """Combine sections into full content."""
        if request.content_type == ContentType.SOCIAL_MEDIA:
            return " ".join(sections)
        else:
            return "\n\n".join(sections)

    def _generate_metadata(
        self, request: ContentRequest, word_count: int
    ) -> dict[str, Any]:
        """Generate metadata for the content."""
        return {
            "topic": request.topic,
            "target_audience": request.target_audience,
            "writing_style": request.writing_style.value,
            "content_type": request.content_type.value,
            "word_count": word_count,
            "keywords": request.keywords or [],
            "tone": request.tone,
            "generated_at": datetime.utcnow().isoformat(),
            "estimated_reading_time": f"{max(1, word_count // 200)} minutes",
        }


class ContentQualityChecker:
    """Checks and scores content quality."""

    def calculate_quality_score(self, content: str, request: ContentRequest) -> float:
        """Calculate quality score for generated content."""
        try:
            score = 0.0
            max_score = 100.0

            # Word count appropriateness (20 points)
            word_count = len(content.split())
            target_count = request.word_count
            word_score = max(0, 20 - abs(word_count - target_count) / target_count * 20)
            score += word_score

            # Content structure (20 points)
            structure_score = self._check_structure(content, request.content_type)
            score += structure_score

            # Readability (20 points)
            readability_score = self._check_readability(content)
            score += readability_score

            # Keyword usage (20 points)
            keyword_score = self._check_keyword_usage(content, request.keywords or [])
            score += keyword_score

            # Style consistency (20 points)
            style_score = self._check_style_consistency(content, request.writing_style)
            score += style_score

            return min(max_score, score)

        except Exception as e:
            logger.error(f"Error calculating quality score: {e}")
            return 50.0  # Default score

    def _check_structure(self, content: str, content_type: ContentType) -> float:
        """Check content structure quality."""
        paragraphs = content.split("\n\n")
        paragraph_count = len(paragraphs)

        # Different content types have different optimal paragraph counts
        optimal_counts = {
            ContentType.ARTICLE: (3, 8),
            ContentType.BLOG_POST: (3, 6),
            ContentType.SOCIAL_MEDIA: (1, 3),
            ContentType.EMAIL: (2, 5),
            ContentType.PRODUCT_DESCRIPTION: (2, 4),
            ContentType.PRESS_RELEASE: (3, 6),
            ContentType.TECHNICAL_DOCUMENTATION: (4, 10),
            ContentType.CREATIVE_WRITING: (3, 8),
        }

        min_count, max_count = optimal_counts.get(content_type, (2, 6))

        if min_count <= paragraph_count <= max_count:
            return 20.0
        elif paragraph_count < min_count:
            return max(0, 20 - (min_count - paragraph_count) * 5)
        else:
            return max(0, 20 - (paragraph_count - max_count) * 2)

    def _check_readability(self, content: str) -> float:
        """Check content readability."""
        sentences = re.split(r"[.!?]+", content)
        words = content.split()

        if not sentences or not words:
            return 0.0

        avg_sentence_length = len(words) / len(sentences)

        # Optimal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            return 20.0
        elif 10 <= avg_sentence_length < 15 or 20 < avg_sentence_length <= 25:
            return 15.0
        elif 5 <= avg_sentence_length < 10 or 25 < avg_sentence_length <= 30:
            return 10.0
        else:
            return 5.0

    def _check_keyword_usage(self, content: str, keywords: list[str]) -> float:
        """Check keyword usage in content."""
        if not keywords:
            return 20.0  # Full score if no keywords specified

        content_lower = content.lower()
        keyword_count = 0

        for keyword in keywords:
            if keyword.lower() in content_lower:
                keyword_count += 1

        usage_ratio = keyword_count / len(keywords)
        return usage_ratio * 20.0

    def _check_style_consistency(self, content: str, style: WritingStyle) -> float:
        """Check writing style consistency."""
        # This is a simplified check - in practice, this would be more
        # sophisticated
        content_lower = content.lower()

        style_indicators = {
            WritingStyle.FORMAL: [
                "furthermore",
                "moreover",
                "consequently",
                "therefore",
            ],
            WritingStyle.CASUAL: ["so", "well", "you know", "actually"],
            WritingStyle.PROFESSIONAL: [
                "experience",
                "research",
                "industry",
                "experts",
            ],
            WritingStyle.CONVERSATIONAL: ["let's", "you", "we", "your"],
            WritingStyle.ACADEMIC: ["research", "studies", "literature", "analysis"],
            WritingStyle.CREATIVE: ["imagine", "picture", "story", "journey"],
            WritingStyle.TECHNICAL: [
                "system",
                "implementation",
                "configuration",
                "process",
            ],
            WritingStyle.PERSUASIVE: ["benefits", "consider", "don't", "should"],
        }

        indicators = style_indicators.get(style, [])
        if not indicators:
            return 20.0

        found_indicators = sum(
            1 for indicator in indicators if indicator in content_lower
        )
        consistency_ratio = found_indicators / len(indicators)

        return consistency_ratio * 20.0

    def generate_suggestions(self, content: str, request: ContentRequest) -> list[str]:
        """Generate improvement suggestions for content."""
        suggestions = []

        word_count = len(content.split())
        target_count = request.word_count

        # Word count suggestions
        if word_count < target_count * 0.8:
            suggestions.append(
                f"Consider expanding the content. Current: {word_count} words, Target: {target_count} words"
            )
        elif word_count > target_count * 1.2:
            suggestions.append(
                f"Consider condensing the content. Current: {word_count} words, Target: {target_count} words"
            )

        # Structure suggestions
        paragraphs = content.split("\n\n")
        if len(paragraphs) < 2:
            suggestions.append(
                "Consider breaking the content into multiple paragraphs for better readability"
            )

        # Keyword suggestions
        if request.keywords:
            content_lower = content.lower()
            missing_keywords = [
                kw for kw in request.keywords if kw.lower() not in content_lower
            ]
            if missing_keywords:
                suggestions.append(
                    f"Consider including these keywords: {
                        ', '.join(missing_keywords)}"
                )

        # Style suggestions
        if (
            request.writing_style == WritingStyle.CONVERSATIONAL
            and "you" not in content.lower()
        ):
            suggestions.append(
                "Consider using more direct address (you, your) for conversational style"
            )

        return suggestions


class AutomatedAuthor:
    """Main automated authoring system."""

    def __init__(self):
        self.generator = ContentGenerator()
        self.content_history = []

    def create_content(self, request: ContentRequest) -> GeneratedContent:
        """Create content based on request."""
        try:
            logger.info(
                f"Creating {
                    request.content_type.value} content: {
                    request.topic}"
            )

            # Generate content
            content = self.generator.generate_content(request)

            # Store in history
            self.content_history.append(
                {
                    "request": request,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

            # Limit history size
            if len(self.content_history) > 100:
                self.content_history = self.content_history[-100:]

            return content

        except Exception as e:
            logger.error(f"Error creating content: {e}")
            raise

    def batch_create_content(
        self, requests: list[ContentRequest]
    ) -> list[GeneratedContent]:
        """Create multiple pieces of content."""
        results = []

        for i, request in enumerate(requests):
            try:
                content = self.create_content(request)
                results.append(content)
                logger.info(f"Completed content {i + 1}/{len(requests)}")

            except Exception as e:
                logger.error(f"Error creating content {i + 1}: {e}")
                # Create error content
                error_content = GeneratedContent(
                    title=f"Error: {request.topic}",
                    content=f"Error generating content: {str(e)}",
                    word_count=0,
                    content_type=request.content_type,
                    writing_style=request.writing_style,
                    metadata={"error": str(e)},
                    quality_score=0.0,
                    suggestions=["Please try again with different parameters"],
                    timestamp=datetime.utcnow().isoformat(),
                )
                results.append(error_content)

        return results

    def get_content_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent content creation history."""
        return self.content_history[-limit:]

    def get_stats(self) -> dict[str, Any]:
        """Get authoring system statistics."""
        if not self.content_history:
            return {
                "total_content_created": 0,
                "average_quality_score": 0.0,
                "content_types_created": {},
                "writing_styles_used": {},
                "total_words_generated": 0,
            }

        content_types = {}
        writing_styles = {}
        total_words = 0
        total_quality = 0.0

        for entry in self.content_history:
            content = entry["content"]

            # Count content types
            content_type = content.content_type.value
            content_types[content_type] = content_types.get(content_type, 0) + 1

            # Count writing styles
            writing_style = content.writing_style.value
            writing_styles[writing_style] = writing_styles.get(writing_style, 0) + 1

            # Sum metrics
            total_words += content.word_count
            total_quality += content.quality_score

        return {
            "total_content_created": len(self.content_history),
            "average_quality_score": total_quality / len(self.content_history),
            "content_types_created": content_types,
            "writing_styles_used": writing_styles,
            "total_words_generated": total_words,
            "average_words_per_content": (
                total_words / len(self.content_history) if self.content_history else 0
            ),
        }


# Global instance
author = AutomatedAuthor()

# Convenience functions


def create_content(
    content_type: str,
    topic: str,
    target_audience: str,
    writing_style: str = "professional",
    word_count: int = 500,
    **kwargs,
) -> GeneratedContent:
    """Convenience function to create content."""
    request = ContentRequest(
        content_type=ContentType(content_type),
        topic=topic,
        target_audience=target_audience,
        writing_style=WritingStyle(writing_style),
        word_count=word_count,
        **kwargs,
    )
    return author.create_content(request)


def create_article(
    topic: str, target_audience: str = "general audience", word_count: int = 800
) -> GeneratedContent:
    """Convenience function to create an article."""
    return create_content("article", topic, target_audience, "professional", word_count)


def create_blog_post(
    topic: str, target_audience: str = "readers", word_count: int = 600
) -> GeneratedContent:
    """Convenience function to create a blog post."""
    return create_content(
        "blog_post", topic, target_audience, "conversational", word_count
    )


def create_social_media_post(
    topic: str, target_audience: str = "followers"
) -> GeneratedContent:
    """Convenience function to create a social media post."""
    return create_content("social_media", topic, target_audience, "casual", 150)
