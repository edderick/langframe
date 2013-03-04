import unittest
from training.expression import Expression
from training.hypothesis import Hypothesis
import training.pairs

from learner import basic_learner, noisy_learner, symbol_table, symbol_set

class SenseTable(unittest.TestCase):
    def setUp(self):
        self.sense_table = noisy_learner.SenseSymbolTable()

    def test_dummy_sense(self):
        self.assertEqual(self.sense_table["example"], {"example_0"})

    def test_add_sense_from_dummy(self):
        self.test_dummy_sense()
        self.sense_table.add_sense("example")
        self.assertEqual(self.sense_table["example"], {"example_0", "example_1"})

    def test_add_sense_to_set(self):
        self.test_add_sense_from_dummy()
        self.sense_table.add_sense("example")
        self.assertEqual(self.sense_table["example"], {"example_0", "example_1", "example_2"})

    def test_remove_sense_from_set(self):
        self.test_add_sense_to_set()

        self.sense_table.remove_sense("example_2")
        self.assertEqual(self.sense_table["example"], {"example_0", "example_1"})

    def test_remove_sense_to_dummy(self):
        self.test_remove_sense_from_set()

        self.sense_table.remove_sense("example_1")
        self.assertEqual(self.sense_table["example"], {"example_0"})

    def test_remove_dummy_sense(self):
        self.sense_table.remove_sense("example")
        self.assertEqual(self.sense_table["example"], {"example_0"})

class BackupTests(unittest.TestCase):
    def setUp(self):
        n = symbol_table.FiniteSymbolTable()
        n.add("a", "A")
        n.add("c", "E")

        p = symbol_table.UniversalSymbolTable()
        p["a"] = symbol_set.SymbolSet({"A", "B"})
        p["d"] = symbol_set.SymbolSet({"ball", "cross"})

        self.np_learner = basic_learner.NPSymbolLearner(necessary=n, possible=p)
        self.noisy_learner = noisy_learner.NoisySymbolLearner(np_learner=self.np_learner)

    def initial_propositions(self):
        self.assertIn("A", self.np_learner.necessary["a"])
        self.assertIn("E", self.np_learner.necessary["c"])

        #
        self.assertNotIn("B", self.np_learner.necessary["a"])

        self.assertIn("A", self.np_learner.possible["a"])
        self.assertIn("B", self.np_learner.possible["a"])
        self.assertIn("ball", self.np_learner.possible["d"])

        #
        self.assertIn("cross", self.np_learner.possible["d"])

        #
        self.assertIn("rand", self.np_learner.possible["c"])

    def test_backup(self):
        # initial propositions
        (n,p) = self.noisy_learner._backup()
        self.initial_propositions()

        # make changes
        self.np_learner.necessary.add("a", "B")
        self.np_learner.possible["d"] = self.np_learner.possible["d"].intersection("ball")
        self.np_learner.possible["c"] = self.np_learner.possible["d"].intersection("hello")

        self.assertIn("B", self.np_learner.necessary["a"])
        self.assertNotIn("cross", self.np_learner.possible["d"])
        self.assertNotIn("rand", self.np_learner.possible["c"])

        # restore from backup
        self.noisy_learner._restore(n,p)

        # initial props should be true; changes shouldn't
        self.initial_propositions()

class SenseAssignment(unittest.TestCase):
    def setUp(self):
        self.noisy_learner = noisy_learner.NoisySymbolLearner()

        self.noisy_learner.manual_entry("john_0", {"john"}, {"john"}, 1000)
        self.noisy_learner.manual_entry("saw_0", {}, {"wood_cutter", "hammer"}, 0)
        self.noisy_learner.manual_entry("saw_1", {}, {"SEE", "GO"}, 0)
        self.noisy_learner.manual_entry("had_0", {}, {"POSSESS", "WANT"}, 0)
        self.noisy_learner.manual_entry("had_1", {}, {"CONDUCT", "CAUSE"}, 0)
        self.noisy_learner.manual_entry("mary_0", {"mary"}, {"mary"}, 1000)
        self.noisy_learner.manual_entry("arrive_0", {"GO", "TO", "BE"}, {"GO", "TO", "BE"}, 10)
        self.noisy_learner.manual_entry("at_0", {"AT"}, {"AT"}, 1000)
        self.noisy_learner.manual_entry("the_0", {}, {}, 10000)
        self.noisy_learner.manual_entry("a_0", {}, {}, 10000)
        self.noisy_learner.manual_entry("ball_0", {"party"}, {"party"}, 10)
        self.noisy_learner.manual_entry("ball_1", {"spherical_toy"}, {"spherical_toy"}, 1000)
        self.noisy_learner.manual_entry("party_0", {"political_group"}, {"political_group"}, 10)
        self.noisy_learner.manual_entry("susan_0", {}, {"DANCE", "mary", "betty", "susan"}, 0)
        self.noisy_learner.manual_entry("with_0", {"WITH"}, {"WITH"}, 1000)

        # cheeky hack; manually enter conceptual expression for "arrive"
        expr = Expression(["GO", "mary", ["TO", ["BE", "mary", ["AT", "party"]]]])
        self.noisy_learner.np_learner.expressions["arrive_0"] = self.noisy_learner.np_learner.expressions["arrive_0"].intersection({expr})

        #print self.noisy_learner
        #print "\n"
        #print self.noisy_learner.confidence

    def test1(self):
        self.assertTrue(False)
        pass
        utm_pair = training.pairs.UtteranceMeaningPair("john saw mary arrive at the ball",
            {Hypothesis(["SEE", "john", ["GO", "mary", ["TO", ["BE", "mary", ["AT", "party"]]]]])})

        self.noisy_learner.process(utm_pair)

        print "processed!:"
        print "\n"*3
        print self.noisy_learner
        print "\n"
        print self.noisy_learner.confidence

class ColourTest(unittest.TestCase):
    def setUp(self):
        self.noisy_learner = noisy_learner.NoisySymbolLearner()

    def test1(self):
        exprSetup = training.pairs.UtteranceMeaningPair("ball", {Hypothesis(["ball"])})
        expr1 = training.pairs.UtteranceMeaningPair("ball red", {Hypothesis(["ball", "r_255", "b_0", "g_0"])})
        expr2 = training.pairs.UtteranceMeaningPair("ball blue", {Hypothesis(["ball", "r_0", "b_255", "g_0"])})
        expr3 = training.pairs.UtteranceMeaningPair("ball green", {Hypothesis(["ball", "r_0", "b_0", "g_255"])})
        expr3a = training.pairs.UtteranceMeaningPair("ball green", {Hypothesis(["ball", "r_10", "b_10", "g_150"])})

        self.noisy_learner.process(exprSetup)
        self.noisy_learner.process(expr1)
        self.noisy_learner.process(expr2)
        self.noisy_learner.process(expr3)
        self.noisy_learner.process(expr3a)

        print "hello"

if __name__ == "__main__":
    unittest.main()