# dicter

[![Python](https://img.shields.io/pypi/pyversions/dicter)](https://img.shields.io/pypi/pyversions/dicter)
[![Pypi](https://img.shields.io/pypi/v/dicter)](https://pypi.org/project/dicter/)
[![Docs](https://img.shields.io/badge/Sphinx-Docs-Green)](https://erdogant.github.io/dicter/)
[![LOC](https://sloc.xyz/github/erdogant/dicter/?category=code)](https://github.com/erdogant/dicter/)
[![Downloads](https://static.pepy.tech/personalized-badge/dicter?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month)](https://pepy.tech/project/dicter)
[![Downloads](https://static.pepy.tech/personalized-badge/dicter?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/dicter)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/dicter/blob/master/LICENSE)
[![Forks](https://img.shields.io/github/forks/erdogant/dicter.svg)](https://github.com/erdogant/dicter/network)
[![Issues](https://img.shields.io/github/issues/erdogant/dicter.svg)](https://github.com/erdogant/dicter/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![DOI](https://zenodo.org/badge/228166657.svg)](https://zenodo.org/badge/latestdoi/228166657)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg?logo=github%20sponsors)](https://erdogant.github.io/dicter/pages/html/Documentation.html#colab-notebook)
![GitHub Repo stars](https://img.shields.io/github/stars/erdogant/dicter)
![GitHub repo size](https://img.shields.io/github/repo-size/erdogant/dicter)
[![Donate](https://img.shields.io/badge/Support%20this%20project-grey.svg?logo=github%20sponsors)](https://erdogant.github.io/dicter/pages/html/Documentation.html#)
<!---[![BuyMeCoffee](https://img.shields.io/badge/buymea-coffee-yellow.svg)](https://www.buymeacoffee.com/erdogant)-->
<!---[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)-->


* ``dicter`` is Python package with dictionary functions:

	* Traverse through nested dicts to retrieve key-path.
	* Set value in dictionary using key-path
	* Get value in dictionary using key-path.
	* Flattens dicts.
	* Compare two dicts.
	* Store and load in json.



# 
**Star this repo if you like it! ⭐️**
#

## Documentation

* [**dicter documentation pages (Sphinx)**](https://erdogant.github.io/dicter/)

* <a href="https://erdogant.github.io/dicter/"> <img src="https://img.shields.io/badge/Sphinx-Docs-Green" alt="Open documentation pages"/> </a> dicter documentation pages 


## Installation
* Install dicter from PyPI (recommended). dicter is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* A new environment can be created as following:


```bash
pip install -U dicter
```

* Alternatively, you can install from the GitHub source:
```bash
# Directly install from github source
pip install git+https://github.com/erdogant/dicter
```

## Examples

#### Import dicter package
```python
import dicter as dt
```

#### Traverse all paths in dictionary.
```python
import dicter as dt
 # Example dict:
d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
# Walk through dict to get all paths
paths = dt.path(d)

print(paths)
# [[['level_a'], 1],
# [['level_c'], 3],
# [['level_e'], 2],
# [['level_b', 'a'], 'hello world'],
# [['level_d', 'a'], 1],
# [['level_d', 'b'], 2],
# [['level_d', 'c', 'e'], 10]]
```

#### Get value from dictionary using nested keys.
```python
# Import dicter
import dicter as dt

# Example dictionary
d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
# Get the value for the nested path for:
value = dt.get_nested(d, key_path=["level_b", "a"])
print(value)
# 'hello world'

```

#### Set value from dictionary using nested keys.
```python
# Import dicter
import dicter as dt

# Example: New path and value in dictionary.
d = {}
key_path = ['person', 'address', 'city']
dt.set_nested(d, key_path, 'New York')
# Print updated dictionary
print(d)
# {'person': {'address': {'city': 'New York'}}}

```

#### Set value from dictionary using nested keys.
```python
# Import dicter
import dicter as dt

# Example dict
d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
# Flatten dictionary
dflat = dt.flatten(d)

print(d_flat)

# [['level_a', 1],
#  ['a', 'hello world'],
#  ['level_c', 3],
#  ['a', 1],
#  ['b', 2],
#  ['e', 10],
#  ['level_e', 2]]
 
```


#### Depth of dictionary.
```python
# Import dicter
import dicter as dt

d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
n = dt.depth(d)

```

#### Compare dictionary.
```python
# Import dicter
import dicter as dt

Example: Add
d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 'new in d2'}
d2 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
out = dt.compare(d1, d2)
print(out)

Example: Remove
d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
d2 = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 'new in d2'}
out = dt.compare(d1, d2)
print(out)

Example: Modified
d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
d2 = {'level_a': 1, 'level_b': {'a': 'modified'}}
out = dt.compare(d1, d2)
print(out['modified'])

```

#### Save and load dictionary.
```python

# Import dicter
import dicter as dt

d = {'level_a': None, 'level_b': {'a': 'hello world'}, 'level_c': True, 'level_d': 2.3, 'level_e': [[1,2,3], [1,2]]}
filepath='c:/temp/test/dicter_save.json'

# First save
dt.save(d, filepath=filepath, overwrite=True)

# Load
d = dt.load(filepath)
```

## General

#### References
* https://github.com/erdogant/dicter

#### Citation
Please cite in your publications if this is useful for your research (see citation).
   
### Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)

### Contribute
* All kinds of contributions are welcome!
* If you wish to buy me a <a href="https://www.buymeacoffee.com/erdogant">Coffee</a> for this work, it is very appreciated :)

### Licence
See [LICENSE](LICENSE) for details.
