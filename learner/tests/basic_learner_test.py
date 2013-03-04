import unittest
from training.expression import Expression
from training.hypothesis import Hypothesis

import training.pairs
import training.sample.siskind_basic
import utils.logger

from learner import basic_learner, symbol_set

# logging configuration (display all from "langframe.np_learner")
utils.logger.display_log("langframe.root.NPLogger")
utils.logger.display_log("langframe.debug.NPLogger")

class TrainingPairs(unittest.TestCase):
    def testHyp1(self):
        expr = ["CAUSE", "john", ["GO", "ball" , ["TO", "john"]]]
        hyp = Hypothesis(expr)
        self.assertEqual(hyp.symbols, {"CAUSE", "john", "GO", "ball", "TO"})

    def testHyp2(self):
        expr = ["WANT", "john", "ball"]
        hyp = Hypothesis(expr)
        self.assertEqual(hyp.symbols, {'WANT', "john", "ball"})

    def testHyp3(self):
        expr = ["CAUSE", "john", ["GO", ["PARTOF", ["LEFT", "arm"], "john"], 
                    ["TO", "ball"]]]
        hyp = Hypothesis(expr)
        self.assertEqual(hyp.symbols, {"CAUSE", "john", "GO", "PARTOF", "LEFT",
                                        "arm", "TO", "ball"} )

    def testContainsSymbol(self):
        expr = ["CAUSE", "john", ["GO", ["PARTOF", ["LEFT", "arm"], "john"],
                                  ["TO", "ball"]]]
        hyp = Hypothesis(expr)

        # check all symbols reported as being in
        self.assertIn("CAUSE", hyp)
        self.assertIn("john", hyp)
        self.assertIn("GO", hyp)
        self.assertIn("PARTOF", hyp)
        self.assertIn("LEFT", hyp)
        self.assertIn("arm", hyp)
        self.assertIn("TO", hyp)
        self.assertIn("ball", hyp)
         
class SymbolTable(unittest.TestCase):
    def setUp(self):
        self.table = basic_learner.FiniteSymbolTable()
        self.table.add("hello", "HELLO")

    def testUniversalSet(self):
        """test our universal set implementation"""
        possible = symbol_set.UniversalSymbolSet()
        
        # test while instantiated as "universal"
        self.assertIn("a", possible)
        self.assertIn("XYZ", possible)

        # intersect with a finite set
        finite_set = {"A", "B"}
        possible = possible.intersection(finite_set)
        self.assertIn("A", possible)
        self.assertIn("B", possible)
        self.assertNotIn("a", possible)
        self.assertNotIn("xyz", possible)

    def testAddNewWord(self):
        """new word added to dictionary"""
        self.assertNotIn("world", self.table)
        self.assertNotIn("WORLD", self.table["world"])
        self.table.add("world", "WORLD")
        self.assertIn("world", self.table)
        self.assertIn("WORLD", self.table["world"])

    def testAddExistingWord(self):
        """existing word added to dictionary, with new symbol"""
        self.assertIn("hello", self.table)
        self.assertNotIn("GREETING", self.table["hello"])
        self.table.add("hello", "GREETING")
        self.assertIn("hello", self.table)
        self.assertIn("GREETING", self.table["hello"])

    def testCaseWhenAdding(self):
        """word should be lowercase, symbol can be any"""
        with self.assertRaises(Exception):
            self.add("LIGHT", "LIGHT")

    def testAddWordWithSymbolSet(self):
        """This test is invalid?"""
        my_set = {"HELLO", "john", "ball"}
        self.table.add("hello", my_set)

        self.assertIn("HELLO", self.table["hello"])
        self.assertIn("john", self.table["hello"])
        self.assertIn("ball", self.table["hello"])

    def testGetSymbols(self):
        self.table.add("hello", "HELLO")
        self.table.add("hello", "john")
        self.table.add("hello", "ball")

        #print self.table["hello"]

        self.assertIn("HELLO", self.table["hello"])
        self.assertIn("john", self.table["hello"])
        self.assertIn("ball", self.table["hello"])

        (constants, variables) = (self.table["hello"].constants(), self.table["hello"].variables())

        self.assertIn("HELLO", constants)
        self.assertIn("john", variables)
        self.assertIn("ball", variables)

