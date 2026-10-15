import unittest

from matrix import Matrix
from calculator import MatrixCalculator


class TestMatrixCalculator(unittest.TestCase):

    def test_add(self):
        a = Matrix([
            [1, 2],
            [3, 4]
        ])

        b = Matrix([
            [5, 6],
            [7, 8]
        ])

        result = MatrixCalculator.add(a, b)

        expected = Matrix([
            [6, 8],
            [10, 12]
        ])

        self.assertEqual(result.data, expected.data)

    def test_subtract(self):
        a = Matrix([
            [5, 6],
            [7, 8]
        ])

        b = Matrix([
            [1, 2],
            [3, 4]
        ])

        result = MatrixCalculator.subtract(a, b)

        expected = Matrix([
            [4, 4],
            [4, 4]
        ])

        self.assertEqual(result.data, expected.data)

    def test_multiply(self):
        a = Matrix([
            [1, 2],
            [3, 4]
        ])

        b = Matrix([
            [5, 6],
            [7, 8]
        ])

        result = MatrixCalculator.multiply(a, b)

        expected = Matrix([
            [19, 22],
            [43, 50]
        ])

        self.assertEqual(result.data, expected.data)

    def test_transpose(self):
        a = Matrix([
            [1, 2, 3],
            [4, 5, 6]
        ])

        result = MatrixCalculator.transpose(a)

        expected = Matrix([
            [1, 4],
            [2, 5],
            [3, 6]
        ])

        self.assertEqual(result.data, expected.data)

    def test_determinant(self):
        a = Matrix([
            [1, 2],
            [3, 4]
        ])

        result = MatrixCalculator.determinant(a)

        self.assertEqual(result, -2)

    # тесты ошибок
    def test_add_different_sizes(self):
        a = Matrix([
            [1, 2],
            [3, 4]
        ])

        b = Matrix([
            [1, 2, 3]
        ])

        with self.assertRaises(ValueError):
            MatrixCalculator.add(a, b)

    def test_multiply_incompatible_matrices(self):
        a = Matrix([
            [1, 2],
            [3, 4]
        ])

        b = Matrix([
            [1, 2]
        ])

        with self.assertRaises(ValueError):
            MatrixCalculator.multiply(a, b)

    def test_determinant_non_square_matrix(self):
        a = Matrix([
            [1, 2, 3],
            [4, 5, 6]
        ])

        with self.assertRaises(ValueError):
            MatrixCalculator.determinant(a)


if __name__ == "__main__":
    unittest.main()