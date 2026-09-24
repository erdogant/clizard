Installation
=============


.. note::

   Latest release: ``0.2.3``

.. note::

   Source code: `clizard on GitHub <https://github.com/erdogant/clizard.git>`_

.. tip::

   Documentation: `https://erdogant.github.io/clizard/ <https://erdogant.github.io/clizard/>`_


Create environment
******************

.. code-block:: console

   conda create -n env_clizard python=3.12
   conda activate env_clizard


Install from PyPI
*****************

.. code-block:: console

   pip install clizard

   # Force update to the latest version
   pip install -U clizard


Install from GitHub
*******************

.. code-block:: console

   pip install git+https://github.com/erdogant/clizard.git

   # Install a specific branch
   pip install git+https://github.com/erdogant/clizard.git@main


Verify the installation
***********************

After installation two console entry points are available:

.. code-block:: console

   # Launch the interactive shell in the current directory
   clizard

   # Generate a standalone clizard_main.py for the current project
   clizardmake

You can confirm the installed version from Python:

.. code-block:: python

   import clizard
   print(clizard.__version__)
   # 0.2.3


Dependencies
************

clizard depends on:

* `rich <https://github.com/Textualize/rich>`_ — terminal styling, panels, spinners, tables
* `tomllib` (Python 3.11+) or `tomli` — reading ``pyproject.toml`` metadata

Optional dependencies used for Snakemake integration:

* `pyyaml <https://pyyaml.org/>`_ — reading ``config.yaml`` workflow files


Uninstall
=========

Remove environment
******************

.. code-block:: console

   conda env list
   conda env remove --name env_clizard
   conda env list


Remove package
**************

.. code-block:: console

   pip uninstall clizard



.. include:: add_bottom.add
