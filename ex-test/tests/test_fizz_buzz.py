import unittest
from coe import fizzbuzz


class FizzBuzzTest(unittest.TestCase):
    def test_give_3_get_Fizz(self):
        num = 3
        result = fizzbuzz.fizzbuzz(num)
        self.assertEqual(result, "Fizz")

    def test_give_5_get_Buzz(self):
        num = 5
        result = fizzbuzz.fizzbuzz(num)
        self.assertEqual(result, "Buzz")

    def test_give_15_get_FizzBuzz(self):
        num = 15
        result = fizzbuzz.fizzbuzz(num)
        self.assertEqual(result, "FizzBuzz")

    def test_give_9_get_Fizz(self):
        num = 9
        result = fizzbuzz.fizzbuzz(num)
        self.assertEqual(result, "Fizz")

    def test_give_10_get_Buzz(self):
        num = 10
        result = fizzbuzz.fizzbuzz(num)
        self.assertEqual(result, "Buzz")

    def test_give_45_get_FizzBuzz(self):
        num = 45
        result = fizzbuzz.fizzbuzz(num)
        self.assertEqual(result, "FizzBuzz")
