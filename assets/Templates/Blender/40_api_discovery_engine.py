#!/usr/bin/env python3
"""
API Discovery Engine

Automated API discovery and integration system that:
- Discovers APIs from multiple sources (PublicAPIs.org, RapidAPI, GitHub, etc.)
- Validates API endpoints and documentation
- Generates integration code automatically
- Manages API credentials and rate limits
- Provides unified interface for discovered APIs
"""

import asyncio
import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


try:
    import requests
except ImportError:
    requests = None

try:
    from enhanced_web_scraping_tools import (
        EnhancedWebScraper,
        ExtractionRule,
        ScrapingConfig,
        ScrapingMethod,
    )
except ImportError:
    logging.warning("Enhanced web scraping tools not available")
    EnhancedWebScraper = None


class APICategory(Enum):
    """API categories for classification"""

    WEATHER = "weather"
    NEWS = "news"
    FINANCE = "finance"
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    PRODUCTIVITY = "productivity"
    DEVELOPER_TOOLS = "developer_tools"
    DATA_SCIENCE = "data_science"
    MACHINE_LEARNING = "machine_learning"
    BLOCKCHAIN = "blockchain"
    IOT = "iot"
    HEALTH = "health"
    EDUCATION = "education"
    TRAVEL = "travel"
    FOOD = "food"
    SPORTS = "sports"
    GAMING = "gaming"
    BUSINESS = "business"
    GOVERNMENT = "government"
    UTILITIES = "utilities"
    OTHER = "other"


class AuthType(Enum):
    """API authentication types"""

    NONE = "none"
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    BASIC_AUTH = "basic_auth"
    OAUTH2 = "oauth2"
    CUSTOM_HEADER = "custom_header"
    QUERY_PARAM = "query_param"


class APIStatus(Enum):
    """API status for tracking"""

    DISCOVERED = "discovered"
    VALIDATED = "validated"
    INTEGRATED = "integrated"
    FAILED = "failed"
    DEPRECATED = "deprecated"


@dataclass
class APIEndpoint:
    """Individual API endpoint information"""

    path: str
    method: str = "GET"
    description: Optional[str] = None
    parameters: dict[str, Any] = field(default_factory=dict)
    response_format: str = "json"
    rate_limit: Optional[str] = None
    example_response: Optional[dict] = None


@dataclass
class APICredentials:
    """API authentication credentials"""

    auth_type: AuthType
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    header_name: Optional[str] = None
    param_name: Optional[str] = None
    additional_headers: dict[str, str] = field(default_factory=dict)


@dataclass
class APIInfo:
    """Comprehensive API information"""

    name: str
    base_url: str
    category: APICategory
    description: str
    auth_type: AuthType = AuthType.NONE
    is_free: bool = True
    rate_limit: Optional[str] = None
    documentation_url: Optional[str] = None
    endpoints: list[APIEndpoint] = field(default_factory=list)
    credentials: Optional[APICredentials] = None
    status: APIStatus = APIStatus.DISCOVERED
    last_validated: Optional[datetime] = None
    validation_score: float = 0.0
    usage_count: int = 0
    error_count: int = 0
    tags: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class APIDiscoveryConfig:
    """Configuration for API discovery"""

    max_apis_per_source: int = 100
    validate_endpoints: bool = True
    generate_integration_code: bool = True
    cache_duration: int = 86400  # 24 hours
    concurrent_validations: int = 10
    timeout: float = 30.0
    retry_attempts: int = 3
    categories_filter: Optional[list[APICategory]] = None
    free_only: bool = True
    min_validation_score: float = 0.7


