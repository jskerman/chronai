from importlib.metadata import version

from . import common, core, parsers, szn, types

__all__ = ["szn", "common", "core", "parsers", "types"]

__version__ = version("chronai")
