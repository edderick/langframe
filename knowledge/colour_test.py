import unittest
from training.expression import Expression
from knowledge import knn_colour

class TestAddingExpressions(unittest.TestCase):
    def setUp(self):
        self.knowledge = knn_colour.KNNColourSemantics()

    def testLearnSingle(self):
        red_expr = Expression(["COLOUR", "r_255", "g_0", "b_10"])
        self.knowledge.learn("red", red_expr)
        self.assertIn(("red", (255, 0, 10)), self.knowledge.points)
        pass

if __name__ == '__main__':
    unittest.main()
