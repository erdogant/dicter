import unittest
import dicter as dt

class Testdicter(unittest.TestCase):

    def test_get_nested(self):
        d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
        assert dt.get_nested(d, ['level_a'])==1
        assert dt.get_nested(d, ['level_b', 'a'])=='hello world'
        assert dt.get_nested(d, ['level_c'])==3
        assert dt.get_nested(d, ['level_d', 'a'])==1
        assert dt.get_nested(d, ['level_d', 'b'])==2
        assert dt.get_nested(d, ['level_d', 'c', 'e'])==10
        assert dt.get_nested(d, ['level_e'])==2

    def test_set_nested(self):
        d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
        assert dt.get_nested(d, ['level_b', 'a'])=='hello world'
        value = 'Amsterdam'
        dt.set_nested(d, ['level_b', 'a'], value)
        assert dt.get_nested(d, ['level_b', 'a'])==value

        # Example: New path and value in dictionary.
        d = {}
        key_path = ['person', 'address', 'city']
        dt.set_nested(d, key_path, 'New York')
        assert str(d)=="{'person': {'address': {'city': 'New York'}}}"

        # Example: Update value in path.
        d = {'person': {'address': {'city': 'New York'}}}
        assert str(d)=="{'person': {'address': {'city': 'New York'}}}"
        dt.set_nested(d, ['person', 'address', 'city'], 'Amsterdam')
        assert str(d)=="{'person': {'address': {'city': 'Amsterdam'}}}"

        # Example: New path with value.
        d = {'person': {'address': {'city': 'New York'}}}
        assert str(d)=="{'person': {'address': {'city': 'New York'}}}"
        dt.set_nested(d, ['person_2', 'address', 'city'], 'Amsterdam')
        assert str(d)=="{'person': {'address': {'city': 'New York'}}, 'person_2': {'address': {'city': 'Amsterdam'}}}"

    def test_set_path(self):
        d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
        # Traverse all paths in dictionary
        paths = dt.path(d)
        assert str(paths)=="[[['level_a'], 1], [['level_c'], 3], [['level_e'], 2], [['level_b', 'a'], 'hello world'], [['level_d', 'a'], 1], [['level_d', 'b'], 2], [['level_d', 'c', 'e'], 10]]"

    def test_set_flatten(self):
        d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
        # Flatten dictionary
        assert str(dt.flatten(d))=="[['level_a', 1], ['a', 'hello world'], ['level_c', 3], ['a', 1], ['b', 2], ['e', 10], ['level_e', 2]]"

    def test_set_depth(self):
        d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
        assert dt.depth(d)==3
        assert dt.depth({})==1
        assert dt.depth(None)==0
        d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_e': 2}
        assert dt.depth(d)==2

    def test_set_compare(self):
        # Example: Add
        d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 'new in d1'}
        # d2 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
        # results = dt.compare(d1, d2)
        # # assert str(results)=="{'added': ['level_c'], 'removed': None, 'modified': None, 'similar': ['level_b', 'level_a']}"
        # # assert results['added'] is None
        # assert results['added'][0]=='level_c'
        # assert results['removed'] is None
        # assert results['modified'] is None
        # assert results['similar'][0]=='level_b'
        # assert results['similar'][1]=='level_a'
        # assert results['modified']['level_b'][0]['a']=='hello world'
        # assert results['modified']['level_b'][1]['a']=='modified'
        # Example: Remove
        d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
        d2 = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 'new in d2'}
        assert str(dt.compare(d1, d2))=="{'added': None, 'removed': ['level_c'], 'modified': None, 'similar': ['level_b', 'level_a']}"
        # Example: Modified
        d1 = {'level_a': 1, 'level_b': {'a': 'hello world'}}
        d2 = {'level_a': 1, 'level_b': {'a': 'modified'}}
        assert str(dt.compare(d1, d2))=="{'added': None, 'removed': None, 'modified': ['level_b'], 'similar': ['level_a']}"
