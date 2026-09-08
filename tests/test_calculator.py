import json
import math
import unittest

from tools.calculator import calculate
from tools.execute import execute_tool
from tools.schema import tool_schema


class CalculatorTests(unittest.TestCase):
    def decode(self, expression, **kwargs):
        response = calculate(expression, **kwargs)
        self.assertIsInstance(response, str)
        payload = json.loads(response)
        self.assertIsInstance(payload, dict)
        return payload

    def assert_result(self, expression, expected, **kwargs):
        payload = self.decode(expression, **kwargs)
        self.assertIs(payload.get("ok"), True, payload)
        self.assertEqual(payload["expression"], expression.strip())
        self.assertIn(payload["angle_unit"], ("radians", "degrees"))
        self.assertIn(type(payload["result"]), (int, float))
        self.assertAlmostEqual(payload["result"], expected, places=12)
        return payload

    def assert_error(self, expression, **kwargs):
        payload = self.decode(expression, **kwargs)
        self.assertIs(payload.get("ok"), False, payload)
        self.assertIsInstance(payload.get("error"), str)
        self.assertTrue(payload["error"].strip())

    def test_requested_expression_has_explicit_angle_semantics(self):
        expression = "sqrt(143) + 2**3 + sin(12) + cos(3)"
        expected = {
            "radians": 18.431695328500517,
            "degrees": 21.164801968673732,
        }
        for unit, result in expected.items():
            with self.subTest(angle_unit=unit):
                payload = self.assert_result(expression, result, angle_unit=unit)
                self.assertEqual(payload["angle_unit"], unit)

    def test_default_matches_advertised_schema(self):
        calculator_schema = next(
            tool["function"]
            for tool in tool_schema
            if tool["function"]["name"] == "calculate"
        )
        parameters = calculator_schema["parameters"]
        self.assertIn("expression", parameters["required"])
        self.assertEqual(parameters["properties"]["expression"]["type"], "string")
        angle_schema = parameters["properties"]["angle_unit"]
        self.assertEqual(set(angle_schema["enum"]), {"radians", "degrees"})
        default = angle_schema["default"]
        self.assertIn(default, angle_schema["enum"])
        expected = math.sin(30) if default == "radians" else 0.5
        payload = self.assert_result("sin(30)", expected)
        self.assertEqual(payload["angle_unit"], default)

    def test_all_trigonometric_functions_respect_angle_unit(self):
        examples = [
            ("sin(pi / 2)", "radians", 1.0),
            ("cos(pi)", "radians", -1.0),
            ("tan(pi / 4)", "radians", 1.0),
            ("sin(30)", "degrees", 0.5),
            ("cos(60)", "degrees", 0.5),
            ("tan(45)", "degrees", 1.0),
        ]
        for expression, unit, expected in examples:
            with self.subTest(expression=expression, angle_unit=unit):
                self.assert_result(expression, expected, angle_unit=unit)

    def test_precedence_and_supported_numeric_operations(self):
        examples = [
            ("2 + 3 * 4", 14),
            ("(2 + 3) * 4", 20),
            ("2**3**2", 512),
            ("-2**2", -4),
            ("(-2)**2", 4),
            ("2**-3", 0.125),
            ("7 // 2 + 7 % 2", 4),
            ("abs(-3) + min(2, 5) + max(2, 5)", 10),
            ("log(e)", 1),
            ("log(100, 10) + log10(100)", 4),
            ("round(10 / 3, 2)", 3.33),
            ("round(10 / 3, ndigits=2)", 3.33),
        ]
        for expression, expected in examples:
            with self.subTest(expression=expression):
                self.assert_result(expression, expected)

    def test_surrounding_whitespace_is_ignored(self):
        self.assert_result(" \t\n 1 + 2 \n ", 3)

    def test_invalid_arguments_return_errors(self):
        examples = [
            "",
            " \n ",
            "1 +",
            "round(10 / 3, unexpected=2)",
            "sqrt(4, unknown=1)",
            "sqrt()",
            "sin(1, 2)",
            "unknown(2)",
            "missing_name + 1",
        ]
        for expression in examples:
            with self.subTest(expression=expression):
                self.assert_error(expression)
        for value in (None, 12, True, [1, 2]):
            with self.subTest(non_string=value):
                self.assert_error(value)
        self.assert_error("1 + 2", angle_unit="gradians")

    def test_domain_errors_and_division_by_zero(self):
        for expression in ("sqrt(-1)", "log(0)", "log(-1)", "1 / 0", "1 // 0", "1 % 0"):
            with self.subTest(expression=expression):
                self.assert_error(expression)

    def test_only_finite_real_numbers_are_accepted(self):
        for expression in (
            "True + 1",
            "False",
            "1j",
            "(-1)**0.5",
            "1e309",
            "1e308 * 1e308",
        ):
            with self.subTest(expression=expression):
                self.assert_error(expression)

    def test_disallowed_python_syntax_is_rejected(self):
        for expression in (
            "(1).__class__",
            "math.sqrt(4)",
            "__import__('math').sqrt(4)",
            "import math",
            "[1, 2][0]",
            "(lambda: 1)()",
            "sum(x for x in range(3))",
        ):
            with self.subTest(expression=expression):
                self.assert_error(expression)

    def test_unreasonable_power_is_rejected(self):
        self.assert_error("2**1000000")

    def test_registry_returns_json_string_ready_for_tool_message(self):
        response = execute_tool(
            "calculate",
            {"expression": "sqrt(143) + 2**3 + sin(12) + cos(3)", "angle_unit": "degrees"},
        )
        self.assertIsInstance(response, str)
        payload = json.loads(response)
        self.assertIs(payload["ok"], True)
        self.assertEqual(payload["angle_unit"], "degrees")
        self.assertAlmostEqual(payload["result"], 21.164801968673732, places=12)


if __name__ == "__main__":
    unittest.main()
