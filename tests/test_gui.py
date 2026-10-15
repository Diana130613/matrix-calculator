"""ЛР 2: сценарии через настоящие виджеты Tkinter и команды кнопок.

Диалоги showerror перехватываются, чтобы проверка не ожидала ручного
закрытия окна. Создание, отображение и закрытие самого диалога здесь
не проверяются. Для запуска требуется доступная графическая сессия.
"""
import tkinter as tk
import unittest
from unittest.mock import patch

from main import MatrixCalculatorApp


A = "1 2\n3 4"
B = "5 6\n7 8"
CASES = [
    ("01", "Сложение", "A + B", A, B, "6.0 8.0\n10.0 12.0", None),
    ("02", "Вычитание", "A - B", A, B, "-4.0 -4.0\n-4.0 -4.0", None),
    ("03", "Умножение", "A × B", A, B, "19.0 22.0\n43.0 50.0", None),
    ("04", "Определитель", "det(A)", A, "", "-2.0", None),
    ("05", "Транспонирование", "Aᵀ", A, B, "1.0 3.0\n2.0 4.0", None),
    ("06", "Размеры при сложении", "A + B", A, "5 6", "", "Для сложения матрицы должны иметь одинаковый размер."),
    ("07", "Размеры при вычитании", "A - B", A, "5 6", "", "Для вычитания матрицы должны иметь одинаковый размер."),
    ("08", "Размеры при умножении", "A × B", A, "5 6", "", "Количество столбцов первой матрицы должно совпадать с количеством строк второй."),
    ("09", "Неквадратный определитель", "det(A)", "1 2 3\n4 5 6", "", "", "Определитель можно вычислить только для квадратной матрицы."),
    ("10", "Буква вместо числа", "Aᵀ", "1 о\n3 4", "", "", "Матрица должна содержать только числа."),
    ("11", "Пустая матрица", "Aᵀ", "", "", "", "Матрица не заполнена."),
    ("12", "Строки разной длины", "Aᵀ", "1 2\n3", "", "", "Все строки матрицы должны иметь одинаковую длину."),
    ("13", "Прямоугольное произведение", "A × B", "1 2 3\n4 5 6", "7 8\n9 10\n11 12", "58.0 64.0\n139.0 154.0", None),
    ("14", "Определитель 3 на 3", "det(A)", "1 2 3\n0 1 4\n5 6 0", "", "1.0", None),
    ("15", "Дробные и отрицательные числа", "A + B", "-1.5 2.25", "0.5 -0.25", "-1.0 2.0", None),
    ("16", "Транспонирование без B", "Aᵀ", "1 2 3\n4 5 6", "", "1.0 4.0\n2.0 5.0\n3.0 6.0", None),
]


def buttons(widget):
    found = {}
    for child in widget.winfo_children():
        if isinstance(child, tk.Button):
            found[child.cget("text")] = child
        found.update(buttons(child))
    return found


class TestGuiScenarios(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = MatrixCalculatorApp(self.root)
        self.controls = buttons(self.root)
        self.callback_errors = []
        self.root.report_callback_exception = lambda *args: self.callback_errors.append(str(args[1]))
        self.dialog_patch = patch("main.messagebox.showerror")
        self.dialog = self.dialog_patch.start()
        self.addCleanup(self.dialog_patch.stop)
        self.addCleanup(self.root.destroy)

    def fill(self, a, b):
        for widget, value in [(self.app.matrix_a, a), (self.app.matrix_b, b)]:
            widget.delete("1.0", tk.END)
            widget.insert("1.0", value)

    def read_result(self):
        return self.app.result.get("1.0", "end-1c")

    def invoke(self, label):
        self.controls[label].invoke()
        self.root.update_idletasks()
        self.assertEqual(self.callback_errors, [], "Необработанная ошибка обработчика")

    def test_17_clear(self):
        """Очистка всех полей"""
        self.fill(A, B)
        self.invoke("A + B")
        self.assertNotEqual(self.read_result(), "")
        self.invoke("Очистить")
        actual = [w.get("1.0", "end-1c") for w in [self.app.matrix_a, self.app.matrix_b, self.app.result]]
        self.actual = str(actual)
        self.assertEqual(actual, ["", "", ""])
        self.dialog.assert_not_called()

    def test_18_recovery(self):
        """Исправление ввода после ошибки"""
        self.fill("1 x", "")
        self.invoke("Aᵀ")
        self.dialog.assert_called_once_with("Ошибка", "Матрица должна содержать только числа.")
        self.dialog.reset_mock()
        self.fill(A, B)
        self.invoke("A + B")
        self.actual = self.read_result()
        self.assertEqual(self.actual, "6.0 8.0\n10.0 12.0")
        self.dialog.assert_not_called()


def make_test(case):
    _, title, button, a, b, expected, error = case

    def test(self):
        self.fill(a, b)
        self.invoke(button)
        self.actual = self.read_result()
        if error:
            self.actual = str(self.dialog.call_args)
            self.dialog.assert_called_once_with("Ошибка", error)
            self.assertEqual(self.read_result(), expected)
        else:
            self.assertEqual(self.read_result(), expected)
            self.dialog.assert_not_called()
        self.assertEqual(self.app.matrix_a.get("1.0", "end-1c"), a)
        self.assertEqual(self.app.matrix_b.get("1.0", "end-1c"), b)
    test.__doc__ = title
    return test


for case in CASES:
    setattr(TestGuiScenarios, "test_" + case[0], make_test(case))


if __name__ == "__main__":
    unittest.main(verbosity=2)
