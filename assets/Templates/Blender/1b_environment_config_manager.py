#!/usr/bin/env python3
"""
Environment Configuration Manager

This module manages environment variable configurations for all integrated services
in the live production environment. It ensures all required API keys and settings
are properly configured for optimal system operation.

Features:
- Environment validation and setup
- API key configuration management
- Service - specific environment templates
- Live environment health checks
- Configuration backup and restore
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnvironmentConfigManager:
    """Manages environment configurations for live production deployment"""

    def __init__(self, env_file_path: str = ".env"):
        self.env_file_path = Path(env_file_path)
        self.config_categories = self._initialize_config_categories()

    def _initialize_config_categories(self) -> dict[str, dict[str, Any]]:
        """Initialize all configuration categories with their requirements"""
        return {
            "core_system": {
                "description": "Core system configuration for live environment",
                "required": True,
                "variables": {
                    "ENVIRONMENT": {
                        "default": "production",
                        "description": "Environment type",
                    },
                    "NODE_ENV": {
                        "default": "production",
                        "description": "Node environment",
                    },
                    "DEBUG": {"default": "false", "description": "Debug mode"},
                    "PORT": {"default": "8000", "description": "Application port"},
                    "HOST": {"default": "0.0.0.0", "description": "Host binding"},
                    "SECRET_KEY": {
                        "required": True,
                        "description": "Application secret key (32+ chars)",
                    },
                    "JWT_SECRET": {"required": True, "description": "JWT token secret"},
                    "JWT_ALGORITHM": {
                        "default": "HS256",
                        "description": "JWT algorithm",
                    },
                    "JWT_EXPIRATION_HOURS": {
                        "default": "24",
                        "description": "JWT expiration time",
                    },
                },
            },
            "database": {
                "description": "Database configuration",
                "required": True,
                "variables": {
                    "DATABASE_PATH": {
                        "default": "data/trae_master.db",
                        "description": "SQLite database path",
                    },
                    "DATABASE_URL": {
                        "default": "sqlite:///data/production_revenue.db",
                        "description": "Database URL",
                    },
                },
            },
            "free_ai_ml": {
                "description": "Free AI/ML API integrations",
                "required": False,
                "variables": {
                    "GROQ_API_KEY": {
                        "service_url": "https://console.groq.com/",
                        "description": "Groq AI API key - Fast inference",
                    },
                    "HUGGINGFACE_API_KEY": {
                        "service_url": "https://huggingface.co/settings/tokens",
                        "description": "Hugging Face API token",
                    },
                },
            },
            "free_media": {
                "description": "Free media API integrations",
                "required": False,
                "variables": {
                    "PEXELS_API_KEY": {
                        "service_url": "https://www.pexels.com/api/",
                        "description": "Pexels stock photos API",
                    }
                },
            },
            "free_news": {
                "description": "Free news API integrations",
                "required": False,
                "variables": {
                    "GUARDIAN_API_KEY": {
                        "service_url": "https://open - platform.theguardian.com/",
                        "description": "Guardian News API",
                    },
                    "NYTIMES_API_KEY": {
                        "service_url": "https://developer.nytimes.com/",
                        "description": "NY Times API",
                    },
                },
            },
            "free_social": {
                "description": "Free social media API integrations",
                "required": False,
                "variables": {
                    "REDDIT_CLIENT_ID": {
                        "service_url": "https://www.reddit.com/prefs/apps",
                        "description": "Reddit API client ID",
                    },
                    "REDDIT_CLIENT_SECRET": {
                        "service_url": "https://www.reddit.com/prefs/apps",
                        "description": "Reddit API client secret",
                    },
                    "YOUTUBE_API_KEY": {
                        "service_url": "https://console.developers.google.com/",
                        "description": "YouTube Data API v3 key",
                    },
                    "GITHUB_TOKEN": {
                        "service_url": "https://github.com/settings/tokens",
                        "description": "GitHub personal access token",
                    },
                },
            },
            "free_email": {
                "description": "Free email service integrations",
                "required": False,
                "variables": {
                    "SENDGRID_API_KEY": {
                        "service_url": "https://app.sendgrid.com/settings/api_keys",
                        "description": "SendGrid API key (100 emails/day free)",
                    },
                    "MAILCHIMP_API_KEY": {
                        "service_url": "https://mailchimp.com/developer/marketing/guides/quick - start/",
                        "description": "Mailchimp API key (2,000 contacts free)",
                    },
                },
            },
            "free_analytics": {
                "description": "Free analytics service integrations",
                "required": False,
                "variables": {
                    "GOOGLE_ANALYTICS_ID": {
                        "service_url": "https://analytics.google.com/",
                        "description": "Google Analytics tracking ID",
                    },
                    "GOOGLE_SEARCH_CONSOLE_KEY": {
                        "service_url": "https://search.google.com/search - console",
                        "description": "Google Search Console API key",
                    },
                },
            },
            "payment_sandbox": {
                "description": "Free payment system sandbox environments",
                "required": False,
                "variables": {
                    "STRIPE_PUBLIC_KEY": {
                        "service_url": "https://dashboard.stripe.com/test/apikeys",
                        "description": "Stripe test public key",
                    },
                    "STRIPE_SECRET_KEY": {
                        "service_url": "https://dashboard.stripe.com/test/apikeys",
                        "description": "Stripe test secret key",
                    },
                    "PAYPAL_CLIENT_ID": {
                        "service_url": "https://developer.paypal.com/",
                        "description": "PayPal sandbox client ID",
                    },
                    "PAYPAL_CLIENT_SECRET": {
                        "service_url": "https://developer.paypal.com/",
                        "description": "PayPal sandbox client secret",
                    },
                    "SQUARE_APPLICATION_ID": {
                        "service_url": "https://developer.squareup.com/",
                        "description": "Square sandbox application ID",
                    },
                    "SQUARE_ACCESS_TOKEN": {
                        "service_url": "https://developer.squareup.com/",
                        "description": "Square sandbox access token",
                    },
                },
            },
            "deployment": {
                "description": "Deployment and hosting configuration",
                "required": False,
                "variables": {
                    "NETLIFY_AUTH_TOKEN": {
                        "service_url": "https://app.netlify.com/user/applications",
                        "description": "Netlify deployment token",
                    },
                    "NETLIFY_SITE_ID": {
                        "service_url": "https://app.netlify.com/",
                        "description": "Netlify site ID",
                    },
                },
            },
            "security": {
                "description": "Security and CORS configuration",
                "required": True,
                "variables": {
                    "ALLOWED_HOSTS": {
                        "default": "localhost,127.0.0.1",
                        "description": "Allowed host domains",
                    },
                    "CORS_ORIGINS": {
                        "default": "http://localhost:8000",
                        "description": "CORS allowed origins",
                    },
                },
            },
        }

    def validate_environment(self) -> dict[str, Any]:
        """Validate current environment configuration"""
        validation_results: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "env_file_exists": self.env_file_path.exists(),
            "categories": {},
            "missing_required": [],
            "configured_optional": [],
            "total_configured": 0,
            "total_possible": 0,
            "configuration_score": 0.0,
        }

        # Load current environment
        current_env = self._load_current_env()

        for category_name, category_config in self.config_categories.items():
            category_result = {
                "description": category_config["description"],
                "required": category_config["required"],
                "configured_vars": [],
                "missing_vars": [],
                "total_vars": len(category_config["variables"]),
                "configured_count": 0,
            }

            for var_name, var_config in category_config["variables"].items():
                validation_results["total_possible"] += 1

                if var_name in current_env and current_env[var_name].strip():
                    category_result["configured_vars"].append(var_name)
                    category_result["configured_count"] += 1
                    validation_results["total_configured"] += 1

                    if not category_config["required"]:
                        validation_results["configured_optional"].append(var_name)
                else:
                    category_result["missing_vars"].append(var_name)
                    if category_config["required"] or var_config.get("required"):
                        validation_results["missing_required"].append(var_name)

            validation_results["categories"][category_name] = category_result

        # Calculate configuration score
        if validation_results["total_possible"] > 0:
            validation_results["configuration_score"] = (
                validation_results["total_configured"]
                / validation_results["total_possible"]
            ) * 100

        return validation_results

    def _load_current_env(self) -> dict[str, str]:
        """Load current environment variables from .env file and system"""
        env_vars = {}

        # Load from .env file if it exists
        if self.env_file_path.exists():
            with open(self.env_file_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip()

        # Override with system environment variables
        for key in os.environ:
            env_vars[key] = os.environ[key]

        return env_vars

    def generate_env_template(self) -> str:
        """Generate a complete .env template with all possible configurations"""
        template_lines = [
            "# TRAE.AI Live Environment Configuration",
            "# Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "# This file contains all possible environment variables for live deployment",
            "",
        ]

        for category_name, category_config in self.config_categories.items():
            template_lines.extend(
                [
                    f"# {category_config['description'].upper()}",
                    f"# Required: {'Yes' if category_config['required'] else 'No'}",
                    "",
                ]
            )

            for var_name, var_config in category_config["variables"].items():
                description = var_config.get("description", "")
                service_url = var_config.get("service_url", "")
                default_value = var_config.get("default", "")
                required = var_config.get("required", False)

                if description:
                    template_lines.append(f"# {description}")
                if service_url:
                    template_lines.append(f"# Get from: {service_url}")
                if required:
                    template_lines.append("# REQUIRED")

                if default_value:
                    template_lines.append(f"{var_name}={default_value}")
                else:
                    template_lines.append(f"# {var_name}=your_{var_name.lower()}_here")

                template_lines.append("")

        return "\n".join(template_lines)

    def create_setup_guide(self) -> dict[str, Any]:
        """Create a comprehensive setup guide for all services"""
        setup_guide = {
            "title": "Live Environment Setup Guide",
            "generated_at": datetime.now().isoformat(),
            "categories": [],
        }

        for category_name, category_config in self.config_categories.items():
            category_guide = {
                "name": category_name,
                "title": category_config["description"],
                "required": category_config["required"],
                "services": [],
            }

            for var_name, var_config in category_config["variables"].items():
                service_info = {
                    "variable": var_name,
                    "description": var_config.get("description", ""),
                    "signup_url": var_config.get("service_url", ""),
                    "required": var_config.get("required", False),
                    "free_tier": self._get_free_tier_info(var_name),
                }
                category_guide["services"].append(service_info)

            setup_guide["categories"].append(category_guide)

        return setup_guide

    def _get_free_tier_info(self, var_name: str) -> str:
        """Get free tier information for specific services"""
        free_tier_info = {
            "GROQ_API_KEY": "Generous free usage limits for fast AI inference",
            "HUGGINGFACE_API_KEY": "1,000 requests/month free",
            "PEXELS_API_KEY": "200 requests/hour free",
            "GUARDIAN_API_KEY": "5,000 calls/day free",
            "NYTIMES_API_KEY": "4,000 requests/day free",
            "REDDIT_CLIENT_ID": "60 requests/minute free",
            "YOUTUBE_API_KEY": "10,000 units/day free",
            "GITHUB_TOKEN": "5,000 requests/hour free",
            "SENDGRID_API_KEY": "100 emails/day free",
            "MAILCHIMP_API_KEY": "2,000 contacts free",
            "GOOGLE_ANALYTICS_ID": "Free with Google account",
            "STRIPE_PUBLIC_KEY": "Free sandbox environment",
            "PAYPAL_CLIENT_ID": "Free sandbox environment",
            "SQUARE_APPLICATION_ID": "Free sandbox environment",
        }
        return free_tier_info.get(var_name, "Free tier available")

    def backup_current_config(self) -> str:
        """Backup current environment configuration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"env_backup_{timestamp}.env"
        backup_path = Path(backup_filename)

        if self.env_file_path.exists():
            with open(self.env_file_path) as source:
                with open(backup_path, "w") as backup:
                    backup.write(source.read())
            logger.info(f"Environment backup created: {backup_filename}")
            return str(backup_path)
        else:
            logger.warning("No .env file found to backup")
            return ""

    def generate_deployment_checklist(self) -> list[dict[str, Any]]:
        """Generate a deployment checklist for live environment"""
        checklist = [
            {
                "category": "Environment Setup",
                "items": [
                    {"task": "Backup current .env file", "critical": True},
                    {"task": "Set ENVIRONMENT = production", "critical": True},
                    {"task": "Set DEBUG = false", "critical": True},
                    {
                        "task": "Configure strong SECRET_KEY (32+ chars)",
                        "critical": True,
                    },
                    {"task": "Set up JWT secrets", "critical": True},
                ],
            },
            {
                "category": "Security Configuration",
                "items": [
                    {
                        "task": "Configure ALLOWED_HOSTS for production domain",
                        "critical": True,
                    },
                    {"task": "Set CORS_ORIGINS for production URLs", "critical": True},
                    {"task": "Verify no secrets in source code", "critical": True},
                    {"task": "Enable HTTPS in production", "critical": True},
                ],
            },
            {
                "category": "API Integration",
                "items": [
                    {
                        "task": "Configure free AI/ML APIs (Groq, Hugging Face)",
                        "critical": False,
                    },
                    {"task": "Set up media APIs (Pexels)", "critical": False},
                    {
                        "task": "Configure news APIs (Guardian, NY Times)",
                        "critical": False,
                    },
                    {
                        "task": "Set up social APIs (Reddit, YouTube, GitHub)",
                        "critical": False,
                    },
                ],
            },
            {
                "category": "Service Integration",
                "items": [
                    {
                        "task": "Configure email services (SendGrid, Mailchimp)",
                        "critical": False,
                    },
                    {"task": "Set up analytics (Google Analytics)", "critical": False},
                    {
                        "task": "Configure payment sandbox environments",
                        "critical": False,
                    },
                ],
            },
            {
                "category": "Deployment",
                "items": [
                    {"task": "Set up Netlify deployment tokens", "critical": False},
                    {"task": "Configure CI/CD pipeline", "critical": False},
                    {"task": "Test all integrations in staging", "critical": True},
                    {"task": "Verify database connectivity", "critical": True},
                ],
            },
        ]
        return checklist


