"""
Test whether the Gaussian learner model can transmit a "class" distinction by
having two colour prototypes, "blue" and "lightblue"

INPUT: piped to stdin or filename as first argument
"""

import random
import fileinput
import utils.logger

from training.expression import Expression
from knowledge import gauss_colour, logger

# PARAMETERS
NUM_SAMPLES = 1000
TRAINING_ITERATIONS = 100
SKIP = 1

def pack_expression(rgb):
    return Expression(["COLOUR", "r_%d" % rgb[0],
                                         "g_%d" % rgb[1],
                                         "b_%d" % rgb[2] ])

def pick_random_blue():
    def clamp(n):
        return max(min(255, n), 0)

    # limit to picking colours that are in "blue" subspace
    (mu_x, mu_y, mu_z) = learnerA.mean['blue']
    (sg_x, sg_y, sg_z) = learnerA.variance['blue']

    return (clamp(random.gauss(mu_x,sg_x**0.5)), 
      clamp(random.gauss(mu_y,sg_y**0.5)), 
      clamp(random.gauss(mu_z,sg_z**0.5)))


# set up learner
learnerA = gauss_colour.GaussianColourSemantics("A", creative=False)
learnerB = gauss_colour.GaussianColourSemantics("B", creative=False)

utils.logger.display_log("langframe.root.colour.sample")
logger = logger.colour_logger.ColourLogger(learnerA)

# train A from stdin
for line in fileinput.input():
    entry = line.split(",")

    if entry[0] == "lang.name":
        continue

    rgb = [int(x) for x in entry[1:4]]
    word = entry[4][:-1]
    learnerA.learn(word, pack_expression(rgb))

# pick sample of N random colours (in blue subspace)
test_colours = [pick_random_blue() for i in range(NUM_SAMPLES)]

# output for learner A
logger.log_points("langA", test_colours)

logger.learner = learnerB

# iteratively train learner B on A's utterances (N iterations)
for i in range(0, TRAINING_ITERATIONS):
    meaning = pack_expression(pick_random_blue())

    word = learnerA.word_for(meaning)
    learnerB.learn(word, meaning)

    if i % SKIP == 0:
        logger.log_points("langB_%02d" % i, test_colours)
