import random
import collections
import knowledge.gauss_colour

from training.expression import Expression

class SpeakerListener:
    def __init__(self, identifier):
        self.identifier = identifier
        
        # dynamically dispatches to some semantic unit based on constant term
        # in the expression; set up associations now
        self.knowledge = {
            "COLOUR" : knowledge.gauss_colour.GaussianColourSemantics(identifier)
        }

        self.incompetence = collections.defaultdict(list)

    def learn(self, word, expression):
        """once a single conceptual expression has been chosen for a word,
        add it to the relevant semantics"""

        constant_term = expression[0][0].name
        self.knowledge[constant_term].learn(word, expression)

    def add_incompetence(self, constant_term, incompetence_filter):
        """add a filter to pipeline, to modify expressions as they're said (used
        to model incorrect interpretation on other end). filter is function
        Expression -> Expression"""

        self.incompetence[constant_term].append(incompetence_filter)

    def say_something(self):
        """return a UTM pair, equally likely to be from each semantic unit"""
        chosen = random.choice(self.knowledge.keys())
        (word,expression) = self.knowledge[chosen].say_something()

        # process each incompetence filter (in order)
        for filt in self.incompetence[chosen]:
            expression = filt(expression)

        return (word,expression)
