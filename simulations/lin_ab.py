"""
Some learner A learns a prototypal semantics (from stdin, e.g. tests/random_source.R),
Generate set of 1000 colours (X), output these with A's word for each as "langA".

Learner B is trained by utterances from Learner A. At each stage, output X with B's
words for X as LangBi (where i is iteration number).

The distance between L(A) and L_B(i) should decrease steadily.

INPUT: piped to stdin or filename as first argument
"""

import fileinput
import random
import argparse

from training.expression import Expression
from knowledge import linear_colour

def get_colour_expression(rgb):
    """ convert to proper expression format to be interpretec"""
    return Expression(["COLOUR", "r_%d" % rgb[0],
                                 "g_%d" % rgb[1],
                                 "b_%d" % rgb[2] ])

def probe_colour(lang_name, learner, rgb):
    """print relevant entry in appropriate CSV format to stdout"""
    word = learner.word_for(get_colour_expression(rgb))
    print "%s,%s" % (lang_name, word)

def probe_mean(lang_name, learner):
    for word in ("black", "darkblue", "green", "red", "cyan", "yellow", "magenta", "white"):
        try:
            print "%s,%s,%d,%d,%d" % (lang_name, word, 
                                    learner.mean[word][0],
                                    learner.mean[word][1],
                                    learner.mean[word][2])
        except KeyError:
            print "%s,%s,0,0,0" % (lang_name, word)


# parse command line arguments
parser = argparse.ArgumentParser(
    description="test training from one agent to another")

parser.add_argument('files', 
    nargs='?', help='specify input files o/w stdin')

parser.add_argument('-I', '--iterations', dest="training_iterations",
                    type=int, nargs="?", default=100)
parser.add_argument('-N', '--samples', dest="num_samples",
                    type=int, nargs="?", default=1000)
parser.add_argument('--skip', dest="skip",
                    type=int, nargs="?", default=1)
parser.add_argument('--k', dest="knearest",
                    type=int, nargs="?", default=3)

args = parser.parse_args()

# set up learner
learnerA = linear_colour.LinearColourSemantics("A")
learnerB = linear_colour.LinearColourSemantics("B")

# train A from stdin
for line in fileinput.input(args.files):
    entry = line.split(",")

    if entry[0] == "lang.name":
        continue

    rgb = [int(x) for x in entry[1:4]]
    word = entry[4][:-1]
    learnerA.learn(word, get_colour_expression(rgb))

# header on stdout
print "lang.name,word"
#print "lang.name,word,r,g,b"

# pick sample of N random colours
test_colours = [
    (random.randint(0,255), 
     random.randint(0,255), 
     random.randint(0,255)) for i in range(args.num_samples)]

# output for learner A
for rgb_tuple in test_colours:
    probe_colour("langA", learnerA, rgb_tuple)
    pass

#probe_mean("langA", learnerA)

# iteratively train learner B on A's utterances (N iterations)
for i in range(0, args.training_iterations):
    (word, meaning) = learnerA.say_something()
    learnerB.learn(word, meaning)
    #probe_mean("langB_%d" % i, learnerB)

    if i % args.skip == 0:
        for rgb_tuple in test_colours:
            probe_colour("langB_%d" % i, learnerB, rgb_tuple)
            pass
