.. _code_directive:

-------------------------------------

Save and Load
''''''''''''''

Saving and loading models is desired as the learning proces of a model for ``dicter`` can take up to hours.
In order to accomplish this, we created two functions: function :func:`dicter.save` and function :func:`dicter.load`
Below we illustrate how to save and load models.


Saving
----------------

Saving a learned model can be done using the function :func:`dicter.save`:

.. code:: python

    import dicter

    # Load example data
    X,y_true = dicter.load_example()

    # Learn model
    model = dicter.fit_transform(X, y_true, pos_label='bad')

    Save model
    status = dicter.save(model, 'learned_model_v1')



Loading
----------------------

Loading a learned model can be done using the function :func:`dicter.load`:

.. code:: python

    import dicter

    # Load model
    model = dicter.load(model, 'learned_model_v1')

.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>
