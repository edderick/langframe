import unittest
import utils.logger

from training.expression import Expression
from knowledge import gauss_colour

utils.logger.display_log("langframe.data.ColourLogger")

class Training(unittest.TestCase):
    def setUp(self):
        self.knowledge = gauss_colour.GaussianColourSemantics("example")

    def testDefaultMean(self):
        point = Expression(["COLOUR", "r_125", "g_255", "b_12"])
        self.knowledge.learn("mycol", point)
        self.assertEqual(self.knowledge.mean["mycol"], (125,255,12))

    def testOnlineMeanUpdate(self):
        p1 = Expression(["COLOUR", "r_125", "g_255", "b_12"])
        p2 = Expression(["COLOUR", "r_108", "g_200", "b_6"])
        p3 = Expression(["COLOUR", "r_129", "g_240", "b_16"])

        self.knowledge.learn("mycol", p1)
        self.assertEqual(self.knowledge.mean["mycol"], (125,255,12))

        self.knowledge.learn("mycol", p2)
        self.assertEqual(self.knowledge.mean["mycol"], (117,228,9))

        self.knowledge.learn("mycol", p3)
        self.assertEqual(self.knowledge.mean["mycol"], (121,232,11))

    def testVarianceUpdate(self):
        p1 = Expression(["COLOUR", "r_125", "g_255", "b_12"])
        p2 = Expression(["COLOUR", "r_108", "g_200", "b_6"])
        p3 = Expression(["COLOUR", "r_129", "g_240", "b_16"])

        self.knowledge.learn("mycol", p1)
        self.assertEqual(self.knowledge.variance["mycol"], (0,0,0))

        self.knowledge.learn("mycol", p2)
        self.assertTrue(False)

        self.knowledge.learn("mycol", p3)
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