class APIDiscoveryEngine:
    """Main API discovery and integration engine"""

    def __init__(self, config: Optional[APIDiscoveryConfig] = None):
        self.config = config or APIDiscoveryConfig()
        self.logger = logging.getLogger(__name__)
        self.discovered_apis: dict[str, APIInfo] = {}
        self.cache_dir = Path("api_discovery_cache")
        self.cache_dir.mkdir(exist_ok=True)

        # Initialize web scraper
        scraping_config = ScrapingConfig(
            method=ScrapingMethod.REQUESTS,
            max_retries=self.config.retry_attempts,
            timeout=self.config.timeout,
            cache_responses=True,
            rate_limit=1.0,
        )

        if EnhancedWebScraper:
            self.scraper = EnhancedWebScraper(scraping_config)
        else:
            self.scraper = None
            self.logger.warning("Enhanced web scraper not available")

        # API source configurations
        self.api_sources = {
            "publicapis": {
                "url": "https://api.publicapis.org/entries",
                "method": "api_endpoint",
            },
            "rapidapi_hub": {
                "url": "https://rapidapi.com/hub",
                "method": "web_scraping",
            },
            "github_awesome_apis": {
                "url": "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md",
                "method": "markdown_parsing",
            },
            "programmableweb": {
                "url": "https://www.programmableweb.com/apis/directory",
                "method": "web_scraping",
            },
        }

    async def discover_apis_from_all_sources(self) -> dict[str, list[APIInfo]]:
        """Discover APIs from all configured sources"""
        results = {}

        for source_name, source_config in self.api_sources.items():
            try:
                self.logger.info(f"Discovering APIs from {source_name}")
                apis = await self._discover_from_source(source_name, source_config)
                results[source_name] = apis
                self.logger.info(
                    f"Discovered {
                        len(apis)} APIs from {source_name}"
                )
            except Exception as e:
                self.logger.error(f"Failed to discover APIs from {source_name}: {e}")
                results[source_name] = []

        return results

    async def _discover_from_source(
        self, source_name: str, source_config: dict
    ) -> list[APIInfo]:
        """Discover APIs from a specific source"""
        method = source_config["method"]

        if method == "api_endpoint":
            return await self._discover_from_api_endpoint(source_config["url"])
        elif method == "web_scraping":
            return await self._discover_from_web_scraping(
                source_name, source_config["url"]
            )
        elif method == "markdown_parsing":
            return await self._discover_from_markdown(source_config["url"])
        else:
            self.logger.warning(f"Unknown discovery method: {method}")
            return []

    async def _discover_from_api_endpoint(self, url: str) -> list[APIInfo]:
        """Discover APIs from PublicAPIs.org API endpoint"""
        if not requests:
            return []

        try:
            response = requests.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            data = response.json()

            apis = []
            entries = data.get("entries", [])

            for entry in entries[: self.config.max_apis_per_source]:
                try:
                    # Parse category
                    category_str = (
                        entry.get("Category", "other").lower().replace(" ", "_")
                    )
                    category = self._parse_category(category_str)

                    # Skip if category filter is set and doesn't match
                    if (
                        self.config.categories_filter
                        and category not in self.config.categories_filter
                    ):
                        continue

                    # Parse authentication
                    auth_str = entry.get("Auth", "").lower()
                    auth_type = self._parse_auth_type(auth_str)

                    # Check if free (skip paid APIs if free_only is True)
                    is_free = (
                        auth_str in ["", "no", "none"]
                        or "free" in entry.get("Description", "").lower()
                    )
                    if self.config.free_only and not is_free:
                        continue

                    api_info = APIInfo(
                        name=entry.get("API", "Unknown API"),
                        base_url=entry.get("Link", ""),
                        category=category,
                        description=entry.get("Description", ""),
                        auth_type=auth_type,
                        is_free=is_free,
                        documentation_url=entry.get("Link", ""),
                        tags={category_str, "publicapis"},
                    )

                    apis.append(api_info)

                except Exception as e:
                    self.logger.warning(f"Failed to parse API entry: {e}")
                    continue

            return apis

        except Exception as e:
            self.logger.error(f"Failed to discover APIs from endpoint {url}: {e}")
            return []

    async def _discover_from_web_scraping(
        self, source_name: str, url: str
    ) -> list[APIInfo]:
        """Discover APIs using web scraping"""
        if not self.scraper:
            return []

        try:
            # Define extraction rules based on source
            if source_name == "rapidapi_hub":
                extraction_rules = [
                    ExtractionRule(
                        name="api_cards",
                        selector=".api - card, [data - testid='api - card']",
                        is_list=True,
                        required=False,
                    )
                ]
            elif source_name == "programmableweb":
                extraction_rules = [
                    ExtractionRule(
                        name="api_listings",
                        selector=".api - listing, .directory - listing",
                        is_list=True,
                        required=False,
                    )
                ]
            else:
                extraction_rules = [
                    ExtractionRule(
                        name="api_links",
                        selector="a[href*='api'], a[href*='API']",
                        is_list=True,
                        required=False,
                    )
                ]

            result = await self.scraper.scrape_url(url, extraction_rules)

            if not result.success:
                self.logger.error(
                    f"Failed to scrape {url}: {
                        result.error_message}"
                )
                return []

            # Parse scraped data into API info
            apis = self._parse_scraped_apis(result.data, source_name)
            return apis[: self.config.max_apis_per_source]

        except Exception as e:
            self.logger.error(f"Failed to scrape APIs from {url}: {e}")
            return []

    async def _discover_from_markdown(self, url: str) -> list[APIInfo]:
        """Discover APIs from GitHub awesome lists (markdown format)"""
        if not requests:
            return []

        try:
            response = requests.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            markdown_content = response.text

            apis = self._parse_markdown_apis(markdown_content)
            return apis[: self.config.max_apis_per_source]

        except Exception as e:
            self.logger.error(f"Failed to discover APIs from markdown {url}: {e}")
            return []

    def _parse_category(self, category_str: str) -> APICategory:
        """Parse category string to APICategory enum"""
        category_mapping = {
            "weather": APICategory.WEATHER,
            "news": APICategory.NEWS,
            "finance": APICategory.FINANCE,
            "financial": APICategory.FINANCE,
            "social": APICategory.SOCIAL_MEDIA,
            "entertainment": APICategory.ENTERTAINMENT,
            "productivity": APICategory.PRODUCTIVITY,
            "development": APICategory.DEVELOPER_TOOLS,
            "developer": APICategory.DEVELOPER_TOOLS,
            "data": APICategory.DATA_SCIENCE,
            "machine_learning": APICategory.MACHINE_LEARNING,
            "ml": APICategory.MACHINE_LEARNING,
            "ai": APICategory.MACHINE_LEARNING,
            "blockchain": APICategory.BLOCKCHAIN,
            "crypto": APICategory.BLOCKCHAIN,
            "iot": APICategory.IOT,
            "health": APICategory.HEALTH,
            "medical": APICategory.HEALTH,
            "education": APICategory.EDUCATION,
            "travel": APICategory.TRAVEL,
            "food": APICategory.FOOD,
            "sports": APICategory.SPORTS,
            "gaming": APICategory.GAMING,
            "games": APICategory.GAMING,
            "business": APICategory.BUSINESS,
            "government": APICategory.GOVERNMENT,
            "utilities": APICategory.UTILITIES,
        }

        for key, category in category_mapping.items():
            if key in category_str.lower():
                return category

        return APICategory.OTHER

    def _parse_auth_type(self, auth_str: str) -> AuthType:
        """Parse authentication string to AuthType enum"""
        auth_str = auth_str.lower()

        if not auth_str or auth_str in ["no", "none", ""]:
            return AuthType.NONE
        elif "api" in auth_str and "key" in auth_str:
            return AuthType.API_KEY
        elif "bearer" in auth_str or "token" in auth_str:
            return AuthType.BEARER_TOKEN
        elif "basic" in auth_str:
            return AuthType.BASIC_AUTH
        elif "oauth" in auth_str:
            return AuthType.OAUTH2
        else:
            return AuthType.API_KEY  # Default assumption

    def _parse_scraped_apis(
        self, scraped_data: dict, source_name: str
    ) -> list[APIInfo]:
        """Parse scraped data into APIInfo objects"""
        apis = []

        # This is a simplified parser - in practice, you'd need specific
        # parsing logic for each source's HTML structure

        if source_name == "rapidapi_hub":
            api_cards = scraped_data.get("api_cards", [])
            for card_html in api_cards:
                # Parse API card HTML to extract API information
                # This would require more sophisticated HTML parsing
                pass

        elif source_name == "programmableweb":
            api_listings = scraped_data.get("api_listings", [])
            for listing_html in api_listings:
                # Parse API listing HTML
                pass

        return apis

    def _parse_markdown_apis(self, markdown_content: str) -> list[APIInfo]:
        """Parse APIs from markdown content (GitHub awesome lists)"""
        apis = []

        # Regular expression to match API entries in markdown
        # Format: **API Name** - Description [Link](url)
        api_pattern = (
            r"\\*\\*([^*]+)\\*\\*\\s*-\\s*([^\\[]+)\\s*\\[([^\\]]+)\\]\\(([^)]+)\\)"
        )

        matches = re.findall(api_pattern, markdown_content)

        for match in matches:
            name, description, link_text, url = match

            # Try to determine category from context
            category = self._infer_category_from_description(description)

            # Skip if category filter is set and doesn't match
            if (
                self.config.categories_filter
                and category not in self.config.categories_filter
            ):
                continue

            api_info = APIInfo(
                name=name.strip(),
                base_url=url.strip(),
                category=category,
                description=description.strip(),
                auth_type=AuthType.NONE,  # Default, will be validated later
                is_free=True,  # Assume free for awesome lists
                documentation_url=url.strip(),
                tags={"github", "awesome-list"},
            )

            apis.append(api_info)

        return apis

    def _infer_category_from_description(self, description: str) -> APICategory:
        """Infer API category from description text"""
        description_lower = description.lower()

        category_keywords = {
            APICategory.WEATHER: ["weather", "climate", "forecast", "temperature"],
            APICategory.NEWS: ["news", "article", "journalism", "media"],
            APICategory.FINANCE: ["finance", "stock", "currency", "exchange", "bank"],
            APICategory.SOCIAL_MEDIA: ["social", "twitter", "facebook", "instagram"],
            APICategory.ENTERTAINMENT: ["movie", "music", "video", "entertainment"],
            APICategory.DEVELOPER_TOOLS: ["developer", "code", "github", "programming"],
            APICategory.MACHINE_LEARNING: ["ai", "ml", "machine learning", "neural"],
            APICategory.HEALTH: ["health", "medical", "drug", "disease"],
            APICategory.TRAVEL: ["travel", "flight", "hotel", "booking"],
            APICategory.FOOD: ["food", "recipe", "restaurant", "nutrition"],
        }

        for category, keywords in category_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return category

        return APICategory.OTHER

    async def validate_apis(self, apis: list[APIInfo]) -> list[APIInfo]:
        """Validate discovered APIs by testing their endpoints"""
        if not self.config.validate_endpoints:
            return apis

        semaphore = asyncio.Semaphore(self.config.concurrent_validations)

        async def validate_single_api(api: APIInfo) -> APIInfo:
            async with semaphore:
                return await self._validate_api(api)

        tasks = [validate_single_api(api) for api in apis]
        validated_apis = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and failed validations
        successful_apis = []
        for result in validated_apis:
            if (
                isinstance(result, APIInfo)
                and result.validation_score >= self.config.min_validation_score
            ):
                successful_apis.append(result)

        return successful_apis

    async def _validate_api(self, api: APIInfo) -> APIInfo:
        """Validate a single API"""
        try:
            if not requests:
                api.status = APIStatus.FAILED
                return api

            # Test basic connectivity
            response = requests.get(
                api.base_url, timeout=self.config.timeout, allow_redirects=True
            )

            score = 0.0

            # Check if URL is reachable
            if response.status_code < 400:
                score += 0.3

            # Check if it returns JSON (common for APIs)
            try:
                response.json()
                score += 0.2
            except Exception:
                pass

            # Check for API - like headers
            headers = response.headers
            if any(
                header in headers
                for header in ["content - type", "x - ratelimit", "x - api"]
            ):
                score += 0.2

            # Check for documentation indicators
            content = response.text.lower()
            if any(
                word in content
                for word in ["api", "endpoint", "documentation", "swagger"]
            ):
                score += 0.3

            api.validation_score = score
            api.last_validated = datetime.now()

            if score >= self.config.min_validation_score:
                api.status = APIStatus.VALIDATED
            else:
                api.status = APIStatus.FAILED

        except Exception as e:
            self.logger.warning(f"Failed to validate API {api.name}: {e}")
            api.status = APIStatus.FAILED
            api.validation_score = 0.0

        return api

    def generate_integration_code(self, api: APIInfo) -> str:
        """Generate Python integration code for an API"""
        if not self.config.generate_integration_code:
            return ""

        # Generate class name
        class_name = "".join(word.capitalize() for word in api.name.split())
        class_name = re.sub(r"[^A-Za-z0-9]", "", class_name) + "Client"

        # Generate authentication setup
        auth_setup = self._generate_auth_setup(api.auth_type)

        # Generate basic client code
        code = f'''#!/usr/bin/env python3
"""
Auto-generated client for {api.name} API
Generated on: {datetime.now().isoformat()}
API Documentation: {api.documentation_url or "N/A"}
"""

import requests
from typing import Dict, Any, Optional
import json


class {class_name}:
    """Client for {api.name} API"""

    def __init__(self{auth_setup["init_params"]}):
        self.base_url = "{api.base_url}"
        self.session = requests.Session()
        {auth_setup["init_code"]}


    def _make_request(self, method: str, endpoint_path: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API endpoint"""
        url = f"{{self.base_url.rstrip('/')}}/{{endpoint_path.lstrip('/')}}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as request_error:
            raise Exception(f"API request failed: {{request_error}}")


    def get(self, endpoint_path: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request to API endpoint"""
        return self._make_request('GET', endpoint_path, params=params)


    def post(self,
    endpoint_path: str,
    data: Optional[Dict] = None,
    json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request to API endpoint"""
        return self._make_request('POST', endpoint_path, data=data, json=json_data)

    # Add specific methods based on discovered endpoints
    {self._generate_endpoint_methods(api)}

# Example usage
if __name__ == "__main__":
    client = {class_name}({auth_setup["example_params"]})

    try:
        # Example API call
        result = client.get("/")
        print(json.dumps(result, indent=2))
    except Exception as api_error:
        print(f"Error: {{api_error}}")
'''

        return code

    def _generate_auth_setup(self, auth_type: AuthType) -> dict[str, str]:
        """Generate authentication setup code"""
        if auth_type == AuthType.API_KEY:
            return {
                "init_params": ", api_key: str",
                "init_code": '        self.session.headers["X - API - Key"] = api_key',
                "example_params": '"your_api_key_here"',
            }
        elif auth_type == AuthType.BEARER_TOKEN:
            return {
                "init_params": ", token: str",
                "init_code": '        self.session.headers["Authorization"] = f"Bearer {token}"',
                "example_params": '"your_token_here"',
            }
        elif auth_type == AuthType.BASIC_AUTH:
            return {
                "init_params": ", username: str, password: str",
                "init_code": "        self.session.auth = (username, password)",
                "example_params": '"username", "password"',
            }
        else:
            return {
                "init_params": "",
                "init_code": "        # No authentication required",
                "example_params": "",
            }

    def _generate_endpoint_methods(self, api: APIInfo) -> str:
        """Generate methods for known endpoints"""
        if not api.endpoints:
            return "    # No specific endpoints discovered"

        methods = []
        for api_endpoint in api.endpoints:  # Renamed from 'endpoint' to 'api_endpoint'
            method_name = (
                api_endpoint.path.strip("/").replace("/", "_").replace("-", "_")
            )
            method_name = (
                re.sub(r"[^a-zA-Z0-9_]", "", method_name) or "root"
            )  # Fixed regex pattern

            method_code = f'''
    def {method_name}(self, **params) -> Dict[str, Any]:
        """
        Call {api_endpoint.path} endpoint

        Description: {api_endpoint.description or "No description available"}
        Method: {api_endpoint.method}
        """
        return self._make_request("{api_endpoint.method}", "{api_endpoint.path}", params=params)
'''

            methods.append(method_code)

        return "\n".join(methods)  # Fixed escaped newline

    def save_discovered_apis(
        self, apis: list[APIInfo], filename: str = "discovered_apis.json"
    ) -> None:
        """Save discovered APIs to file"""
        api_data = []
        for api in apis:
            api_dict = {
                "name": api.name,
                "base_url": api.base_url,
                "category": api.category.value,
                "description": api.description,
                "auth_type": api.auth_type.value,
                "is_free": api.is_free,
                "rate_limit": api.rate_limit,
                "documentation_url": api.documentation_url,
                "status": api.status.value,
                "validation_score": api.validation_score,
                "last_validated": (
                    api.last_validated.isoformat() if api.last_validated else None
                ),
                "tags": list(api.tags),
                "metadata": api.metadata,
            }
            api_data.append(api_dict)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Saved {len(apis)} APIs to {filename}")

    def load_discovered_apis(
        self, filename: str = "discovered_apis.json"
    ) -> list[APIInfo]:
        """Load discovered APIs from file"""
        try:
            with open(filename, encoding="utf-8") as f:
                api_data = json.load(f)

            apis = []
            for data in api_data:
                api = APIInfo(
                    name=data["name"],
                    base_url=data["base_url"],
                    category=APICategory(data["category"]),
                    description=data["description"],
                    auth_type=AuthType(data["auth_type"]),
                    is_free=data["is_free"],
                    rate_limit=data.get("rate_limit"),
                    documentation_url=data.get("documentation_url"),
                    status=APIStatus(data["status"]),
                    validation_score=data.get("validation_score", 0.0),
                    tags=set(data.get("tags", [])),
                    metadata=data.get("metadata", {}),
                )

                if data.get("last_validated"):
                    api.last_validated = datetime.fromisoformat(data["last_validated"])

                apis.append(api)

            self.logger.info(f"Loaded {len(apis)} APIs from {filename}")
            return apis

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to load APIs from {filename}: {e}")
            return []

    def get_apis_by_category(self, category: APICategory) -> list[APIInfo]:
        """Get APIs filtered by category"""
        return [
            api for api in self.discovered_apis.values() if api.category == category
        ]

    def get_free_apis(self) -> list[APIInfo]:
        """Get only free APIs"""
        return [api for api in self.discovered_apis.values() if api.is_free]

    def get_validated_apis(self) -> list[APIInfo]:
        """Get only validated APIs"""
        return [
            api
            for api in self.discovered_apis.values()
            if api.status == APIStatus.VALIDATED
        ]

    def search_apis(self, query: str) -> list[APIInfo]:
        """Search APIs by name or description"""
        query_lower = query.lower()
        results = []

        for api in self.discovered_apis.values():
            if (
                query_lower in api.name.lower()
                or query_lower in api.description.lower()
                or any(query_lower in tag for tag in api.tags)
            ):
                results.append(api)

        return results

    async def run_full_discovery(self) -> dict[str, Any]:
        """Run complete API discovery process"""
        start_time = time.time()

        # Discover APIs from all sources
        discovery_results = await self.discover_apis_from_all_sources()

        # Flatten results
        all_apis = []
        for source_apis in discovery_results.values():
            all_apis.extend(source_apis)

        # Remove duplicates based on base URL
        unique_apis = {}
        for api in all_apis:
            key = api.base_url.lower().strip("/")
            if (
                key not in unique_apis
                or api.validation_score > unique_apis[key].validation_score
            ):
                unique_apis[key] = api

        unique_apis_list = list(unique_apis.values())

        # Validate APIs
        validated_apis = await self.validate_apis(unique_apis_list)

        # Store in memory
        for api in validated_apis:
            self.discovered_apis[api.name] = api

        # Generate integration code for top APIs
        integration_codes = {}
        if self.config.generate_integration_code:
            top_apis = sorted(
                validated_apis, key=lambda x: x.validation_score, reverse=True
            )[:10]
            for api in top_apis:
                integration_codes[api.name] = self.generate_integration_code(api)

        # Save results
        self.save_discovered_apis(validated_apis)

        end_time = time.time()

        return {
            "total_discovered": len(all_apis),
            "unique_apis": len(unique_apis_list),
            "validated_apis": len(validated_apis),
            "discovery_sources": discovery_results,
            "integration_codes": integration_codes,
            "execution_time": end_time - start_time,
            "categories": {
                category.value: len(self.get_apis_by_category(category))
                for category in APICategory
            },
            "free_apis": len(self.get_free_apis()),
            "validated_count": len(self.get_validated_apis()),
        }

    def cleanup(self) -> None:
        """Clean up resources"""
        if self.scraper:
            self.scraper.cleanup()

        self.logger.info("API Discovery Engine cleanup completed")


