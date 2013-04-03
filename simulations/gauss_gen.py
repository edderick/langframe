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
import utils.logger

from training.expression import Expression
from knowledge import gauss_colour, logger

# parse command line arguments
parser = argparse.ArgumentParser(
    description="test training from one agent to another")

parser.add_argument('files', 
    nargs='?', help='specify input files o/w stdin')

parser.add_argument('-M', '--generations', dest="generations",
                    type=int, nargs="?", default=15)
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
learnerB = gauss_colour.GaussianColourSemantics("L_0")

utils.logger.display_log("langframe.root.colour.sample")
logger = logger.colour_logger.ColourLogger(learnerB)

for line in fileinput.input(args.files):
    entry = line.split(",")

    if entry[0] == "lang.name":
        continue

    rgb = [int(x) for x in entry[1:4]]
    word = entry[4][:-1]
    learnerB.learn(word, Expression(["COLOUR", "r_%d" % rgb[0],
                                         "g_%d" % rgb[1],
                                         "b_%d" % rgb[2] ]))


# pick sample of N random colours
test_colours = [
    (random.randint(0,255), 
     random.randint(0,255), 
     random.randint(0,255)) for i in range(args.num_test_samples)]

logger.log_points("langA", test_colours)

# generation simulation
for generation in range(1,args.generations):
    learnerA = learnerB
    learnerB = gauss_colour.GaussianColourSemantics("L_%d" % generation, creative=True)

    logger.learner = learnerB
    
    # train L(i+1) (B) from L(i) (A)
    for i in range(0, args.num_train_samples):
        (word, meaning) = learnerA.say_something()
        learnerB.learn(word, meaning)

    # output sample from trained L(i+1)
    if i % args.skip == 0:
        logger.log_points("langL_%d" % generation, test_colours)
