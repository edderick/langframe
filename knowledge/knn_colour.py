from itertools import izip
from collections import Counter
from training.expression import Expression
from knowledge.logger.colour_logger import ColourLogger

import random

class KNNColourSemantics:
    """
    This class stores the "knowledge" the speaker-learner has about
    colour. i.e. an arbitrary mapping from colour class word symbols to some
    subspace of RGB/HSV colour-space.

    This is achieved by using a k-Nearest Neighbour classifier on all previously
    learned points.
    """

    def __init__(self, k=3):
        self.k = k
        self.points = []
        self.words = []
        self.log = ColourLogger()

    def _unpack_expression(self, expression):
        """Abstract away unpacking of numerical (R,G,B) tuple from expressions of the
        form <COLOUR r_X g_Y b_Z>"""
        return tuple( int(subexpr.subexpressions[0].name[2:])
                      for subexpr in expression.subexpressions[1:] )

    def learn(self, word, expression):
        """Add new entry into mapping (as it's been learned by a word-
        learning algorithm in the framework)."""

        # maintain two (ordered) lists of points & colour words
        point = self._unpack_expression(expression)
        self.points.append(point)
        self.words.append(word)

        self.log.new_point(word, point)

    def word_for(self, expression):
        """Query to get a word for a certain colour value (point). This may
        not in general be one-to-one, -- there may be multiple words
        for a single colour value, so a random word will be selected. Although
        k-nearest neighbour will produce a unique result."""

        given = self._unpack_expression(expression)

        # create tuple of sum of squared errors for each known colour point
        errs = tuple(sum((p - x)**2 for p,x in izip(point, given)) for point in self.points)

        # errors sorted low->high and the point indicies from errs used here (i.e. argsort)
        min_errs_args = sorted(range(len(errs)), key=lambda k: errs[k])

        # return colour label with most votes (modal average from k nearest
        k_nearest_colours = tuple(self.words[point] for point in min_errs_args[:self.k])
        colour_counts = Counter(k_nearest_colours)
        most_common = max(name for name, count in colour_counts.items())

        return most_common

    def expression_for(self, word):
        """Return a typical colour value (point) belonging to a colour label"""

        # first check colour label exists, otherwise return MISUNDERSTOOD expression
        if word not in self.words:
            return Expression("MISUNDERSTOOD")
        else:
            # terrible solution! bad Sam!
            for i in range(50):
                point = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )
                expression = Expression("COLOUR", "r_%d" % point[0], "g_%d" % point[1], "b_%d" % point[2])
                if self.word_for(expression) is word:
                    return expression
            pass
