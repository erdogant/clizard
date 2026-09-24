clizard's documentation!
========================

|python| |pypi| |docs| |stars| |LOC| |downloads_month| |downloads_total| |license| |forks| |open issues| |project status| |DOI| |repo-size|

-----------------------------------

*clizard* — Python library by erdogant.


**clizard** is a lightweight Python toolkit that wraps any existing Python project in a rich, interactive terminal interface — with no changes to your existing code required.

Point ``clizard`` at a repository root and it automatically discovers your project's ``main()`` function, extracts its arguments (from the function signature or an internal ``argparse`` parser), and launches a guided shell with settings persistence, a setup wizard, and one-click execution. Developers get a polished user experience; their colleagues get a tool they can actually run without reading the docs.

Key capabilities:

* **Auto-discovery** — finds ``main()`` by scanning for named entry files, argument-handling patterns, and ``__name__`` guards
* **Argument extraction** — reads keyword parameters directly from the signature, or AST-parses internal ``ArgumentParser`` blocks
* **Settings persistence** — saves and restores configuration between sessions via ``.clizard/settings.json``
* **Interactive shell** — built-in slash commands: ``/wizard``, ``/run``, ``/settings``, ``/reset``, ``/install``, ``/docs``, ``/help``
* **Scaffold generation** — ``/scaffold`` (or ``clizardmake``) bakes settings into a standalone ``clizard_main.py``
* **Snakemake support** — detects ``Snakefile`` config directives and exposes workflow parameters as editable settings
* **Customisable identity** — app name, ASCII art, accent colour, and tips menu via ``.clizard/meta.json``


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
