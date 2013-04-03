from itertools import izip
from training.expression import Expression
from knowledge.logger.colour_logger import ColourLogger

import random
import math

class GaussianColourSemantics:
    """
    This class stores the "knowledge" the speaker-learner has about
    colour. i.e. an arbitrary mapping from colour class word symbols to some
    subspace of RGB/HSV colour-space.

    This is achieved by using a Gaussian model, whereby each word is modelled as
    an independent multivariate Gaussian distribution built online from its training
    examples.
    """

    def __init__(self, agent_name, creative=True):
        self.creative = True

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

        if word not in self.mean.keys():
            self.n[word] = 0
            self.mean[word] = (0,0,0)
            self._M2[word] = (0,0,0)

        self.n[word] += 1
        n = self.n[word]

        delta = map(lambda x,mean: x-mean, point, self.mean[word]) # X - Mean
        norm_delta = map(lambda delt: float(delt)/float(n), delta)
        self.mean[word] = tuple(map(lambda m,nd: m+nd, self.mean[word], norm_delta))

        M2_delta = map(lambda x,y,z : x*(y-z), delta, point, self.mean[word])
        self._M2[word] = map(lambda x,y: x+y, self._M2[word], M2_delta)

        if n != 1:
            self.variance[word] = tuple(map(lambda x: x / float(n - 1), self._M2[word]))
        else:
            self.variance[word] = (5,5,5) # small variance for new point

        self.log.new_point(word, point)

    def word_for(self, expression):
        """Query to get a word for a certain colour value (point). This may
        not in general be one-to-one, -- there may be multiple words
        for a single colour value, so a random word will be selected. 
        """
        point = self._unpack_expression(expression)
        prob_density = dict()

        # if there are no nearby prototypes, make up a word
        distances = [sum(map(lambda x,mu: (x-mu)**2, point,self.mean[word])) 
                        for word in self.n]
        if self.creative and all(x > 35000 for x in distances):
            self.invent_word(point)

        # calculate probability density at point for each word
        for word in self.n:
            mean = self.mean[word]
            variance = self.variance[word]

            sq_diff = map(lambda x,mu,var: ((x-mu)**2)/var, point, mean, variance)
            prob_density[word] = math.exp(-0.5 * sum(sq_diff))

        # pick random number 0..sum(densities)
        # build cumulative sum of densities for words until sum > random number
        s = 0
        random_num = random.random() * sum(prob_density[x] for x in prob_density) 

        for word in prob_density:
            s += prob_density[word] 
            if s > random_num:
                return word
        return "WAT"

    def expression_for(self, word):
        """Return a typical colour value (point) belonging to a colour label"""

        # first check colour label exists, otherwise return MISUNDERSTOOD expression
        if word not in self.mean.keys():
            return Expression("MISUNDERSTOOD")
        else:
            # pick random point according to Gaussiandistribution of word
            (r,g,b) = map(lambda mu,var: round(random.gauss(mu,math.sqrt(var))),
                            self.mean[word], self.variance[word])

            # makeshift bounds handling: clamp co-ords to 0..255 range
            (r,g,b) = map(lambda x: 0 if x < 0 else x, (r,g,b))
            (r,g,b) = map(lambda x: 255 if x > 255 else x, (r,g,b))

            return Expression(["COLOUR", "r_%d" % r, "g_%d" % g, "b_%d" % b])

    def invent_word(self, point):
        """Creates a new word; boringly named new_i for the ith word in the vocab"""
        #TODO: more interesting names

        new_word = "new_%d" % len(self.n)
        self.n[new_word] = 1
        self.mean[new_word] = point
        self.variance[new_word] = (1600, 1600, 1600) # arbitrary variance

    def say_something(self):
        """Return a random UTM pair"""
        col_expr = Expression(["COLOUR",
                               "r_%d" % random.randint(0,255),
                               "g_%d" % random.randint(0,255),
                               "b_%d" % random.randint(0,255)  ])
        word = self.word_for(col_expr)

        return (word, col_expr)
