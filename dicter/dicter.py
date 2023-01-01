# --------------------------------------------------
# Name        : dicter.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : https://github.com/erdogant/dicter
# Licence     : See licences
# --------------------------------------------------

import os
import logging
import json
from functools import reduce
from operator import getitem
import re
import pandas as pd

logger = logging.getLogger('')
for handler in logger.handlers[:]:  # get rid of existing old handlers
    logger.removeHandler(handler)
console = logging.StreamHandler()
# formatter = logging.Formatter('[%(asctime)s] [dicter]> %(levelname)s> %(message)s', datefmt='%H:%M:%S')
formatter = logging.Formatter('[dicter] >%(levelname)s> %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
logger = logging.getLogger()
logger.setLevel(20)


# %% Get nested item from dictionary
def get_nested(d: dict, key_path: list):
    """Get nested value from dictionary.

    Parameters
    ----------
    d : dict
        Input dictionary.
    key_path : list
        The nested path of keys in a ordered list.

    Returns
    -------
    value : string or numerical
        * value belonging to the key.
        * None: if the key_path does not exists.

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> # Example dictionary
    >>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
    >>> # Get the value for the nested path for:
    >>> value = dt.get_nested(d, key_path=["level_a"])
    >>> print(value)  # 1
    >>> #
    >>> # Get the value for the nested path for:
    >>> value = dt.get_nested(d, key_path=["level_b","a"])
    >>> print(value)  # hello world
    >>> #
    >>> # Get the value for the nested path for:
    >>> value = dt.get_nested(d, key_path=["level_d","c", "e"])
    >>> print(value)  # 10
    >>> #
    >>> # Get the value for the nested path for a list:
    >>> l = [[[1,2,3],[10,20,30]]]
    >>> value = dt.get_nested(l, key_path=[0,1,2])    # =>>> 30
    >>> print(value)  # 30

    """
    value = None
    try:
        value = reduce(getitem, key_path, d)
    except:
        pass

    return value


# %%
def set_nested(d: dict, key_path: list, value: str) -> dict:
    """Set nested value in dictionary.

    Parameters
    ----------
    d : dict
        Input dictionary.
    key_path : list
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
    >>> key_path = ['person', 'address', 'city']
    >>> dt.set_nested(d, key_path, 'New York')
    >>> # Print updated dictionary
    >>> print(d)
    >>> # {'person': {'address': {'city': 'New York'}}}
    >>> #
    >>> # Example: Update value in path.
    >>> d = {'person': {'address': {'city': 'New York'}}}
    >>> key_path = ['person', 'address', 'city']
    >>> dt.set_nested(d, key_path, 'Amsterdam')
    >>> # Print updated dictionary
    >>> print(d)
    >>> # {'person': {'address': {'city': 'Amsterdam'}}, 'person_2': {'address': {'city': 'Amsterdam'}}}
    >>> #
    >>> # Example: New path with value.
    >>> d = {'person': {'address': {'city': 'New York'}}}
    >>> key_path = ['person_2', 'address', 'city']
    >>> dt.set_nested(d, key_path, 'Amsterdam')
    >>> # Print updated dictionary
    >>> print(d)
    >>> # {'person': {'address': {'city': 'New York'}}, 'person_2': {'address': {'city': 'Amsterdam'}}}

    """
    for k in key_path[:-1]:
        d = d.setdefault(k, {})
    d[key_path[-1]] = value


# %% Traverse all paths in dictionary.
def path(d: dict, sep: str = '$->$', keys_as_list: bool = True, verbose: [str, int] = 'info') -> list:
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
        list containing two columns: [[key_path, value]].

    Examples
    --------
    >>> # Import dicter
    >>> import dicter as dt
    >>> #
    >>> Example dict
    >>> d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
    >>> # Traverse all paths in dictionary
    >>> paths = dt.path(d)
    >>> #
    >>> print(paths)
    >>> # [[['level_a'], 1],
    >>> # [['level_c'], 3],
    >>> # [['level_e'], 2],
    >>> # [['level_b', 'a'], 'hello world'],
    >>> # [['level_d', 'a'], 1],
    >>> # [['level_d', 'b'], 2],
    >>> # [['level_d', 'c', 'e'], 10]]
    >>> #
    >>> # Example to retrieve value from a dictionary using key path
    >>> key_paths = list(map(lambda x: x[0], paths))
    >>> value = dt.get_nested(d, key_paths[3])  # ['level_b', 'a']
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
        for k,v in d.items():        
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

    Description
    -----------
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
            * [0, None, 'silent', 'off', 'no']: No message.
            * [10, 'debug']: Messages from debug level and higher.
            * [20, 'info']: Messages from info level and higher.
            * [30, 'warning']: Messages from warning level and higher.
            * [40, 'critical']: Messages from critical level and higher.

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
    # Check filepath
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
def load(filepath: str, verbose: str = 'info'):
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

    # Show examples
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
