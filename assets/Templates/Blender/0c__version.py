# This file must be kept very simple, because it is consumed from several
# places -- it is imported by h11/__init__.py, execfile'd by setup.py, etc.

# We use a simple scheme:
#   100 -> 100+dev -> 110 -> 110+dev
# where the +dev versions are never released into the wild, they're just what
# we stick into the VCS in between releases.
#
# This is compatible with PEP 440:
#   http://legacy.python.org/dev/peps/pep-440/
# via the use of the "local suffix" "+dev", which is disallowed on index
# servers and causes 100+dev to sort after plain 100, which is what we
# want. (Contrast with the special suffix 100dev, which sorts *before*
# 100.)

__version__ = "160"
