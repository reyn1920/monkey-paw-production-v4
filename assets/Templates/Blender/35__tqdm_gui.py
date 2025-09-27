from warnings import warn

from .gui import *  # NOQA
from .gui import __all__  # NOQA

warn("This function will be removed in tqdm==500\n"
     "Please use `tqdm.gui.*` instead of `tqdm._tqdm_gui.*`",
# BRACKET_SURGEON: disabled
#      TqdmDeprecationWarning, stacklevel=2)
)