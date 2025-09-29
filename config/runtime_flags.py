import os


def allow_unauth_runtime() -> bool:
    return os.getenv("ALLOW_UNAUTH_RUNTIME", "false").lower() in ("1", "true", "yes")


def health_cache_ttl_seconds() -> int:
    return int(os.getenv("HEALTH_TTL_SECONDS", "5"))
