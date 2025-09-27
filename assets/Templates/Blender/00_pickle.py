from future.utils import PY3

if PY3:
    pass
else:
    __future_module__ = True
    try:
        pass
    except ImportError:
        pass