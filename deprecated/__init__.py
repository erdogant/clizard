from .core import GenericCLI
from .config import Config
from .cli_args import parse_args, build_parser, auto_cli
import logging

__all__ = ["GenericCLI", "Config", "parse_args", "build_parser", "auto_cli"]

__author__ = 'Erdogan Taskesen'
__email__ = 'erdogant@gmail.com'
__version__ = "0.1.0"

# Setup package-level logger
_logger = logging.getLogger('clizard')
_log_handler = logging.StreamHandler()
_formatter = logging.Formatter(fmt='[{asctime}] [{name:<12.12}] [{levelname:<8}] {message}', style='{', datefmt='%d-%m-%Y %H:%M:%S')
_log_handler.setFormatter(_formatter)
_log_handler.setLevel(logging.DEBUG)
if not _logger.hasHandlers():  # avoid duplicate handlers if re-imported
    _logger.addHandler(_log_handler)
_logger.setLevel(logging.DEBUG)
_logger.propagate = True  # allow submodules to inherit this handler


# module level doc-string
__doc__ = """
clizard
=====================================================================

clizard creates command line interfaces arround main files.

Example
-------
>>> # Install
>>> pip install clizard
>>> # From the terminal run:
>>> clizard
>>>


References
----------
https://github.com/erdogant/clizard

"""
