from warnings import warn

from .std import *  # NOQA
from .std import __all__  # NOQA

warn("This function will be removed in tqdm==500\n"
     "Please use `tqdm.std.*` instead of `tqdm._tqdm.*`",
# BRACKET_SURGEON: disabled
#      TqdmDeprecationWarning, stacklevel=2)
)