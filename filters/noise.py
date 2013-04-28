import random
from training.expression import Expression

def _unpack_expression(expression):
    """Abstract away unpacking of numerical (R,G,B) tuple from expressions of the
    form <COLOUR r_X g_Y b_Z>"""
    return tuple( int(subexpr.subexpressions[0].name[2:])
                      for subexpr in expression.subexpressions[1:] )

def gaussian_20(expression):
    """Apply a random amount of Gaussian noise to each element with uniform random 
    variance between 0 and 20"""
    rgb = _unpack_expression(expression)
hhiglhlhlghgghkjh
    new = map(lambda x : int(random.gauss(x, random.randint(0,20))), rgb)
    new_form = map(lambda col,x: "%s_%s" % (col, x), ("r","g","b"), new)
    return Expression(["COLOUR"] + new_form)
