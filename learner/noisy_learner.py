"""
noisy_learner.py - implements the extended approach, by being able to handle noisy 
hypothesised utterances (i.e. where no correct expression is hypothesised) and or
homonymous words (i.e. where one word maps to multiple meanings). These events
would have otherwise caused lexical corruption if these were processed.
"""

import copy
import itertools
import basic_learner
from training.expression import VariableExpression, BottomExpression
import training.pairs
from symbol_set import SymbolSet

class ConfidenceTable:
    """Maps a sense symbol to a non-negative integer representing the confidence """
    def __init__(self):
        self.table = dict()

    def __getitem__(self, key):
        """override usage of [] for getting an entry; so default is 0, not keyerror"""
        if key in self.table.keys():
            return self.table[key]
        else:
            return 0

    def __setitem__(self, key, value):
        """Override usage of [] for setting an entry: standard"""
        self.table[key] = value

    def __repr__(self):
        """String representation of a ConfidenceTable"""
        return "\n".join("%s | %d" %
                         (word.rjust(10), self.table[word]) for word in self.table.keys()  )

    def poke(self, sense):
        """increment the confidence of the sense by one"""
        self.table[sense] = self[sense] + 1

class SenseSymbolTable:
    """Maps a word to a set of sense symbols for this word"""
    def __init__(self):
        self.table = dict()

    def __getitem__(self, key):
        """
        To avoid having many singleton senses, we have a "catch" for empty entries
        which returns a default value of {word}_0
        """
        try:
            # if there are sense entries, return them... (plus dummy "_0" entry)
            return self.table[key].union({"%s_0" % key})
        except KeyError:
            # otherwise, return singleton default sense set (word_0)
            return {"%s_0" % key}

    def __contains__(self, word):
        """Does a word have a mapping? WARNING: will return False if it has single sense"""

        return word in self.table.keys()

    def add_sense(self, word):
        """ Add a new sense for a word (i.e. automatically increment subscript)"""
        try:
            # if entry already exists, add new sense to sense set
            count = len(self.table[word])
            sense_name = "%s_%d" % (word, count + 1)
            self.table[word].add(sense_name)
            return sense_name

        except KeyError:
            # if singleton entry was emulated (i.e. wasn't an actual instantiated set: was a dummy sense)
            self.table[word] = set()

            sense_name = "%s_%d" % (word, 1)
            self.table[word].add(sense_name)
            return sense_name

    def manual_add(self, word, sense):
        """Usage not recommended! Should really only be used for tests"""
        if word in self.table.keys():
            self.table[word].add(sense)
        else:
            self.table[word] = {sense}

    def remove_sense(self, sense):
        try:
            underscore_pos = sense.find("_")
            word = sense[:underscore_pos]

            count = len(self.table[word])

            # remove entire sense entry from dictionary: the single sense definition can be emulated
            if count is 1:
                del self.table[word]

            # multiple entries: remove the latest sense entry
            else:
                self.table[word].remove(sense)
        except KeyError:
            # single sense being emulated: do nothing
            pass

