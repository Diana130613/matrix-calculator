class Matrix:
    """Класс для представления матрицы и выполнения операций над ней."""

    def __init__(self, data):
        if not data:
            raise ValueError("Матрица не может быть пустой.")

        if not all(isinstance(row, list) for row in data):
            raise ValueError("Матрица должна быть двумерным списком.")

        columns = len(data[0])

        if columns == 0:
            raise ValueError("Матрица не может иметь нулевое количество столбцов.")

        if not all(len(row) == columns for row in data):
            raise ValueError("Все строки матрицы должны иметь одинаковую длину.")

        self.data = data

    @property
    def rows(self):
        return len(self.data)

    @property
    def cols(self):
        return len(self.data[0])

    def add(self, other):
        """Сложение двух матриц."""

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Для сложения матрицы должны иметь одинаковый размер."
            )

        result = [
            [
                self.data[i][j] + other.data[i][j]
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

        return Matrix(result)

    def subtract(self, other):
        """Вычитание двух матриц."""

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Для вычитания матрицы должны иметь одинаковый размер."
            )

        result = [
            [
                self.data[i][j] - other.data[i][j]
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]

        return Matrix(result)

    def multiply(self, other):
        """Умножение двух матриц."""

        if self.cols != other.rows:
            raise ValueError(
                "Количество столбцов первой матрицы "
                "должно совпадать с количеством строк второй."
            )

        result = []

        for i in range(self.rows):
            row = []

            for j in range(other.cols):
                value = 0

                for k in range(self.cols):
                    value += self.data[i][k] * other.data[k][j]

                row.append(value)

            result.append(row)

        return Matrix(result)

    def transpose(self):
        """Транспонирование матрицы."""

        result = [
            [
                self.data[i][j]
                for i in range(self.rows)
            ]
            for j in range(self.cols)
        ]

        return Matrix(result)

    def determinant(self):
        """Вычисление определителя квадратной матрицы."""

        if self.rows != self.cols:
            raise ValueError(
                "Определитель можно вычислить только для квадратной матрицы."
            )

        if self.rows == 1:
            return self.data[0][0]

        if self.rows == 2:
            return (
                self.data[0][0] * self.data[1][1]
                - self.data[0][1] * self.data[1][0]
            )

        result = 0

        for column in range(self.cols):
            minor = [
                [
                    self.data[i][j]
                    for j in range(self.cols)
                    if j != column
                ]
                for i in range(1, self.rows)
            ]

            sign = (-1) ** column
            result += sign * self.data[0][column] * Matrix(minor).determinant()

        return result

    def __str__(self):
        return "\n".join(
            " ".join(str(value) for value in row)
            for row in self.data
        )