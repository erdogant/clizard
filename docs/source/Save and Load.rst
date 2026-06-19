
Save and Load
''''''''''''''

Saving and loading models is desired as the learning proces of a model for ``clizard`` can take up to hours.
In order to accomplish this, we created two functions: function :func:`clizard.save` and function :func:`clizard.load`
Below we illustrate how to save and load models.


Saving
----------------

Saving a learned model can be done using the function :func:`clizard.save`:

.. code:: python

    import clizard

    # Load example data
    X,y_true = clizard.load_example()

    # Learn model
    model = clizard.fit_transform(X, y_true, pos_label='bad')

    Save model
    status = clizard.save(model, 'learned_model_v1')



Loading
----------------------

Loading a learned model can be done using the function :func:`clizard.load`:

.. code:: python

    import clizard

    # Load model
    model = clizard.load(model, 'learned_model_v1')

