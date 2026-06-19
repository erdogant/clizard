"""clizard.

Name        : clizard.py
Author      : Erdogan Taskesen
Contact     : erdogant@gmail.com
github      : https://github.com/erdogant/clizard
Licence     : See licences

"""
# from . import utils

from tqdm import tqdm
import datazets as dz
import os
import requests

import logging
logger = logging.getLogger(__name__)
# if not logger.hasHandlers(): logging.basicConfig(level=logging.INFO, format='[{asctime}] [{name}] [{levelname}] {message}', style='{', datefmt='%d-%m-%Y %H:%M:%S')

# %%
class clizard():
    """clizard."""

    def __init__(self, method='xgboost'):
        """Initialize clizard with user-defined parameters.

        Parameters
        ----------
        method : str, default='xgboost'
            Method selection:
            - xgboost
            - catboost

        Returns
        -------
        object.

        Examples
        --------
        >>> from clizard import clizard
        >>> model = clizard()
        >>> clizard.plot()
        >>>

        References
        ----------
            * https://erdogant.github.io/clizard
            * https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.goodness_of_fit.html

        """
        self.method=method

    def plot(self):
        logger.info(f'Make plot implementation for {self.method}')

    def import_example(self, data='titanic', url=None, sep=','):
        """Import example dataset from github source.

        Import one of the few datasets from github source or specify your own download url link.

        Parameters
        ----------
        data : str
            Name of datasets: 'sprinkler', 'titanic', 'student', 'fifa', 'cancer', 'waterpump', 'retail'
        url : str
            url link to to dataset.

        Returns
        -------
        pd.DataFrame()
            Dataset containing mixed features.

        References
        ----------
            * https://github.com/erdogant/datazets

        """
        return dz.get(data=data, url=url, sep=sep)

# %% Verbosity
def get_logger():
    return logger.getEffectiveLevel()

def disable_tqdm():
    """Set the logger for verbosity messages."""
    return (True if (logger.getEffectiveLevel()>=30) else False)


# %% Retrieve files files.
class wget:
    """Retrieve file from url."""

    def filename_from_url(url, ext=True):
        """Return filename."""
        urlname = os.path.basename(url)
        if not ext: _, ext = os.path.splitext(urlname)
        return urlname

    def download(url, writepath):
        """Download.

        Parameters
        ----------
        url : str.
            Internet source.
        writepath : str.
            Directory to write the file.

        Returns
        -------
        None.

        """
        writepath = str(writepath)
        logger.info(f'Downloading {wget.filename_from_url(url)}')
        r = requests.get(url, stream=True)
        filepath = os.path.join(writepath, wget.filename_from_url(url))
        with open(filepath, "wb") as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)

# %% Main
if __name__ == "__main__":
    import clizard as clizard
