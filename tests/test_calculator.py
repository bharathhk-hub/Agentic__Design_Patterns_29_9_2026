import unittest

from tools.calculator import calculator


class CalculatorTests(unittest.TestCase):
    def test_evaluates_arithmetic_expression(self):
        self.assertEqual(calculator("((10 + 5) / 2) ** 2"), "56.25")

    def test_supports_unary_and_precedence(self):
        self.assertEqual(calculator("-5 + 3 * 4"), "7")

    def test_rejects_python_calls(self):
        result = calculator("__import__('os').system('whoami')")
        self.assertTrue(result.startswith("Error:"))

    def test_rejects_unbounded_power(self):
        result = calculator("2 ** 1000")
        self.assertTrue(result.startswith("Error:"))

    def test_rejects_complex_results(self):
        result = calculator("(-1) ** 0.5")
        self.assertTrue(result.startswith("Error:"))

    def test_reports_division_by_zero(self):
        result = calculator("10 / 0")
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()