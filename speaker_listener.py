import random
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

    def learn(self, word, expression):
        """once a single conceptual expression has been chosen for a word,
        add it to the relevant semantics"""

        constant_term = expression[0][0].name
        self.knowledge[constant_term].learn(word, expression)

    def say_something(self):
        """return a UTM pair, equally likely to be from each semantic unit"""
        chosen = random.choice(self.knowledge.keys())
        return self.knowledge[chosen].say_something()
