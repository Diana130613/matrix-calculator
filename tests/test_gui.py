"""Тесты интерфейса матричного калькулятора.

Запуск: python -m unittest tests.test_gui -v
Для создания виджетов нужна графическая сессия.
"""
import tkinter as tk
import unittest
from unittest.mock import patch

from main import MatrixCalculatorApp


def buttons(widget):
    """Найти кнопки приложения по их подписям."""
    found = {}
    for child in widget.winfo_children():
        if isinstance(child, tk.Button):
            found[child.cget("text")] = child
        found.update(buttons(child))
    return found


class TestGuiScenarios(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.addCleanup(self.root.destroy)
        self.root.withdraw()
        self.app = MatrixCalculatorApp(self.root)
        self.controls = buttons(self.root)
        self.app.matrix_a.insert("1.0", "1 2\n3 4")
        self.app.matrix_b.insert("1.0", "5 6\n7 8")
        self.dialog_patch = patch("main.messagebox.showerror")
        self.dialog = self.dialog_patch.start()
        self.addCleanup(self.dialog_patch.stop)
        self.callback_errors = []
        self.root.report_callback_exception = lambda *args: self.callback_errors.append(args[1])

    def click(self, label):
        self.controls[label].invoke()
        self.assertEqual(self.callback_errors, [], "Ошибка обработчика кнопки")

    def read_result(self):
        return self.app.result.get("1.0", "end-1c")

    def check_operation(self, label, expected):
        self.click(label)
        self.assertEqual(self.read_result(), expected)
        self.dialog.assert_not_called()

    def test_01_add(self):
        """Сложение двух матриц"""
        self.check_operation("A + B", "6.0 8.0\n10.0 12.0")

    def test_02_subtract(self):
        """Вычитание двух матриц"""
        self.check_operation("A - B", "-4.0 -4.0\n-4.0 -4.0")

    def test_03_multiply(self):
        """Умножение двух матриц"""
        self.check_operation("A × B", "19.0 22.0\n43.0 50.0")

    def test_04_determinant(self):
        """Определитель матрицы A"""
        self.check_operation("det(A)", "-2.0")

    def test_05_transpose(self):
        """Транспонирование матрицы A"""
        self.check_operation("Aᵀ", "1.0 3.0\n2.0 4.0")

    def test_06_invalid_input(self):
        """Буква вместо числа"""
        self.app.matrix_a.delete("1.0", tk.END)
        self.app.matrix_a.insert("1.0", "1 x\n3 4")
        self.click("A + B")
        self.dialog.assert_called_once_with(
            "Ошибка", "Матрица должна содержать только числа."
        )
        self.assertEqual(self.read_result(), "")

    def test_07_clear(self):
        """Очистка заполненных полей"""
        self.check_operation("A + B", "6.0 8.0\n10.0 12.0")
        self.click("Очистить")
        for field in (self.app.matrix_a, self.app.matrix_b, self.app.result):
            self.assertEqual(field.get("1.0", "end-1c"), "")
        self.dialog.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
