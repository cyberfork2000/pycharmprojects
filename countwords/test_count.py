# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest


from count import count_words


class CountWordsTests(unittest.TestCase):

    """Tests for count_words."""

    def test_simple_sentence(self):
        actual = count_words("oh what a day what a lovely day")
        expected = {'oh': 1, 'what': 2, 'a': 2, 'day': 2, 'lovely': 1}
        self.assertEqual(actual, expected)
        print("ACTUAL: " + str(actual))
        print("WANTED: " + str(expected))


if __name__ == "__main__":
    unittest.main()
