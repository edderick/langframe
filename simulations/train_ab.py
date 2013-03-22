"""
Some learner A learns a prototypal semantics (from stdin, e.g. tests/random_source.R),
Generate set of 1000 colours (X), output these with A's word for each as "langA".

Learner B is trained by utterances from Learner A. At each stage, output X with B's
words for X as LangBi (where i is iteration number).

The distance between L(A) and L_B(i) should decrease steadily.
"""

import fileinput
import random

from training.expression import Expression
from knowledge import knn_colour

def get_colour_expression(rgb):
    return Expression(["COLOUR", "r_%d" % rgb[0],
                                 "g_%d" % rgb[1],
                                 "b_%d" % rgb[2] ])

def probe_colour(lang_name, learner, rgb):
    word = learner.word_for(get_colour_expression(rgb))
    print "%s,%s" % (lang_name, word)

learnerA = knn_colour.KNNColourSemantics("A", k=3)
learnerB = knn_colour.KNNColourSemantics("B", k=3)

# train A from stdin
for line in fileinput.input():
    entry = line.split(",")

    if entry[0] == "lang.name":
        continue

    rgb = [int(x) for x in entry[1:4]]
    word = entry[4][:-1]
    learnerA.learn(word, get_colour_expression(rgb))

# header on stdout
print "lang.name,word"

# pick 1000 random colours
test_colours = [(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    for i in range(100)]

# output for learner A
for rgb_tuple in test_colours:
    probe_colour("langA", learnerA, rgb_tuple)

# iteratively train learner B on A's utterances
for i in range(100):
    (word, meaning) = learnerA.say_something()
    learnerB.learn(word, meaning)

    for rgb_tuple in test_colours:
        probe_colour("langB_%d" % i, learnerB, rgb_tuple)