class NPTables(unittest.TestCase):
    """ Siskind 1996, p57 example """

    def IndividualSetUp(self):
        """ Create midway symbol tables as per Siskind 1996 """
        n = basic_learner.FiniteSymbolTable()
        n.add("john", "john")
        n.add("took", "CAUSE")
        n.add("the", set())
        n.add("ball", "ball")

        p = basic_learner.FiniteSymbolTable()
        p.add("john", {"john", "ball"})
        p.add("took", {"CAUSE", "WANT", "GO", "TO", "arm"})
        p.add("the", {"WANT", "arm"})
        p.add("ball", {"ball", "arm"})

        self.learner = basic_learner.NPSymbolLearner(necessary=n, possible=p)
        self.pair = training.sample.siskind_basic.pair1()

    def test_rule1(self):
        self.IndividualSetUp()

        self.assertIn(training.sample.siskind_basic.hyp1, self.pair.hypotheses)
        self.assertIn(training.sample.siskind_basic.hyp2, self.pair.hypotheses)
        self.assertIn(training.sample.siskind_basic.hyp3, self.pair.hypotheses)

        self.learner._rule1(self.pair)  # rule 1

        self.assertIn(training.sample.siskind_basic.hyp1, self.pair.hypotheses)
        self.assertNotIn(training.sample.siskind_basic.hyp2, self.pair.hypotheses)
        self.assertNotIn(training.sample.siskind_basic.hyp3, self.pair.hypotheses)

    def test_rule2(self):
        self.IndividualSetUp()

        self.learner._rule1(self.pair)  # rule 1
        self.learner._rule2(self.pair) # rule 2

        self.assertNotIn("WANT", self.learner.possible["took"])
        self.assertNotIn("arm", self.learner.possible["took"])
        self.assertNotIn("WANT", self.learner.possible["the"])
        self.assertNotIn("arm", self.learner.possible["the"])
        self.assertNotIn("arm", self.learner.possible["ball"])

    def test_rule3(self):
        self.IndividualSetUp()

        self.learner._rule1(self.pair)  # rule 1
        self.learner._rule2(self.pair) # rule 2

        self.assertNotIn("GO", self.learner.necessary["took"])
        self.assertNotIn("TO", self.learner.necessary["took"])

        self.learner._rule3(self.pair) # rule 3

        self.assertIn("GO", self.learner.necessary["took"])
        self.assertIn("TO", self.learner.necessary["took"])

    def test_rule4(self):
        self.IndividualSetUp()

        self.learner._rule1(self.pair)  # rule 1
        self.learner._rule2(self.pair) # rule 2
        self.learner._rule3(self.pair) # rule 3

        self.assertIn("ball", self.learner.possible["john"])

        self.learner._rule4(self.pair) # rule 4

        self.assertNotIn("ball", self.learner.possible["john"])


class ConvergenceMeasure(unittest.TestCase):
    def setUp(self):
        """ Create midway symbol tables as per Siskind 1996 """
        n = basic_learner.FiniteSymbolTable()
        n.add("john", "john")
        n.add("took", "CAUSE")
        n.add("the", set())
        n.add("ball", "ball")

        p = basic_learner.FiniteSymbolTable()
        p.add("john", {"john", "ball"})
        p.add("took", {"CAUSE", "WANT", "GO", "TO", "arm"})
        p.add("the", {"WANT", "arm"})
        p.add("ball", {"ball", "arm"})

        self.learner = basic_learner.NPSymbolLearner(necessary=n, possible=p)

        self.pair = training.sample.siskind_basic.pair1()

    def testNoConvergence(self):
        unconverged = set() 
        for word in self.learner.necessary:
            if not self.learner.converged(word):
                unconverged.add(word)

        self.assertNotEqual(unconverged, set()) # i.e. set non-empty


    def testConvergence(self):
        # perform rules
        self.learner._rule1(self.pair)  # rule 1
        self.learner._rule2(self.pair) # rule 2
        self.learner._rule3(self.pair) # rule 3
        self.learner._rule4(self.pair) # rule 4

        for word in self.learner.necessary:
            self.assertTrue(self.learner.converged(word))

class ConceptualExpressionTable(unittest.TestCase):
    def setUp(self):
        self.np_learner = basic_learner.NPSymbolLearner()

    def testUniversal(self):
        expression = Expression(["CAUSE", ["GO", "to"]])
        self.assertIn(expression, self.np_learner.expressions["word"] )

class ConceptualExpressionRules(unittest.TestCase):
    def setUp(self):
        n = basic_learner.FiniteSymbolTable()
        n.add("john", "john")
        n.add("catches", {"CAUSE", "GO", "TO"})
        n.add("the", set())
        n.add("ball", "ball")

        p = basic_learner.FiniteSymbolTable()
        p.add("john", "john")
        p.add("catches", {"CAUSE", "GO", "TO"})
        p.add("the", set())
        p.add("ball", "ball")

        self.learner = basic_learner.NPSymbolLearner(necessary=n, possible=p)
        self.hypothesis = Hypothesis(["CAUSE", ["john", ["GO", ["ball" , ["TO", "john"]]]]])

    def testEmptyTerms(self):
        utm_pair = training.pairs.UtteranceMeaningPair("the", {self.hypothesis})
        self.learner._rule5(utm_pair)
        self.assertEqual(len(self.learner.expressions["the"]), 0)

    def testVariableTerms(self):
        utm_pair = training.pairs.UtteranceMeaningPair("john", {self.hypothesis})
        self.assertTrue(self.learner.expressions["john"])
        self.learner._rule5(utm_pair)
        self.assertIn("john", self.learner.expressions["john"])
        self.assertNotIn("ball", self.learner.expressions["john"])

        utm_pair2 = training.pairs.UtteranceMeaningPair("ball", {self.hypothesis})
        self.learner._rule5(utm_pair2)
        self.assertIn("ball", self.learner.expressions["ball"])
        self.assertNotIn("john", self.learner.expressions["ball"])

    def testConstantTerms(self):
        subexpressions = self.hypothesis.subexpressions_for_constants({"GO", "TO"})

        for expression in subexpressions:
           self.assertIn("GO", expression)
           self.assertIn("TO", expression)
           self.assertNotIn("CAUSE", expression)

    def testRule5(self):
        self.assertIn("john", self.learner.expressions["catches"] ) # arbitrary membership; universal
        utm_pair = training.pairs.UtteranceMeaningPair("catches", {self.hypothesis})

        self.learner._rule5(utm_pair)

        for expression in self.learner.expressions["catches"]:
            self.assertIn("GO", expression)
            self.assertIn("TO", expression)
            self.assertIn("CAUSE", expression)

if __name__ == "__main__":
    unittest.main()