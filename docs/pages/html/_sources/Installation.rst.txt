.. include:: add_top.add

Installation
################

Create environment
**********************

If desired, install ``dicter`` from an isolated Python environment using conda:

.. code-block:: python

    conda create -n env_dicter python=3.10
    conda activate env_dicter


Pypi
**********************

.. code-block:: console

    # Install from Pypi:
    pip install dicter

    # Force update to latest version
    pip install -U dicter


Github source
************************************

.. code-block:: console

    # Install directly from github
    pip install git+https://github.com/erdogant/dicter


Uninstalling
################

Remove environment
**********************

.. code-block:: console

   # List all the active environments. dicter should be listed.
   conda env list

   # Remove the dicter environment
   conda env remove --name dicter

   # List all the active environments. dicter should be absent.
   conda env list


Remove installation
**********************

Note that the removal of the environment will also remove the ``dicter`` installation.

.. code-block:: console

    # Install from Pypi:
    pip uninstall dicter



.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>




.. include:: add_bottom.add