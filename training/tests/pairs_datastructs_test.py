import unittest

from training import pairs
from training.expression import Expression, VariableExpression, ConstantExpression


class RootExpression(unittest.TestCase):
    def test_equal_expression(self):
        expression1 = VariableExpression("name")
        expression2 = VariableExpression("name")
        self.assertEqual(expression1, expression2)

        expression3 = VariableExpression("different")
        self.assertNotEqual(expression2, expression3)

    def test_equal_string(self):
        expression = VariableExpression("name")
        self.assertEqual(expression, "name")
        self.assertNotEqual(expression, "different")

class VariableExpression(unittest.TestCase):
    def test_replace_success(self):
        expression = VariableExpression("CATCH")
        new_expression = expression.replace({"CATCH" : "CAUGHT"})
        self.assertEqual(new_expression, "CAUGHT")

    def test_replace_fail(self):
        expression = VariableExpression("CATCH")
        new_expression = expression.replace({"NOPE" : "CAUGHT"})
        self.assertEqual(new_expression, "CATCH")

class FullExpression(unittest.TestCase):
    def test_create_variable(self):
        variable_expr = Expression("variable")
        self.assertIsInstance(variable_expr.subexpressions[0],
                              VariableExpression)

    def test_create_constant(self):
        constant_expr = Expression("CONSTANT")
        self.assertIsInstance(constant_expr.subexpressions[0],
                              ConstantExpression)

    def test_create_mixed(self):
        expr = Expression(["WANT", ["john", "ball"]])
        self.assertIsInstance(expr.subexpressions[0][0],
                              ConstantExpression)
        self.assertIsInstance(expr.subexpressions[1][0][0],
                              VariableExpression)
        self.assertIsInstance(expr.subexpressions[1][1][0],
                              VariableExpression)

    def test_contains(self):
        expr = Expression(["WANT", ["john", "ball"]])
        self.assertIn("WANT", expr)
        self.assertIn("john", expr)
        self.assertIn("ball", expr)

    def test_replace(self):
        self.assertTrue(False)

    def test_iteration(self):
        pass

    def test_equality(self):
        expr1 = Expression(
            ["CAUSE",
             ["john",
              ["CAUSE",
               ["PARTOF",
                ["CAUSE", "arm"], "john"],
               ["TO", "ball"]]]]  )
        expr2 = Expression(
            ["CAUSE",
             ["john",
              ["CAUSE",
               ["PARTOF",
                ["CAUSE", "arm"], "john"],
               ["TO", "ball"]]]]  )
        self.assertEqual(expr1, expr2)

    def test_counts(self):
        expr = Expression(
            ["CAUSE",
                ["john",
                    ["CAUSE",
                        ["PARTOF",
                            ["CAUSE", "arm"], "john"],
                            ["TO", "ball"]]]]  )
        (consts, vars) = expr.counts()

        self.assertEqual(consts["CAUSE"], 3)
        self.assertEqual(consts["PARTOF"], 1)
        self.assertEqual(consts["TO"], 1)
        self.assertEqual(vars["john"], 2)
        self.assertEqual(vars["arm"], 1)
        self.assertEqual(vars["ball"], 1)

    def test_subexpressions(self):
        expr = Expression(
            ["CAUSE",
             ["john",
              ["CAUSE",
               ["PARTOF",
                ["CAUSE", "arm"], "john"],
               ["TO", "ball"]]]]  )

        subexpressions = expr.deep_subexpressions()

        for subexpr in subexpressions:
            print subexpr

        self.assertTrue(False)