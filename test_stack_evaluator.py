import unittest
from stack_evaluator import Stack, evaluate_expression


class TestStack(unittest.TestCase):
    def test_push_peek_pop(self):
        stack = Stack()
        stack.push(10)
        stack.push(20)
        self.assertEqual(stack.peek(), 20)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack.pop(), 10)
        self.assertTrue(stack.is_empty())


class TestExpressionEvaluator(unittest.TestCase):
    def test_precedence(self):
        self.assertEqual(evaluate_expression("3 + 5 * 2"), 13)

    def test_parentheses(self):
        self.assertEqual(evaluate_expression("(8 / 4) + 7 * 2"), 16)

    def test_exponent(self):
        self.assertEqual(evaluate_expression("2 ** 3 ** 2"), 512)

    def test_complex_expression(self):
        self.assertEqual(evaluate_expression("10 - (2 + 3) ** 4"), -615)

    def test_division(self):
        self.assertEqual(evaluate_expression("(12 + 8) / 5"), 4)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            evaluate_expression("5 / 0")

    def test_mismatched_parentheses(self):
        with self.assertRaises(ValueError):
            evaluate_expression("(2 + 3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
