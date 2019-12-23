import unittest
from fizzbuzz import fizz_buzz


class TestFizzBuzz(unittest.TestCase):
    def test_3_is_fizz(self):
        self.assertEqual(fizz_buzz(3), 'Fizz')

    def test_5_is_buzz(self):
        self.assertEqual(fizz_buzz(5), 'Buzz')

    def test_15_is_fizz_buzz(self):
        self.assertEqual(fizz_buzz(15), 'FizzBuzz')

    def test_1_is_1(self):
        self.assertEqual(fizz_buzz(1), 1)

    def test_2_is_2(self):
        self.assertEqual(fizz_buzz(2), 2)

    def test_6_is_fizz(self):
        self.assertEqual(fizz_buzz(6), 'Fizz')

    def test_10_is_buzz(self):
        self.assertEqual(fizz_buzz(10), 'Buzz')

    def test_30_is_fizz_buzz(self):
        self.assertEqual(fizz_buzz(30), 'FizzBuzz')


if __name__ == '__main__':
    unittest.main()
