class UtteranceMeaningPair:
    """
    An element of the training corpus: a set of words said and possible hypotheses
    of its meanings as conceptual symbolic expressions.
    """

    def __init__(self, utterance, hypotheses=set()):
        self.utterance = utterance
        self.words = set(utterance.split(" "))
        self.hypotheses = hypotheses

    def __repr__(self):
        return self.utterance

    def __str__(self):
        return "\"%s\" => { %s }\n" % \
               (self.utterance, ",\n\t\t\t".join(str(hypothesis) for hypothesis in self.hypotheses))

