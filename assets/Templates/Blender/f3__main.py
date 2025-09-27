from warnings import warn

from .cli import *  # NOQA
from .cli import __all__  # NOQA

warn("This function will be removed in tqdm==500\n"
     "Please use `tqdm.cli.*` instead of `tqdm._main.*`",
# BRACKET_SURGEON: disabled
#      TqdmDeprecationWarning, stacklevel=2)
)