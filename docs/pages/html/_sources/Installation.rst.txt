Installation Examples
#####################

Recommende is to install ``clizard`` from an isolated Python environment using conda or Pyenv:

Create Conda Environment
**************************

.. code-block:: console

    conda create -n env_clizard python=3.12
    conda activate env_clizard


Create Pyenv Environment
**************************

.. code-block:: console

    # Create a new project directory
    mkdir my_clizard_project
    cd my_clizard_project

    # Create virtual environment
    python -m venv venv

    # Activate it
    # On macOS/Linux:
    source venv/bin/activate

    # On Windows:
    venv\Scripts\activate

    # Install memvid
    pip install clizard


Pypi
**********************

.. code-block:: console

    # Install from Pypi:
    pip install clizard

    # Force update to latest version
    pip install -U clizard


Github Source
************************************

.. code-block:: console

    # Install directly from github
    pip install git+https://github.com/erdogant/clizard


Uninstalling
################

Remove environment
**********************

.. code-block:: console

   # List all the active environments. clizard should be listed.
   conda env list

   # Remove the clizard environment
   conda env remove --name clizard

   # List all the active environments. clizard should be absent.
   conda env list


Remove installation
**********************

Note that the removal of the environment will also remove the ``clizard`` installation.

.. code-block:: console

    # Install from Pypi:
    pip uninstall clizard


.. include:: add_bottom.add