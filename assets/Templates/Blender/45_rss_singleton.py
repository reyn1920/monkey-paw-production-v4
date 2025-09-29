"""RSS Singleton Manager

This module provides a singleton RSS feed manager for handling RSS feeds,
feed parsing, caching, and content extraction across the application.
"""

import asyncio
import hashlib
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Optional
import threading
from dataclasses import dataclass, asdict
from enum import Enum

# Optional imports with fallbacks
try:
    import feedparser

    feedparser_available = True
except ImportError:
    feedparser = None
    feedparser_available = False

try:
    import requests

    requests_available = True
except ImportError:
    requests = None
    requests_available = False

try:
    from bs4 import BeautifulSoup

    bs4_available = True
except ImportError:
    BeautifulSoup = None
    bs4_available = False

# Logger setup
logger = logging.getLogger(__name__)


class FeedStatus(Enum):
    """RSS feed status enumeration"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PARSING_ERROR = "parsing_error"
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"


class ContentType(Enum):
    """Content type enumeration"""

    ARTICLE = "article"
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    UNKNOWN = "unknown"


@dataclass
class FeedItem:
    """RSS feed item data structure"""

    title: str
    link: str
    description: str
    published: Optional[datetime] = None
    author: Optional[str] = None
    categories: Optional[list[str]] = None
    content: Optional[str] = None
    content_type: ContentType = ContentType.UNKNOWN
    guid: Optional[str] = None
    enclosures: Optional[list[dict[str, Any]]] = None

    def __post_init__(self):
        if self.categories is None:
            self.categories = []
        if self.enclosures is None:
            self.enclosures = []


@dataclass
class FeedInfo:
    """RSS feed information data structure"""

    url: str
    title: str
    description: str
    link: str
    language: Optional[str] = None
    last_updated: Optional[datetime] = None
    status: FeedStatus = FeedStatus.ACTIVE
    error_message: Optional[str] = None
    item_count: int = 0
    last_fetch: Optional[datetime] = None
    fetch_interval: int = 3600  # seconds


class RSSCache:
    """RSS feed caching system"""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: dict[str, dict[str, Any]] = {}
        self._access_times: dict[str, float] = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        """Get cached item"""
        with self._lock:
            if key not in self._cache:
                return None

            cache_entry = self._cache[key]
            if time.time() - cache_entry["timestamp"] > self.ttl:
                self._remove(key)
                return None

            self._access_times[key] = time.time()
            return cache_entry["data"]

    def set(self, key: str, value: Any) -> None:
        """Set cached item"""
        with self._lock:
            if len(self._cache) >= self.max_size:
                self._evict_lru()

            self._cache[key] = {"data": value, "timestamp": time.time()}
            self._access_times[key] = time.time()

    def _remove(self, key: str) -> None:
        """Remove item from cache"""
        self._cache.pop(key, None)
        self._access_times.pop(key, None)

    def _evict_lru(self) -> None:
        """Evict least recently used item"""
        if not self._access_times:
            return

        lru_key = min(self._access_times.keys(), key=lambda k: self._access_times[k])
        self._remove(lru_key)

    def clear(self) -> None:
        """Clear all cached items"""
        with self._lock:
            self._cache.clear()
            self._access_times.clear()


class RSSParser:
    """RSS feed parser with multiple backend support"""

    def __init__(self):
        self.session = None
        if requests_available and requests:
            self.session = requests.Session()
            self.session.headers.update({"User-Agent": "TRAE.AI RSS Reader/1.0"})

    def parse_feed(self, url: str, timeout: int = 30) -> Optional[dict[str, Any]]:
        """Parse RSS feed from URL"""
        try:
            if not feedparser_available or not feedparser:
                logger.warning("feedparser not available, using fallback parser")
                return self._fallback_parse(url, timeout)

            # Fetch feed content
            if self.session and requests_available and requests:
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                content = response.content
            else:
                # Fallback to feedparser's built-in fetching
                parsed = feedparser.parse(url)
                return self._process_feedparser_result(parsed)

            # Parse with feedparser
            parsed = feedparser.parse(content)
            return self._process_feedparser_result(parsed)

        except Exception as e:
            logger.error(f"Error parsing RSS feed {url}: {e}")
            return None

    def _process_feedparser_result(self, parsed) -> Optional[dict[str, Any]]:
        """Process feedparser result into standardized format"""
        if not parsed or parsed.bozo:
            return None

        feed_info = {
            "title": parsed.feed.get("title", "Unknown Feed"),
            "description": parsed.feed.get("description", ""),
            "link": parsed.feed.get("link", ""),
            "language": parsed.feed.get("language"),
            "last_updated": self._parse_datetime(parsed.feed.get("updated")),
            "items": [],
        }

        for entry in parsed.entries:
            item = FeedItem(
                title=entry.get("title", "Untitled"),
                link=entry.get("link", ""),
                description=entry.get("description", ""),
                published=self._parse_datetime(entry.get("published")),
                author=entry.get("author"),
                categories=[tag.get("term", "") for tag in entry.get("tags", [])],
                content=self._extract_content(entry),
                guid=entry.get("id", entry.get("link")),
                enclosures=self._extract_enclosures(entry),
            )
            item.content_type = self._detect_content_type(item)
            feed_info["items"].append(asdict(item))

        return feed_info

    def _fallback_parse(self, url: str, timeout: int) -> Optional[dict[str, Any]]:
        """Fallback RSS parser using basic HTTP and XML parsing"""
        try:
            if not requests_available or not requests or not self.session:
                logger.error("No HTTP library available for RSS parsing")
                return None

            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()

            # Basic XML parsing fallback
            if bs4_available and BeautifulSoup:
                soup = BeautifulSoup(response.content, "xml")
                return self._parse_with_bs4(soup)
            else:
                logger.error("No XML parsing library available")
                return None

        except Exception as e:
            logger.error(f"Fallback parsing failed for {url}: {e}")
            return None

    def _parse_with_bs4(self, soup) -> Optional[dict[str, Any]]:
        """Parse RSS using BeautifulSoup"""
        channel = soup.find("channel")
        if not channel:
            return None

        feed_info = {
            "title": self._get_text(channel.find("title")),
            "description": self._get_text(channel.find("description")),
            "link": self._get_text(channel.find("link")),
            "language": self._get_text(channel.find("language")),
            "items": [],
        }

        for item in channel.find_all("item"):
            feed_item = FeedItem(
                title=self._get_text(item.find("title")),
                link=self._get_text(item.find("link")),
                description=self._get_text(item.find("description")),
                published=self._parse_datetime(self._get_text(item.find("pubDate"))),
                author=self._get_text(item.find("author")),
                guid=self._get_text(item.find("guid")),
            )
            feed_info["items"].append(asdict(feed_item))

        return feed_info

    def _get_text(self, element) -> str:
        """Safely extract text from XML element"""
        return element.get_text().strip() if element else ""

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string"""
        if not date_str:
            return None

        try:
            # Try common RSS date formats
            formats = [
                "%a, %d %b %Y %H:%M:%S %z",
                "%a, %d %b %Y %H:%M:%S %Z",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue

            return None
        except Exception:
            return None

    def _extract_content(self, entry) -> Optional[str]:
        """Extract content from RSS entry"""
        # Try different content fields
        content_fields = ["content", "summary", "description"]

        for field in content_fields:
            content = entry.get(field)
            if content:
                if isinstance(content, list) and content:
                    return content[0].get("value", "")
                elif isinstance(content, str):
                    return content

        return None

    def _extract_enclosures(self, entry) -> list[dict[str, Any]]:
        """Extract enclosures from RSS entry"""
        enclosures = []

        for enclosure in entry.get("enclosures", []):
            enclosures.append(
                {
                    "url": enclosure.get("href", ""),
                    "type": enclosure.get("type", ""),
                    "length": enclosure.get("length", 0),
                }
            )

        return enclosures

    def _detect_content_type(self, item: FeedItem) -> ContentType:
        """Detect content type from feed item"""
        # Check enclosures for media types
        if item.enclosures:
            for enclosure in item.enclosures:
                mime_type = enclosure.get("type", "").lower()
                if mime_type.startswith("video/"):
                    return ContentType.VIDEO
                elif mime_type.startswith("audio/"):
                    return ContentType.AUDIO
                elif mime_type.startswith("image/"):
                    return ContentType.IMAGE

        # Check categories
        if item.categories:
            categories = [cat.lower() for cat in item.categories]
            if any(cat in categories for cat in ["video", "youtube", "vimeo"]):
                return ContentType.VIDEO
            elif any(cat in categories for cat in ["audio", "podcast", "music"]):
                return ContentType.AUDIO

        return ContentType.ARTICLE


class RSSManager:
    """RSS feed manager singleton"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self.feeds: dict[str, FeedInfo] = {}
        self.cache = RSSCache()
        self.parser = RSSParser()
        self._lock = threading.RLock()
        self._background_tasks: set[asyncio.Task[Any]] = set()

    def add_feed(self, url: str, fetch_interval: int = 3600) -> bool:
        """Add RSS feed to manager"""
        try:
            with self._lock:
                if url in self.feeds:
                    logger.info(f"Feed {url} already exists")
                    return True

                # Parse feed to get initial info
                feed_data = self.parser.parse_feed(url)
                if not feed_data:
                    logger.error(f"Failed to parse feed: {url}")
                    return False

                feed_info = FeedInfo(
                    url=url,
                    title=feed_data["title"],
                    description=feed_data["description"],
                    link=feed_data["link"],
                    language=feed_data.get("language"),
                    last_updated=feed_data.get("last_updated"),
                    item_count=len(feed_data["items"]),
                    last_fetch=datetime.now(),
                    fetch_interval=fetch_interval,
                )

                self.feeds[url] = feed_info

                # Cache the feed data
                cache_key = self._get_cache_key(url)
                self.cache.set(cache_key, feed_data)

                logger.info(f"Added RSS feed: {url}")
                return True

        except Exception as e:
            logger.error(f"Error adding RSS feed {url}: {e}")
            return False

    def remove_feed(self, url: str) -> bool:
        """Remove RSS feed from manager"""
        with self._lock:
            if url in self.feeds:
                del self.feeds[url]
                cache_key = self._get_cache_key(url)
                self.cache._remove(cache_key)
                logger.info(f"Removed RSS feed: {url}")
                return True
            return False

    def get_feed_items(
        self, url: str, force_refresh: bool = False
    ) -> list[dict[str, Any]]:
        """Get items from RSS feed"""
        try:
            cache_key = self._get_cache_key(url)

            if not force_refresh:
                cached_data = self.cache.get(cache_key)
                if cached_data:
                    return cached_data.get("items", [])

            # Fetch fresh data
            feed_data = self.parser.parse_feed(url)
            if feed_data:
                self.cache.set(cache_key, feed_data)

                # Update feed info
                with self._lock:
                    if url in self.feeds:
                        self.feeds[url].last_fetch = datetime.now()
                        self.feeds[url].item_count = len(feed_data["items"])
                        self.feeds[url].status = FeedStatus.ACTIVE

                return feed_data.get("items", [])
            else:
                # Update error status
                with self._lock:
                    if url in self.feeds:
                        self.feeds[url].status = FeedStatus.PARSING_ERROR

                return []

        except Exception as e:
            logger.error(f"Error getting feed items for {url}: {e}")
            with self._lock:
                if url in self.feeds:
                    self.feeds[url].status = FeedStatus.ERROR
                    self.feeds[url].error_message = str(e)
            return []

    def get_all_feeds(self) -> dict[str, FeedInfo]:
        """Get all managed feeds"""
        with self._lock:
            return self.feeds.copy()

    def get_feed_info(self, url: str) -> Optional[FeedInfo]:
        """Get feed information"""
        with self._lock:
            return self.feeds.get(url)

    def refresh_all_feeds(self) -> dict[str, bool]:
        """Refresh all feeds"""
        results = {}

        with self._lock:
            urls = list(self.feeds.keys())

        for url in urls:
            try:
                items = self.get_feed_items(url, force_refresh=True)
                results[url] = len(items) > 0
            except Exception as e:
                logger.error(f"Error refreshing feed {url}: {e}")
                results[url] = False

        return results

    def search_items(
        self, query: str, feeds: Optional[list[str]] = None
    ) -> list[dict[str, Any]]:
        """Search for items across feeds"""
        results = []
        query_lower = query.lower()

        search_feeds = feeds or list(self.feeds.keys())

        for url in search_feeds:
            items = self.get_feed_items(url)
            for item in items:
                if (
                    query_lower in item.get("title", "").lower()
                    or query_lower in item.get("description", "").lower()
                    or query_lower in item.get("content", "").lower()
                ):
                    item["feed_url"] = url
                    results.append(item)

        return results

    def get_recent_items(
        self, hours: int = 24, feeds: Optional[list[str]] = None
    ) -> list[dict[str, Any]]:
        """Get recent items from feeds"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        results = []

        search_feeds = feeds or list(self.feeds.keys())

        for url in search_feeds:
            items = self.get_feed_items(url)
            for item in items:
                published = item.get("published")
                if published and isinstance(published, str):
                    try:
                        published = datetime.fromisoformat(
                            published.replace("Z", "+00:00")
                        )
                    except BaseException:
                        continue

                if published and published > cutoff_time:
                    item["feed_url"] = url
                    results.append(item)

        # Sort by published date
        results.sort(key=lambda x: x.get("published", ""), reverse=True)
        return results

    def get_stats(self) -> dict[str, Any]:
        """Get RSS manager statistics"""
        with self._lock:
            total_feeds = len(self.feeds)
            active_feeds = sum(
                1 for feed in self.feeds.values() if feed.status == FeedStatus.ACTIVE
            )
            error_feeds = sum(
                1
                for feed in self.feeds.values()
                if feed.status in [FeedStatus.ERROR, FeedStatus.PARSING_ERROR]
            )
            total_items = sum(feed.item_count for feed in self.feeds.values())

        return {
            "total_feeds": total_feeds,
            "active_feeds": active_feeds,
            "error_feeds": error_feeds,
            "total_items": total_items,
            "cache_size": len(self.cache._cache),
            "last_updated": datetime.now().isoformat(),
        }

    def _get_cache_key(self, url: str) -> str:
        """Generate cache key for URL"""
        return hashlib.md5(url.encode()).hexdigest()

    def clear_cache(self) -> None:
        """Clear RSS cache"""
        self.cache.clear()
        logger.info("RSS cache cleared")

    def export_feeds(self) -> dict[str, Any]:
        """Export feeds configuration"""
        with self._lock:
            return {
                "feeds": {url: asdict(info) for url, info in self.feeds.items()},
                "exported_at": datetime.now().isoformat(),
            }

    def import_feeds(self, data: dict[str, Any]) -> bool:
        """Import feeds configuration"""
        try:
            feeds_data = data.get("feeds", {})

            for url, feed_data in feeds_data.items():
                if self.add_feed(url, feed_data.get("fetch_interval", 3600)):
                    logger.info(f"Imported feed: {url}")
                else:
                    logger.warning(f"Failed to import feed: {url}")

            return True

        except Exception as e:
            logger.error(f"Error importing feeds: {e}")
            return False


# Global RSS manager instance
rss_manager = RSSManager()


# Convenience functions
def add_rss_feed(url: str, fetch_interval: int = 3600) -> bool:
    """Add RSS feed to global manager"""
    return rss_manager.add_feed(url, fetch_interval)


def get_rss_items(url: str, force_refresh: bool = False) -> list[dict[str, Any]]:
    """Get RSS feed items"""
    return rss_manager.get_feed_items(url, force_refresh)


def search_rss_items(
    query: str, feeds: Optional[list[str]] = None
) -> list[dict[str, Any]]:
    """Search RSS items"""
    return rss_manager.search_items(query, feeds)


def get_recent_rss_items(
    hours: int = 24, feeds: Optional[list[str]] = None
) -> list[dict[str, Any]]:
    """Get recent RSS items"""
    return rss_manager.get_recent_items(hours, feeds)


def get_rss_stats() -> dict[str, Any]:
    """Get RSS manager statistics"""
    return rss_manager.get_stats()
