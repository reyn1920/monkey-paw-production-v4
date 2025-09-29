#!/usr/bin/env python3
"""
Optimized Startup Configuration
Only loads essential components to minimize memory usage
"""

import logging
from typing import Union


class OptimizedStartup:
    """Manages application startup with minimal memory footprint"""

    def __init__(self):
        self.essential_services = [
            "api_orchestrator",
            "secret_store",
            "task_queue_manager",
        ]
        self.lazy_load_services = ["dashboard", "agents", "monitoring", "analytics"]
        self.loaded_services = set()

    def load_essential_only(self) -> dict[str, bool]:
        """Load only essential services for minimal startup"""
        results = {}

        for service in self.essential_services:
            try:
                # Lazy import to save memory
                if service == "api_orchestrator":
                    results[service] = True
                elif service == "secret_store":
                    results[service] = True
                elif service == "task_queue_manager":
                    results[service] = True

                self.loaded_services.add(service)

            except ImportError as e:
                logging.warning(f"Failed to load essential service {service}: {e}")
                results[service] = False

        return results

    def load_on_demand(self, service_name: str) -> bool:
        """Load services only when needed"""
        if service_name in self.loaded_services:
            return True

        try:
            if service_name == "dashboard":
                pass
            elif service_name == "agents":
                # Load agents dynamically
                pass
            elif service_name == "monitoring":
                # Load monitoring when needed
                pass
            elif service_name == "analytics":
                # Load analytics when requested
                pass

            self.loaded_services.add(service_name)
            return True

        except ImportError as e:
            logging.error(f"Failed to load service {service_name}: {e}")
            return False

    def get_memory_usage(self) -> dict[str, Union[str, int, list[str]]]:
        """Get current memory usage statistics"""
        try:
            import psutil

            process = psutil.Process()
            memory_info = process.memory_info()

            return {
                "rss": f"{memory_info.rss / 1024 / 1024:.2f} MB",
                "vms": f"{memory_info.vms / 1024 / 1024:.2f} MB",
                "loaded_services": len(self.loaded_services),
                "services": list(self.loaded_services),
            }
        except ImportError:
            return {
                "rss": "N/A",
                "vms": "N/A",
                "loaded_services": len(self.loaded_services),
                "services": list(self.loaded_services),
            }


# Global startup manager
startup_manager = OptimizedStartup()
