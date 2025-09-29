# trae_ai/agents/preflight_agent.py
import shutil
import psutil  # You'll need to run: pip install psutil

MIN_DISK_GB = 5  # Minimum required free disk space in GB
MIN_MEM_MB = 512  # Minimum required free memory in MB


class PreflightAgent:
    """A zero-dependency agent to check basic system health before the main workflow."""

    def check_environment(self) -> tuple[bool, str]:
        """Returns (is_healthy, failure_reason)."""
        print("₀ [PreflightAgent] Running system pre-flight checks...")

        # Check Disk Space
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        if free_gb < MIN_DISK_GB:
            reason = f"CRITICAL: Low disk space. Only {free_gb}GB free. Required: {MIN_DISK_GB}GB."
            print(f"❌ [PreflightAgent] {reason}")
            return False, reason

        # Check Memory
        mem = psutil.virtual_memory()
        free_mb = mem.available // (1024 * 1024)
        if free_mb < MIN_MEM_MB:
            reason = f"CRITICAL: Low memory. Only {free_mb}MB available. Required: {MIN_MEM_MB}MB."
            print(f"❌ [PreflightAgent] {reason}")
            return False, reason

        print("✅ [PreflightAgent] Environment is healthy.")
        return True, "OK"
