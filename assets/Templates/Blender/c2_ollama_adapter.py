import logging
import os
import time

# Handle optional dependencies with fallbacks
try:
    import requests
except ImportError:
    requests = None
    logging.warning(
        "requests library not available, ollama adapter will use fallback responses"
    )

try:
    from backend.utils.timeout_utils import pick_timeout
except ImportError:

    def pick_timeout(timeout, ci_default=None):
        """Fallback timeout picker when utils not available"""
        return ci_default if ci_default is not None else timeout


log = logging.getLogger("integrations.llm.ollama")

# Ollama configuration from environment variables
USE_OLLAMA = os.environ.get("USE_OLLAMA", "1") == "1"
OLLAMA_URL = os.environ.get(
    "OLLAMA_URL", os.environ.get("OLLAMA_ENDPOINT", "http://127.0.0.1:11434")
)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

# Generation parameters
OLLAMA_TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.8"))
OLLAMA_MAX_TOKENS = int(os.environ.get("OLLAMA_MAX_TOKENS", "800"))
OLLAMA_TOP_P = float(os.environ.get("OLLAMA_TOP_P", "0.9"))
OLLAMA_TOP_K = int(os.environ.get("OLLAMA_TOP_K", "40"))
OLLAMA_REPEAT_PENALTY = float(os.environ.get("OLLAMA_REPEAT_PENALTY", "1.1"))
OLLAMA_CONTEXT_LENGTH = int(os.environ.get("OLLAMA_CONTEXT_LENGTH", "4096"))

# Timeout settings
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "30"))
OLLAMA_CONNECT_TIMEOUT = int(os.environ.get("OLLAMA_CONNECT_TIMEOUT", "10"))
OLLAMA_READ_TIMEOUT = int(os.environ.get("OLLAMA_READ_TIMEOUT", "60"))

# Debug settings
OLLAMA_DEBUG = os.environ.get("OLLAMA_DEBUG", "false").lower() == "true"
OLLAMA_VERBOSE = os.environ.get("OLLAMA_VERBOSE", "false").lower() == "true"


def is_up(timeout=None):
    """Check if Ollama service is available"""
    if not USE_OLLAMA:
        log.info("Ollama is disabled via USE_OLLAMA environment variable")
        return False

    if requests is None:
        log.warning("requests library not available, cannot check Ollama status")
        return False

    timeout = timeout or OLLAMA_CONNECT_TIMEOUT
    try:
        r = requests.get(
            f"{OLLAMA_URL}/api/tags", timeout=pick_timeout(timeout, ci_default=2)
        )
        if OLLAMA_DEBUG:
            log.debug(f"Ollama health check response: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        if OLLAMA_VERBOSE:
            log.warning(f"Ollama health check failed: {e}")
        return False


def gen(prompt: str, temperature=None, max_tokens=None):
    """Generate text using Ollama with configurable parameters"""
    if not USE_OLLAMA:
        log.info("Ollama is disabled, returning fallback response")
        return f"Ollama disabled - fallback response at {
            time.strftime('%Y-%m-%d %H:%M:%S')
        }"

    if requests is None:
        log.warning("requests library not available, using fallback response")
        return f"Runtime showcase generated at {
            time.strftime('%Y-%m-%d %H:%M:%S')}."

    # Use provided parameters or fall back to environment defaults
    temp = temperature if temperature is not None else OLLAMA_TEMPERATURE
    tokens = max_tokens if max_tokens is not None else OLLAMA_MAX_TOKENS

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temp,
                    "num_predict": tokens,
                    "top_p": OLLAMA_TOP_P,
                    "top_k": OLLAMA_TOP_K,
                    "repeat_penalty": OLLAMA_REPEAT_PENALTY,
                    "num_ctx": OLLAMA_CONTEXT_LENGTH,
                },
            },
            timeout=OLLAMA_READ_TIMEOUT,
        )

        if OLLAMA_DEBUG:
            log.debug(
                f"Ollama generation request: model={OLLAMA_MODEL}, temp={temp}, tokens={tokens}"
            )

        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("response", "")

            if OLLAMA_VERBOSE:
                log.info(
                    f"Ollama generation successful: {
                        len(generated_text)} characters"
                )

            return generated_text
        else:
            log.error(
                f"Ollama generation failed with status {
                    response.status_code}"
            )
            return f"Generation failed - fallback response at {
                time.strftime('%Y-%m-%d %H:%M:%S')
            }"

    except Exception as e:
        log.warning(f"Ollama generation error: {e}")
        return f"Runtime showcase generated at {
            time.strftime('%Y-%m-%d %H:%M:%S')}."
