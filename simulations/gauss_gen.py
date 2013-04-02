"""
train_gen.py : inter-generational learning

Some learner L0 learns a prototypal semantics (from stdin, e.g. tests/random_source.R),
Generate set of N colour points, output these with L0's word for each as "langL0".

Learner L(i) trains learner L(i+1) with N utterances. (for M generations)

The distance L(i) -> L(i+1) should remain roughly constant, while the distance
L(0) -> L(i) should roughly increase.

INPUT: piped to stdin or filename as first argument
"""

import fileinput
import random
import argparse

from training.expression import Expression
from knowledge import knn_colour

def get_colour_expression(rgb):
    """ convert to proper expression format to be interpretec"""
    return Expression(["COLOUR", "r_%d" % rgb[0],
                                 "g_%d" % rgb[1],
                                 "b_%d" % rgb[2] ])

def probe_colour(lang_name, learner, rgb):
    """print relevant entry in appropriate CSV format to stdout"""
    word = learner.word_for(get_colour_expression(rgb))
    print "%s,%s" % (lang_name, word)


# parse command line arguments
parser = argparse.ArgumentParser(
    description="test training from one agent to another")

parser.add_argument('files', 
    nargs='?', help='specify input files o/w stdin')

parser.add_argument('-M', '--generations', dest="generations",
                    type=int, nargs="?", default=5)
parser.add_argument('-N', '--train-samples', dest="num_train_samples",
                    type=int, nargs="?", default=100)
parser.add_argument('-t', '--test-samples', dest="num_test_samples",
                    type=int, nargs="?", default=1000)
parser.add_argument('--skip', dest="skip",
                    type=int, nargs="?", default=1)
parser.add_argument('--k', dest="knearest",
                    type=int, nargs="?", default=3)

args = parser.parse_args()

# set up L0 & train from stdin
learnerB = knn_colour.KNNColourSemantics("L_0", k=args.knearest)

for line in fileinput.input(args.files):
    entry = line.split(",")

    if entry[0] == "lang.name":
        continue

    rgb = [int(x) for x in entry[1:4]]
    word = entry[4][:-1]
    learnerB.learn(word, get_colour_expression(rgb))

# pick sample of N random colours
test_colours = [
    (random.randint(0,255), 
     random.randint(0,255), 
     random.randint(0,255)) for i in range(args.num_test_samples)]

# header on stdout
print "lang.name,word"

# output for learner L0
for rgb_tuple in test_colours:
    probe_colour("langL_0", learnerB, rgb_tuple)

# generation simulation
for generation in range(1,args.generations):
    learnerA = learnerB
    learnerB = knn_colour.KNNColourSemantics("L_%d" % generation, k=args.knearest)
    
    # train L(i+1) (B) from L(i) (A)
    for i in range(0, args.num_train_samples):
        (word, meaning) = learnerA.say_something()
        learnerB.learn(word, meaning)

    # output sample from trained L(i+1)
    if i % args.skip == 0:
        for rgb_tuple in test_colours:
            probe_colour("langL_%d" % generation, learnerB, rgb_tuple)
