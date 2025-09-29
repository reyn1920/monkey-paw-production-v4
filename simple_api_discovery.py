#!/usr/bin/env python3
"""
Simple API Discovery Script

Standalone script to discover and integrate free APIs without complex dependencies.
"""

import json
import sqlite3
import requests
import time
from datetime import datetime
from typing import Any


class SimpleAPIDiscovery:
    """Simple API discovery without complex dependencies"""

    def __init__(self, db_path: str = "databases/master.db"):
        self.db_path = db_path
        self.discovered_apis = []

    def discover_free_apis(self) -> list[dict[str, Any]]:
        """Discover free APIs from PublicAPIs.org"""
        print("🔍 Discovering free APIs from PublicAPIs.org...")

        try:
            # Get APIs from PublicAPIs.org
            response = requests.get("https://api.publicapis.org/entries", timeout=30)
            if response.status_code == 200:
                data = response.json()
                all_apis = data.get("entries", [])

                # Filter for free APIs
                free_apis = [
                    api
                    for api in all_apis
                    if api.get("Auth", "").lower() in ["", "no", "none"]
                    or "free" in api.get("Description", "").lower()
                ]

                print(
                    f"✅ Found {len(free_apis)} free APIs out of {len(all_apis)} total"
                )
                return free_apis[:50]  # Limit to first 50 for processing
            else:
                print(f"❌ Failed to fetch APIs: HTTP {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Error discovering APIs: {e}")
            return []

    def categorize_apis(
        self, apis: list[dict[str, Any]]
    ) -> dict[str, list[dict[str, Any]]]:
        """Categorize APIs by their category"""
        categorized = {}

        for api in apis:
            category = api.get("Category", "Other")
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(api)

        return categorized

    def save_to_database(self, apis: list[dict[str, Any]]) -> int:
        """Save discovered APIs to database"""
        print("💾 Saving APIs to database...")

        try:
            with sqlite3.connect(self.db_path) as conn:
                saved_count = 0

                for api in apis:
                    # Insert API data
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO discovered_apis
                        (name, description, url, category, auth_required, https_support, cors_support)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            api.get("API", "Unknown"),
                            api.get("Description", ""),
                            api.get("Link", ""),
                            api.get("Category", "Other"),
                            api.get("Auth", "") != "",
                            api.get("HTTPS", False),
                            api.get("Cors", "unknown"),
                        ),
                    )
                    #                     )
                    saved_count += 1

                conn.commit()
                print(f"✅ Saved {saved_count} APIs to database")
                return saved_count

        except Exception as e:
            print(f"❌ Error saving to database: {e}")
            return 0

    def update_system_config(self, api_count: int) -> bool:
        """Update system configuration with API discovery results"""
        try:
            config = {
                "last_discovery": datetime.now().isoformat(),
                "apis_discovered": api_count,
                "discovery_status": "completed",
            }

            with open("config/api_discovery.json", "w") as f:
                json.dump(config, f, indent=2)

            print(f"✅ Updated system config with {api_count} APIs")
            return True

        except Exception as e:
            print(f"❌ Error updating config: {e}")
            return False

    def generate_report(self) -> dict[str, Any]:
        """Generate discovery report"""
        print("📊 Generating discovery report...")

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row

                # Get category statistics
                cursor = conn.execute(
                    """
                    SELECT category, COUNT(*) as count
                    FROM discovered_apis
                    GROUP BY category
                    ORDER BY count DESC
                    """
                )

                category_stats = [dict(row) for row in cursor.fetchall()]

                # Get total count
                cursor = conn.execute(
                    """
                    SELECT COUNT(*) as total
                    FROM discovered_apis
                    """
                )

                total_count = cursor.fetchone()[0]

                # Get recent discoveries
                cursor = conn.execute(
                    """
                    SELECT name, category, description
                    FROM discovered_apis
                    ORDER BY rowid DESC
                    LIMIT 10
                    """
                )

                recent_discoveries = [dict(row) for row in cursor.fetchall()]

                return {
                    "total_apis": total_count,
                    "categories": category_stats,
                    "recent_discoveries": recent_discoveries,
                    "generated_at": datetime.now().isoformat(),
                }

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return {}

    def run_discovery(self) -> dict[str, Any]:
        """Run complete API discovery process"""
        print("🚀 Starting API discovery process...")
        start_time = time.time()

        # Discover APIs
        apis = self.discover_free_apis()
        if not apis:
            print("❌ No APIs discovered")
            return {"success": False, "message": "No APIs discovered"}

        # Categorize APIs
        categorized = self.categorize_apis(apis)
        print(f"📊 Categorized into {len(categorized)} categories")

        # Save to database
        saved_count = self.save_to_database(apis)
        if saved_count == 0:
            print("❌ Failed to save APIs to database")
            return {"success": False, "message": "Failed to save APIs"}

        # Update system config
        self.update_system_config(saved_count)

        # Generate report
        report = self.generate_report()

        end_time = time.time()
        duration = end_time - start_time

        print(f"✅ Discovery completed in {duration:.2f} seconds")
        print(f"📈 Discovered and saved {saved_count} APIs")

        return {
            "success": True,
            "apis_discovered": saved_count,
            "categories": list(categorized.keys()),
            "duration": duration,
            "report": report,
        }


def main():
    """Main function to run API discovery"""
    # DEBUG_REMOVED: print("=" * 50)
    # DEBUG_REMOVED: print("Simple API Discovery Tool")
    # DEBUG_REMOVED: print("=" * 50)

    discovery = SimpleAPIDiscovery()
    result = discovery.run_discovery()

    if result.get("success"):
        # DEBUG_REMOVED: print("\n🎉 API Discovery completed successfully!")
        print(f"📊 Total APIs: {result.get('apis_discovered', 0)}")
        print(f"📂 Categories: {', '.join(result.get('categories', []))}")
        print(f"⏱️  Duration: {result.get('duration', 0):.2f} seconds")
    else:
        print(f"\n❌ Discovery failed: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    main()