class NoisySymbolLearner:
    """
    Learn from noisy/homonymous data by maintaining a basic_learner/NPLearner with sense symbols instead of word
    symbols -- processes all combinations of sense assignment in NPLearner to determine which would be consistent,
    and if none would be, determine minimal subset of extra sense assignments necessary to make it consistent.
    """
    def __init__(self, np_learner=basic_learner.NPSymbolLearner()):
        self.np_learner = np_learner
        self.sense_table = SenseSymbolTable()
        self.confidence = ConfidenceTable()

    def __repr__(self):
        """string representation (of internal NPLearner)"""
        return str(self.np_learner)

    def __contains__(self, sense):
        """is a sense (not word!) contained in this learner?"""
        return sense in self.np_learner

    def _backup(self):
        """return a copy of the current NP tables, to be restored if any entries become inconsistent"""
        return (copy.deepcopy(self.np_learner.necessary),
            copy.deepcopy(self.np_learner.possible))

    def _restore(self, necessary, possible):
        """restore the lexical entries after experimenting with new senses"""
        self.np_learner.necessary = necessary
        self.np_learner.possible = possible

    def manual_entry(self, sense, n_set, p_set, confidence_level):
        """
        used to manually enter a whole lexical entry; usually used in tests, to
        start learner in some known state that is useful to test further
        """
        self.np_learner.necessary.add(sense, n_set)
        self.np_learner.possible[sense] = self.np_learner.possible[sense].intersection(p_set)
        self.confidence[sense] = confidence_level

        # calculate variable expressions
        if len(n_set) > 0:
            p_var = p_set.pop()
            n_var = n_set.pop()
            if n_var.islower() and p_var.islower() and n_var is p_var:
                self.np_learner.expressions[sense] = SymbolSet(VariableExpression(n_var))

        # calculate "empty" expressions
        if len(n_set) is 0 and len(p_set) is 0:
            self.np_learner.expressions[sense] = SymbolSet(BottomExpression())

        # sort out sense table
        word = sense[:-2]
        sense_count = int(sense[-1:])
        if sense_count > 0:
            self.sense_table.manual_add(word, sense)

    def _consider_sense_assignments(self, senses, hypotheses):
        """
        checks to see which of the possible sense symbol assignments, when processed, will produce
        consistent lexical entries; returns those which do produce consistent lexical entries
        """
        # backup the current state of the lexical tables
        # TODO: optimisation; only backup relevant senses

        consistent_senses = list()

        # cartesian product; i.e. all combinations of sense symbols: which are consistent?
        senses_tuple = tuple( [tuple(senses[k]) for k in senses.keys() ] )

        for sense_assignment in itertools.product(*senses_tuple):
            (n, p) = self._backup()

            # create new utterance-meaning pair using sense symbols instead of words
            new_utterance = " ".join(sense_assignment)
            hyp_copy = copy.deepcopy(hypotheses)
            sense_pair = training.pairs.UtteranceMeaningPair(new_utterance, hyp_copy)

            # apply NP learner rules 1-4
            self.np_learner.process(sense_pair)

            # check lexical consistency; add to list if it's consistent
            if self.np_learner.all_consistent():
                consistent_senses.append(sense_pair)

            # restore the lexical table
            self._restore(n,p)
        return consistent_senses

    def process(self, pair):
        """process an utterance/meaning pair"""

        # all sense symbols for the words in this utterance
        senses = dict()
        for word in pair.words:
            senses[word] = self.sense_table[word]

        # returns a list of the sense assignments that would be consistent after
        # processing the utterance
        consistent_senses = self._consider_sense_assignments(senses, pair.hypotheses)

        # analyse results
        if len(consistent_senses) == 1:
            # one sense assignment is consistent
            # => this is obviously the sense assignment to permanently use
            print "one sense consistent"
            chosen_sense_assignment = consistent_senses.pop()

        elif len(consistent_senses) > 1:
            # more than one sense assignment is consistent
            # => choose the "best" sense assignment by some selection metric
            #  i.e. which sense assignment maximises the sum of confidence table entries
            print "more than one sense consistent"
            max_confidence = 0
            for sense_assignment in consistent_senses:
                confidence_sum = sum(self.confidence[sense] for sense in sense_assignment.words)
                if confidence_sum >= max_confidence:
                    max_confidence = confidence_sum
                    chosen_sense_assignment = sense_assignment
        else:
            print "no senses consistent"
            # calculate the possible subset of words to add a new sense for; starting with the smallest

            # create a list of iterators in order of size of combinations
            # iterator for 1-combinations, ... , iterator for n-combinations
            fixed_size_subset_iterators = [itertools.combinations(pair.words, num_elems)
                                           for num_elems in range(1, len(pair.words) + 1)]

            # chain these iterators in ascending order; as we want minimal subset (plus smaller
            # combinations are faster)
            for subset in itertools.chain.from_iterable(fixed_size_subset_iterators):
                print "new subset: %s" % str(subset)

                sense_names = copy.deepcopy(senses)
                new_sense_names = []
                for word in subset:
                    new_sense = self.sense_table.add_sense(word) # add sense to sense table
                    sense_names[word].add(new_sense)
                    new_sense_names.append(new_sense) # keep track of new senses, in case we want to delete

                consistent_senses = self._consider_sense_assignments(sense_names, pair.hypotheses)

                # finish if this sense assignment is consistent
                if len(consistent_senses) > 0:
                    chosen_sense_assignment = consistent_senses.pop()
                    break

                # o/w remove these new senses from the sense table
                for sense in new_sense_names:
                    self.sense_table.remove_sense(sense)

        print "finished"

        # this shouldn't happen: worst case is every symbol having new sense
        if not chosen_sense_assignment:
            print "ERROR: no consistent sense assignment"

        # each of these senses has a usage: increase confidence that this sense isn't spurious
        for sense in chosen_sense_assignment.words:
            self.confidence.poke(sense)

        # permanently process with new chosen sense assignment
        self.np_learner.process(chosen_sense_assignment)
