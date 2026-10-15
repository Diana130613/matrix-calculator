from matrix import Matrix


class MatrixCalculator:
    """Калькулятор для выполнения операций над матрицами."""

    @staticmethod
    def add(first, second):
        return first.add(second)

    @staticmethod
    def subtract(first, second):
        return first.subtract(second)

    @staticmethod
    def multiply(first, second):
        return first.multiply(second)

    @staticmethod
    def transpose(matrix):
        return matrix.transpose()

    @staticmethod
    def determinant(matrix):
        return matrix.determinant()