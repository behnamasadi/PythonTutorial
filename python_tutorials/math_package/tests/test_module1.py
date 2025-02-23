import unittest
from math_package.algebra import mean, sum_numbers


class TestAlgebra(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean(2, 4), 3)
        self.assertEqual(mean(10, 20), 15)

    def test_sum_numbers(self):
        self.assertEqual(sum_numbers(1, 2, 3), 6)
        self.assertEqual(sum_numbers(5, 5, 5, 5), 20)


if __name__ == "__main__":
    unittest.main()
