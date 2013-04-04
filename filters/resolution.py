from training.expression import Expression

def _unpack_expression(expression):
    """Abstract away unpacking of numerical (R,G,B) tuple from expressions of the
    form <COLOUR r_X g_Y b_Z>"""
    return tuple( int(subexpr.subexpressions[0].name[2:])
                      for subexpr in expression.subexpressions[1:] )

def three_bit(expression):
    """Reduce precision of expression from 8-bit (0..255) to 3-bit (0..7) but
    within same range"""

    rgb = _unpack_expression(expression)

    new = map(lambda x : int(round(float(x) / 32)*32), rgb)
    new_form = map(lambda col,x: "%s_%s" % (col, x), ("r","g","b"), new)

    return Expression(["COLOUR"] + new_form)
