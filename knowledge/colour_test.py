import unittest
import utils.logger

from training.expression import Expression
from knowledge import knn_colour

utils.logger.display_log("langframe.data.ColourLogger")

class TestAddingExpressions(unittest.TestCase):
    def setUp(self):
        self.knowledge = knn_colour.KNNColourSemantics()

    def testLearnSingle(self):
        red_expr = Expression(["COLOUR", "r_255", "g_0", "b_10"])
        self.knowledge.learn("red", red_expr)
        self.assertIn((255, 0, 10), self.knowledge.points)
        self.assertIn("red", self.knowledge.words)

    def testKNearest(self):
        black_expr = Expression(["COLOUR", "r_0", "g_0", "b_0"])
        dark_red = Expression(["COLOUR", "r_125", "g_0", "b_0"])
        reddish_expr = Expression(["COLOUR", "r_250", "g_25", "b_30"])

        self.knowledge.learn("black", black_expr)
        self.knowledge.learn("red", dark_red)
        self.knowledge.learn("red", reddish_expr)

        self.knowledge.word_for(Expression(["COLOUR", "r_255", "g_0", "b_0"]))
        self.assertTrue(False)


    def testNoColourLabel(self):
        black_expr = Expression(["COLOUR", "r_0", "g_0", "b_0"])
        dark_red = Expression(["COLOUR", "r_125", "g_0", "b_0"])
        reddish_expr = Expression(["COLOUR", "r_250", "g_25", "b_30"])

        self.knowledge.learn("black", black_expr)
        self.knowledge.learn("red", dark_red)
        self.knowledge.learn("red", reddish_expr)

        self.assertEqual(self.knowledge.expression_for("blue"), Expression("MISUNDERSTOOD"))

    def testReturnColourValue(self):
        black_expr = Expression(["COLOUR", "r_0", "g_0", "b_0"])
        dark_red = Expression(["COLOUR", "r_125", "g_0", "b_0"])
        reddish_expr = Expression(["COLOUR", "r_250", "g_25", "b_30"])

        self.knowledge.learn("black", black_expr)
        self.knowledge.learn("red", dark_red)
        self.knowledge.learn("red", reddish_expr)

        self.knowledge.expression_for("red")

if __name__ == '__main__':
    unittest.main()
