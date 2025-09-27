"""
Policy definitions for do-not-delete items and revenue sources.
This module contains critical system policies that must be preserved.
"""

# Core system policies that must not be deleted
DO_NOT_DELETE = {
    "core_files": ["main.py", "app.py", "run.py", "requirements.txt", "README.md"],
    "directories": ["backend/", "fastapi_app/", "routers/", "api/"],
    "config_files": [".env", ".env.example", "config/", "settings.json"],
}

# Revenue source configurations
REVENUE_SOURCES = {
    "youtube": {"enabled": True, "monetization": ["ads", "memberships", "super_chat"]},
    "affiliate": {"enabled": True, "platforms": ["amazon", "clickbank"]},
    "direct": {"enabled": True, "methods": ["paypal", "stripe"]},
}


def decoded_paths():
    """Return decoded file paths for the do-not-delete registry."""
    return {
        "absolute_paths": [
            "/Users/thomasbrianreynolds/Library/CloudStorage/GoogleDrive-brianinpty@gmail.com/My Drive/online production/main.py",
            "/Users/thomasbrianreynolds/Library/CloudStorage/GoogleDrive-brianinpty@gmail.com/My Drive/online production/backend/app.py",
            "/Users/thomasbrianreynolds/Library/CloudStorage/GoogleDrive-brianinpty@gmail.com/My Drive/online production/fastapi_app/main.py",
        ],
        "relative_paths": ["./main.py", "./backend/app.py", "./fastapi_app/main.py"],
    }
