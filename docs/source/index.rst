clizard's documentation!
========================

|python| |pypi| |docs| |stars| |LOC| |downloads_month| |downloads_total| |license| |forks| |open issues| |project status| |DOI| |repo-size|

-----------------------------------

*clizard* — Python library by erdogant.


Clizard is a lightweight Python toolkit that automates the creation and management of command‑line interfaces (CLIs). It assumes most CLI applications share common options—verbosity, configuration file paths, help flags—and generates these automatically with minimal boilerplate around `argparse`. Developers can focus on business logic while still delivering a polished user experience. The library provides utilities to build parsers (`build_parser`), auto‑generate rich‑based chat CLIs (`auto_cli`, `GenericCLI`), load and merge configuration files (`load_clizard_file`, `ensure_clizard_file`), and expose settings via a JSON‑backed store (`Config`). It also supports decorator‑style command registration (`@command`) for slash commands, automatic type casting of CLI arguments, and helper functions to locate main modules or Snakemake config files. Clizard’s goal is to streamline CLI development, reduce repetitive code, and enable consistent, maintainable interfaces across Python projects.


.. code-block:: console

   pip install clizard

-----------------------------------


Content
=======

.. toctree::
   :maxdepth: 1
   :caption: Installation

   Installation


.. toctree::
   :maxdepth: 1
   :caption: Summary

   Summary


.. toctree::
   :maxdepth: 1
   :caption: Examples

   Examples


.. toctree::
   :maxdepth: 1
   :caption: FAQ

   FAQ


.. toctree::
   :maxdepth: 1
   :caption: Configuration

   configuration


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |python| image:: https://img.shields.io/pypi/pyversions/clizard.svg
    :alt: Python
    :target: https://erdogant.github.io/clizard/

.. |pypi| image:: https://img.shields.io/pypi/v/clizard.svg
    :alt: PyPI version
    :target: https://pypi.org/project/clizard/

.. |docs| image:: https://img.shields.io/badge/Sphinx-Docs-blue.svg
    :alt: Sphinx documentation
    :target: https://erdogant.github.io/clizard/

.. |stars| image:: https://img.shields.io/github/stars/erdogant/clizard
    :alt: Stars
    :target: https://github.com/erdogant/clizard

.. |LOC| image:: https://sloc.xyz/github/erdogant/clizard/?category=code
    :alt: lines of code
    :target: https://github.com/erdogant/clizard

.. |downloads_month| image:: https://static.pepy.tech/personalized-badge/clizard?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month
    :alt: Downloads per month
    :target: https://pepy.tech/project/clizard

.. |downloads_total| image:: https://static.pepy.tech/personalized-badge/clizard?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads
    :alt: Downloads in total
    :target: https://pepy.tech/project/clizard

.. |license| image:: https://img.shields.io/badge/license-MIT-green.svg
    :alt: License
    :target: https://github.com/erdogant/clizard/blob/master/LICENSE

.. |forks| image:: https://img.shields.io/github/forks/erdogant/clizard.svg
    :alt: Github Forks
    :target: https://github.com/erdogant/clizard/network

.. |open issues| image:: https://img.shields.io/github/issues/erdogant/clizard.svg
    :alt: Open Issues
    :target: https://github.com/erdogant/clizard/issues

.. |project status| image:: http://www.repostatus.org/badges/latest/active.svg
    :alt: Project Status
    :target: http://www.repostatus.org/#active

.. |DOI| image:: https://zenodo.org/badge/246504758.svg
    :alt: Cite
    :target: https://zenodo.org/badge/latestdoi/246504758

.. |repo-size| image:: https://img.shields.io/github/repo-size/erdogant/clizard
    :alt: repo-size
    :target: https://github.com/erdogant/clizard


.. include:: add_bottom.add
