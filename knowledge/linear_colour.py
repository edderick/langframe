from itertools import izip
from training.expression import Expression
from knowledge.logger.colour_logger import ColourLogger

import random
import math

class LinearColourSemantics:
    """
    This class stores the "knowledge" the speaker-learner has about
    colour. i.e. an arbitrary mapping from colour class word symbols to some
    subspace of RGB/HSV colour-space.

    This is achieved by using a basic model storing the mean (prototype) of each
    colour class, which is dynamically updated on learning a new example. The
    probability of emitting a word for a given colour point is based on the linear
    distance from the point to each prototype.
    """

    def __init__(self, agent_name):
        self.n = dict()             # word => num training examples
        self.mean = dict()         # word => (m_x, m_y, m_z)

        self.log = ColourLogger(agent_name)

    def _unpack_expression(self, expression):
        """Abstract away unpacking of numerical (R,G,B) tuple from expressions of the
        form <COLOUR r_X g_Y b_Z>"""
        return tuple( int(subexpr.subexpressions[0].name[2:])
                      for subexpr in expression.subexpressions[1:] )

    def learn(self, word, expression):
        """Add new entry into mapping (as it's been learned by a word-
        learning algorithm in the framework)."""
        
        point = self._unpack_expression(expression)

        if word not in self.mean.keys():
            self.n[word] = 0
            self.mean[word] = (0,0,0)

        self.n[word] += 1
        n = self.n[word]
        
        delta = map(lambda x,mean: x-mean, point, self.mean[word]) # X - Mean
        norm_delta = map(lambda delt: float(delt)/float(n), delta)
        self.mean[word] = tuple(map(lambda m,nd: m+nd, self.mean[word], norm_delta))

        self.log.new_point(word, point)

    def word_for(self, expression):
        """Query to get a word for a certain colour value (point). This may
        not in general be one-to-one, -- there may be multiple words
        for a single colour value, so a random word will be selected. 
        """
        point = self._unpack_expression(expression)
        distance = dict()
        prob_density = dict()

        # calculate probability density at point for each word
        for word in self.n:
            mean = self.mean[word]

            dist = map(lambda x,mu: ((x-mu)**2), point, mean )
            distance[word] = 1/sum(dist)

        norm_const = sum(distance[x] for x in distance)

        for word in distance:
            prob_density[word] = distance[word]/norm_const

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
                            self.mean[word], (1, 1, 1))

            # makeshift bounds handling: clamp co-ords to 0..255 range
            (r,g,b) = map(lambda x: 0 if x < 0 else x, (r,g,b))
            (r,g,b) = map(lambda x: 255 if x > 255 else x, (r,g,b))

            return Expression(["COLOUR", "r_%d" % r, "g_%d" % g, "b_%d" % b])

    def say_something(self):
        """Return a random UTM pair"""
            
        col_expr = Expression(["COLOUR",
                               "r_%d" % random.randint(0,255),
                               "g_%d" % random.randint(0,255),
                               "b_%d" % random.randint(0,255)  ])
        word = self.word_for(col_expr)

        return (word, col_expr)
