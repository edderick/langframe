from itertools import izip
from training.expression import Expression
from knowledge.logger.colour_logger import ColourLogger

import random

class GaussianColourSemantics:
    """
    This class stores the "knowledge" the speaker-learner has about
    colour. i.e. an arbitrary mapping from colour class word symbols to some
    subspace of RGB/HSV colour-space.

    This is achieved by using a Gaussian model, whereby each word is modelled as
    an independent multivariate Gaussian distribution built online from its training
    examples.
    """

    def __init__(self, agent_name):
        self.n = dict()             # word => num training examples
        self.mean = dict()         # word => (m_x, m_y, m_z)
        self.variance = dict()     # word -> (sig_x, sig_y, sig_z)

        self._M2 = dict()   # sum squares diff from current mean

        self.log = ColourLogger(agent_name)

    def _unpack_expression(self, expression):
        """Abstract away unpacking of numerical (R,G,B) tuple from expressions of the
        form <COLOUR r_X g_Y b_Z>"""
        return tuple( int(subexpr.subexpressions[0].name[2:])
                      for subexpr in expression.subexpressions[1:] )

    def learn(self, word, expression):
        """Add new entry into mapping (as it's been learned by a word-
        learning algorithm in the framework)."""

        # for details of algorithm, see:
        # http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Online_algorithm

        point = self._unpack_expression(expression)

        if word in self.mean.keys():
            self.n[word] += 1
            n = self.n[word]

            delta = map(lambda x,y: x-y, point, self.mean[word]) # X - Mean
            norm_delta = map(lambda x: float(x)/float(n), delta)
            self.mean[word] = tuple(map(lambda x,y: round(x+y), self.mean[word], norm_delta))

            #M2_delta = map(lambda x,y,z : x*(y-z), delta, point, self.mean[word])
            #self._M2[word] = map(sum, self._M2[word], M2_delta)

            #self.variance = map(lambda x: x / float(n - 1), self._M2[word])

        else:
            # set mean to current value
            self.n[word] = 1
            self.mean[word] = point
            self._M2[word] = (0.0,0.0,0.0)
            self.variance[word] = (0.0,0.0,0.0)

        self.log.new_point(word, point)

    def word_for(self, expression):
        """Query to get a word for a certain colour value (point). This may
        not in general be one-to-one, -- there may be multiple words
        for a single colour value, so a random word will be selected. 
        """
        pass


    def expression_for(self, word):
        """Return a typical colour value (point) belonging to a colour label"""

        # first check colour label exists, otherwise return MISUNDERSTOOD expression
        if word not in self.means.keys():
            return Expression("MISUNDERSTOOD")
        else:
            (r,g,b) = map(lambda mu,var: random.gauss(mu,math.sqrt(var)),
                            self.means[word], self.variances[word])

            return Expression(["COLOUR", "r_%d" % r, "g_%d" % g, "b_%d" % b])

    def say_something(self):
        """Return a random UTM pair"""
        col_expr = Expression(["COLOUR",
                               "r_%d" % random.randint(0,255),
                               "g_%d" % random.randint(0,255),
                               "b_%d" % random.randint(0,255)  ])
        word = self.word_for(col_expr)

        return (word, col_expr)
