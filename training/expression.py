from abc import ABCMeta, abstractmethod
import collections

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
        """String representation"""
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
            # get constant/variable counts from some subexpression
            (subexpr_const_count, subexpr_var_count) = element.counts()
            for constant in subexpr_const_count.keys():
                try: # if we have count for this const already...
                    self.const_counts[constant] += subexpr_const_count[constant]
                except KeyError: # o/w add entry with subexpression's value
                    self.const_counts[constant] = subexpr_const_count[constant]

            for variable in subexpr_var_count.keys():
                try:
                    self.var_counts[variable] += subexpr_var_count[variable]
                except KeyError:
                    self.var_counts[variable] = subexpr_var_count[variable]

        return self.const_counts, self.var_counts

    def general_form(self):
        if isinstance(self.subexpressions[0], ConstantExpression):
            general_subexpr = [self.subexpressions[0].name]

            for remaining_subexpr in self.subexpressions[1:]:
                general_subexpr.append("x")

            return {Expression(general_subexpr)}
        else:
            return set()

    def deep_subexpressions(self):
        """Determine all possible subexpressions of this Expression"""
        subexpression_set = set()

        # this expression is a subexpression of itself (trivially)
        subexpression_set = subexpression_set.union( {self} )
        subexpression_set = subexpression_set.union( self.general_form() )

        # recurse; this will terminate for RootExpressions
        for subexpression in self.subexpressions:
            recursive_subexprs = subexpression.deep_subexpressions()
            subexpression_set = subexpression_set.union( recursive_subexprs )

        return subexpression_set


class RootExpression(object):
    """
    Some kind of Expression at the 'leaf' of the expression in tree form. Must be some
    subclass of RootExpression
    """
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
        if isinstance(other, str):
            return self.name == other
        else:
            return self.name == other.name

    def deep_subexpressions(self):
        return set()

    def general_form(self):
        return set()


class VariableExpression(RootExpression):
    def counts(self):
        """no constants & one instance of itself (variable)"""
        return dict(), {self.name : 1}

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
        return {self.name : 1}, dict()

    def replace(self, substitutions):
        """constant cannot be replaced"""
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