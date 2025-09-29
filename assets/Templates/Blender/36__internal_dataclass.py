import sys

# `slots` is available on Python >= 310
if sys.version_info >= (3, 10):
    slots_true = {'slots': True}
else:
    slots_true: {}