# Example usage
if __name__ == "__main__":

    async def main():
        # Configure discovery
        config = APIDiscoveryConfig(
            max_apis_per_source=50,
            validate_endpoints=True,
            generate_integration_code=True,
            categories_filter=[
                APICategory.WEATHER,
                APICategory.NEWS,
                APICategory.FINANCE,
            ],
            free_only=True,
        )

        # Initialize discovery engine
        engine = APIDiscoveryEngine(config)

        try:
            # Run full discovery
            results = await engine.run_full_discovery()

            print("\\n=== API Discovery Results ===")
            print(f"Total APIs discovered: {results['total_discovered']}")
            print(f"Unique APIs: {results['unique_apis']}")
            print(f"Validated APIs: {results['validated_apis']}")
            print(f"Execution time: {results['execution_time']:.2f} seconds")

            print("\\n=== Categories ===")
            for category, count in results["categories"].items():
                if count > 0:
                    print(f"{category}: {count} APIs")

            print("\\n=== Top Validated APIs ===")
            validated_apis = engine.get_validated_apis()
            top_apis = sorted(
                validated_apis, key=lambda x: x.validation_score, reverse=True
            )[:5]

            for api in top_apis:
                print(f"\\n{api.name}")
                print(f"  URL: {api.base_url}")
                print(f"  Category: {api.category.value}")
                print(f"  Score: {api.validation_score:.2f}")
                print(f"  Description: {api.description[:100]}...")

        finally:
            engine.cleanup()

    # Run the discovery
    asyncio.run(main())
