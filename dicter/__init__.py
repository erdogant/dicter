from dicter.dicter import (
    set_nested,
    get_nested,
    traverse,
    flatten,
    depth,
    compare,
    save,
    load,
    to_df,
    clean_filename,
    is_key,
    set_logger)


__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.5'

# module level doc-string
__doc__ = """
dicter
=====================================================================

Description
-----------
dicter is a Python package with advanced dictionary functions:
	* Traverse through nested dicts to retrieve key-path.
	* Set value in dictionary using path.
	* Get value in dictionary using path.
	* Flattens dicts.
	* Compare two dicts.
	* Store and load in json.
    
Example
-------
>>> # Import dicter
>>> import dicter as dt
>>>
>>> # Example dict
>>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
>>>
>>> # Get values using nested key
>>> dt.get_nested(d, ['level_b', 'a'])
>>>
>>> # Set value using nested key
>>> dt.set_nested(d, ['level_b', 'a'], 'Amsterdam')
>>>
>>> # Traverse all paths in dictionary
>>> paths = dt.traverse(d)
>>>
>>> # Flatten
>>> fdict = dt.flatten(d)
>>>
>>> # Depth
>>> depth = dt.depth(d)
>>>
>>> # Compare
>>> results = dt.compare(d, d)
>>>
>>> # To dataframe
>>> results = dt.to_df(d)
>>>
>>> # save
>>> dt.save('./test_dict.json', d)
>>>
>>> # load
>>> d = dt.save('./test_dict.json')
>>>

References
----------
* https://github.com/erdogant/dicter
* https://erdogant.github.io/dicter/

"""
