import logging

# from datazets import get as import_example

from clizard.clizard import clizard

# from clizard.clizard import (
    # import_example,
    # )


__author__ = 'Erdogan Taskesen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.0'

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

clizard is for...

Example
-------
>>> from clizard import clizard
>>> model = clizard()
>>> clizard.plot()

References
----------
https://github.com/erdogant/clizard

"""
