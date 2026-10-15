"""Запуск сценариев ЛР 2 и сохранение фактического протокола."""
import argparse
import io
import json
from pathlib import Path
import platform
import sys
import tkinter as tk
import unittest

from main import MatrixCalculatorApp
from tests.test_gui import buttons, A, B


class RecordedResult(unittest.TextTestResult):
    records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"id": test._testMethodName, "name": test.shortDescription(), "status": "PASS", "actual": getattr(test, "actual", "")})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({"id": test._testMethodName, "name": test.shortDescription(), "status": "FAIL", "actual": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({"id": test._testMethodName, "name": test.shortDescription(), "status": "ERROR", "actual": self._exc_info_to_string(err, test)})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("artifacts/lab2"))
    parser.add_argument("--show-results", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromName("tests.test_gui")
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=RecordedResult).run(suite)
    log = stream.getvalue()
    (args.output / "test-run.txt").write_text(log, encoding="utf-8")
    data = {"python": platform.python_version(), "os": platform.platform(), "tk": tk.TkVersion, "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "records": result.records}
    (args.output / "results.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(log)
    if args.show_results:
        root = tk.Tk()
        app = MatrixCalculatorApp(root)
        app.matrix_a.insert("1.0", A)
        app.matrix_b.insert("1.0", B)
        buttons(root)["A + B"].invoke()
        window = tk.Toplevel(root)
        window.title("Лабораторная работа 2 — протокол автоматизированного тестирования")
        window.geometry("1000x680")
        viewer = tk.Text(window, font=("Consolas", 12), wrap="word", padx=16, pady=12)
        viewer.pack(fill="both", expand=True)
        summary = f"Лабораторная работа 2 — Матричный калькулятор\nPython {data['python']} | Tk {data['tk']}\n\n"
        summary += "\n".join(f"{r['id'].replace('test_', 'TC-'):16} {r['status']:5} {r['name']}" for r in result.records)
        summary += f"\n\nВыполнено: {result.testsRun}; ошибок: {len(result.errors)}; провалов: {len(result.failures)}\n" + ("OK" if result.wasSuccessful() else "FAILED")
        viewer.insert("1.0", summary)
        viewer.configure(state="disabled", cursor="arrow")
        root.mainloop()
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
