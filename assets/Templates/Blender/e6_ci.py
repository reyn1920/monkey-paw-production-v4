import os


def ci() -> bool:
    return os.environ.get("TRAE_CI", "0") == "1"


def fast() -> bool:
    # default fast in CI; explicit FAST_MODE = 0 disables
    return os.environ.get("FAST_MODE", "1") != "0"


def pick_timeout(default: float, ci_default: float = 50) -> float:
    return ci_default if ci() or fast() else default


def cap_reel_minutes(default_minutes: int = 20) -> int:
    # CI shrinks to 1 minute unless overridden via CAP_REEL_MINUTES
    env = os.environ.get("CAP_REEL_MINUTES")
    if env:
        try:
            return max(1, int(env))
        except Exception:
            pass
    return 1 if (ci() or fast()) else default_minutes
