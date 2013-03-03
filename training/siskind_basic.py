from pairs import Hypothesis, UtteranceMeaningPair

# UTM pair 1 from Siskind's paper
hyp1 = Hypothesis(["CAUSE", ["john", ["GO", ["ball" , ["TO", "john"]]]]])
hyp2 = Hypothesis(["WANT", ["john", "ball"]])
hyp3 = Hypothesis(["CAUSE", ["john", ["GO", ["PARTOF", ["LEFT", "arm"], "john"], ["TO", "ball"]]]] )

def pair1():
    return UtteranceMeaningPair("john took the ball", {hyp1, hyp2, hyp3})