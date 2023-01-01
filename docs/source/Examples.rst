Quickstart
################

A quick example how to learn a model on a given dataset.


.. code:: python

    # Import library
    import dicter

    # Retrieve URLs of malicous and normal urls:
    X, y = dicter.load_example()

    # Learn model on the data
    model = dicter.fit_transform(X, y, pos_label='bad')

    # Plot the model performance
    results = dicter.plot(model)



Learn new model with gridsearch and train-test set
################################################################

AAA

.. code:: python

    # Import library
    import dicter

    # Load example data set    
    X,y_true = dicter.load_example()

    # Retrieve URLs of malicous and normal urls:
    model = dicter.fit_transform(X, y_true, pos_label='bad', train_test=True, gridsearch=True)

    # The test error will be shown
    results = dicter.plot(model)


Learn new model on the entire data set
################################################

BBBB


.. code:: python

    # Import library
    import dicter

    # Load example data set    
    X,y_true = dicter.load_example()

    # Retrieve URLs of malicous and normal urls:
    model = dicter.fit_transform(X, y_true, pos_label='bad', train_test=False, gridsearch=True)

    # The train error will be shown. Such results are heavily biased as the model also learned on this set of data
    results = dicter.plot(model)


.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>
