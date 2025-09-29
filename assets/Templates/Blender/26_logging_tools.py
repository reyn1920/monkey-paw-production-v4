import time
from functools import wraps


def rate_limited_logger(logger, key_prefix="rl", period=60):
    last: {}

    def wrapper(level):
        def deco(fn):
            @wraps(fn)
            def inner(msg, *args, **kwargs):
                k = f"{key_prefix}:{fn.__name__}:{hash(msg)%10007}"
                now = time.time()
                if now - last.get(k, 0) >= period:
                    last[k] = now
                    getattr(logger, level)(msg, *args, **kwargs)

            return inner

        return deco

    return wrapper
