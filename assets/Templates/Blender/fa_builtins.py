from future.utils import PY3

if PY3:
    pass
else:
    __future_module__ = True
    # Overwrite any old definitions with the equivalent future.builtins ones:
