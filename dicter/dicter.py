import os
import logging
import json
from functools import reduce
from operator import getitem
import re
import pandas as pd
import numpy as np
from tqdm import tqdm

logger = logging.getLogger('')
for handler in logger.handlers[:]:
    logger.removeHandler(handler)
console = logging.StreamHandler()
formatter = logging.Formatter('[dicter] >%(levelname)s> %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
logger = logging.getLogger()
logger.setLevel(20)


# %%
def is_key(d: dict, path: list) -> bool:
    """Check whether the dictionary contains the key.

    Parameters
    ----------
    d : dict
        Input dictionary.
    path : list
        The nested path of keys in a ordered list.
        Example: ['level 1', 'level 2']

    Returns
    -------
    Bool
        True: Key exists.
        False: Key does not exist.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> # Example dictionary
    >>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
    >>> #
    >>> # Get the value for the nested path for:
    >>> value = dt.is_key(d, ["level_b","a"])
    """

    if not isinstance(d, dict):
        raise AttributeError('is_key() expects dict as first argument.')
    if not isinstance(path, list):
        raise AttributeError('is_key() expects at least two arguments, one given.')

    _d = d
    for key in path:
        try:
            _d = _d[key]
        except KeyError:
            return False
    return True


# %% Get nested item from dictionary
def to_df(d: dict, sep: str = '_', verbose: [str, int] = 'info') -> pd.DataFrame():
    """Convert to dataFrame.

    Parameters
    ----------
    d : dict
        Input dictionary.
    sep : str, default is '->'
        The seperator should be unique and is used to normalize the dictionary.

    Returns
    -------
    None.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> # Example 1
    >>> d = {'Person 1': {'Country': 'NL', 'Income': {'Amsterdam': 100, 'The Haque': 50}, 'Age': 33, 'Type': 'bicycle'},
             'Person 2': {'Country': 'USA', 'Income': {'NY': 150, 'The Haque': 50}, 'Age': 23, 'Type': 'Taxi'},
             'Person 3': {'Country': 'DE', 'Income': {'BE': 90}, 'Age': 43, 'Type': 'Car'} }
    >>> #
    >>> # Convert to DataFrame
    >>> df = dt.to_df(d)
    >>> #
    >>> #
    >>> # Example 2
    >>> d = {'Country': 'NL', 'Weight': {'Amsterdam': 100, 'The Haque': 50}, 'Age': 33}
    >>> df = dt.to_df(d)
    >>> #

    """
    if not isinstance(d, dict): raise Exception('Input should be of type dict.')
    # Set the logger
    set_logger(verbose)

    # If no keys in dict > return
    if len(d.keys())==0:
        logger.debug('Empty DataFrame returned.')
        return pd.DataFrame()

    # Start with emtpy list to append all dataframes.
    dfs=[]
    for key in tqdm(d.keys(), disable=disable_tqdm()):
        if isinstance(d[key], dict):
            dlist = np.array(traverse(d[key], sep=sep, keys_as_list=False, verbose=verbose))
            dfs = dfs + [pd.DataFrame(data=dlist[:, 1], columns=[key], index=dlist[:, 0])]

    # Concat all dfs
    if len(dfs)>0:
        df = pd.concat(dfs, axis=1)
    else:
        dlist = np.array(traverse(d, sep=sep, keys_as_list=False, verbose=verbose))
        df = pd.DataFrame(data=dlist[:, 1], index=dlist[:, 0])
        df.columns = df.columns.astype(str)
    return df


# %% Get nested item from dictionary
def get_nested(d: dict, path: list):
    """Get nested value from dictionary.

    Parameters
    ----------
    d : dict
        Input dictionary.
    path : list
        The nested path of keys in a ordered list.
        Example: ['level 1', 'level 2']

    Returns
    -------
    value : string or numerical
        * value belonging to the key.
        * None: if the path does not exists.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> # Example dictionary
    >>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
    >>> # Get the value for the nested path for:
    >>> value = dt.get_nested(d, ["level_a"])
    >>> print(value)  # 1
    >>> #
    >>> # Get the value for the nested path for:
    >>> value = dt.get_nested(d, ["level_b","a"])
    >>> print(value)  # hello world
    >>> #
    >>> # Get the value for the nested path for:
    >>> value = dt.get_nested(d, ["level_d","c", "e"])
    >>> print(value)  # 10
    >>> #
    >>> # Get the value for the nested path for a list:
    >>> l = [[[1,2,3],[10,20,30]]]
    >>> value = dt.get_nested(l, [0,1,2])    # =>>> 30
    >>> print(value)  # 30

    """
    value = None
    try:
        value = reduce(getitem, path, d)
    except:
        pass

    return value


# %%
def set_nested(d: dict, path: list, value: str) -> dict:
    """Set nested value in dictionary.

    Parameters
    ----------
    d : dict
        Input dictionary.
    path : list
        The nested path of keys in a ordered list.
    value : str
        The value that needs to be set.

    Returns
    -------
    Dictionary is updated without a return.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> # Example: New path and value in dictionary.
    >>> d = {}
    >>> path = ['person', 'address', 'city']
    >>> dt.set_nested(d, path, 'New York')
    >>> # Print updated dictionary
    >>> print(d)
    >>> # {'person': {'address': {'city': 'New York'}}}
    >>> #
    >>> # Example: Update value in path.
    >>> d = {'person': {'address': {'city': 'New York'}}}
    >>> path = ['person', 'address', 'city']
    >>> dt.set_nested(d, path, 'Amsterdam')
    >>> # Print updated dictionary
    >>> print(d)
    >>> # {'person': {'address': {'city': 'Amsterdam'}}, 'person_2': {'address': {'city': 'Amsterdam'}}}
    >>> #
    >>> # Example: New path with value.
    >>> d = {'person': {'address': {'city': 'New York'}}}
    >>> path = ['person_2', 'address', 'city']
    >>> dt.set_nested(d, path, 'Amsterdam')
    >>> # Print updated dictionary
    >>> print(d)
    >>> # {'person': {'address': {'city': 'New York'}}, 'person_2': {'address': {'city': 'Amsterdam'}}}

    """
    for k in path[:-1]:
        d = d.setdefault(k, {})
    d[path[-1]] = value


# %% Traverse all paths in dictionary.
def traverse(d: dict, sep: str = '$->$', keys_as_list: bool = True, verbose: [str, int] = 'info') -> list:
    """Traverse through all paths in dictionary.

    Parameters
    ----------
    d : dict
        Input dictionary.
    sep : str, default is '$->$'
        The seperator should be unique and is used to normalize the dictionary.
        Change the sep in case a string exists with such pattern in the input dictionary.
    keys_as_list : bool, default is True
        True: Output is structured list with keys.
        False: Output is list with keys seperated with the "sep" string.
    verbose : int, default is 'info' or 20
        Set the verbose messages using string or integer values.
            * [0, None, 'silent', 'off', 'no']: No message.
            * [10, 'debug']: Messages from debug level and higher.
            * [20, 'info']: Messages from info level and higher.
            * [30, 'warning']: Messages from warning level and higher.
            * [40, 'critical']: Messages from critical level and higher.

    Returns
    -------
    dic : list
        list containing two columns: [[key], value].

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> Example dict
    >>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
    >>> # Traverse all paths in dictionary
    >>> dlist = dt.traverse(d)
    >>> #
    >>> print(dlist)
    >>> # [[['level_a'], 1],
    >>> # [['level_c'], 3],
    >>> # [['level_e'], 2],
    >>> # [['level_b', 'a'], 'hello world'],
    >>> # [['level_d', 'a'], 1],
    >>> # [['level_d', 'b'], 2],
    >>> # [['level_d', 'c', 'e'], 10]]
    >>> #
    >>> # Example to retrieve value from a dictionary
    >>> value = dt.get_nested(d, dlist[3])
    >>> # Look up for ['level_b', 'a']
    >>> print(value)  # hello world

    """
    set_logger(verbose)
    # Normalize the dictionary
    df = pd.json_normalize(d, sep=sep)
    dic = df.to_dict(orient='records')[0]
    # Get items
    dic = [*dic.items()]
    # First row is the path of keys, second row the value.
    if keys_as_list:
        dic = list(map(lambda x: [x[0].split(sep)] + [x[1]], dic))
    # Return
    logger.info("[%d] paths traversed." %(len(dic)))
    return dic


# %% Flatten dict to deepest level of key->value
def flatten(d: dict):
    """Flatten dictionary to the deepest level and return key-value.

    Parameters
    ----------
    d : dict
        Input dictionary.

    Returns
    -------
    d_flatten : list
        Flattened dictionary containing key and value.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> # Example dict
    >>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
    >>> # Flatten dictionary
    >>> dflat = dt.flatten(d)
    >>> #
    >>> print(d_flat)

    """
    def _flatten(d: dict, dflat: list = []):
        for k, v in d.items():
            if isinstance(v, dict):
                # print (k,":",v)
                _flatten(v, dflat=dflat)
            else:
                # print (k,":",v)
                dflat.append([k, v])
        return dflat

    # Run inner function to avoid accidental increasing of the output list.
    return _flatten(d)


# %% Depth of dict.
def depth(d: dict):
    """Depth of dictionary.

    Parameters
    ----------
    d : dict
        Input dictionary.

    Returns
    -------
    depth: int
        Depth of dictionary.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> Example dict
    >>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
    >>> n = dt.depth(d)

    """
    if isinstance(d, dict):
        return 1 + (max(map(depth, d.values())) if d else 0)

    return 0


# %% Compare two dictionaries.
def compare(d1: dict, d2: dict):
    """Compare two dictionaries.

    The second dictionary is compared with the first one, and results are shown accordingly.

    Parameters
    ----------
    d1 : dict
        Dictionary.
    d2 : dict
        Dictionary.

    Returns
    -------
    added : list
        added keys in d1 compared with d2.
    removed : list
        Removed keys in d1 compared with d2.
    modified : list
        Modified keys in d1 compared with d2.
    same : list
        Similar keys in d1 compared with d2.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> Example: Add
    >>> d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 'new in d2'}
    >>> d2 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
    >>> out = dt.compare(d1, d2)
    >>> print(out)
    >>> #
    >>> Example: Remove
    >>> d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
    >>> d2 = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 'new in d2'}
    >>> out = dt.compare(d1, d2)
    >>> print(out)
    >>> #
    >>> Example: Modified
    >>> d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
    >>> d2 = {'level_a': 1, 'level_b': {'a': 'modified'}}
    >>> out = dt.compare(d1, d2)
    >>> print(out['modified'])
    >

    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    # Some cleaning
    added=None if len(added)==0 else list(added)
    removed=None if len(removed)==0 else list(removed)
    modified=None if len(modified)==0 else list(modified)
    same=None if len(same)==0 else list(same)
    return {'added': added, 'removed': removed, 'modified': modified, 'similar': same}


# %% Save
def save(d: dict, filepath: str, overwrite: bool = False, verbose: [str, int] = 'info'):
    """Save dictionary to json.

    Parameters
    ----------
    d : dict
        Dictionary.
    filepath : str
        File path to store the dictionary.
    overwrite : bool, default: False
        True: Overwrite if file exists.
        False: Do not overwrite existing files.
    verbose : int, default is 'info' or 20
        Set the verbose messages using string or integer values.
            * 0, None, 'silent', 'off', 'no': No message.
            * 10,'debug': Messages from debug level and higher.
            * 20,'info': Messages from info level and higher.
            * 30,'warning': Messages from warning level and higher.
            * 40,'critical': Messages from critical level and higher.

    Returns
    -------
    writeok : bool
        True: Succesful writing to json on disk.
        False: Nothing is written to disk.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >
    >>> d = {'level_a': None, 'level_b': {'a': 'hello world'}, 'level_c': True, 'level_d': 2.3, 'level_e': [[1,2,3], [1,2]]}
    >>> dt.save(d, filepath='c:/temp/test/dicter_save.json', overwrite=True)

    """
    # Set the logger
    set_logger(verbose)
    writeok = False
    # Check filepath and extension. Add .json if not exists.
    filepath = _check_filepath(filepath)

    # Dump to json when allowed to overwrite or if the file not exists yet.
    if overwrite or (not os.path.isfile(filepath)):
        if os.path.isfile(filepath): os.remove(filepath)
        with open(filepath, "w") as f:
            json.dump(d, f)
        if logger is not None: logger.info('Saved: [%s]' %(filepath))
        writeok=True
    elif os.path.isfile(filepath):
        logger.warning('Could not write [%s]. File already exists.' %(filepath))

    # Return
    return writeok


# %% Load
def load(filepath: str, verbose: [str, int] = 'info'):
    """Load dictionary from json file.

    Parameters
    ----------
    filepath : str
        path location to json.
    verbose : str, optional
        Set the verbose messages using string or integer values.
            * [0, None, 'silent', 'off', 'no']: No message.
            * [10, 'debug']: Messages from debug level and higher.
            * [20, 'info']: Messages from info level and higher.
            * [30, 'warning']: Messages from warning level and higher.
            * [40, 'critical']: Messages from critical level and higher.

    Returns
    -------
    dictionary : dict
        None or Dictionary.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> d = {'level_a': None, 'level_b': {'a': 'hello world'}, 'level_c': True, 'level_d': 2.3, 'level_e': [[1,2,3], [1,2]]}
    >>> filepath='c:/temp/test/dicter_save.json'
    >>> # First save
    >>> dt.save(d, filepath=filepath, overwrite=True)
    >>> # Load
    >>> d = dt.load(filepath)

    """
    d = None
    if os.path.isfile(filepath):
        with open(filepath) as json_file:
            d = json.load(json_file)
        logger.info('File loaded.')
    else:
        logger.warning('File not found: %s' %(filepath))
    return d


# %%
def update(dictionary, key_to_update, new_value):
    """Update a nested dictionary for a specific key with a new value.

        Parameters
        ----------
        dictionary : dict
            The nested dictionary to update.
        key_to_update : str
            The key to update.
        new_value : any
            The new value to assign to the specified key.

        Examples
        --------
        >>> data_dict_template = {
        ...     'DEPARTURE': {
        ...         'SLOPE': 3,
        ...         'INTERSECTION': 'V4',
        ...         'TORA': '1234',
        ...         'CIRCUIT_ALTITUDE': '1000',
        ...         'TOWER': '122.108',
        ...         'alignment': 'concrete'
        ...     }
        ... }
        >>> update(data_dict_template['DEPARTURE'], 'SLOPE', 5)
        >>> data_dict_template['DEPARTURE']['SLOPE']
        5

        >>> update(data_dict_template['DEPARTURE'], 'INTERSECTION', 'V5')
        >>> data_dict_template['DEPARTURE']['INTERSECTION']
        'V5'

        >>> update(data_dict_template['DEPARTURE'], 'TORA', '2000')
        >>> data_dict_template['DEPARTURE']['TORA']
        '2000'

        >>> update(data_dict_template['DEPARTURE'], 'CIRCUIT_ALTITUDE', '1500')
        >>> data_dict_template['DEPARTURE']['CIRCUIT_ALTITUDE']
        '1500'

        >>> update(data_dict_template['DEPARTURE'], 'TOWER', '122.109')
        >>> data_dict_template['DEPARTURE']['TOWER']
        '122.109'

        >>> update(data_dict_template['DEPARTURE'], 'alignment', 'asphalt')
        >>> data_dict_template['DEPARTURE']['alignment']
        'asphalt'

    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            update(value, key_to_update, new_value)
        elif key == key_to_update:
            dictionary[key] = new_value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    update(item, key_to_update, new_value)
                    if key_to_update in item:
                        item[key_to_update] = new_value


# %%
def set_logger(verbose: [str, int] = 'info'):
    """Set the logger for verbosity messages.

    Parameters
    ----------
    verbose : [str, int], default is 'info' or 20
        Set the verbose messages using string or integer values.
            * [10, 'debug']: Messages from debug level and higher.
            * [20, 'info']: Messages from info level and higher.
            * [30, 'warning']: Messages from warning level and higher.
            * [50, 'critical']: Messages from critical level and higher.
            * [60, 0, None, 'silent', 'off', 'no']: No message.

    Returns
    -------
    None.

    Examples
    --------
    >>> # Set the logger to warning
    >>> set_logger(verbose='warning')
    >>> # Test with different messages
    >>> logger.debug("Hello debug")
    >>> logger.info("Hello info")
    >>> logger.warning("Hello warning")
    >>> logger.critical("Hello critical")

    """
    # Set 0 and None as no messages.
    if (verbose==0) or (verbose is None):
        verbose=60
    # Convert str to levels
    if isinstance(verbose, str):
        levels = {'silent': 60,
                  'off': 60,
                  'no': 60,
                  'debug': 10,
                  'info': 20,
                  'warning': 30,
                  'critical': 50}
        verbose = levels[verbose]

    logger.setLevel(verbose)


# %%
def disable_tqdm():
    """Set the logger for verbosity messages."""
    return (True if (logger.getEffectiveLevel()>=30) else False)


# %%
def mkdir(dirpath):
    """Create directory."""
    if not os.path.isdir(dirpath):
        logger.info('Path created: [%s]' %(dirpath))
        os.makedirs(dirpath, exist_ok=True)


# %%
def clean_filename(name):
    """Clean filename."""
    return re.sub(r'[ |&|,|?|$|!|/|\\]', r'_', name)


# %%
def _check_filepath(filepath):
    dirpath, filename = os.path.split(filepath)
    # Clean filename
    filename = clean_filename(filename)
    # Add json if required
    if filename[-5:]!='.json':
        filename=filename + '.json'
        logger.info('[%s] -> .json added to filename' %(filename))
    # Create dir if required
    mkdir(dirpath)
    # Return
    return os.path.abspath(os.path.join(dirpath, filename))
