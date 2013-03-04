from training.expression import Expression

__author__ = 'sam'


class Hypothesis:
    """
    Originally, expression is a list of strings: recursively convert to our more
    appropriate format of a nested tuple of variables/constants; store other useful data
    """
    def __init__(self, expression):
        self.bound_expression = Expression(expression)
        self.subexprs = self.bound_expression.deep_subexpressions()
        (self.constants, self.variables) = self.bound_expression.counts()

        self.symbols = set(self.constants.keys() + self.variables.keys())

        self.symbol_count = dict()
        for var in self.variables.keys():
            self.symbol_count[var] = self.variables[var]
        for const in self.constants.keys():
            self.symbol_count[const] = self.constants[const]

    def __repr__(self):
        return repr(self.bound_expression)

    def __contains__(self, symbol):
        return symbol in self.bound_expression

    def subexpressions_for_constants(self, word_constants):
        """
        Return the subexpressions of this hypothesis' meaning which only
        contain some constants.
        """
        valid_subexpressions = set()
        for subexpression in self.subexprs:
            (subexpr_const_count, subexpr_var_count) = subexpression.counts()
            subexpr_constants = subexpr_const_count.keys()
            subexpr_constants = set(subexpr_constants)

            if word_constants.issubset(subexpr_constants):
                valid_subexpressions.add(subexpression)

        return valid_subexpressions