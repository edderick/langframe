"""
loader.py -- loads a set of pairs of utterances & hypothesised meanings from a 
standard text format into a format friendly for processing by the learner.

The text follows the following grammar:

* pair : utterance "->" hypothesis_set
* utterance : "[a-z]+"     # tokenised by space
* hypothesis_set: \{ hypothesis? (", " hypothesis)* \}
* hypothesis : ATOM | \(ATOM(hypothesis " ")+\)

* ATOM : [A-Z]+

e.g.
"i like computers" -> { (LIKE (SAM (PLURAL COMPUTER))), (LIKE (ME COMPUTER)) } 
"""

import os

def from_file(filename, path=''):
    full_path = os.path.join(path, filename)

    pair_file = open(full_path, 'r')

    # unpacks from a perfectly-formed file: will fail terribly if incorrect
    for pair in pair_file:
        if pair[0] == "#" or len(pair) < 2:
            continue

        utterance, hypothesis_set = pair.split('->')
        utterance = utterance.strip().strip('"')

        hypothesis_set = [hyp for hyp in hypothesis_set.strip()[1:-1].split(",")]
        yield UtteranceMeaningPair(utterance, hypothesis_set)

def dump(pairs, path='' ):
        full_path = os.path.join(path, filename)
        pair_file = open(full_path, 'w')

        for pair in pairs:
            pair_file.write(pair)

class UtteranceMeaningPair:
    def __init__(self, utterance, symbols_sets=[]):
        self.words = set(utterance.split(" "))
        self.symbol_sets = symbol_sets

    def __str__(self):
        return "%s => {%s}\n" % (self.utterance, ", ".join(self.symbol_sets))
