# API Integrations Module
# Comprehensive integration layer for external services

from .arxiv_api import ArxivAPI
from .base_api import APIError, BaseAPI, RateLimitError
from .github_api import GitHubAPI
from .google_trends import GoogleTrendsAPI
from .groq_api import GroqAPI
from .guardian_api import GuardianAPI
from .huggingface_api import HuggingFaceAPI
from .nytimes_api import NYTimesAPI
from .pexels_api import PexelsAPI
from .reddit_api import RedditAPI
from .youtube_api import YouTubeAPI

__all__ = [
    "ArxivAPI",
    "BaseAPI",
    "APIError",
    "RateLimitError",
    "GitHubAPI",
    "GoogleTrendsAPI",
    "GroqAPI",
    "GuardianAPI",
    "HuggingFaceAPI",
    "NYTimesAPI",
    "PexelsAPI",
    "RedditAPI",
    "YouTubeAPI",
]
