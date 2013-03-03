"""
basic_learner.py - follows the basic word acquisition algorithm given in Siskind
1996 (Computational Approaches to Language Acquisition): developing a mapping of
words to "meanings". Input data for this training comes as utterances (a series
of words in a structured, grammatical form) with a set of hypothesised meanings
(symbolic relationships).

Contains a class for a symbol-table (mapping an expression to two sets of symbols:
the necessary and the possible. Also contains a lexicon object that manages these
and can train on utterance-meaning pairs).
"""

import copy
import utils.logger
from symbol_set import SymbolSet, UniversalSymbolSet
from symbol_table import FiniteSymbolTable, UniversalSymbolTable
from training.pairs import BottomExpression

class NPSymbolLearner:
    def __init__(self, necessary=FiniteSymbolTable(), possible=UniversalSymbolTable()):
        self.necessary = necessary
        self.possible = possible
        self.expressions = UniversalSymbolTable()

        self.log = utils.logger.NPLogger()

        class Foo:
            def debug(self, bar):
                pass
        self.main_log = Foo()

    def __str__(self):
        """String representation of symbol learner state (show both N and P tables side by side)"""
        return "\n".join("%s || %s | %s" % (word.rjust(10),
                str(self.necessary[word]).ljust(25),
                str(self.possible[word]).ljust(25))
                          for word in self.necessary )

    def __contains__(self, word):
        """is there an entry in this learner for some word?"""
        return word in self.necessary


    def process(self,pair):
        """Perform one iteration, based on an utterance -> meaning pair"""
        self.log.info("[~~>] %s" % pair)
        self._rule1(pair)
        self._rule2(pair)
        self._rule3(pair)
        self._rule4(pair)
        self._rule5(pair)

    def converged(self, word):
        """Have the symbol sets have converged on the same values for an entry?"""
        return self.necessary[word] == self.possible[word]

    def all_consistent(self):
        """Checks all lexical entries for consistency"""
        for word in self.necessary:
            if not self.consistent(word):
                return False 
        return True

    def consistent(self, word):
        """
        Inconsistency implies a lexical entry has been 
        corrupted by noise (no correct meanings hypothesised) or homonymy (multiple
        disparate meanings for the same word)
        """
        # universal possible set trivially consistent (non-empty and n is subset)
        #print "consistent? : %s" % word
        if self.possible[word].is_universal():
            return True

        # if conceptual expressions for sense empty => corrupted
        if (not self.expressions[word].is_universal()) and len(self.expressions[word]) is 0:
            return False

        # consistency: necessary subset of possible
        for symbol in self.necessary[word]:
            if symbol not in self.possible[word]:
                return False
        return True
            
    
    def _rule1(self, pair):
        """
        For an utterance/meaning pair, filter out the hypotheses that violate Rule 1 in Siskind 1996.
        """

        # create sets p,n which are the union of the possible, necessary (respectively) sets for each word in the
        # utterance
        self.log.rule_debug("", symbol="1")
        self.log.rule_debug(pair, indent=1, symbol="->")

        p_universal = False
        p = set()
        n = set()
        for word in pair.words:
            if self.possible[word].is_universal():
                p_universal = True

            # if any possible set for a word is universal, then the union of p's is universal..
            if not p_universal:
                #print self.possible[word]
                p = p.union(self.possible[word])
            n = n.union(self.necessary[word])

        def test(hypothesis):
            # remove hypotheses that contain a symbol ruled out for all words
            # NB. if p is universal, this trivally passes
            if not p_universal and not hypothesis.symbols.issubset(p):
                debug_msg = "Sym/s Not Poss: %s for %s" % (hypothesis,
                    hypothesis.symbols.difference(p))
                self.log.rule_debug(debug_msg, symbol="-", indent=2)
                return False

            # filter out hypotheses that are missing a necessary symbol for a word
            if not n.issubset(hypothesis.symbols):
                debug_msg = "Sym/s in N missing: %s for %s" % (hypothesis,
                   n.difference(hypothesis.symbols))
                self.log.rule_debug(debug_msg, symbol="-", indent=2)
                return False

            return True

        pair.hypotheses = {hyp for hyp in pair.hypotheses if test(hyp)}
        self.log.rule_debug(pair, indent=1, symbol="<-")

    def _rule2(self, pair):
        """
        For each word in the utterance, eliminate from the possible symbols any
        symbols that don't appear in any utterance meanings... i.e. symbols that don't show
        up at all for an utterance are obviously not possible symbols
        """
        self.log.rule_debug("", symbol="2", indent=1)
        self.log.rule_debug("", symbol="->", indent=2)
        self.log.rule_debug(self, indent=3)

        # find all the symbols in each of the remaining hypotheses...
        remaining_symbols = set()
        for hypothesis in pair.hypotheses:
            remaining_symbols = remaining_symbols.union(hypothesis.symbols)

        # remove from the possible entry for each word, those symbols not in the above set
        for word in pair.words:
            self.possible[word] = self.possible[word].intersection(remaining_symbols)

        self.log.rule_debug("", symbol="<-", indent=2)
        self.log.rule_debug(self,  indent=2)

    def _rule3(self, pair):
        """
        Add to necessary symbols for a word those symbols which appear in all remaining hypotheses, but
        are missing from the possible table for all other words in the utterance. i.e. we have a symbol
        that is in all hypotheses for an utterance, and it is impossible for all words but one => that must be part
        of the definition for that remaining word.
        """
        
        # NOTE: could be optimised by breaking loop as symbol set becomes negative/
        # identity

        self.log.rule_debug("", symbol="3", indent=1)

        # which symbols are in all remaining hypotheses?
        if len(pair.hypotheses) > 0:
            element = pair.hypotheses.pop()
            pair.hypotheses.add(element)
            common_symbols = element.symbols

            for expression in pair.hypotheses:
                common_symbols.intersection_update(expression.symbols)
        else: # empty hypothesis set
            return

        self.log.rule_debug("Common: %s" % common_symbols,
                            symbol="", indent=3)

        # test all word combinations (Cartesian product)
        for word in pair.words:
            symbols = copy.copy(common_symbols)
            self.log.rule_debug(word, symbol="", indent=2)
            for other_word in pair.words:
                if word != other_word:
                    symbols.difference_update(self.possible[other_word])
                    self.log.rule_debug("P(%s):\t\t %s" % (other_word, symbols), indent=3)
            self.necessary[word].update(symbols)

        self.log.rule_debug("", symbol="<-", indent=2)
        self.log.rule_debug(self,  indent=2)

    def _rule4(self, pair):
        """
        Remove from the possible any symbols that only appear once.
        """
        #TODO: explain this rule properly

        self.log.rule_debug("", symbol="4", indent=1)

        # find symbols that appear only once
        once_symbols = set()
        for hypothesis in pair.hypotheses:
            for symbol in hypothesis.symbols:
                if hypothesis.symbol_count[symbol] <= 1:
                    once_symbols.add(symbol)

        self.log.rule_debug("once: %s" % once_symbols,
                            indent=2)

        # remove the appropriate symbols
        for word in pair.words:
            self.log.rule_debug("%s:\tP:%s" % (word, self.possible[word]),
                                indent=2)
            for other_word in pair.words:
                if other_word != word:
                    self.log.rule_debug("%s:" % other_word, indent=3)
                    for symbol in self.necessary[other_word]:
                        symbols = once_symbols.intersection(self.necessary[other_word])
                        self.possible[word].difference_update(symbols)
                        self.log.rule_debug("%s:\tP(%s=%s" % (symbol, word, self.possible[word]),
                                            indent=4)
        self.log.rule_debug("", symbol="<-", indent=2)
        self.log.rule_debug(self,  indent=2)

    def _rule5(self, pair):
        self.log.rule_debug("", symbol="5", indent=1)
        for word in pair.words:
            # has the word converged?
            if self.converged(word):
                self.log.rule_debug("convergence: %s" % word, indent=1)

                # empty => empty
                if len(self.necessary[word]) is 0 and len(self.possible[word]) is 0:
                    self.log.rule_debug("empty", indent=2)
                    self.expressions[word] = SymbolSet({BottomExpression()})

                # variables => variables
                elif self.necessary[word] == self.necessary[word].variables():
                    self.log.rule_debug("variable: %s" % self.necessary[word],
                                          indent=2)
                    self.expressions[word] = self.expressions[word].intersection( self.necessary[word] )

                # compare constant terms
                else:
                    valid_subexpressions = set()
                    word_constants = set(symbol for symbol in self.necessary[word] if symbol.isupper())

                    self.log.rule_debug("constants: %s" % word_constants,
                                                      indent=2)

                    for hypothesis in pair.hypotheses:
                       valid_subexpressions = valid_subexpressions.union(
                           hypothesis.subexpressions_for_constants(word_constants) )

                    self.log.rule_debug("compatible exprs:", indent=2)
                    self.log.rule_debug("\n".join("%s" % str(expr)
                                                  for expr in valid_subexpressions),
                                        indent=2)

                    self.expressions[word] = self.expressions[word].intersection(valid_subexpressions)