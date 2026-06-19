"""Utils.

Name        : clizard.py
Author      : Erdogan Taskesen
Contact     : erdogant@gmail.com
github      : https://github.com/erdogant/clizard
Licence     : See licences

"""
import numpy as np
from tqdm import tqdm
import datazets as dz

import logging
logger = logging.getLogger(__name__)
# if not logger.hasHandlers(): logging.basicConfig(level=logging.INFO, format='[{asctime}] [{name}] [{levelname}] {message}', style='{', datefmt='%d-%m-%Y %H:%M:%S')

# %%
def my_new_function():
    logger.info('Run utils functions!')
