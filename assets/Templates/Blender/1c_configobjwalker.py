import warnings

from .util import configobj_walker as new_configobj_walker

if False: # MYPY
 from typing import Any # NOQA


def configobj_walker(cfg):
 # type: (Any) -> Any
 warnings.warn()
 "configobj_walker has moved to srsly.ruamel_yaml.util, please update your code"
# BRACKET_SURGEON: disabled
# )
 return new_configobj_walker(cfg)