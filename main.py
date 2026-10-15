import tkinter as tk
from tkinter import messagebox

from matrix import Matrix
from calculator import MatrixCalculator


class MatrixCalculatorApp:
    """Графическое приложение матричного калькулятора."""

    def __init__(self, root):
        self.root = root
        self.root.title("Матричный калькулятор")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Матричный калькулятор",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        left_frame = tk.Frame(input_frame)
        left_frame.grid(row=0, column=0, padx=20)

        right_frame = tk.Frame(input_frame)
        right_frame.grid(row=0, column=1, padx=20)

        tk.Label(
            left_frame,
            text="Матрица A"
        ).pack()

        self.matrix_a = tk.Text(
            left_frame,
            width=25,
            height=10
        )
        self.matrix_a.pack()

        tk.Label(
            right_frame,
            text="Матрица B"
        ).pack()

        self.matrix_b = tk.Text(
            right_frame,
            width=25,
            height=10
        )
        self.matrix_b.pack()

        operations_frame = tk.Frame(self.root)
        operations_frame.pack(pady=10)

        tk.Button(
            operations_frame,
            text="A + B",
            width=12,
            command=self.add
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            operations_frame,
            text="A - B",
            width=12,
            command=self.subtract
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            operations_frame,
            text="A × B",
            width=12,
            command=self.multiply
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            operations_frame,
            text="det(A)",
            width=12,
            command=self.determinant
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            operations_frame,
            text="Aᵀ",
            width=12,
            command=self.transpose
        ).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            operations_frame,
            text="Очистить",
            width=12,
            command=self.clear
        ).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(
            self.root,
            text="Результат:"
        ).pack()

        self.result = tk.Text(
            self.root,
            width=55,
            height=8
        )
        self.result.pack(pady=10)

    def parse_matrix(self, text):
        """Преобразование текста в объект Matrix."""

        lines = text.strip().splitlines()

        if not lines:
            raise ValueError("Матрица не заполнена.")

        data = []

        for line in lines:
            values = line.split()

            try:
                row = [float(value) for value in values]
            except ValueError:
                raise ValueError(
                    "Матрица должна содержать только числа."
                )

            data.append(row)

        return Matrix(data)

    def get_matrices(self):
        matrix_a = self.parse_matrix(
            self.matrix_a.get("1.0", tk.END)
        )

        matrix_b = self.parse_matrix(
            self.matrix_b.get("1.0", tk.END)
        )

        return matrix_a, matrix_b

    def show_result(self, matrix):
        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, str(matrix))

    def show_message(self, message):
        messagebox.showerror("Ошибка", message)

    def add(self):
        try:
            a, b = self.get_matrices()
            result = MatrixCalculator.add(a, b)
            self.show_result(result)
        except ValueError as error:
            self.show_message(str(error))

    def subtract(self):
        try:
            a, b = self.get_matrices()
            result = MatrixCalculator.subtract(a, b)
            self.show_result(result)
        except ValueError as error:
            self.show_message(str(error))

    def multiply(self):
        try:
            a, b = self.get_matrices()
            result = MatrixCalculator.multiply(a, b)
            self.show_result(result)
        except ValueError as error:
            self.show_message(str(error))

    def determinant(self):
        try:
            a = self.parse_matrix(
                self.matrix_a.get("1.0", tk.END)
            )

            result = MatrixCalculator.determinant(a)

            self.result.delete("1.0", tk.END)
            self.result.insert(tk.END, str(result))
        except ValueError as error:
            self.show_message(str(error))

    def transpose(self):
        try:
            a = self.parse_matrix(
                self.matrix_a.get("1.0", tk.END)
            )

            result = MatrixCalculator.transpose(a)
            self.show_result(result)
        except ValueError as error:
            self.show_message(str(error))

    def clear(self):
        self.matrix_a.delete("1.0", tk.END)
        self.matrix_b.delete("1.0", tk.END)
        self.result.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    app = MatrixCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()