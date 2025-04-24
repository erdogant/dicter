import unittest
import dicter as dt
import pandas as pd
import numpy as np
import unittest

class TestIs_key(unittest.TestCase):
    def test_is_key(self):

        data = {
            "level1": {
                "level2": {
                    "level3": "Well..",
                    "sausages": "level1 level2 and level1",
                    "level1": "does not have much level1 in it"
                }
            }
        }

        self.assertEqual(dt.is_key(data, ["level1"]), True)
        self.assertEqual(dt.is_key(data, ["level1", "level3"]), False)
        self.assertEqual(dt.is_key(data, ["level1", "level2"]), True)
        self.assertEqual(dt.is_key(data, ["level1", "level2", "level3"]), True)


class TestTraverse(unittest.TestCase):
    def test_traverse(self):
        # Test input of type dict
        d = {'a': 1, 'b': 2}
        traversed_list = dt.traverse(d)
        self.assertIsInstance(traversed_list, list)
        self.assertEqual(traversed_list, [[['a'], 1], [['b'], 2]])

        # Test input of type dict with nested dict
        d = {'a': {'b': 1, 'c': 2}, 'd': {'e': 3, 'f': 4}}
        traversed_list = dt.traverse(d)
        self.assertIsInstance(traversed_list, list)
        self.assertEqual(traversed_list, [[['a', 'b'], 1], [['a', 'c'], 2], [['d', 'e'], 3], [['d', 'f'], 4]])

        # Test input of type dict with sep
        d = {'a': 1, 'b': 2}
        traversed_list = dt.traverse(d, sep='_')
        self.assertIsInstance(traversed_list, list)
        self.assertEqual(traversed_list, [[['a'], 1], [['b'], 2]])

        # Test input of type dict with keys_as_list = False
        d = {'a': {'b': 1, 'c': 2}, 'd': {'e': 3, 'f': 4}}
        traversed_list = dt.traverse(d, keys_as_list=False, sep='_')
        self.assertIsInstance(traversed_list, list)
        self.assertEqual(traversed_list, [('a_b', 1), ('a_c', 2), ('d_e', 3), ('d_f', 4)])
        

class TestToDf(unittest.TestCase):
    def test_to_df(self):
        # Test input of type dict
        d = {'a': 1, 'b': 2}
        df = dt.to_df(d)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(list(df.index), ['a', 'b'])

        # Test input of type dict with nested dict
        d = {'a': {'b': 1, 'c': 2}, 'd': {'e': 3, 'f': 4}}
        df = dt.to_df(d)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(list(df.columns), ['a', 'd'])
        self.assertEqual(list(df.index), ['b', 'c', 'e', 'f'])
        self.assertEqual(df.loc['b', 'a'], '1')
        self.assertEqual(df.loc['c', 'a'], '2')
        self.assertEqual(df.loc['e', 'd'], '3')
        self.assertEqual(df.loc['f', 'd'], '4')
        self.assertEqual(df.loc['c', 'a'], '2')
        self.assertEqual(list(df.values.ravel()), ['1', np.nan, '2', np.nan, np.nan, '3', np.nan, '4'])

        # Test input of empty dict
        d = {}
        df = dt.to_df(d)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.empty, True)

        # Test input of type list
        d = [1, 2, 3]
        self.assertRaises(Exception, dt.to_df, d)

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
        path = ['person', 'address', 'city']
        dt.set_nested(d, path, 'New York')
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

    def test_set_traverse(self):
        d = {'level_a': 1, 'level_b': {'a': 'hello world'}, 'level_c': 3, 'level_d': {'a': 1, 'b': 2, 'c': {'e': 10}}, 'level_e': 2}
        # Traverse all paths in dictionary
        paths = dt.traverse(d)
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

if __name__ == '__main__':
    unittest.main()
