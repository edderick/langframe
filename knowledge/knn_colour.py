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
       pass

    def learn(self, word, expression):
        """Add new entry into mapping (as it's been learned by a word-
        learning algorithm in the framework)."""

        # expression is of the form <COLOUR r_X g_Y b_Z>
        vals = []
        for subexpression in expression.subexpressions[1:]:
            vals.append(int(subexpression.subexpressions[0].name[2:]))

        self.points.append((word, tuple(vals)))

    def word_for(self, expression):
        """Query to get a word for a certain colour value (point). This may
        not in general be one-to-one, -- there may be multiple words
        for a single colour value, so a random word will be selected."""
        pass

    def expression_for(self, word):
        """Return a typical colour value (point) belonging to a colour label"""
        pass