def main():
    """Main function to demonstrate environment configuration management"""
    logger.info("Starting Environment Configuration Manager")

    # Initialize manager
    env_manager = EnvironmentConfigManager()

    # Validate current environment
    logger.info("Validating current environment configuration...")
    validation = env_manager.validate_environment()

    print("\n" + "=" * 80)
    print("LIVE ENVIRONMENT CONFIGURATION STATUS")
    print("=" * 80)

    print(f"\nConfiguration Score: {validation['configuration_score']:.1f}%")
    print(
        f"Total Variables Configured: {validation['total_configured']}/{validation['total_possible']}"
    )

    if validation["missing_required"]:
        print(
            f"\n❌ CRITICAL: Missing Required Variables ({len(validation['missing_required'])})"
        )
        for var in validation["missing_required"]:
            print(f"  - {var}")

    print(
        f"\n✅ Optional Services Configured ({len(validation['configured_optional'])})"
    )
    for var in validation["configured_optional"]:
        print(f"  - {var}")

    print("\nCATEGORY BREAKDOWN:")
    print("-" * 40)
    for category_name, category_data in validation["categories"].items():
        status = (
            "✅"
            if category_data["configured_count"] > 0
            else "❌" if category_data["required"] else "⚪"
        )
        print(
            f"{status} {category_name.upper()}: {category_data['configured_count']}/{category_data['total_vars']}"
        )
        print(f"    {category_data['description']}")

    # Generate setup guide
    logger.info("Generating setup guide...")
    setup_guide = env_manager.create_setup_guide()

    # Save setup guide
    setup_filename = (
        f"environment_setup_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(setup_filename, "w") as f:
        json.dump(setup_guide, f, indent=2)

    print(f"\n📋 Setup guide saved to: {setup_filename}")

    # Generate deployment checklist
    checklist = env_manager.generate_deployment_checklist()
    checklist_filename = (
        f"deployment_checklist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(checklist_filename, "w") as f:
        json.dump(checklist, f, indent=2)

    print(f"📋 Deployment checklist saved to: {checklist_filename}")

    # Generate .env template
    template = env_manager.generate_env_template()
    template_filename = "env_template_complete.env"
    with open(template_filename, "w") as f:
        f.write(template)

    print(f"📄 Complete .env template saved to: {template_filename}")

    print("\n" + "=" * 80)
    print("NEXT STEPS FOR LIVE DEPLOYMENT:")
    print("=" * 80)
    print("1. Review the setup guide for API key registration")
    print("2. Follow the deployment checklist")
    print("3. Configure critical environment variables")
    print("4. Test all integrations in staging environment")
    print("5. Deploy to live production environment")

    logger.info("Environment configuration analysis complete")


if __name__ == "__main__":
    main()
