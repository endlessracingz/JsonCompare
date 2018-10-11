import os
import json
import unittest

from jsoncompare.ignore import Ignore


class IgnoreTestCase(unittest.TestCase):
    obj = None
    rules = None
    transformed = None

    def setUp(self):
        curr_dir = os.path.dirname(__file__)
        with open('{}/{}'.format(curr_dir, 'data/rules.json'), 'r') as fp:
            self.rules = json.load(fp)
        with open('{}/{}'.format(curr_dir, 'data/expected.json'), 'r') as fp:
            self.obj = json.load(fp)
        with open('{}/{}'.format(curr_dir, 'data/transformed.json'), 'r') as fp:
            self.transformed = json.load(fp)

    def test_ignore_with_listable_rules(self):
        obj = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4
        }
        rules = [
            'a',
            'd',
            'e',
        ]

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, {
            'b': 2,
            'c': 3,
        })

    def test_ignore_with_dictable_rules(self):
        obj = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
        }
        rules = {
            'a': '*',
            'd': '*',
            'e': '*'
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, {
            'b': 2,
            'c': 3,
        })

    def test_ignore_with_sub_rule(self):
        obj = {
            'a': {
                'a': 1,
                'b': 2,
                'c': 3,
                'd': 4,
            },
            'b': {
                'a': {
                    'a': 1,
                    'b': 2,
                },
                'b': 2,
                'c': 3,
                'd': 4,
            },
            'c': 3,
            'd': 4,
        }
        rules = {
            'a': [
                'b',
                'd',
            ],
            'b': {
                'a': [
                    'a',
                ],
                'b': '*',
                'd': '*',
            },
            'd': '*',
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, {
            'a': {
                'a': 1,
                'c': 3,
            },
            'b': {
                'a': {
                    'b': 2,
                },
                'c': 3,
            },
            'c': 3,
        })

    def test_ignore_with_values_key(self):
        obj = [
            1,
            2,
            3,
            4,
        ]
        rules = {
            '_values': [
                1,
                3,
            ],
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, [
            2,
            4,
        ])

    def test_ignore_with_list_key(self):
        obj = [
            {
                'a': 1,
                'b': 2,
                'c': 3,
            },
            {
                'a': 4,
                'b': 5,
                'c': 6,
            },
        ]
        rules = {
            '_list': [
                'a',
                'c',
            ]
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, [
            {
                'b': 2,
            },
            {
                'b': 5,
            },
        ])

    def test_super(self):
        obj = Ignore.transform(self.obj, self.rules)
        self.assertEqual(obj, self.transformed)


if __name__ == '__main__':
    unittest.main()
