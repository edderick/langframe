import collections
from abc import ABCMeta, abstractmethod

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

class Hypothesis:
    """
    Originally, expression is a list of strings: recursively convert to our more
    appropriate format of a nested tuple of variables/constants; store other useful data
    """
    def __init__(self, expression, count=0):
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
        valid_subexpressions = set()
        for subexpression in self.subexprs:
            (subexpr_const_count, subexpr_var_count) = subexpression.counts()
            subexpr_constants = subexpr_const_count.keys()
            subexpr_constants = set(subexpr_constants)

            if word_constants.issubset(subexpr_constants):
#                print "\t\t\t~>valid\n"
                valid_subexpressions.add(subexpression)

        return valid_subexpressions


class Expression(object):
    """Takes a string/list of strings, and returns a recursive data structure of Expressions"""
    def __init__(self, subexpressions):

        # Case 1: parameter is string; this is some type of RootExpression
        if isinstance(subexpressions, str):
            # upper case symbol => constant
            if subexpressions.isupper():
                self.subexpressions = [ConstantExpression(subexpressions)]
            # lower case symbol => variable
            else:
                self.subexpressions = [VariableExpression(subexpressions)]

        # Case 2: parameter is (nested?) list of strings; recursively make each element
        # an Expression
        elif isinstance(subexpressions, collections.Iterable):
            self.subexpressions = []
            for subexpression in subexpressions:
                self.subexpressions.append(Expression(subexpression))


    def __getitem__(self, index):
        #TODO: is this necessary apart from tests?
        return self.subexpressions[index]

    def __eq__(self, other):
        """
        Equality defined recursively; two expressions are the same if
        all subexpressions are the same. will eventually terminate from
        RootExpressions
        """
        return all( subexp == other[index]
            for (index, subexp) in enumerate(self.subexpressions) )

    def __contains__(self, other):
        """
        Symbol containment calculated recursively; return True if any subexpressions
        contain the symbol. Will terminate at RootExpressions
        """
        return any(other in subexpression for subexpression in self.subexpressions)

    def __repr__(self):
        return "<%s>" % ",".join(repr(elem) for elem in self.subexpressions)

    def replace(self, substitutions):
        #TODO: implement
        pass

    def counts(self):
        """
        Count how many instances of a constant/variable there are in this expression.
        Determined recursively for all subexpressions.

        Returns a tuple of dictionaries counting constants & variables respectively, which
        map a symbol to its count.
        """
        self.const_counts = dict()
        self.var_counts = dict()

        for element in self.subexpressions:
            (subexpr_const_count, subexpr_var_count) = element.counts()
            for constant in subexpr_const_count.keys():
                try:
                    self.const_counts[constant] += subexpr_const_count[constant]
                except KeyError:
                    self.const_counts[constant] = subexpr_const_count[constant]

            for variable in subexpr_var_count.keys():
                try:
                    self.var_counts[variable] += subexpr_var_count[variable]
                except KeyError:
                    self.var_counts[variable] = subexpr_var_count[variable]

        return (self.const_counts, self.var_counts)

    def deep_subexpressions(self):
        subexpression_set = set()
        subexpression_set = subexpression_set.union( {self} )
        for subexpression in self.subexpressions:
            recursive_subexprs = subexpression.deep_subexpressions()
            subexpression_set = subexpression_set.union( recursive_subexprs )

        return subexpression_set

class RootExpression(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def counts(self):
        pass

    @abstractmethod
    def replace(self, substitutions):
        pass

    def __iter__(self):
        yield self.name

    def __eq__(self, other):
        """Equality of root expressions simply is string comparison"""
        if isinstance(other, string):
            return self.name == other
        else:
            return self.name == other.name

    def deep_subexpressions(self):
#        print "root %s" % self
        return set()


class VariableExpression(RootExpression):
    def counts(self):
        """no constants & one instance of itself (variable)"""
        return (dict(), {self.name : 1})

    def replace(self, substitutions):
        if self.name in substitutions.keys():
            return VariableExpression(substitutions[self.name])
        else:
            return self

    def __repr__(self):
        return "V(%s)" % self.name

class ConstantExpression(RootExpression):
    def counts(self):
        """one instance of itself (constant) & no variables"""
        return({self.name : 1}, dict())

    def replace(self, substitutions):
        return self

    def __repr__(self):
        return "C(%s)" % self.name

class BottomExpression:
    """
    represents the 'bottom' symbol, used to indicate that a word cannot be expressed conceptually
    (e.g. is idiomatic/function word) but is STILL consistent
    """

    def __iter__(self):
        yield self

    def __str__(self):
        return "_|_"

    def __repr__(self):
        return "_|_"
